#!/usr/bin/env python3
"""
Delta Debugging Experiment CLI.

Usage:
    python -m quantum.cli --algorithm artifacts/grover3-2
    python -m quantum.cli --algorithm artifacts/grover3-2 --test-mode
    python -m quantum.cli --algorithm artifacts/grover3-2 --max-granularity 8
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from qiskit import qpy

from .delta_debug import run_delta_debug_on_isa, aggregate_reports
from .executor import QuantumExecutor

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_circuit(artifacts_dir: Path):
    """Load the latest QPY circuit from an artifacts directory."""
    qpy_files = sorted(artifacts_dir.glob("*.qpy"), reverse=True)
    if not qpy_files:
        print(f"No .qpy files found in {artifacts_dir}")
        return None
    path = qpy_files[0]
    print(f"Loading circuit: {path}")
    with open(path, "rb") as f:
        return list(qpy.load(f))[0]


def run_experiment(
    algorithm_dir: str,
    config_file: str = "quantum_config.json",
    max_granularity: int = 16,
    test_mode: bool = False,
):
    artifacts_path = Path(algorithm_dir)
    if not artifacts_path.is_absolute():
        artifacts_path = REPO_ROOT / artifacts_path
    if not artifacts_path.exists():
        print(f"Directory not found: {artifacts_path}")
        return

    isa = load_circuit(artifacts_path)
    if isa is None:
        return

    config_path = str((REPO_ROOT / config_file).resolve())
    executor = QuantumExecutor(config_file=config_path)

    print("\n" + "=" * 60)
    print("Delta Debugging")
    print("=" * 60)

    result = run_delta_debug_on_isa(
        executor=executor,
        isa_circuit=isa,
        max_granularity=max_granularity,
        test_mode=test_mode,
    )

    # Save results
    artifacts_path.mkdir(parents=True, exist_ok=True)
    backend_name = executor.backend.name if executor.backend else "unknown"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{backend_name}_{ts}"

    json_path = artifacts_path / f"{base}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"JSON report: {json_path}")

    # Summary
    baseline = next(e for e in result["ddmin_log"] if e["action"] == "baseline")
    print(f"\nKey Findings:")
    print(f"  Total segments: {len(result['segments_info'])}")
    print(f"  Problematic: {result['problematic_segments']}")
    print(f"  Baseline ratio: {baseline.get('ratio', 'N/A'):.3f} (expected={baseline.get('expected_tvd',0):.4f}, actual={baseline.get('actual_tvd',0):.4f})")
    print(f"  Noise threshold: {baseline.get('noise_threshold', 'N/A')}")
    print(f"  Tests run: {len(result['ddmin_log'])}")
    if result.get("pattern"):
        print(f"  Pattern ({len(result['pattern'])} gates): {result['pattern']}")

    return result


def run_multi(
    algorithm_dir: str,
    runs: int,
    config_file: str = "quantum_config.json",
    max_granularity: int = 16,
    test_mode: bool = False,
):
    """Run DDMin multiple times and produce an aggregate frequency report."""
    results = []
    for i in range(1, runs + 1):
        print(f"\n{'=' * 60}")
        print(f"DDMin Run {i}/{runs}")
        print("=" * 60)
        result = run_experiment(
            algorithm_dir=algorithm_dir,
            config_file=config_file,
            max_granularity=max_granularity,
            test_mode=test_mode,
        )
        if result is not None:
            results.append(result)

    if not results:
        print("No successful runs.")
        return

    # Aggregate
    agg = aggregate_reports(results)

    artifacts_path = Path(algorithm_dir)
    if not artifacts_path.is_absolute():
        artifacts_path = REPO_ROOT / artifacts_path
    artifacts_path.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"aggregate_{runs}runs_{ts}"

    agg_json_path = artifacts_path / f"{base}.json"
    with open(agg_json_path, "w", encoding="utf-8") as f:
        json.dump(agg, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nAggregate JSON: {agg_json_path}")

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"Aggregate Results ({len(results)}/{runs} successful runs)")
    print("=" * 60)
    print(f"{'Segment':>8}  {'Flagged':>7}  {'Freq':>6}  Description")
    print("-" * 60)
    for s in agg["segment_scores"]:
        print(f"  seg {s['segment_id']:<3}  {s['flagged_count']:>3}/{agg['total_runs']}    {s['frequency']:>5.0%}   {s['description']}")


def main():
    parser = argparse.ArgumentParser(description="Delta debugging experiment runner")
    parser.add_argument("--algorithm", "-a", required=True, help="Artifacts directory")
    parser.add_argument("--config", default="quantum_config.json")
    parser.add_argument("--max-granularity", type=int, default=16)
    parser.add_argument("--test-mode", action="store_true")
    parser.add_argument("--runs", type=int, default=1, help="Number of independent DDMin runs (produces aggregate report when > 1)")
    args = parser.parse_args()

    algorithm_dir = args.algorithm
    if not algorithm_dir.startswith("artifacts/"):
        algorithm_dir = f"artifacts/{algorithm_dir}"

    if args.runs > 1:
        run_multi(
            algorithm_dir=algorithm_dir,
            runs=args.runs,
            config_file=args.config,
            max_granularity=args.max_granularity,
            test_mode=args.test_mode,
        )
    else:
        run_experiment(
            algorithm_dir=algorithm_dir,
            config_file=args.config,
            max_granularity=args.max_granularity,
            test_mode=args.test_mode,
        )


if __name__ == "__main__":
    main()
