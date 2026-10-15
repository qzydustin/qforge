#!/usr/bin/env python3
"""
Step 2 — submit ONE small job to measure the real QPU cost per circuit.

Runs the Grover reference circuit (first layout) once at the configured shot
count, prints the QPU seconds IBM charged, and records it in the shared
ledger, so the budget guard uses a measured per-circuit cost from then on.
Also prints the instance's remaining quota when IBM reports one.

Usage:
    python -m scripts.xalg.probe --backend ibm_fez
"""

from __future__ import annotations

import argparse
import time

from scripts.xalg.common import (
    GROVER, add_common_args, circuit_path, load_qpy, make_budget, make_executor,
    parse_layouts, results_root,
)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(p)
    args = p.parse_args()

    root = results_root(args)
    layout = parse_layouts(args.layouts, args.backend)[0]
    budget = make_budget(args)
    ex = make_executor(args, budget=budget)

    if args.hardware == "ibm":
        try:
            usage = ex.service_manager.service.usage()
            rem = usage.get("usage_remaining_seconds")
            if rem is not None:
                print(f"IBM instance quota remaining: {rem:.0f}s ({rem / 60:.1f} min)")
            else:
                print(f"IBM usage info: {usage}")
        except Exception as e:
            print(f"(could not read instance usage: {e})")
        try:
            print(f"{args.backend} pending jobs in queue: {ex.backend.status().pending_jobs}")
        except Exception:
            pass

    isa = load_qpy(circuit_path(root, args.backend, layout, GROVER))
    print(f"Submitting 1 circuit ({ex.config['execution']['shots']} shots) to {args.backend} ...", flush=True)
    t0 = time.time()
    res = ex.run_circuit(isa, "real_device", label="probe")
    if not res.get("success"):
        raise SystemExit(f"Probe failed: {res.get('error')}")
    print(f"Done in {time.time() - t0:.0f}s wall-clock (includes queue).")
    print(f"QPU seconds charged: {ex.last_job.get('seconds')} (measured={ex.last_job.get('measured')})")
    print(budget.summary())


if __name__ == "__main__":
    main()
