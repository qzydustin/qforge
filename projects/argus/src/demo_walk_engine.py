from __future__ import annotations

import ast
import copy
import hashlib
import multiprocessing as mp
import traceback
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from codemutationengine.random_mutator import (
    CoverageGuidedStrategy,
    DependencyGuidedStrategy,
    MutationContext,
    MutationOperator,
    SemanticAnalyzer,
    SemanticAwareStrategy,
    create_default_mutation_graph,
)

from codemutationengine.utils.ast_graph import (
    build_ast_graph,
    export_graph_json,
    map_lineno_to_node_id,
)


@dataclass
class CandidateScore:
    operator: MutationOperator
    operator_name: str
    coverage_score: float
    semantic_score: float
    dependency_score: float
    total_score: float
    reason_coverage: str
    reason_semantic: str
    reason_dependency: str


def r4(x: Any) -> float:
    """Round numeric values to 4 decimal places for UI stability."""
    try:
        return round(float(x), 4)
    except Exception:
        return 0.0


def compute_static_executed_lines(source_code: str) -> Set[int]:
    """Fallback coverage: treat all statement lines as executed.

    Used when runtime coverage data is unavailable.
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return set()

    lines: Set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.stmt):
            ln = getattr(node, "lineno", None)
            if isinstance(ln, int):
                lines.add(ln)
    return lines


def compute_coverage_hash(executed_lines: Sequence[int]) -> str:
    """Stable signature for executed line sets (deterministic for sorted inputs)."""
    sorted_lines = ",".join(str(l) for l in sorted(executed_lines))
    return hashlib.sha1(sorted_lines.encode("utf-8")).hexdigest()


def _compute_operator_coverage_score(
    op: MutationOperator,
    tree: ast.AST,
    executed_lines: Set[int],
) -> Tuple[float, str]:
    """Estimate how strongly an operator is tied to executed lines.

    Score is in [0, 1], based on the fraction of operator targets that lie on executed lines.
    """
    if not executed_lines:
        return 0.0, "coverage-disabled"

    targets = getattr(op, "target_nodes", None)
    if isinstance(targets, list) and targets:
        total = len(targets)
        hits = 0
        for n in targets:
            ln = getattr(n, "lineno", None)
            if isinstance(ln, int) and ln in executed_lines:
                hits += 1
        if total <= 0:
            return 0.0, "no targets"
        if hits > 0:
            return hits / float(total), f"{hits}/{total} targets on executed lines"
        return 0.0, "no targets on executed lines"

    # Special-case candidate-based renamers
    from codemutationengine.random_mutator import (  # local import to avoid cycles
        ParamRenameMutator,
        VariableRenameMutator,
    )

    if isinstance(op, (VariableRenameMutator, ParamRenameMutator)) and getattr(op, "candidates", None):
        candidates = getattr(op, "candidates")
        total_funcs = len(candidates)
        if total_funcs <= 0:
            return 0.0, "no candidates"

        def func_has_coverage(fn: ast.AST) -> bool:
            for n in ast.walk(fn):
                ln = getattr(n, "lineno", None)
                if isinstance(ln, int) and ln in executed_lines:
                    return True
            return False

        covered = 0
        for fn, _name in candidates:
            if func_has_coverage(fn):
                covered += 1

        if covered > 0:
            return covered / float(total_funcs), f"{covered}/{total_funcs} functions touch executed lines"
        return 0.0, "no candidate functions touch executed lines"

    return 0.0, "no coverage-specific signal"


def _compute_operator_semantic_score(
    op: MutationOperator,
    tree: ast.AST,
    semantic_analyzer: SemanticAnalyzer,
) -> Tuple[float, str]:
    """Semantic affinity score via SemanticAwareStrategy heuristics."""
    semantic_info = semantic_analyzer.analyze(tree)
    strat = SemanticAwareStrategy()
    try:
        score = strat._assess_meaningfulness(op, semantic_info, tree)  # type: ignore[attr-defined]
    except Exception:
        return 0.0, "semantic evaluation failed"

    if score >= 0.8:
        reason = "strong semantic affinity"
    elif score >= 0.6:
        reason = "moderate semantic affinity"
    elif score > 0.0:
        reason = "weak semantic affinity"
    else:
        reason = "no semantic signal"
    return float(score), reason


def _compute_operator_dependency_score(
    op: MutationOperator,
    tree: ast.AST,
    dep_strategy: Optional[DependencyGuidedStrategy],
) -> Tuple[float, str]:
    """Dependency-priority score: 1.0 if operator hits any dependency, else 0.0."""
    if not dep_strategy:
        return 0.0, "dependency-disabled"
    try:
        hit = dep_strategy._operator_has_dep_affinity(op, tree)  # type: ignore[attr-defined]
    except Exception:
        return 0.0, "dependency evaluation failed"
    return (1.0, "hits dependency-priority target") if hit else (0.0, "no dependency hit")


def _build_candidate_scores(
    operators: List[MutationOperator],
    tree: ast.AST,
    executed_lines: Set[int],
    priority_dependencies: Set[str],
    policy: str,
    dep_strategy: Optional[DependencyGuidedStrategy] = None,
    semantic_analyzer: Optional[SemanticAnalyzer] = None,
) -> List[CandidateScore]:
    """Compute per-operator scores for UI/explainability.

    Note: scoring here is for explain.json/UI only. Actual filtering/prioritization
    is handled by MutationGraph strategies.

    Policy decides which signals contribute to total_score:
      - random:    base operator weight only
      - coverage:  base + coverage
      - composite: base + coverage + semantic + dependency
    """
    if policy == "composite":
        semantic_analyzer = semantic_analyzer or SemanticAnalyzer()
        if dep_strategy is None and priority_dependencies:
            dep_strategy = DependencyGuidedStrategy(list(priority_dependencies))
    else:
        semantic_analyzer = None
        dep_strategy = None

    candidates: List[CandidateScore] = []

    for op in operators:
        op_name = getattr(op, "name", op.__class__.__name__)
        base_weight = float(getattr(op, "weight", 1.0))

        cov_score, cov_reason = _compute_operator_coverage_score(op, tree, executed_lines)
        if policy not in {"coverage", "composite"}:
            cov_score = 0.0
            cov_reason = "coverage-disabled" if not executed_lines else "coverage present but unused in policy"

        if semantic_analyzer is not None:
            sem_score, sem_reason = _compute_operator_semantic_score(op, tree, semantic_analyzer)
        else:
            sem_score, sem_reason = 0.0, "semantic-disabled"

        dep_score, dep_reason = _compute_operator_dependency_score(op, tree, dep_strategy)

        if policy == "random":
            total = base_weight
        elif policy == "coverage":
            total = base_weight + 2.0 * cov_score
        else:
            total = base_weight + 1.5 * cov_score + 1.2 * sem_score + 2.0 * dep_score

        candidates.append(
            CandidateScore(
                operator=op,
                operator_name=op_name,
                coverage_score=r4(cov_score),
                semantic_score=r4(sem_score),
                dependency_score=r4(dep_score),
                total_score=r4(total),
                reason_coverage=cov_reason,
                reason_semantic=sem_reason,
                reason_dependency=dep_reason,
            )
        )

    return candidates


def _candidate_sort_key(c: CandidateScore) -> Tuple:
    """Deterministic ordering: higher scores first, then operator name."""
    return (-c.total_score, -c.dependency_score, -c.coverage_score, -c.semantic_score, c.operator_name)


def _select_candidate(
    ctx: MutationContext,
    candidates: List[CandidateScore],
    walk: str,
    policy: str,
) -> CandidateScore:
    """Select one candidate according to walk mode and policy."""
    if not candidates:
        raise RuntimeError("no candidates to select from")

    ordered = sorted(candidates, key=_candidate_sort_key)

    if walk == "random" or policy == "random":
        weights = [max(float(getattr(c.operator, "weight", 1.0)), 1e-6) for c in ordered]
    else:
        weights = [max(c.total_score, 1e-6) for c in ordered]

    total = sum(weights)
    r = ctx.random.random() * total
    acc = 0.0
    for cand, w in zip(ordered, weights):
        acc += w
        if r <= acc:
            return cand
    return ordered[-1]


def _select_candidate_with_trace(
    ctx: MutationContext,
    candidates: List[CandidateScore],
    walk: str,
    policy: str,
) -> Tuple[CandidateScore, Dict[str, Any]]:
    """Select one candidate and also return a trace explaining why it was selected."""
    if not candidates:
        raise RuntimeError("no candidates to select from")

    ordered = sorted(candidates, key=_candidate_sort_key)

    if walk == "random" or policy == "random":
        weights = [max(float(getattr(c.operator, "weight", 1.0)), 1e-6) for c in ordered]
        weight_kind = "base_weight"
    else:
        weights = [max(c.total_score, 1e-6) for c in ordered]
        weight_kind = "total_score"

    total = float(sum(weights))
    r = float(ctx.random.random() * total)

    acc = 0.0
    chosen = ordered[-1]
    chosen_index = len(ordered) - 1
    for i, (cand, w) in enumerate(zip(ordered, weights)):
        acc += float(w)
        if r <= acc:
            chosen = cand
            chosen_index = i
            break

    trace = {
        "strategy": "weighted_sample",
        "weight_kind": weight_kind,
        "random_draw": r4(r),
        "weight_sum": r4(total),
        "chosen_index": int(chosen_index),
        "ordered": [
            {
                "rank": i + 1,
                "operator": c.operator_name,
                "total_score": r4(c.total_score),
                "coverage_score": r4(c.coverage_score),
                "semantic_score": r4(c.semantic_score),
                "dependency_score": r4(c.dependency_score),
                "base_weight": r4(getattr(c.operator, "weight", 1.0)),
                "weight_used": r4(w),
            }
            for i, (c, w) in enumerate(zip(ordered, weights))
        ],
    }
    return chosen, trace


def _smoke_run_worker(code: str, q: mp.Queue) -> None:
    """Execute code in an isolated process and report success/error via queue."""
    try:
        compiled = compile(code, "<mutant>", "exec")
        glb: Dict[str, Any] = {"__name__": "__main__", "__file__": "<mutant>"}
        exec(compiled, glb, glb)
        q.put({"ok": True})
    except BaseException as e:  # noqa: BLE001
        tb = traceback.format_exc(limit=12)
        q.put(
            {
                "ok": False,
                "error_type": type(e).__name__,
                "error_msg": str(e),
                "traceback_snippet": tb,
            }
        )


def _validate_mutant_code(
    code: str,
    *,
    enable_smoke_run: bool,
    smoke_timeout_sec: float,
) -> Dict[str, Any]:
    """Validate a mutant as a first-class artifact.

    Returns a dict with:
      ok: bool
      mutant_status: valid | syntax_error | runtime_error | timeout
      validation_stage: parse | compile | smoke_run
      error_type / error_msg / traceback_snippet (optional)
    """
    # Stage 1: parse
    try:
        ast.parse(code)
    except SyntaxError as e:
        return {
            "ok": False,
            "mutant_status": "syntax_error",
            "validation_stage": "parse",
            "error_type": type(e).__name__,
            "error_msg": str(e),
            "traceback_snippet": "".join(traceback.format_exception_only(type(e), e))[:800],
        }

    # Stage 2: compile
    try:
        compile(code, "<mutant>", "exec")
    except SyntaxError as e:
        return {
            "ok": False,
            "mutant_status": "syntax_error",
            "validation_stage": "compile",
            "error_type": type(e).__name__,
            "error_msg": str(e),
            "traceback_snippet": "".join(traceback.format_exception_only(type(e), e))[:800],
        }

    if not enable_smoke_run:
        return {
            "ok": True,
            "mutant_status": "valid",
            "validation_stage": "compile",
            "error_type": None,
            "error_msg": None,
            "traceback_snippet": None,
        }

    # Stage 3: smoke_run (subprocess + timeout)
    q: mp.Queue = mp.Queue()
    p = mp.Process(target=_smoke_run_worker, args=(code, q))
    p.daemon = True
    p.start()
    p.join(timeout=smoke_timeout_sec)

    if p.is_alive():
        try:
            p.terminate()
        except Exception:
            pass
        return {
            "ok": False,
            "mutant_status": "timeout",
            "validation_stage": "smoke_run",
            "error_type": "TimeoutError",
            "error_msg": f"smoke_run exceeded {smoke_timeout_sec}s",
            "traceback_snippet": None,
        }

    result: Dict[str, Any] = {}
    try:
        if not q.empty():
            result = q.get_nowait()
    except Exception:
        result = {}

    if result.get("ok") is True:
        return {
            "ok": True,
            "mutant_status": "valid",
            "validation_stage": "smoke_run",
            "error_type": None,
            "error_msg": None,
            "traceback_snippet": None,
        }

    return {
        "ok": False,
        "mutant_status": "runtime_error",
        "validation_stage": "smoke_run",
        "error_type": result.get("error_type") or "Exception",
        "error_msg": result.get("error_msg") or "unknown runtime error",
        "traceback_snippet": (result.get("traceback_snippet") or "")[:1200],
    }


def run_guided_demo(
    *,
    source_code: str,
    input_path: str,
    walk: str,
    policy: str,
    seed: Optional[int],
    steps: int,
    coverage_lines: Set[int],
    target_api: Optional[str],
    extra_dependencies: Optional[List[str]] = None,
    validate: bool = True,
    smoke_run: bool = True,
    smoke_timeout_sec: float = 2.0,
) -> Tuple[str, Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
    """Run a demo mutation walk with explain events and AST graph export.

    Returns:
        mutated_code: final mutated source code
        manifest_meta: metadata including coverage hash and mutation path
        explain_events: per-step events
        graph_json: AST graph JSON with highlighted mutation path
    """
    if walk not in {"random", "guided"}:
        raise ValueError(f"Unsupported walk mode: {walk}")
    if policy not in {"random", "coverage", "composite"}:
        raise ValueError(f"Unsupported policy: {policy}")

    deps: Set[str] = set()
    if extra_dependencies:
        for d in extra_dependencies:
            if isinstance(d, str) and d.strip():
                deps.add(d.strip().lower())
    if target_api:
        deps.add(str(target_api).strip().lower())

    executed_lines = set(coverage_lines or set())
    coverage_hash = compute_coverage_hash(sorted(executed_lines))

    try:
        original_tree = ast.parse(source_code)
    except SyntaxError as e:
        raise ValueError(f"Input code has syntax error: {e}") from e

    ast_graph = build_ast_graph(source_code)

    ctx = MutationContext(seed)
    if executed_lines:
        ctx.coverage_info = set(executed_lines)
    if deps:
        ctx.priority_dependencies = set(deps)

    graph = create_default_mutation_graph()
    graph.enable_validation = bool(validate)

    semantic_analyzer: Optional[SemanticAnalyzer] = SemanticAnalyzer() if policy == "composite" else None

    if policy in {"coverage", "composite"} and executed_lines:
        graph.coverage_strategy = CoverageGuidedStrategy({"executed_lines": sorted(executed_lines)})

    if policy == "composite":
        graph.semantic_strategy = SemanticAwareStrategy()
        if deps:
            graph.dependency_strategy = DependencyGuidedStrategy(list(deps))

    mutated_tree = copy.deepcopy(original_tree)
    explain_events: List[Dict[str, Any]] = []

    discarded_summary: List[Dict[str, Any]] = []

    for step_index in range(steps):
        applicable_ops = graph.get_applicable_operators(mutated_tree)
        before_names = [getattr(op, "name", op.__class__.__name__) for op in applicable_ops]

        if not applicable_ops:
            explain_events.append(
                {
                    "step": step_index + 1,
                    "status": "no-op",
                    "reason": "no applicable operators",
                    "walk": walk,
                    "policy": policy,
                    "validate": validate,
                    "candidates": {"before": 0, "after_dependency": 0, "after_coverage": 0, "after_semantic": 0},
                }
            )
            break

        ops_after_dep = applicable_ops
        removed_by_dep: List[str] = []
        if getattr(graph, "dependency_strategy", None) is not None:
            dep_filtered = graph.dependency_strategy.prioritize_operators(ops_after_dep, mutated_tree)  # type: ignore[union-attr]
            after_dep_names = [getattr(op, "name", op.__class__.__name__) for op in dep_filtered]
            removed_by_dep = sorted(set(before_names) - set(after_dep_names))
            ops_after_dep = dep_filtered
        else:
            after_dep_names = list(before_names)

        ops_after_cov = ops_after_dep
        removed_by_cov: List[str] = []
        if getattr(graph, "coverage_strategy", None) is not None:
            cov_ranked = graph.coverage_strategy.prioritize_operators(ops_after_cov, mutated_tree)  # type: ignore[union-attr]
            after_cov_names = [getattr(op, "name", op.__class__.__name__) for op in cov_ranked]
            removed_by_cov = sorted(set(after_dep_names) - set(after_cov_names))
            ops_after_cov = cov_ranked
        else:
            after_cov_names = list(after_dep_names)

        ops_after_sem = ops_after_cov
        removed_by_sem: List[str] = []
        if getattr(graph, "semantic_strategy", None) is not None:
            sem_filtered = graph.semantic_strategy.select_meaningful_mutations(  # type: ignore[union-attr]
                ops_after_sem, mutated_tree, ctx
            )
            after_sem_names = [getattr(op, "name", op.__class__.__name__) for op in sem_filtered]
            removed_by_sem = sorted(set(after_cov_names) - set(after_sem_names))
            ops_after_sem = sem_filtered
        else:
            after_sem_names = list(after_cov_names)

        if not ops_after_sem:
            explain_events.append(
                {
                    "step": step_index + 1,
                    "status": "no-op",
                    "reason": "no operators available after strategy filtering",
                    "walk": walk,
                    "policy": policy,
                    "validate": validate,
                    "candidates": {
                        "before": len(applicable_ops),
                        "after_dependency": len(ops_after_dep),
                        "after_coverage": len(ops_after_cov),
                        "after_semantic": 0,
                    },
                    "filtered_out": {"dependency": removed_by_dep, "coverage": removed_by_cov, "semantic": removed_by_sem},
                }
            )
            continue

        candidate_scores = _build_candidate_scores(
            ops_after_sem,
            mutated_tree,
            executed_lines,
            deps,
            policy,
            dep_strategy=getattr(graph, "dependency_strategy", None),
            semantic_analyzer=semantic_analyzer,
        )
        if not candidate_scores:
            explain_events.append(
                {
                    "step": step_index + 1,
                    "status": "no-op",
                    "reason": "no candidate scores computed",
                    "walk": walk,
                    "policy": policy,
                    "validate": validate,
                    "candidates": {
                        "before": len(applicable_ops),
                        "after_dependency": len(ops_after_dep),
                        "after_coverage": len(ops_after_cov),
                        "after_semantic": len(ops_after_sem),
                    },
                    "filtered_out": {"dependency": removed_by_dep, "coverage": removed_by_cov, "semantic": removed_by_sem},
                }
            )
            continue

        ordered_candidates_all = sorted(candidate_scores, key=_candidate_sort_key)
        top_k_all = ordered_candidates_all[:5]

        selection_strategy = (
            "weighted_sample(base_weight)" if (walk == "random" or policy == "random") else "weighted_sample(total_score)"
        )

        retries_info: Dict[str, Any] = {"attempts": 0, "discarded": [], "final_selection_trace": None}
        selected: Optional[CandidateScore] = None
        selection_trace_for_step: Optional[Dict[str, Any]] = None

        success = False
        rolled_back = False
        validation_error: Optional[str] = None
        mutation_record: Optional[Dict[str, Any]] = None

        applied_validation_meta: Dict[str, Any] = {
            "mutant_status": None,
            "validation_stage": None,
            "error_type": None,
            "error_msg": None,
            "traceback_snippet": None,
        }

        if validate:
            remaining = list(candidate_scores)
            max_attempts = len(remaining)

            while remaining and retries_info["attempts"] < max_attempts:
                selected, sel_trace = _select_candidate_with_trace(ctx, remaining, walk, policy)
                selection_trace_for_step = sel_trace
                retries_info["attempts"] += 1

                backup_tree = copy.deepcopy(mutated_tree)
                before_mutation_count = len(ctx.applied_mutations)

                success = selected.operator.apply(mutated_tree, ctx)

                rolled_back = False
                validation_error = None

                if success:
                    try:
                        mutated_preview = ast.unparse(mutated_tree)  # type: ignore[attr-defined]
                    except Exception as e:
                        mutated_preview = ""
                        validation_error = f"unparse failed: {e}"

                    if validation_error is None:
                        is_valid, err_msg = graph._validate_mutation(mutated_preview)  # type: ignore[attr-defined]
                        if not is_valid:
                            validation_error = str(err_msg or "invalid mutation (graph validation)")

                    if validation_error is None:
                        v = _validate_mutant_code(
                            mutated_preview,
                            enable_smoke_run=bool(smoke_run),
                            smoke_timeout_sec=float(smoke_timeout_sec),
                        )
                        if not v.get("ok", False):
                            validation_error = (
                                f"{v.get('mutant_status')} at {v.get('validation_stage')}: "
                                f"{v.get('error_type')}: {v.get('error_msg')}"
                            )
                            applied_validation_meta = {
                                "mutant_status": v.get("mutant_status"),
                                "validation_stage": v.get("validation_stage"),
                                "error_type": v.get("error_type"),
                                "error_msg": v.get("error_msg"),
                                "traceback_snippet": v.get("traceback_snippet"),
                            }
                        else:
                            applied_validation_meta = {
                                "mutant_status": "valid",
                                "validation_stage": v.get("validation_stage"),
                                "error_type": None,
                                "error_msg": None,
                                "traceback_snippet": None,
                            }

                    if validation_error is not None:
                        rolled_back = True
                        mutated_tree = backup_tree
                        while len(ctx.applied_mutations) > before_mutation_count:
                            ctx.applied_mutations.pop()
                            try:
                                ctx.mutation_count -= 1
                            except Exception:
                                pass

                if success and (not rolled_back) and ctx.applied_mutations:
                    retries_info["final_selection_trace"] = selection_trace_for_step
                    mutation_record = ctx.applied_mutations[-1]
                    break

                discard = {
                    "operator": selected.operator_name if selected else None,
                    "reason": "operator.apply returned false",
                    "mutant_status": None,
                    "validation_stage": None,
                    "error_type": None,
                    "error_msg": None,
                    "traceback_snippet": None,
                    "selection_trace": selection_trace_for_step,
                }
                if rolled_back and validation_error:
                    discard["reason"] = f"validate failed: {validation_error}"
                    discard["mutant_status"] = applied_validation_meta.get("mutant_status")
                    discard["validation_stage"] = applied_validation_meta.get("validation_stage")
                    discard["error_type"] = applied_validation_meta.get("error_type")
                    discard["error_msg"] = applied_validation_meta.get("error_msg")
                    discard["traceback_snippet"] = applied_validation_meta.get("traceback_snippet")

                retries_info["discarded"].append(discard)
                discarded_summary.append(discard)

                remaining = [c for c in remaining if c.operator_name != (selected.operator_name if selected else "")]

            if not (success and (not rolled_back) and mutation_record):
                explain_events.append(
                    {
                        "step": step_index + 1,
                        "status": "no-op",
                        "reason": "all candidates failed validation",
                        "walk": walk,
                        "policy": policy,
                        "validate": validate,
                        "selection_strategy": selection_strategy,
                        "selection_trace": selection_trace_for_step,
                        "candidates": {
                            "before": len(applicable_ops),
                            "after_dependency": len(ops_after_dep),
                            "after_coverage": len(ops_after_cov),
                            "after_semantic": len(ops_after_sem),
                        },
                        "filtered_out": {"dependency": removed_by_dep, "coverage": removed_by_cov, "semantic": removed_by_sem},
                        "retries": retries_info,
                    }
                )
                continue

        else:
            selected, selection_trace_for_step = _select_candidate_with_trace(ctx, candidate_scores, walk, policy)
            success = selected.operator.apply(mutated_tree, ctx)
            if success and ctx.applied_mutations:
                mutation_record = ctx.applied_mutations[-1]

        lineno = mutation_record.get("line") if mutation_record else None
        node_id = map_lineno_to_node_id(ast_graph, lineno)

        status = "applied" if (success and not rolled_back) else ("rolled_back" if rolled_back else "failed")
        reason = None
        if rolled_back:
            reason = f"validate failed: {validation_error}"
        elif not success:
            reason = "operator.apply returned false"

        selected_name = selected.operator_name if selected else None
        not_selected_top: List[Dict[str, Any]] = []
        for rank, c in enumerate(ordered_candidates_all[:10], start=1):
            if selected_name is not None and c.operator_name == selected_name:
                continue
            not_selected_top.append(
                {
                    "operator": c.operator_name,
                    "rank": rank,
                    "reason": "not selected by weighted sampling",
                    "total_score": r4(c.total_score),
                    "coverage_score": r4(c.coverage_score),
                    "semantic_score": r4(c.semantic_score),
                    "dependency_score": r4(c.dependency_score),
                }
            )

        explain_event: Dict[str, Any] = {
            "step": step_index + 1,
            "walk": walk,
            "policy": policy,
            "selection_strategy": selection_strategy,
            "selection_trace": (retries_info.get("final_selection_trace") if validate else selection_trace_for_step),
            "filtered_after_rank": {
                "not_selected_top": not_selected_top,
                "discarded_after_selection": (retries_info.get("discarded") if validate else []),
            },
            "selected_operator": selected.operator_name if selected else None,
            "selected_node": {
                "node_id": node_id,
                "lineno": lineno,
                "snippet": mutation_record["node"] if mutation_record else None,
            },
            "scores": {
                "total": r4(selected.total_score) if selected else 0.0,
                "coverage": r4(selected.coverage_score) if selected else 0.0,
                "semantic": r4(selected.semantic_score) if selected else 0.0,
                "dependency": r4(selected.dependency_score) if selected else 0.0,
                "reasons": {
                    "coverage": selected.reason_coverage if selected else "n/a",
                    "semantic": selected.reason_semantic if selected else "n/a",
                    "dependency": selected.reason_dependency if selected else "n/a",
                },
            },
            "top_candidates": [
                {
                    "operator": c.operator_name,
                    "total_score": r4(c.total_score),
                    "coverage_score": r4(c.coverage_score),
                    "semantic_score": r4(c.semantic_score),
                    "dependency_score": r4(c.dependency_score),
                    "reason": {
                        "coverage": c.reason_coverage,
                        "semantic": c.reason_semantic,
                        "dependency": c.reason_dependency,
                    },
                }
                for c in top_k_all
            ],
            "status": status,
            "reason": reason,
            "validate": validate,
            "candidates": {
                "before": len(applicable_ops),
                "after_dependency": len(ops_after_dep),
                "after_coverage": len(ops_after_cov),
                "after_semantic": len(ops_after_sem),
            },
            "filtered_out": {"dependency": removed_by_dep, "coverage": removed_by_cov, "semantic": removed_by_sem},
            "mutant_validation": {
                "mutant_status": applied_validation_meta.get("mutant_status") if status == "applied" else None,
                "validation_stage": applied_validation_meta.get("validation_stage") if status == "applied" else None,
                "error_type": None,
                "error_msg": None,
                "traceback_snippet": None,
            },
        }

        if validate:
            explain_event["retries"] = retries_info

        explain_events.append(explain_event)

        if (not validate) and (not success or rolled_back):
            continue

    ast.fix_missing_locations(mutated_tree)
    mutated_code = ast.unparse(mutated_tree)  # type: ignore[attr-defined]

    # Final mutant validation (top-level manifest fields)
    final_v = _validate_mutant_code(
        mutated_code,
        enable_smoke_run=bool(smoke_run),
        smoke_timeout_sec=float(smoke_timeout_sec),
    )

    path_steps: List[Dict[str, Any]] = []
    mutation_path_ids: List[int] = []
    for idx, m in enumerate(ctx.applied_mutations):
        ln = m.get("line")
        nid = map_lineno_to_node_id(ast_graph, ln)
        if isinstance(nid, int):
            mutation_path_ids.append(nid)
        path_steps.append(
            {
                "index": idx + 1,
                "operator": m.get("operator"),
                "line": ln,
                "node_id": nid,
                "node": m.get("node"),
            }
        )

    manifest_meta: Dict[str, Any] = {
        "input_file": input_path,
        "walk": walk,
        "policy": policy,
        "seed": seed,
        "validate": validate,
        "validation_config": {
            "smoke_run": bool(smoke_run),
            "smoke_timeout_sec": float(smoke_timeout_sec),
        },
        # First-class invalid mutant fields (final artifact status)
        "mutant_status": final_v.get("mutant_status"),
        "validation_stage": final_v.get("validation_stage"),
        "error_type": final_v.get("error_type"),
        "error_msg": final_v.get("error_msg"),
        "traceback_snippet": final_v.get("traceback_snippet"),
        "discarded_candidates": discarded_summary,
        "coverage": {"executed_lines": sorted(executed_lines), "hash": coverage_hash},
        "path": path_steps,
    }

    graph_meta = {
        "input_file": input_path,
        "walk": walk,
        "policy": policy,
        "seed": seed,
        "validate": validate,
    }
    graph_json = export_graph_json(ast_graph, mutation_path_ids, graph_meta)

    return mutated_code, manifest_meta, explain_events, graph_json