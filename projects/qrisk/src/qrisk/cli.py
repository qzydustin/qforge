#!/usr/bin/env python3
"""
Run DDMin on one circuit group (the last .qpy by name in the group directory).

Usage:
    python -m qrisk.cli --algorithm grover3-marrakesh-O3-6_7_8_17
    python -m qrisk.cli --algorithm grover3-marrakesh-O3-6_7_8_17 --test-mode
    python -m qrisk.cli --algorithm path/to/group --runs 5

A bare group name is looked up in the data tree's artifacts directory.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from qiskit import qpy

from .ddmin import aggregate_reports, print_summary, run_delta_debug_on_isa, save_report
from .executor import QuantumExecutor
from .paths import ARTIFACTS_DIR, CONFIG_FILE


def group_dir(name: str) -> Path:
    path = Path(name)
    return path if path.is_dir() else ARTIFACTS_DIR / name


def load_circuit(group: Path):
    qpy_files = sorted(group.glob("*.qpy"), reverse=True)
    if not qpy_files:
        sys.exit(f"No .qpy files found in {group}")
    print(f"Loading circuit: {qpy_files[0]}")
    with open(qpy_files[0], "rb") as f:
        return qpy.load(f)[0]


def run_experiment(group: Path, isa, config_file: str, max_granularity: int, test_mode: bool):
    executor = QuantumExecutor(config_file=config_file)

    print("\n" + "=" * 60)
    print("Delta Debugging")
    print("=" * 60)
    result = run_delta_debug_on_isa(
        executor, isa, max_granularity=max_granularity, test_mode=test_mode,
    )

    backend_name = executor.backend.name if executor.backend else "unknown"
    path = group / f"{backend_name}_{datetime.now():%Y%m%d_%H%M%S}.json"
    save_report(result, path)
    print(f"JSON report: {path}")
    print_summary(result)
    return result


def run_multi(group: Path, isa, runs: int, config_file: str, max_granularity: int, test_mode: bool):
    """Run DDMin ``runs`` times and save an aggregate segment-frequency report."""
    results = []
    for i in range(1, runs + 1):
        print(f"\n{'=' * 60}")
        print(f"DDMin Run {i}/{runs}")
        print("=" * 60)
        results.append(run_experiment(group, isa, config_file, max_granularity, test_mode))

    agg = aggregate_reports(results)
    path = group / f"aggregate_{runs}runs_{datetime.now():%Y%m%d_%H%M%S}.json"
    save_report(agg, path)
    print(f"\nAggregate JSON: {path}")

    print(f"\n{'=' * 60}")
    print(f"Aggregate Results ({runs} runs)")
    print("=" * 60)
    print(f"{'Segment':>8}  {'Flagged':>7}  {'Freq':>6}  Description")
    print("-" * 60)
    for s in agg["segment_scores"]:
        print(f"  seg {s['segment_id']:<3}  {s['flagged_count']:>3}/{agg['total_runs']}    {s['frequency']:>5.0%}   {s['description']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--algorithm", "-a", required=True,
                        help="Group directory, or a group name under the artifacts directory")
    parser.add_argument("--config", default=str(CONFIG_FILE))
    parser.add_argument("--max-granularity", type=int, default=16)
    parser.add_argument("--test-mode", action="store_true")
    parser.add_argument("--runs", type=int, default=1, help="Number of independent DDMin runs (produces aggregate report when > 1)")
    args = parser.parse_args()

    group = group_dir(args.algorithm)
    if not group.is_dir():
        sys.exit(f"Directory not found: {group}")
    isa = load_circuit(group)

    if args.runs > 1:
        run_multi(group, isa, args.runs, args.config, args.max_granularity, args.test_mode)
    else:
        run_experiment(group, isa, args.config, args.max_granularity, args.test_mode)


if __name__ == "__main__":
    main()
