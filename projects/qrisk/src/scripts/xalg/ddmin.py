#!/usr/bin/env python3
"""
Exp 1 — DDMin on Grover + MQT Bench algorithms in ONE calibration window.

For each run r = 1..R, for each layout, for each algorithm (Grover first):
run the QRisk DDMin with the same oracle as the discovery runs, plus:
  * tau clamped at 0,
  * segment 0 (initial state-preparation layer) never a DDMin candidate
    (disable with --no-protect-first-segment),
  * a per-run oracle-call cap (--max-oracle-calls),
  * raw counts of every oracle call saved (for Hellinger re-analysis),
  * a global QPU-time cap shared by all xalg scripts (--budget-min).

Order is round-robin (run 1 of everything before run 2), so if the budget
stops the experiment early you still have one run per (layout, algorithm).
Independent runs execute --parallel at a time so their queue waits overlap;
the budget guard reserves in-flight jobs, so parallelism cannot overshoot it.
Re-running the command resumes: finished runs are skipped.

Usage:
    python -m scripts.xalg.ddmin --backend ibm_fez --runs 2 --budget-min 40
    python -m scripts.xalg.ddmin --backend ibm_fez --hardware emulate --runs 1
"""

from __future__ import annotations

import argparse
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from scripts.xalg.common import (
    DEFAULT_EXP1, GROVER, MOMENTS_PER_SEGMENT, add_common_args, circuit_path, default_emulate_fault,
    load_preflight, load_qpy, make_budget, make_executor, now, parse_layouts, passing_algorithms,
    results_root, software_versions,
)
from qrisk.budget import BudgetExceeded
from qrisk.circuits import layout_str
from qrisk.ddmin import QuantumDeltaDebugger, save_report
from qrisk.patterns import gate_type_key, pattern_core


def report_path(root: Path, backend: str, layout, alg: str, rep: int) -> Path:
    return root / "ddmin" / backend / layout_str(layout) / alg / f"run{rep}.json"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(p)
    p.add_argument("--algorithms", nargs="*", default=DEFAULT_EXP1,
                   help=f"Default: {' '.join(DEFAULT_EXP1)} (only preflight-passing ones run)")
    p.add_argument("--runs", type=int, default=2, help="DDMin runs per (layout, algorithm)")
    p.add_argument("--max-oracle-calls", type=int, default=30,
                   help="Cap on real-device jobs per DDMin run")
    p.add_argument("--max-granularity", type=int, default=16)
    p.add_argument("--no-protect-first-segment", action="store_true",
                   help="Let DDMin select segment 0")
    p.add_argument("--parallel", type=int, default=4,
                   help="DDMin runs in flight at once (overlaps queue waits; each run stays sequential)")
    p.add_argument("--session", action="store_true",
                   help="Use a runtime Session (paid plans; cuts queue waits between DDMin steps)")
    args = p.parse_args()

    root = results_root(args)
    layouts = parse_layouts(args.layouts, args.backend)
    preflight = load_preflight(root, args.backend)
    budget = make_budget(args)
    protected = [] if args.no_protect_first_segment else [0]

    plan = []
    for rep in range(1, args.runs + 1):
        for layout in layouts:
            ok = set(passing_algorithms(preflight, layout)) | {GROVER}
            algs = [a for a in args.algorithms if a in ok]
            skipped = [a for a in args.algorithms if a not in ok]
            if skipped and rep == 1:
                print(f"Layout {layout}: skipping {skipped} (failed preflight)")
            algs = sorted(algs, key=lambda a: a != GROVER)  # Grover first
            for alg in algs:
                plan.append((rep, layout, alg))

    todo = [x for x in plan if not report_path(root, args.backend, x[1], x[2], x[0]).exists()]
    print(f"{len(plan)} DDMin runs planned, {len(plan) - len(todo)} already done, {len(todo)} to go.")
    print(budget.summary())
    if not todo:
        return

    stop = threading.Event()
    stop_reason: list = []
    local = threading.local()
    executors: list = []
    lock = threading.Lock()

    def get_executor(layout):
        fault = None
        if args.hardware == "emulate":
            fault = default_emulate_fault(load_qpy(circuit_path(root, args.backend, layout, GROVER)))
            return make_executor(args, budget=budget, emulate_fault=fault), fault
        ex = getattr(local, "ex", None)
        if ex is None:
            ex = make_executor(args, budget=budget)
            if args.session:
                ex.open_session()
            local.ex = ex
            with lock:
                executors.append(ex)
        else:
            ex.refresh_calibration()
        return ex, fault

    def run_one(i, rep, layout, alg):
        if stop.is_set():
            return
        label = f"ddmin {alg} {layout_str(layout)} run{rep}"
        # Do not start a run the budget cannot plausibly finish.
        need = budget.seconds_per_circuit_estimate() * min(args.max_oracle_calls, 15)
        if budget.remaining_seconds() < need:
            stop.set()
            stop_reason.append(f"remaining budget {budget.remaining_seconds():.0f}s < "
                               f"~{need:.0f}s needed for another run")
            return
        isa = load_qpy(circuit_path(root, args.backend, layout, alg))
        ex, fault = get_executor(layout)
        print(f"\n[{i}/{len(todo)}] START {label}  ({budget.summary()})", flush=True)
        dbg = QuantumDeltaDebugger(
            executor=ex,
            max_granularity=args.max_granularity,
            moments_per_segment=MOMENTS_PER_SEGMENT,
            clamp_threshold=True,
            protected_segments=protected,
            max_oracle_calls=args.max_oracle_calls,
            record_counts=True,
        )
        started = now()
        t0 = time.time()
        incomplete = False
        try:
            result = dbg.debug_circuit(isa)
        except BudgetExceeded as e:
            # Keep what the hardware already produced.
            incomplete = True
            result = dbg._build_result(dbg._last_candidates if dbg.ddmin_log else [])
            stop.set()
            stop_reason.append(str(e))

        pattern = result.get("pattern") or []
        core = pattern_core(pattern) if pattern else []
        report = {
            "experiment": "xalg_exp1_ddmin",
            "algorithm": alg,
            "backend": args.backend,
            "layout": layout,
            "run": rep,
            "hardware": args.hardware,
            "emulate_fault": fault,
            "started": started,
            "finished": now(),
            "wall_seconds": round(time.time() - t0, 1),
            "incomplete": incomplete,
            "calibration": ex.calibration_info(),
            "versions": software_versions(),
            "qpu_seconds": round(sum((c.get("qpu_seconds") or 0) for c in result.get("oracle_log", [])), 2),
            "pattern_key": gate_type_key(pattern) if pattern else "",
            "core_key": gate_type_key(core) if core else "",
            "core": [list(t) for t in core],
            **result,
        }
        save_report(report, report_path(root, args.backend, layout, alg, rep))
        base = next((e for e in result["ddmin_log"] if e.get("action") == "baseline"), {})
        print(f"[{i}/{len(todo)}] DONE {label}: baseline R={base.get('ratio')} tau={base.get('noise_threshold')} "
              f"segments={result['problematic_segments']} calls={result.get('oracle_calls')}"
              f"{' (truncated)' if result.get('truncated') else ''}"
              f"{' core: ' + report['core_key'] if report['core_key'] else ''}", flush=True)

    workers = max(1, args.parallel)
    print(f"Running with {workers} parallel DDMin worker(s).")
    pool = ThreadPoolExecutor(max_workers=workers)
    futures = [pool.submit(run_one, i, rep, layout, alg)
               for i, (rep, layout, alg) in enumerate(todo, 1)]
    try:
        for f in as_completed(futures):
            exc = f.exception()
            if exc is not None:
                print(f"  run failed: {type(exc).__name__}: {exc}", flush=True)
    except KeyboardInterrupt:
        stop.set()
        stop_reason.append("interrupted by user (finished runs are saved; re-run to resume)")
        pool.shutdown(wait=False, cancel_futures=True)
        raise SystemExit(2)
    finally:
        pool.shutdown(wait=True, cancel_futures=True)
        for ex in executors:
            ex.close_session()

    print("\n" + budget.summary())
    if stop_reason:
        print(f"STOPPED: {stop_reason[0]}")
        sys.exit(2)
    print("Exp 1 complete.")


if __name__ == "__main__":
    main()
