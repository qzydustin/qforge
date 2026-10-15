"""
Moment-based circuit segmentation for QRisk.

Partitions a quantum circuit into segments of consecutive *moments*
(parallel time slices).  A moment groups all gates that can execute in
parallel — each gate is assigned to the earliest moment where all of
its qubits are free (ASAP scheduling, equivalent to Qiskit's
``DAGCircuit.layers()``).
"""

from __future__ import annotations

from typing import Dict, List

from qiskit import QuantumCircuit

SKIP_OPS = frozenset(["measure", "barrier", "delay", "reset"])


def assign_moments(circuit: QuantumCircuit) -> Dict[int, List[Dict]]:
    """Assign each gate to its ASAP moment.

    Returns a dict mapping moment index to a list of instruction dicts.
    Each dict contains:
      - instruction: the original ``CircuitInstruction``
      - index: position in ``circuit.data``
      - operation: gate name
      - qubits: list of physical qubit indices
      - params: list of gate parameters
      - moment: the moment index
    """
    qubit_busy_until: Dict[int, int] = {}
    moments: Dict[int, List[Dict]] = {}

    for i, instruction in enumerate(circuit.data):
        if instruction.operation.name in SKIP_OPS:
            continue
        q_indices = [circuit.find_bit(q).index for q in instruction.qubits]
        moment = max(
            (qubit_busy_until.get(q, 0) for q in q_indices), default=0,
        )
        moments.setdefault(moment, []).append({
            "instruction": instruction,
            "index": i,
            "operation": instruction.operation.name,
            "qubits": q_indices,
            "params": list(getattr(instruction.operation, "params", [])),
            "moment": moment,
        })
        for q in q_indices:
            qubit_busy_until[q] = moment + 1

    return moments


def segment_circuit(
    circuit: QuantumCircuit,
    moments_per_segment: int = 3,
) -> List[Dict]:
    """Partition a circuit into segments of consecutive moments.

    Args:
        circuit: The quantum circuit to segment.
        moments_per_segment: How many moments to group into one segment.

    Returns:
        A list of segment dicts, each containing:
          - instructions: list of instruction dicts (see ``assign_moments``)
          - layer_id: segment index
          - moments: list of moment indices covered
          - description: human-readable summary of operations
    """
    moments = assign_moments(circuit)
    if not moments:
        return []

    segments: List[Dict] = []
    moment_ids = sorted(moments.keys())

    for seg_start in range(0, len(moment_ids), moments_per_segment):
        seg_moment_ids = moment_ids[seg_start:seg_start + moments_per_segment]
        layer: List[Dict] = []
        for m_id in seg_moment_ids:
            layer.extend(moments[m_id])

        if not layer:
            continue

        op_counts: Dict[str, int] = {}
        for inst in layer:
            op_counts[inst["operation"]] = op_counts.get(inst["operation"], 0) + 1

        segments.append({
            "instructions": layer,
            "layer_id": len(segments),
            "moments": seg_moment_ids,
            "description": ", ".join(
                f"{c}x{op}" for op, c in op_counts.items()
            ),
        })

    return segments
