#!/usr/bin/env python3
"""
Run all verify-set QPY circuits on real hardware and record TVD results.

Reads a selection_manifest.json, executes each circuit on ideal simulator,
noisy simulator, and real device, then outputs a summary.json matching
the project's standard bucket format.

Usage:
    python experiments/run_verify_batch.py \
        --verify-dir artifacts/grover3-fez-O3-97_106_107_108/variants/verify

    python experiments/run_verify_batch.py \
        --verify-dir artifacts/grover3-marrakesh-O3-6_7_8_17/variants/verify \
        --shots 8192
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from pathlib import Path
from typing import Any

from qiskit import qpy

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from quantum.executor import QuantumExecutor
from quantum.metrics import calculate_tvd


def resolve_path(path_str: str) -> Path:
    path = Path(path_str)
    if path.is_absolute():
        return path
    return (REPO_ROOT / path).resolve()


def load_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Flatten manifest into a shuffled list of entries."""
    entries = []
    for bucket_name, items in manifest.get("selected", {}).items():
        for item in items:
            entries.append({
                "bucket": bucket_name,
                "variant_index": item["variant_index"],
                "n_swaps": item.get("n_swaps", 0),
                "qpy_path": resolve_path(item["qpy_path"]),
                "qpy_name": item.get("qpy_name", Path(item["qpy_path"]).name),
                "pattern_hits": item.get("total_hits", 0),
            })
    # Shuffle to interleave buckets, avoiding hardware drift bias
    random.seed(42)
    random.shuffle(entries)
    return entries


def run_single(executor: QuantumExecutor, circuit, shots: int) -> dict[str, Any]:
    """Execute circuit on ideal, noisy, and real backends."""
    ideal = executor.run_circuit(circuit, execution_type="ideal_simulator", shots=shots)
    noisy = executor.run_circuit(circuit, execution_type="noisy_simulator", shots=shots)
    real = executor.run_circuit(circuit, execution_type="real_device", shots=shots)

    for label, result in [("ideal", ideal), ("noisy", noisy), ("real", real)]:
        if not result.get("success"):
            raise RuntimeError(f"{label} execution failed: {result.get('error')}")

    tvd_ideal_real, _ = calculate_tvd(ideal["counts"], real["counts"])
    tvd_noisy_real, _ = calculate_tvd(noisy["counts"], real["counts"])
    tvd_ideal_noisy, _ = calculate_tvd(ideal["counts"], noisy["counts"])

    return {
        "tvd_ideal_vs_real": tvd_ideal_real,
        "tvd_noisy_vs_real": tvd_noisy_real,
        "tvd_ideal_vs_noisy": tvd_ideal_noisy,
        "real_backend": real.get("backend", ""),
    }


def build_summary(
    manifest: dict[str, Any],
    results: list[dict[str, Any]],
    shots: int,
) -> dict[str, Any]:
    """Build summary.json in the project's standard bucket format."""
    by_bucket: dict[str, list[dict]] = {}
    for r in results:
        by_bucket.setdefault(r["bucket"], []).append(r)

    buckets = {}
    for bucket_name in sorted(by_bucket):
        items = by_bucket[bucket_name]
        vals = [r["tvd_noisy_vs_real"] for r in items]

        completed = []
        for r in items:
            completed.append({
                "pattern_hits": r["pattern_hits"],
                "n_swaps": r["n_swaps"],
                "tvd_ideal_vs_real": r["tvd_ideal_vs_real"],
                "tvd_noisy_vs_real": r["tvd_noisy_vs_real"],
                "tvd_ideal_vs_noisy": r["tvd_ideal_vs_noisy"],
            })

        buckets[bucket_name] = {
            "stats": {
                "count": len(vals),
                "mean": round(sum(vals) / len(vals), 6),
                "std": round(statistics.stdev(vals), 6) if len(vals) > 1 else 0,
                "min": min(vals),
                "max": max(vals),
                "median": round(statistics.median(vals), 6),
            },
            "completed": completed,
        }

    return {
        "experiment": manifest.get("experiment", "verify_batch"),
        "backend": manifest.get("backend", ""),
        "layout": manifest.get("layout", []),
        "pattern": manifest.get("pattern", ""),
        "shots": shots,
        "buckets": buckets,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run verify-set circuits on real hardware and record TVD results."
    )
    parser.add_argument(
        "--verify-dir", required=True,
        help="Directory containing selection_manifest.json and hit_*/",
    )
    parser.add_argument("--config", default="quantum_config.json")
    parser.add_argument("--shots", type=int, default=None)
    parser.add_argument(
        "--backend", default=None,
        help="Override backend (e.g. ibm_fez, ibm_kingston, ibm_marrakesh). "
             "Defaults to the group's own backend inferred from the manifest.",
    )
    args = parser.parse_args()

    verify_dir = resolve_path(args.verify_dir)
    manifest_path = verify_dir / "selection_manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"selection_manifest.json not found in {verify_dir}")

    with manifest_path.open() as f:
        manifest = json.load(f)

    entries = load_entries(manifest)
    if not entries:
        raise ValueError(f"No entries found in {manifest_path}")

    # Resolve the backend for this run: explicit flag > manifest backend.
    desired_backend = args.backend or manifest.get("backend")
    config_path = resolve_path(args.config)
    # Create a per-backend temp config copy so parallel runs on different
    # backends don't clobber the shared quantum_config.json.
    if desired_backend:
        import tempfile, shutil
        with open(config_path) as f:
            cfg = json.load(f)
        if cfg.get("ibm_quantum", {}).get("backend") != desired_backend:
            cfg["ibm_quantum"]["backend"] = desired_backend
        tmp_config = verify_dir / f".tmp_config_{desired_backend}.json"
        with open(tmp_config, "w") as f:
            json.dump(cfg, f, indent=2)
        config_path = tmp_config
        print(f"[config] using temp config for backend -> {desired_backend}")
    executor = QuantumExecutor(config_file=str(config_path))
    shots = args.shots or executor.config["execution"]["shots"]

    print(f"Verify dir: {verify_dir}")
    print(f"Circuits: {len(entries)}")
    print(f"Shots: {shots}")
    print(f"Backend: {getattr(executor.backend, 'name', '?')}")
    print()

    results = []
    progress_path = verify_dir / "progress.jsonl"
    for idx, entry in enumerate(entries, 1):
        qpy_path = entry["qpy_path"]
        print(
            f"[{idx:02d}/{len(entries):02d}] {entry['bucket']} | "
            f"hits={entry['pattern_hits']} | {entry['qpy_name']}",
            flush=True,
        )

        try:
            with qpy_path.open("rb") as f:
                circuit = list(qpy.load(f))[0]
            metrics = run_single(executor, circuit, shots)
            record = {**entry, **metrics, "status": "success"}
            results.append(record)
            print(
                f"  TVD(noisy,real)={metrics['tvd_noisy_vs_real']:.4f} | "
                f"backend={metrics['real_backend']}",
                flush=True,
            )
        except Exception as exc:
            record = {**entry, "status": "failed", "error": str(exc)}
            results.append(record)
            print(f"  FAILED: {exc}", flush=True)

        # Incremental save — each result appended immediately so nothing is
        # lost if the process is killed (SSH disconnect, timeout, etc.).
        with progress_path.open("a") as pf:
            # Convert Path objects to str for JSON serialization
            serializable = {k: (str(v) if isinstance(v, Path) else v)
                           for k, v in record.items()}
            pf.write(json.dumps(serializable) + "\n")

    # Build and save summary
    successful = [r for r in results if r["status"] == "success"]
    summary = build_summary(manifest, successful, shots)

    summary_path = verify_dir / "summary.json"
    with summary_path.open("w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nResults: {len(successful)}/{len(entries)} successful")
    print(f"Summary: {summary_path}")
    for b, d in summary["buckets"].items():
        s = d["stats"]
        print(f"  {b}: N={s['count']}, mean={s['mean']:.4f}, std={s['std']:.4f}")


if __name__ == "__main__":
    main()
