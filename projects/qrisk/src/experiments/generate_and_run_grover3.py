#!/usr/bin/env python3
"""
Generate grover3 ISA circuits for 3 backends x 3 qubit layouts each,
then run delta debug on each configuration.

Backends: ibm_fez, ibm_marrakesh, ibm_kingston
Each backend gets 3 different qubit layout groups (star-4 topology).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, qpy
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from quantum.delta_debug import run_delta_debug_on_isa
from quantum.executor import QuantumExecutor


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


def grover_3q_circuit(marked_state: int = 7) -> QuantumCircuit:
    n = 3
    inp = QuantumRegister(n, "inp")
    anc = QuantumRegister(1, "anc")
    creg = ClassicalRegister(n, "c")
    qc = QuantumCircuit(inp, anc, creg)

    for q in range(n):
        qc.h(inp[q])
    qc.x(anc[0])
    qc.h(anc[0])
    qc.barrier()

    bitstring = format(marked_state, f"0{n}b")[::-1]
    for i, b in enumerate(bitstring):
        if b == "0":
            qc.x(inp[i])
    qc.mcx([inp[i] for i in range(n)], anc[0])
    for i, b in enumerate(bitstring):
        if b == "0":
            qc.x(inp[i])
    qc.barrier()

    for q in range(n):
        qc.h(inp[q])
    for q in range(n):
        qc.x(inp[q])
    qc.h(inp[-1])
    qc.mcx([inp[i] for i in range(n - 1)], inp[-1])
    qc.h(inp[-1])
    for q in range(n):
        qc.x(inp[q])
    for q in range(n):
        qc.h(inp[q])
    qc.barrier()

    qc.h(anc[0])
    qc.x(anc[0])
    qc.barrier()

    for i in range(n):
        qc.measure(inp[i], creg[i])
    return qc


def grover_3q_repeated(repetitions: int = 3, marked_state: int = 7) -> QuantumCircuit:
    n = 3
    inp = QuantumRegister(n, "inp")
    anc = QuantumRegister(1, "anc")
    creg = ClassicalRegister(n, "c")
    qc = QuantumCircuit(inp, anc, creg)

    for q in range(n):
        qc.h(inp[q])
    qc.x(anc[0])
    qc.h(anc[0])
    qc.barrier()

    bitstring = format(marked_state, f"0{n}b")[::-1]

    for _ in range(repetitions):
        for i, b in enumerate(bitstring):
            if b == "0":
                qc.x(inp[i])
        qc.mcx([inp[i] for i in range(n)], anc[0])
        for i, b in enumerate(bitstring):
            if b == "0":
                qc.x(inp[i])
        qc.barrier()

        for q in range(n):
            qc.h(inp[q])
        for q in range(n):
            qc.x(inp[q])
        qc.h(inp[-1])
        qc.mcx([inp[i] for i in range(n - 1)], inp[-1])
        qc.h(inp[-1])
        for q in range(n):
            qc.x(inp[q])
        for q in range(n):
            qc.h(inp[q])
        qc.barrier()

    qc.h(anc[0])
    qc.x(anc[0])
    qc.barrier()

    for i in range(n):
        qc.measure(inp[i], creg[i])
    return qc


def generate_isa_circuit(backend, circuit: QuantumCircuit, initial_layout: list[int]) -> QuantumCircuit:
    pm = generate_preset_pass_manager(
        optimization_level=3,
        backend=backend,
        initial_layout=initial_layout,
    )
    return pm.run(circuit)


def layout_str(layout: list[int]) -> str:
    return "_".join(map(str, layout))


def generate_all(config_path: Path):
    """Generate all ISA circuits and save to artifacts."""
    with open(config_path) as f:
        config = json.load(f)

    runtime_config = config["ibm_quantum"]
    accounts = runtime_config.get("accounts", [])
    if not accounts or not accounts[0].get("token"):
        raise ValueError("Configure at least one IBM Quantum account with a token.")
    account = accounts[0]
    service = QiskitRuntimeService(
        channel=account.get("channel") or runtime_config.get("channel"),
        token=account["token"],
        instance=account.get("instance") or runtime_config.get("instance"),
    )

    logical_1x = grover_3q_circuit(marked_state=7)
    logical_3x = grover_3q_repeated(repetitions=3, marked_state=7)

    generated = []

    for backend_name, layouts in EXPERIMENTS.items():
        print(f"\n{'='*60}")
        print(f"Backend: {backend_name}")
        print(f"{'='*60}")
        backend = service.backend(backend_name)

        for layout in layouts:
            layout_s = layout_str(layout)
            dir_name = f"grover3-{backend_name.replace('ibm_', '')}-O3-{layout_s}"
            artifacts_dir = REPO_ROOT / "artifacts" / dir_name
            artifacts_dir.mkdir(parents=True, exist_ok=True)

            print(f"\n  Layout: {layout} -> {dir_name}")

            isa_1x = generate_isa_circuit(backend, logical_1x, layout)
            isa_3x = generate_isa_circuit(backend, logical_3x, layout)

            qpy_1x = artifacts_dir / "base_1x.qpy"
            qpy_3x = artifacts_dir / "base_3x.qpy"

            with open(qpy_1x, "wb") as f:
                qpy.dump([isa_1x], f)
            with open(qpy_3x, "wb") as f:
                qpy.dump([isa_3x], f)

            print(f"    1x: depth={isa_1x.depth()}, ops={sum(isa_1x.count_ops().values())}")
            print(f"    3x: depth={isa_3x.depth()}, ops={sum(isa_3x.count_ops().values())}")
            print(f"    Saved: {qpy_1x.name}, {qpy_3x.name}")

            generated.append({
                "backend": backend_name,
                "layout": layout,
                "dir": str(artifacts_dir),
                "dir_name": dir_name,
            })

    return generated


def run_ddmin_all(generated: list[dict], config_path: Path):
    """Run delta debug on each generated circuit."""
    config_path = config_path.resolve()

    for item in generated:
        backend_name = item["backend"]
        layout = item["layout"]
        dir_name = item["dir_name"]
        artifacts_dir = Path(item["dir"])

        print(f"\n{'='*60}")
        print(f"Delta Debug: {dir_name}")
        print(f"  Backend: {backend_name}, Layout: {layout}")
        print(f"{'='*60}")

        qpy_3x = artifacts_dir / "base_3x.qpy"
        with open(qpy_3x, "rb") as f:
            isa = list(qpy.load(f))[0]

        # Create executor with the correct backend
        with open(config_path) as f:
            config = json.load(f)
        config["ibm_quantum"]["backend"] = backend_name

        tmp_config = artifacts_dir / "config_tmp.json"
        with open(tmp_config, "w") as f:
            json.dump(config, f)

        try:
            executor = QuantumExecutor(config_file=str(tmp_config))
        except Exception as e:
            print(f"  ERROR creating executor: {e}")
            continue

        try:
            result = run_delta_debug_on_isa(
                executor=executor,
                isa_circuit=isa,
                max_granularity=16,
            )
        except Exception as e:
            print(f"  ERROR running ddmin: {e}")
            continue

        # Save result
        ddmin_dir = artifacts_dir / "ddmin_reports"
        ddmin_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = ddmin_dir / f"{backend_name.replace('ibm_', '')}_{ts}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=str)
        print(f"  Report saved: {json_path}")

        # Summary
        baseline = next(
            (e for e in result["ddmin_log"] if e["action"] == "baseline"), {}
        )
        print(f"  Baseline ratio: {baseline.get('ratio', 'N/A')}")
        print(f"  Noise threshold: {baseline.get('noise_threshold', 'N/A')}")
        print(f"  Problematic segments: {result.get('problematic_segments', [])}")

        # Cleanup tmp config
        tmp_config.unlink(missing_ok=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-only", action="store_true",
                        help="Only generate circuits, don't run delta debug")
    parser.add_argument("--run-only", action="store_true",
                        help="Only run delta debug (circuits must exist)")
    parser.add_argument("--backend", type=str, default=None,
                        help="Run only for specific backend (e.g. ibm_fez)")
    parser.add_argument("--layout-index", type=int, default=None,
                        help="Run only for specific layout index (0, 1, 2)")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "quantum_config.json",
                        help="Path to a local IBM Quantum configuration file")
    args = parser.parse_args()

    if args.backend:
        EXPERIMENTS = {k: v for k, v in EXPERIMENTS.items() if k == args.backend}
    if args.layout_index is not None:
        EXPERIMENTS = {k: [v[args.layout_index]] for k, v in EXPERIMENTS.items()}

    if args.run_only:
        items = []
        for backend_name, layouts in EXPERIMENTS.items():
            for layout in layouts:
                layout_s = layout_str(layout)
                dir_name = f"grover3-{backend_name.replace('ibm_', '')}-O3-{layout_s}"
                artifacts_dir = REPO_ROOT / "artifacts" / dir_name
                items.append({
                    "backend": backend_name,
                    "layout": layout,
                    "dir": str(artifacts_dir),
                    "dir_name": dir_name,
                })
        run_ddmin_all(items, args.config)
    elif args.generate_only:
        generate_all(args.config)
    else:
        generated = generate_all(args.config)
        run_ddmin_all(generated, args.config)
