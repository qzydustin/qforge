"""The Grover-3 workload and its compilation onto a fixed physical layout."""

from __future__ import annotations

from typing import List, Optional

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def grover_3q(iterations: int = 1, marked_state: int = 7) -> QuantumCircuit:
    """3-qubit Grover search with a phase-kickback ancilla.

    iterations=1 is the groups' base_1x circuit; iterations=3 is base_3x,
    the paper's discovery workload.
    """
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

    for _ in range(iterations):
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


def compile_isa(circuit: QuantumCircuit, backend, layout: List[int],
                seed_transpiler: Optional[int] = None) -> QuantumCircuit:
    pm = generate_preset_pass_manager(
        optimization_level=3,
        backend=backend,
        initial_layout=layout,
        seed_transpiler=seed_transpiler,
    )
    return pm.run(circuit)


def layout_str(layout: List[int]) -> str:
    """[46, 47, 48, 57] -> '46_47_48_57', the layout part of group directory names."""
    return "_".join(map(str, layout))
