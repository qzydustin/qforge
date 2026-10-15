#!/usr/bin/env python3
"""
Compile the Grover-3 circuit for every (backend, layout) group in EXPERIMENTS,
then run DDMin on each group's base_3x circuit on IBM hardware.

Each group directory gets base_1x.qpy and base_3x.qpy (1 and 3 Grover
iterations); DDMin reports go to its ddmin_reports/.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from qiskit import qpy

from qrisk.circuits import compile_isa, grover_3q, layout_str
from qrisk.config import load_config
from qrisk.ddmin import print_summary, run_delta_debug_on_isa, save_report
from qrisk.executor import QuantumExecutor
from qrisk.ibm_runtime import QuantumServiceManager
from qrisk.paths import ARTIFACTS_DIR


EXPERIMENTS = {
    "ibm_fez": [
        [2, 3, 4, 16],
        [24, 25, 26, 37],
        [46, 47, 48, 57],
        [50, 51, 52, 58],
        [64, 65, 66, 77],
        [97, 106, 107, 108],
        [100, 101, 102, 116],
        [126, 127, 128, 137],
        [130, 131, 132, 138],
        [138, 150, 151, 152],
    ],
    "ibm_marrakesh": [
        [2, 3, 4, 16],
        [6, 7, 8, 17],
        [20, 21, 22, 36],
        [24, 25, 26, 37],
        [50, 51, 52, 58],
        [64, 65, 66, 77],
        [100, 101, 102, 116],
        [118, 128, 129, 130],
        [126, 127, 128, 137],
        [138, 150, 151, 152],
    ],
    "ibm_kingston": [
        [2, 3, 4, 16],
        [10, 11, 12, 18],
        [24, 25, 26, 37],
        [50, 51, 52, 58],
        [56, 62, 63, 64],
        [64, 65, 66, 77],
        [100, 101, 102, 116],
        [126, 127, 128, 137],
        [136, 142, 143, 144],
        [138, 150, 151, 152],
    ],
}


def group_dir(backend_name: str, layout: list[int]) -> Path:
    short = backend_name.replace("ibm_", "")
    return ARTIFACTS_DIR / f"grover3-{short}-O3-{layout_str(layout)}"


def generate_all(experiments: dict[str, list[list[int]]]) -> None:
    manager = QuantumServiceManager(load_config())
    if not manager.connect():
        sys.exit(f"Could not connect to IBM Quantum: {manager.last_connect_error}")
    logical = {"base_1x": grover_3q(iterations=1), "base_3x": grover_3q(iterations=3)}

    for backend_name, layouts in experiments.items():
        print(f"\n{'='*60}")
        print(f"Backend: {backend_name}")
        print(f"{'='*60}")
        backend = manager.select_backend(backend_name)
        if backend is None:
            sys.exit(f"Backend {backend_name} is not available to the selected account")

        for layout in layouts:
            out = group_dir(backend_name, layout)
            out.mkdir(parents=True, exist_ok=True)
            print(f"\n  Layout: {layout} -> {out.name}")
            for name, circuit in logical.items():
                isa = compile_isa(circuit, backend, layout)
                with open(out / f"{name}.qpy", "wb") as f:
                    qpy.dump([isa], f)
                print(f"    {name}.qpy: depth={isa.depth()}, ops={sum(isa.count_ops().values())}")


def run_ddmin_all(experiments: dict[str, list[list[int]]]) -> None:
    for backend_name, layouts in experiments.items():
        for layout in layouts:
            group = group_dir(backend_name, layout)
            print(f"\n{'='*60}")
            print(f"Delta Debug: {group.name}")
            print(f"  Backend: {backend_name}, Layout: {layout}")
            print(f"{'='*60}")

            with open(group / "base_3x.qpy", "rb") as f:
                isa = qpy.load(f)[0]
            try:
                executor = QuantumExecutor(backend_name=backend_name)
                result = run_delta_debug_on_isa(executor, isa)
            except Exception as e:
                print(f"  ERROR: {type(e).__name__}: {e}")
                continue

            short = backend_name.replace("ibm_", "")
            path = group / "ddmin_reports" / f"{short}_{datetime.now():%Y%m%d_%H%M%S}.json"
            save_report(result, path)
            print(f"  Report saved: {path}")
            print_summary(result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--generate-only", action="store_true",
                      help="Only generate circuits, don't run delta debug")
    mode.add_argument("--run-only", action="store_true",
                      help="Only run delta debug (circuits must exist)")
    parser.add_argument("--backend", choices=sorted(EXPERIMENTS),
                        help="Run only for this backend")
    parser.add_argument("--layout-index", type=int, default=None,
                        help="Run only the layout at this index of each backend's list")
    args = parser.parse_args()

    experiments = {b: layouts for b, layouts in EXPERIMENTS.items()
                   if args.backend in (None, b)}
    if args.layout_index is not None:
        experiments = {b: [layouts[args.layout_index]] for b, layouts in experiments.items()}

    if not args.run_only:
        generate_all(experiments)
    if not args.generate_only:
        run_ddmin_all(experiments)


if __name__ == "__main__":
    main()
