#!/usr/bin/env python3
"""
Exp 2 — does Grover's pattern raise excess hardware error INSIDE other algorithms?

  --plan  (no QPU): for each layout, take the pattern core that today's Grover
          DDMin runs isolated (Exp 1; most frequent core, ties -> highest
          baseline ratio) or --pattern, find its occurrences in every other
          preflight-passing algorithm compiled on the same qubits (qubit-
          timeline matching, parameters ignored), and for the algorithms with
          the most occurrences build dose-response variants:
            * levels = occurrence counts reachable by semantics-preserving
              commuting swaps (up to 4 levels, e.g. 3/2/1/0),
            * --per-level variants per level, diversified by random
              count-preserving ("neutral") commuting swaps drawn from the
              SAME swap grid at every level (no swap-count confound),
            * every variant verified unitary-equivalent to the original,
            * the untouched compiled circuit is included as 'original'.
  --run   (QPU): each algorithm's variants go to the device as ONE batched job
          (shuffled order), checked against the global budget first.

Usage:
    python -m scripts.xalg.variants --backend ibm_fez --plan
    python -m scripts.xalg.variants --backend ibm_fez --run --budget-min 40
    python -m scripts.xalg.variants --backend ibm_fez --plan \\
        --pattern "rz(47) cz(46,47) sx(47)" --layouts "46,47,48,57"
"""

from __future__ import annotations

import argparse
import random
import re
import sys
from collections import Counter
from pathlib import Path
from statistics import mean

from scripts.xalg.common import (
    GROVER, add_common_args, circuit_path, default_emulate_fault, load_preflight,
    load_qpy, make_budget, make_executor, now, parse_layouts, passing_algorithms, read_json,
    results_root, save_qpy, software_versions,
)
from qrisk.budget import BudgetExceeded
from qrisk.circuits import layout_str
from qrisk.ddmin import save_report
from qrisk.metrics import calculate_tvd, hellinger
from qrisk.patterns import (
    circuits_equivalent, count_linear, count_occurrences, gate_type_key, moment_signature,
    neutral_swaps, normalize_pattern, occurrence_depths, pattern_components, reduce_occurrences,
    timeline_tokens,
)

NEUTRAL_GRID = [0, 2, 4, 6, 8, 10, 12, 15, 18, 20]


def variants_dir(root: Path, backend: str, layout, alg: str) -> Path:
    return root / "variants" / backend / layout_str(layout) / alg


def parse_pattern(text: str):
    """'rz(47) cz(46,47) sx(47)' (arrows/commas between tokens optional)."""
    toks = re.findall(r"([a-z]+)\(([\d,\s]+)\)", text)
    if not toks:
        sys.exit(f"Could not parse pattern: {text}")
    return [(name, [int(q) for q in qs.split(",")], []) for name, qs in toks]


def grover_pattern_for_layout(root: Path, backend: str, layout):
    """Most frequent core among today's Grover DDMin runs (ties: highest R)."""
    d = root / "ddmin" / backend / layout_str(layout) / GROVER
    reports = [read_json(p) for p in sorted(d.glob("run*.json"))] if d.exists() else []
    cores = []
    for r in reports:
        if r.get("core"):
            base = next((e for e in r["ddmin_log"] if e.get("action") == "baseline"), {})
            cores.append((r["core_key"], base.get("ratio", 0.0), r["core"], r["run"]))
    if not cores:
        return None, []
    freq = Counter(k for k, *_ in cores)
    best = max(cores, key=lambda c: (freq[c[0]], c[1]))
    return best[2], [{"run": c[3], "core_key": c[0], "baseline_ratio": c[1]} for c in cores]


def pick_levels(levels):
    levels = sorted(set(levels), reverse=True)
    if len(levels) <= 4:
        return levels
    hi, lo = levels[0], levels[-1]
    want = [hi, lo + round((hi - lo) * 2 / 3), lo + round((hi - lo) / 3), lo]
    return sorted({min(levels, key=lambda x: abs(x - w)) for w in want}, reverse=True)


def build_variants(base, core, per_level: int, n_seeds: int = 40):
    """Return (levels, [variant dicts]) or (levels, []) if not enough range."""
    snaps_by_level = {}
    for seed in range(n_seeds):
        for cnt, circ in reduce_occurrences(base, core, seed=seed):
            snaps_by_level.setdefault(cnt, []).append((seed, circ))
    levels = pick_levels(snaps_by_level)
    variants = []
    for level in levels:
        seen = set()
        chosen = []
        sources = snaps_by_level[level]
        k = 0
        while len(chosen) < per_level and k < per_level * 30:
            n_neutral = NEUTRAL_GRID[len(chosen) % len(NEUTRAL_GRID)]
            src_seed, src = sources[k % len(sources)]
            v = neutral_swaps(src, core, n_neutral, seed=1000 + k) if n_neutral else src
            k += 1
            if count_occurrences(v, core) != level:
                continue
            sig = moment_signature(v)
            if sig in seen:
                continue
            seen.add(sig)
            chosen.append({"level": level, "reduce_seed": src_seed, "n_neutral": n_neutral,
                           "neutral_seed": 1000 + k - 1, "circuit": v})
        variants.extend(chosen)
    return levels, variants


def cmd_plan(args, root: Path, layouts) -> None:
    preflight = load_preflight(root, args.backend)
    manual = parse_pattern(args.pattern) if args.pattern else None
    plans = []
    for layout in layouts:
        if manual:
            core, source = manual, [{"source": "--pattern", "text": args.pattern}]
        else:
            core, source = grover_pattern_for_layout(root, args.backend, layout)
            if not core:
                print(f"Layout {layout}: no Grover pattern from Exp 1 — skipping (or pass --pattern).")
                continue
        if len(pattern_components(core)) != 1:
            print(f"Layout {layout}: pattern is not qubit-connected; skipping.")
            continue
        key = gate_type_key(core)
        print(f"\nLayout {layout}: Grover pattern core = {key}")

        occ = []
        for alg in passing_algorithms(preflight, layout):
            if alg == GROVER and not args.include_grover:
                continue
            isa = load_qpy(circuit_path(root, args.backend, layout, alg))
            toks, _ = timeline_tokens(isa)
            n = count_occurrences(toks, core)
            occ.append((alg, n, count_linear(toks, core)))
            print(f"  {alg:>15}: {n} occurrences (timeline), {occ[-1][2]} (linear, paper matcher)")
        # Rank by the dose range commuting swaps can actually reach (a set that
        # goes to 0 and spans many levels is the strongest test), not raw count.
        eligible = []
        for o in occ:
            if o[1] < args.min_hits:
                continue
            base = load_qpy(circuit_path(root, args.backend, layout, o[0]))
            lo = min(reduce_occurrences(base, core, seed=s)[-1][0] for s in range(5))
            eligible.append((o, lo))
            print(f"  {o[0]:>15}: reachable range {o[1]} -> {lo}")
        eligible.sort(key=lambda x: (x[1] == 0, x[0][1] - x[1]), reverse=True)
        chosen = [o for o, _ in eligible[: args.max_algorithms]]
        for alg, n, _ in chosen:
            base = load_qpy(circuit_path(root, args.backend, layout, alg))
            levels, variants = build_variants(base, core, args.per_level)
            if len(levels) < 3:
                print(f"  {alg}: only levels {levels} reachable — need >= 3; skipped.")
                continue
            out_dir = variants_dir(root, args.backend, layout, alg)
            entries = []
            orig_depths = occurrence_depths(base, core)
            save_qpy(base, out_dir / "original.qpy")
            entries.append({"id": "original", "level": n, "is_original": True, "n_neutral": 0,
                            "qpy": "original.qpy", "linear_hits": count_linear(timeline_tokens(base)[0], core),
                            "mean_depth": round(mean(orig_depths), 4) if orig_depths else None,
                            "depth": base.depth()})
            base_ops = dict(base.count_ops())
            for i, v in enumerate(variants):
                c = v["circuit"]
                if dict(c.count_ops()) != base_ops or not circuits_equivalent(base, c):
                    raise RuntimeError(f"variant {i} of {alg} is not equivalent to the original")
                vid = f"L{v['level']}_{i:03d}"
                save_qpy(c, out_dir / f"{vid}.qpy")
                depths = occurrence_depths(c, core)
                entries.append({"id": vid, "level": v["level"], "is_original": False,
                                "n_neutral": v["n_neutral"], "reduce_seed": v["reduce_seed"],
                                "neutral_seed": v["neutral_seed"], "qpy": f"{vid}.qpy",
                                "linear_hits": count_linear(timeline_tokens(c)[0], core),
                                "mean_depth": round(mean(depths), 4) if depths else None,
                                "depth": c.depth()})
            by_level = Counter(e["level"] for e in entries if not e["is_original"])
            manifest = {
                "created": now(), "backend": args.backend, "layout": layout, "algorithm": alg,
                "pattern_core": [list(t) for t in normalize_pattern(core)], "pattern_key": key,
                "pattern_source": source, "levels": levels, "per_level": dict(by_level),
                "original_level": n, "entries": entries, "versions": software_versions(),
            }
            save_report(manifest, out_dir / "manifest.json")
            plans.append((layout, alg, len(entries)))
            print(f"  -> {alg}: original has {n}; levels {levels}; "
                  f"{dict(by_level)} variants + original = {len(entries)} circuits")

    total = sum(n for *_, n in plans)
    budget = make_budget(args)
    est = budget.seconds_per_circuit_estimate() * total
    print(f"\nPlanned {len(plans)} dose-response sets, {total} circuits; "
          f"estimated QPU ~{est:.0f}s ({est / 60:.1f} min) at {budget.seconds_per_circuit_estimate():.1f}s/circuit.")
    print(budget.summary())


def cmd_run(args, root: Path, layouts) -> None:
    budget = make_budget(args)
    manifests = []
    for layout in layouts:
        base_dir = root / "variants" / args.backend / layout_str(layout)
        for m in sorted(base_dir.glob("*/manifest.json")) if base_dir.exists() else []:
            manifests.append(m)
    if not manifests:
        sys.exit("No manifests found. Run with --plan first.")

    ex = None
    stopped = None
    for mpath in manifests:
        out = mpath.parent / "summary.json"
        if out.exists():
            print(f"{mpath.parent}: already run, skipping.")
            continue
        m = read_json(mpath)
        entries = m["entries"]
        circuits = [load_qpy(mpath.parent / e["qpy"]) for e in entries]
        try:
            budget.check(n_circuits=len(circuits), label=f"variants {m['algorithm']}")
        except BudgetExceeded as e:
            stopped = str(e)
            break
        fault = None
        if args.hardware == "emulate":
            fault = default_emulate_fault(load_qpy(circuit_path(root, args.backend, m["layout"], GROVER)))
        if ex is None or args.hardware == "emulate":
            ex = make_executor(args, budget=budget, emulate_fault=fault)
        else:
            ex.refresh_calibration()

        print(f"\n{m['algorithm']} on {m['layout']}: {len(circuits)} circuits, pattern {m['pattern_key']}")
        calib_before = ex.calibration_info()
        ideal = ex.run_sim_batch(circuits, "ideal_simulator")
        noisy = ex.run_sim_batch(circuits, "noisy_simulator")
        order = list(range(len(circuits)))
        random.Random(42).shuffle(order)
        try:
            real_shuffled = ex.run_real_batch([circuits[i] for i in order],
                                              label=f"variants {m['algorithm']} {layout_str(m['layout'])}")
        except BudgetExceeded as e:
            stopped = str(e)
            break
        real = [None] * len(circuits)
        for pos, i in enumerate(order):
            real[i] = real_shuffled[pos]

        rows = []
        for e, ci, cn, cr in zip(entries, ideal, noisy, real):
            rows.append({
                **e,
                "tvd_noisy_real": calculate_tvd(cn, cr)[0],
                "tvd_ideal_real": calculate_tvd(ci, cr)[0],
                "tvd_ideal_noisy": calculate_tvd(ci, cn)[0],
                "hellinger_noisy_real": hellinger(cn, cr),
                "hellinger_ideal_noisy": hellinger(ci, cn),
                "counts": {"ideal": ci, "noisy": cn, "real": cr},
            })
        summary = {
            "experiment": "xalg_exp2_dose_response",
            **{k: m[k] for k in ("backend", "layout", "algorithm", "pattern_key", "pattern_core",
                                 "levels", "original_level")},
            "hardware": args.hardware, "emulate_fault": fault,
            "calibration_before": calib_before, "calibration_after": ex.calibration_info(),
            "job": ex.last_job, "finished": now(), "shuffle_seed": 42,
            "rows": rows,
        }
        save_report(summary, out)
        for level in m["levels"]:
            vals = [r["tvd_noisy_real"] for r in rows if r["level"] == level and not r["is_original"]]
            if vals:
                print(f"  level {level}: mean TVD(noisy,real) = {mean(vals):.4f}  (n={len(vals)})")
        print(f"  {budget.summary()}")

    if stopped:
        print(f"\nSTOPPED: {stopped}")
        sys.exit(2)
    print("\nExp 2 complete.")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(p)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--plan", action="store_true", help="Build variant sets (no QPU)")
    g.add_argument("--run", action="store_true", help="Execute planned variant sets on hardware")
    p.add_argument("--pattern", default=None,
                   help="Use this pattern instead of Exp 1's Grover pattern, e.g. 'rz(47) cz(46,47) sx(47)'")
    p.add_argument("--per-level", type=int, default=10, help="Variants per occurrence level")
    p.add_argument("--min-hits", type=int, default=2, help="Min occurrences in an algorithm to test it")
    p.add_argument("--max-algorithms", type=int, default=2,
                   help="Algorithms per layout (highest occurrence counts first)")
    p.add_argument("--include-grover", action="store_true",
                   help="Also build variants for Grover itself (positive control)")
    args = p.parse_args()

    root = results_root(args)
    layouts = parse_layouts(args.layouts, args.backend)
    if args.plan:
        cmd_plan(args, root, layouts)
    else:
        cmd_run(args, root, layouts)


if __name__ == "__main__":
    main()
