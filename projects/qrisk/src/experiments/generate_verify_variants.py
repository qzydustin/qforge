#!/usr/bin/env python3
"""
Generate verify-set variant circuits for a group, mirroring the fez-97 methodology.

For a given group's base_3x.qpy and a target bad pattern, this script:
  1. Applies many random commuting-gate swaps (different n_swaps × seed) to produce
     candidate variants — all semantically equivalent to the base circuit.
  2. Scores each variant by how many times the target pattern occurs (pattern_hits).
  3. Selects 10 variants per hit bucket (hit_0 ... hit_3), balancing n_swaps so the
     dose-response test is not confounded by swap count.
  4. Writes selection_manifest.json + per-variant QPY under <group>/variants/verify/.

This is the generation half; experiments/run_verify_batch.py is the execution half
(runs each variant on ideal/noisy/real and writes summary.json).

Usage:
    python experiments/generate_verify_variants.py \
        --group candidate_groups/grover3-fez-O3-46_47_48_57 \
        --pattern 'rz(47) → cz(46,47) → sx(47)'

    # or let it auto-pick the strongest pattern from the group's DDMin reports
    python experiments/generate_verify_variants.py \
        --group candidate_groups/grover3-fez-O3-46_47_48_57 --auto-pattern

The --pattern string is the canonical display form produced by analyze_pattern_repeats
("op(q) → op(q1,q2) → ..."); it is parsed back into (name, qubits, params) tokens.
For patterns whose gates carry parameters (e.g. rz angles), pass --pattern-json with
the exact DDMin token list instead, so params are preserved.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from qiskit import qpy, QuantumCircuit

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from qiskit.converters import circuit_to_dag

from quantum.pattern_transform import commuting_swap_circuit
from quantum.pattern_db import token_sequence, count_pattern_hits


def moment_signature(circ: QuantumCircuit) -> tuple:
    """Per-moment multiset of gates, invariant to intra-moment ordering.

    Quantum hardware runs one moment (layer) at a time; gates within a moment
    execute in parallel and reordering them has no physical effect. Two circuits
    with the same moment_signature execute identically on hardware, so a swap
    that leaves the signature unchanged is physically meaningless and must be
    discarded for the dose-response experiment.
    """
    dag = circuit_to_dag(circ)
    sigs = []
    for layer in dag.layers():
        ops = sorted(
            (node.name, tuple(sorted(circ.find_bit(q).index for q in node.qargs)))
            for node in layer["graph"].op_nodes()
        )
        sigs.append(tuple(ops))
    return tuple(sigs)


# ---------------------------------------------------------------------------
# Pattern parsing
# ---------------------------------------------------------------------------

def parse_pattern_str(s: str) -> list[tuple]:
    """Parse 'rz(47) → cz(46,47) → sx(47)' into (name, qubits, ()) tokens.

    Note: this form loses gate parameters. Use parse_pattern_tokens for the
    parameterized DDMin token list when params matter (they usually do for rz).
    """
    tokens = []
    for part in s.split("→"):
        part = part.strip()
        if not part:
            continue
        name = part.split("(")[0].strip()
        qstr = part[part.find("(") + 1: part.rfind(")")]
        qubits = tuple(int(q) for q in qstr.split(",") if q.strip() != "")
        tokens.append((name, qubits, ()))
    return tokens


def parse_pattern_tokens(tok_list: list) -> list[tuple]:
    """Parse a DDMin pattern token list [[name, [qubits], [params]], ...] into
    (name, qubits_tuple, params_tuple) with params rounded to 6 dp to match
    normalize_token in pattern_db."""
    tokens = []
    for t in tok_list:
        name = t[0]
        qubits = tuple(int(q) for q in t[1])
        params = tuple(round(float(p), 6) if isinstance(p, (int, float)) else p
                       for p in (t[2] if len(t) > 2 else []))
        tokens.append((name, qubits, params))
    return tokens


def auto_pick_pattern(group_dir: Path) -> list[tuple]:
    """Pick the strongest repeating pattern from the group's DDMin reports.

    Ranks canonical patterns by (repeat count desc, contains-cz first), returns
    the parameterized token list of the winner.
    """
    from collections import Counter
    from itertools import groupby

    def canon(ops):
        indexed = [(op, tuple(sorted(q)), i) for i, (op, q) in enumerate(ops)]
        qnl = defaultdict(int)
        gl = []
        for n, q, i in indexed:
            l = max(qnl[x] for x in q)
            gl.append((l, q, n, i))
            for x in q:
                qnl[x] = l + 1
        gl.sort(key=lambda x: (x[0], x[1]))
        out = []
        for _, grp in groupby(gl, key=lambda x: x[0]):
            out.extend(f"{n}({','.join(map(str, q))})" for _, q, n, _ in grp)
        return " → ".join(out)

    reports = sorted((group_dir / "ddmin_reports").glob("*.json"))
    cnt: Counter = Counter()
    sample: dict[str, list] = {}
    for f in reports:
        d = json.loads(f.read_text())
        p = d.get("pattern", [])
        if p:
            ck = canon([(g[0], tuple(g[1])) for g in p])
            cnt[ck] += 1
            sample.setdefault(ck, p)
    if not cnt:
        raise ValueError(f"No patterns found in {group_dir}/ddmin_reports")
    ranked = sorted(cnt.items(), key=lambda x: (-x[1], -(1 if "cz" in x[0] else 0)))
    top_ck = ranked[0][0]
    return parse_pattern_tokens(sample[top_ck])


# ---------------------------------------------------------------------------
# Variant generation + selection
# ---------------------------------------------------------------------------

SWAP_GRID = [1, 2, 3, 5, 8, 10, 15, 20, 30, 50, 80, 100, 150, 200, 300, 500]
SEED_SPACE = range(1, 2000)
PER_BUCKET = 30


def generate_candidates(base: QuantumCircuit, n_candidates: int = 400) -> list[dict]:
    """Generate candidate variants across the swap×seed grid.

    Filters out variants whose moment signature matches the base — those swaps
    only reordered gates within moments and would execute identically on hardware.
    """
    cands = []
    seen_seqs = set()
    base_seq = token_sequence(base)
    base_moment_sig = moment_signature(base)

    # base itself (0 swaps) — kept as reference, marked is_base
    cands.append({"n_swaps": 0, "seed": 0, "circuit": base,
                  "seq": base_seq, "is_base": True})
    seen_seqs.add(_seq_key(base_seq))

    rng = random.Random(12345)
    attempts = 0
    skipped_same_moment = 0
    while len(cands) - 1 < n_candidates and attempts < n_candidates * 12:
        attempts += 1
        n_swaps = rng.choice(SWAP_GRID)
        seed = rng.choice(SEED_SPACE)
        try:
            var = commuting_swap_circuit(base, n_swaps, seed)
        except Exception:
            continue
        # Discard physically-meaningless swaps (moment structure unchanged).
        if moment_signature(var) == base_moment_sig:
            skipped_same_moment += 1
            continue
        seq = token_sequence(var)
        key = _seq_key(seq)
        if key in seen_seqs:
            continue
        seen_seqs.add(key)
        cands.append({"n_swaps": n_swaps, "seed": seed,
                      "circuit": var, "seq": seq, "is_base": False})
    print(f"  (discarded {skipped_same_moment} candidates with unchanged moment structure)")
    return cands


def _seq_key(seq):
    return json.dumps(seq, separators=(",", ":"))


def score_against_pattern(seq, pattern_tokens) -> int:
    return count_pattern_hits(seq, pattern_tokens)


def select_balanced(cands, pattern_tokens, max_buckets: int = 5) -> dict[str, list[dict]]:
    """Select PER_BUCKET variants per hit bucket, balancing n_swaps.

    Buckets are dynamic: we group candidates by their actual pattern-hit count
    and keep up to `max_buckets` distinct hit values (the most populated ones),
    sampling PER_BUCKET variants from each. This avoids forcing the fez-97
    0/1/2/3 grid when a pattern's reachable hit range is different (e.g. 2~9).

    Within each bucket, variants are sorted by n_swaps and sampled evenly so the
    swap distribution is similar across buckets (controls the n_swaps confound).
    """
    by_hit = defaultdict(list)
    for c in cands:
        h = score_against_pattern(c["seq"], pattern_tokens)
        by_hit[h].append(c)

    # Pick up to max_buckets distinct hit values, preferring a spread across
    # the reachable range. Only include buckets with >= MIN_BUCKET_SIZE samples
    # to ensure statistical significance in each dose-response bucket.
    MIN_BUCKET_SIZE = 3
    viable_hits = sorted(h for h in by_hit if len(by_hit[h]) >= MIN_BUCKET_SIZE)
    if not viable_hits:
        # Fallback: use all available hits regardless of size
        viable_hits = sorted(by_hit.keys())
    all_hits = viable_hits
    if len(all_hits) <= max_buckets:
        chosen_hits = all_hits
    else:
        # Always include the extremes, then fill remaining with evenly spaced
        # interior hits to maximize the dose-response range.
        chosen = {all_hits[0], all_hits[-1]}
        step = (len(all_hits) - 1) / (max_buckets - 1)
        i = 1
        while len(chosen) < max_buckets and i < max_buckets - 1:
            idx = round(i * step)
            chosen.add(all_hits[idx])
            i += 1
        chosen_hits = sorted(chosen)

    selected: dict[str, list[dict]] = {}
    for hit in chosen_hits:
        pool = sorted(by_hit[hit], key=lambda c: c["n_swaps"])
        picks = _even_sample(pool, PER_BUCKET)
        selected[f"hit_{hit}"] = picks
    return selected


def _even_sample(pool: list[dict], k: int) -> list[dict]:
    """Pick k items spread evenly across the pool's n_swaps ordering."""
    if len(pool) <= k:
        return list(pool)
    step = len(pool) / k
    return [pool[int(i * step)] for i in range(k)]


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_outputs(group_dir: Path, base_circuit: QuantumCircuit,
                  pattern_tokens: list[tuple], backend: str,
                  selected: dict[str, list[dict]],
                  experiment_name: str) -> Path:
    verify_dir = group_dir / "variants" / "verify"
    verify_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "experiment": experiment_name,
        "backend": backend,
        "base_circuit": str(group_dir / "base_3x.qpy"),
        "pattern_db": "(inline target pattern)",
        "pattern": _pattern_display(pattern_tokens),
        "total_selected": sum(len(v) for v in selected.values()),
        "selected": {},
    }

    for bucket, picks in selected.items():
        bucket_dir = verify_dir / bucket
        bucket_dir.mkdir(exist_ok=True)
        items = []
        for idx, c in enumerate(picks, 1):
            tag = bucket.replace("hit_", "hit")
            qpy_name = f"{group_dir.name}_{tag}_sw{c['n_swaps']}_s{c['seed']}.qpy"
            qpy_path = bucket_dir / qpy_name
            with open(qpy_path, "wb") as f:
                qpy.dump(c["circuit"], f)
            hits = count_pattern_hits(c["seq"], pattern_tokens)
            items.append({
                "variant_index": idx,
                "n_swaps": c["n_swaps"],
                "seed": c["seed"],
                "qpy_path": str(qpy_path),
                "qpy_name": qpy_name,
                "op_count": len(c["circuit"].data),
                "total_hits": hits,
                "distinct_hits": 1 if hits > 0 else 0,
                "weighted_hits": hits * len(pattern_tokens),
            })
        manifest["selected"][bucket] = items

    manifest_path = verify_dir / "selection_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    return manifest_path


def _pattern_display(tokens):
    parts = []
    for name, qubits, params in tokens:
        q = ",".join(map(str, qubits))
        if params:
            p = ",".join(f"{x:.6g}" if isinstance(x, float) else str(x) for x in params)
            parts.append(f"{name}({q}, {p})")
        else:
            parts.append(f"{name}({q})")
    return " -> ".join(parts)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--group", required=True,
                    help="Group directory (e.g. candidate_groups/grover3-fez-O3-46_47_48_57)")
    ap.add_argument("--pattern", default=None,
                    help="Target pattern string 'rz(47) → cz(46,47) → sx(47)' (params lost)")
    ap.add_argument("--pattern-json", default=None,
                    help="Path to a JSON file with the DDMin pattern token list (preserves params)")
    ap.add_argument("--auto-pattern", action="store_true",
                    help="Auto-pick strongest repeating pattern from DDMin reports")
    ap.add_argument("--backend", default=None,
                    help="Override backend name (default: inferred from group name)")
    ap.add_argument("--n-candidates", type=int, default=400)
    args = ap.parse_args()

    group_dir = (REPO_ROOT / args.group).resolve() if not os.path.isabs(args.group) \
        else Path(args.group)
    if not group_dir.is_dir():
        raise SystemExit(f"Group dir not found: {group_dir}")

    # load base circuit
    base_path = group_dir / "base_3x.qpy"
    with open(base_path, "rb") as f:
        base = list(qpy.load(f))[0]
    print(f"Base: {base_path.name} ({base.num_qubits} qubits, {len(base.data)} ops)")

    # resolve pattern
    if args.pattern_json:
        pattern_tokens = parse_pattern_tokens(json.loads(Path(args.pattern_json).read_text()))
    elif args.pattern:
        pattern_tokens = parse_pattern_str(args.pattern)
    elif args.auto_pattern:
        pattern_tokens = auto_pick_pattern(group_dir)
    else:
        raise SystemExit("Provide --pattern, --pattern-json, or --auto-pattern")
    print(f"Target pattern: {_pattern_display(pattern_tokens)}")

    base_hits = count_pattern_hits(token_sequence(base), pattern_tokens)
    print(f"Pattern hits in base circuit: {base_hits}")

    # generate + select
    cands = generate_candidates(base, n_candidates=args.n_candidates)
    print(f"Generated {len(cands)} candidate variants")
    selected = select_balanced(cands, pattern_tokens)
    for bucket, picks in selected.items():
        hits = [count_pattern_hits(c["seq"], pattern_tokens) for c in picks]
        print(f"  {bucket}: {len(picks)} variants, hit distribution {sorted(set(hits))}")

    backend = args.backend or _infer_backend(group_dir.name)
    exp_name = f"{group_dir.name}_verify"
    manifest_path = write_outputs(group_dir, base, pattern_tokens, backend,
                                  selected, exp_name)
    print(f"\nManifest: {manifest_path}")
    print(f"Total selected: {sum(len(v) for v in selected.values())}")


def _infer_backend(group_name: str) -> str:
    if "-fez-" in group_name:
        return "ibm_fez"
    if "-kingston-" in group_name:
        return "ibm_kingston"
    if "-marrakesh-" in group_name:
        return "ibm_marrakesh"
    return "unknown"


if __name__ == "__main__":
    main()
