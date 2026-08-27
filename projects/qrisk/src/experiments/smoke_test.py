"""Integration test — real IBM Quantum connection with a simple Bell circuit.

Usage:
    python test_integration.py              # simulators only
    python test_integration.py --real       # simulators + real device
"""
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from qiskit import QuantumCircuit
from quantum.executor import QuantumExecutor

CONFIG = str(REPO_ROOT / "quantum_config.json")


def make_bell_isa(executor):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return executor.transpile(qc)


def validate(result, label):
    print(f"\n--- {label} ---")
    assert result["success"], f"{label} failed: {result.get('error')}"
    counts = result["counts"]
    shots = result["shots"]
    total = sum(counts.values())
    print(f"  backend : {result['backend']}")
    print(f"  job_id  : {result.get('job_id')}")
    print(f"  shots   : {shots}")
    print(f"  total   : {total}")
    print(f"  counts  : {counts}")

    p00 = counts.get("00", 0) / total
    p11 = counts.get("11", 0) / total
    dominant = p00 + p11
    print(f"  P(00)   : {p00:.3f}")
    print(f"  P(11)   : {p11:.3f}")
    print(f"  P(00+11): {dominant:.3f}")

    assert total == shots, f"total counts {total} != shots {shots}"
    for k in counts:
        assert len(k) == 2, f"bitstring '{k}' not zero-padded"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--real", action="store_true", help="include real device test")
    args = parser.parse_args()

    print("Connecting to IBM Quantum...")
    qe = QuantumExecutor(config_file=CONFIG)
    print(f"Backend: {qe._backend_name}")

    isa = make_bell_isa(qe)
    print(f"ISA circuit: {isa.num_qubits} qubits, {len(isa.data)} ops")

    validate(qe.run_circuit(isa, "ideal_simulator"), "Ideal Simulator")
    validate(qe.run_circuit(isa, "noisy_simulator"), "Noisy Simulator")

    if args.real:
        validate(qe.run_circuit(isa, "real_device"), "Real Device")

    print("\n=== ALL TESTS PASSED ===")


if __name__ == "__main__":
    main()
