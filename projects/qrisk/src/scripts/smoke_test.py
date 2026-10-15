"""Smoke test of QuantumExecutor with a Bell circuit.

Usage:
    python -m scripts.smoke_test          # offline: fake backend, emulated device, no IBM calls
    python -m scripts.smoke_test --real   # IBM Quantum: simulators + one real-device job
"""
import argparse

from qiskit import QuantumCircuit

from qrisk.executor import QuantumExecutor
from qrisk.paths import CONFIG_EXAMPLE, CONFIG_FILE


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
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--real", action="store_true", help="connect to IBM Quantum and run on the real device")
    args = parser.parse_args()

    if args.real:
        print("Connecting to IBM Quantum...")
        qe = QuantumExecutor(config_file=CONFIG_FILE)
    else:
        # The example config: an offline run never needs the credentials file.
        qe = QuantumExecutor(config_file=CONFIG_EXAMPLE, hardware="emulate")

    isa = make_bell_isa(qe)
    print(f"ISA circuit: {isa.num_qubits} qubits, {len(isa.data)} ops")

    validate(qe.run_circuit(isa, "ideal_simulator"), "Ideal Simulator")
    validate(qe.run_circuit(isa, "noisy_simulator"), "Noisy Simulator")
    validate(qe.run_circuit(isa, "real_device"), "Real Device" if args.real else "Emulated Device")

    print("\n=== ALL TESTS PASSED ===")


if __name__ == "__main__":
    main()
