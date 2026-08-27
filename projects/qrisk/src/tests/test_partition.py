"""Tests for quantum.partition — moment-based circuit segmentation.

Verifies that our ASAP moment assignment matches Qiskit's DAGCircuit.layers()
across a variety of circuit structures.
"""

import pytest
from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag

from quantum.partition import assign_moments, segment_circuit

SKIP_OPS = frozenset(["measure", "barrier", "delay", "reset"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _dag_moments(circuit: QuantumCircuit) -> dict[int, list[tuple]]:
    """Extract moments from Qiskit's dag.layers() as {moment_id: [(op, qubits), ...]}."""
    dag = circuit_to_dag(circuit)
    moments: dict[int, list[tuple]] = {}
    moment_id = 0
    for layer_dict in dag.layers():
        ops = []
        for node in layer_dict["graph"].op_nodes():
            if node.op.name in SKIP_OPS:
                continue
            qubits = sorted(circuit.find_bit(q).index for q in node.qargs)
            ops.append((node.op.name, tuple(qubits)))
        if ops:
            moments[moment_id] = sorted(ops)
            moment_id += 1
    return moments


def _our_moments(circuit: QuantumCircuit) -> dict[int, list[tuple]]:
    """Extract moments from our assign_moments() in the same format."""
    raw = assign_moments(circuit)
    moments: dict[int, list[tuple]] = {}
    for m_id in sorted(raw.keys()):
        ops = [(d["operation"], tuple(sorted(d["qubits"]))) for d in raw[m_id]]
        moments[m_id] = sorted(ops)
    return moments


def assert_moments_match(circuit: QuantumCircuit) -> None:
    """Assert our moments match Qiskit's dag.layers() for the given circuit."""
    ours = _our_moments(circuit)
    theirs = _dag_moments(circuit)
    assert len(ours) == len(theirs), (
        f"Moment count mismatch: ours={len(ours)}, dag={len(theirs)}"
    )
    for m_id in ours:
        assert ours[m_id] == theirs[m_id], (
            f"Moment {m_id} mismatch:\n  ours:  {ours[m_id]}\n  dag:   {theirs[m_id]}"
        )


# ---------------------------------------------------------------------------
# Test: assign_moments matches dag.layers()
# ---------------------------------------------------------------------------

class TestAssignMomentsDagConsistency:
    """Verify assign_moments produces the same layers as Qiskit's DAG."""

    def test_linear_chain(self):
        """All gates on the same qubit — each gets its own moment."""
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.x(0)
        qc.z(0)
        qc.measure_all()
        assert_moments_match(qc)
        moments = assign_moments(qc)
        assert len(moments) == 3

    def test_fully_parallel(self):
        """All gates on disjoint qubits — all in one moment."""
        qc = QuantumCircuit(4)
        qc.h(0)
        qc.x(1)
        qc.z(2)
        qc.y(3)
        qc.measure_all()
        assert_moments_match(qc)
        moments = assign_moments(qc)
        assert len(moments) == 1
        assert len(moments[0]) == 4

    def test_mixed_parallel_serial(self):
        """Paper-like example: some parallelism, some serial dependencies."""
        qc = QuantumCircuit(3)
        qc.h(0)
        qc.h(1)
        qc.cx(0, 1)
        qc.h(2)
        qc.cx(1, 2)
        qc.h(0)
        qc.cx(0, 2)
        qc.measure_all()
        assert_moments_match(qc)
        moments = assign_moments(qc)
        # Moment 0: h(0), h(1), h(2)
        # Moment 1: cx(0,1)
        # Moment 2: cx(1,2), h(0)
        # Moment 3: cx(0,2)
        assert len(moments) == 4

    def test_two_qubit_gate_chain(self):
        """Chain of CX gates forces serial moments."""
        qc = QuantumCircuit(3)
        qc.cx(0, 1)
        qc.cx(1, 2)
        qc.cx(0, 2)
        qc.measure_all()
        assert_moments_match(qc)

    def test_interleaved_single_two_qubit(self):
        """Mix of single-qubit and two-qubit gates with partial parallelism."""
        qc = QuantumCircuit(4)
        qc.h(0)
        qc.h(1)
        qc.cx(0, 1)
        qc.h(2)
        qc.h(3)
        qc.cx(2, 3)
        qc.cx(1, 2)
        qc.measure_all()
        assert_moments_match(qc)

    def test_parametric_gates(self):
        """Gates with parameters should be assigned to moments correctly."""
        qc = QuantumCircuit(2)
        qc.rz(0.5, 0)
        qc.rz(0.3, 1)
        qc.cz(0, 1)
        qc.rz(1.0, 0)
        qc.measure_all()
        assert_moments_match(qc)

    def test_empty_circuit(self):
        """Circuit with no gates produces no moments."""
        qc = QuantumCircuit(2)
        qc.measure_all()
        moments = assign_moments(qc)
        assert len(moments) == 0

    def test_single_gate(self):
        """Single gate in the circuit."""
        qc = QuantumCircuit(2)
        qc.cx(0, 1)
        qc.measure_all()
        assert_moments_match(qc)
        moments = assign_moments(qc)
        assert len(moments) == 1

    def test_wide_circuit(self):
        """Many qubits with parallel operations."""
        n = 10
        qc = QuantumCircuit(n)
        for i in range(n):
            qc.h(i)
        for i in range(0, n - 1, 2):
            qc.cx(i, i + 1)
        for i in range(n):
            qc.x(i)
        qc.measure_all()
        assert_moments_match(qc)


# ---------------------------------------------------------------------------
# Test: segment_circuit
# ---------------------------------------------------------------------------

class TestSegmentCircuit:
    """Verify segment grouping logic."""

    def _make_test_circuit(self) -> QuantumCircuit:
        """4-moment circuit for segmentation tests."""
        qc = QuantumCircuit(3)
        qc.h(0)        # moment 0
        qc.h(1)        # moment 0
        qc.cx(0, 1)    # moment 1
        qc.h(2)        # moment 0
        qc.cx(1, 2)    # moment 2
        qc.h(0)        # moment 2
        qc.cx(0, 2)    # moment 3
        qc.measure_all()
        return qc

    def test_default_3_moments_per_segment(self):
        qc = self._make_test_circuit()
        segs = segment_circuit(qc, moments_per_segment=3)
        assert len(segs) == 2
        assert segs[0]["moments"] == [0, 1, 2]
        assert segs[1]["moments"] == [3]

    def test_1_moment_per_segment(self):
        qc = self._make_test_circuit()
        segs = segment_circuit(qc, moments_per_segment=1)
        assert len(segs) == 4
        for i, seg in enumerate(segs):
            assert seg["moments"] == [i]

    def test_large_segment_size(self):
        """Segment size larger than total moments -> single segment."""
        qc = self._make_test_circuit()
        segs = segment_circuit(qc, moments_per_segment=100)
        assert len(segs) == 1
        assert segs[0]["moments"] == [0, 1, 2, 3]

    def test_2_moments_per_segment(self):
        qc = self._make_test_circuit()
        segs = segment_circuit(qc, moments_per_segment=2)
        assert len(segs) == 2
        assert segs[0]["moments"] == [0, 1]
        assert segs[1]["moments"] == [2, 3]

    def test_segment_ids_are_sequential(self):
        qc = self._make_test_circuit()
        segs = segment_circuit(qc, moments_per_segment=1)
        for i, seg in enumerate(segs):
            assert seg["layer_id"] == i

    def test_all_gates_accounted_for(self):
        """Every non-skip gate appears in exactly one segment."""
        qc = self._make_test_circuit()
        segs = segment_circuit(qc, moments_per_segment=2)
        all_indices = set()
        for seg in segs:
            for inst in seg["instructions"]:
                assert inst["index"] not in all_indices, (
                    f"Gate index {inst['index']} appears in multiple segments"
                )
                all_indices.add(inst["index"])

        # Count non-skip gates in original circuit
        skip = {"measure", "barrier", "delay", "reset"}
        expected = sum(
            1 for inst in qc.data if inst.operation.name not in skip
        )
        assert len(all_indices) == expected

    def test_empty_circuit(self):
        qc = QuantumCircuit(2)
        qc.measure_all()
        segs = segment_circuit(qc, moments_per_segment=3)
        assert segs == []

    def test_description_format(self):
        qc = self._make_test_circuit()
        segs = segment_circuit(qc, moments_per_segment=1)
        # Moment 0 has 3 h gates
        assert "3xh" in segs[0]["description"]
        # Moment 1 has 1 cx gate
        assert "1xcx" in segs[1]["description"]

    def test_data_index_correctness(self):
        """Each instruction's index should point to the right gate in circuit.data."""
        qc = self._make_test_circuit()
        segs = segment_circuit(qc, moments_per_segment=3)
        for seg in segs:
            for inst in seg["instructions"]:
                orig = qc.data[inst["index"]]
                assert orig.operation.name == inst["operation"]
                orig_qubits = [qc.find_bit(q).index for q in orig.qubits]
                assert orig_qubits == inst["qubits"]
