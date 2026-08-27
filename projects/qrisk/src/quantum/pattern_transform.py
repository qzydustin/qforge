"""
Pattern-aware circuit transformation pass for QRisk.

Implements the online stage described in the paper: scan a compiled circuit
for occurrences of known problematic patterns, then apply targeted commuting
gate swaps to disrupt them.

Commutation is checked via Qiskit's built-in ``CommutationChecker``.
"""

from __future__ import annotations

from typing import List, Optional

from qiskit import QuantumCircuit
from qiskit.circuit.commutation_library import SessionCommutationChecker
from qiskit.circuit.library import get_standard_gate_name_mapping
from qiskit.dagcircuit import DAGCircuit
from qiskit.transpiler import TransformationPass

# Qiskit's commutation checker — handles diagonal gates, cx-cx, etc.
_commutation_checker = SessionCommutationChecker

# Gate name -> Gate class lookup for the commutation checker
_GATE_MAP = get_standard_gate_name_mapping()


def _make_gate(name: str, params: tuple):
    """Instantiate a gate object from name and params for commutation check."""
    gate_or_cls = _GATE_MAP.get(name)
    if gate_or_cls is None:
        return None
    try:
        if not params:
            return gate_or_cls
        # For parametric gates, instantiate the class with concrete params
        return type(gate_or_cls)(*params)
    except Exception:
        return None


def _ops_commute(name_a: str, qubits_a: list[int], params_a: tuple,
                 name_b: str, qubits_b: list[int], params_b: tuple) -> bool:
    """Check whether two gates commute using Qiskit's CommutationChecker."""
    gate_a = _make_gate(name_a, params_a)
    gate_b = _make_gate(name_b, params_b)
    if gate_a is None or gate_b is None:
        return False
    try:
        return _commutation_checker.commute(gate_a, qubits_a, [], gate_b, qubits_b, [])
    except Exception:
        return False


def _normalize_token(circuit: QuantumCircuit, inst) -> tuple:
    """Convert a circuit instruction to a normalized (name, qubits, params) token."""
    params = []
    for p in getattr(inst.operation, "params", []):
        try:
            params.append(round(float(p), 6))
        except Exception:
            params.append(str(p))
    return (
        inst.operation.name,
        tuple(circuit.find_bit(q).index for q in inst.qubits),
        tuple(params),
    )


def _token_sequence(circuit: QuantumCircuit) -> list[tuple]:
    """Extract normalized token sequence from a circuit (excluding non-gate ops)."""
    skip = {"measure", "barrier", "delay", "reset"}
    seq = []
    for inst in circuit.data:
        if inst.operation.name in skip:
            continue
        seq.append(_normalize_token(circuit, inst))
    return seq


def _find_pattern_occurrences(
    sequence: list[tuple], pattern: list[tuple],
) -> list[int]:
    """Find all start indices where *pattern* occurs in *sequence*."""
    n = len(pattern)
    target = tuple(pattern)
    return [
        i for i in range(len(sequence) - n + 1)
        if tuple(sequence[i:i + n]) == target
    ]


def disrupt_patterns(
    circuit: QuantumCircuit,
    patterns: list[list[tuple]],
) -> QuantumCircuit:
    """Apply targeted commuting gate swaps to disrupt all pattern occurrences.

    For each pattern occurrence, identify commuting gate pairs *on the same
    qubit timeline* — two gates that share a qubit and are separated only by
    gates on disjoint qubits.  "Bubble" them together (swapping past the
    disjoint gates, which is always safe) and then swap them if they commute
    (e.g. both diagonal in the computational basis).

    This matches the paper's description: rz(107) and cz(108,107) are
    adjacent on qubit 107's timeline even though sx(108) sits between them
    in the linear instruction sequence.

    Repeat until no pattern occurrence remains or no further swap can
    disrupt the remaining occurrences.

    Args:
        circuit: A compiled (ISA) quantum circuit.
        patterns: List of patterns, each a list of (name, qubits, params) tokens.

    Returns:
        A semantically equivalent circuit with pattern occurrences disrupted.
    """
    skip_ops = {"measure", "barrier", "delay", "reset"}

    # Separate gate instructions from non-gate instructions
    gate_insts = []
    measure_insts = []
    for inst in circuit.data:
        if inst.operation.name in skip_ops:
            measure_insts.append(inst)
        else:
            gate_insts.append(inst)

    # Build mutable token sequence from gate_insts
    tokens = [_normalize_token(circuit, inst) for inst in gate_insts]

    changed = True
    while changed:
        changed = False
        for pattern in patterns:
            pat_tokens = [tuple(t) if isinstance(t, list) else t for t in pattern]
            occurrences = _find_pattern_occurrences(tokens, pat_tokens)
            for start in occurrences:
                end = start + len(pat_tokens)

                # First try within the pattern, then expand to ±1
                swapped = _try_qubit_timeline_swap(
                    tokens, gate_insts, start, end,
                )
                if not swapped:
                    search_start = max(0, start - 1)
                    search_end = min(len(tokens), end + 1)
                    swapped = _try_qubit_timeline_swap(
                        tokens, gate_insts, search_start, search_end,
                    )
                if swapped:
                    # Verify the pattern is actually broken
                    new_occ = _find_pattern_occurrences(
                        tokens[max(0, start - 1):end + 1], pat_tokens,
                    )
                    if not new_occ:
                        changed = True
                        break
                    # else: swap happened but didn't break this occurrence,
                    # continue trying (the swap is still valid semantically)

            if changed:
                break  # restart full scan after a successful disruption

    # Rebuild circuit
    new = circuit.copy_empty_like()
    for inst in gate_insts:
        qargs = [new.qubits[circuit.find_bit(q).index] for q in inst.qubits]
        cargs = [new.clbits[circuit.find_bit(c).index] for c in inst.clbits]
        new.append(inst.operation, qargs, cargs)
    for inst in measure_insts:
        qargs = [new.qubits[circuit.find_bit(q).index] for q in inst.qubits]
        cargs = [new.clbits[circuit.find_bit(c).index] for c in inst.clbits]
        new.append(inst.operation, qargs, cargs)
    return new


def _try_qubit_timeline_swap(
    tokens: list[tuple],
    gate_insts: list,
    search_start: int,
    search_end: int,
) -> bool:
    """Try to find and execute a meaningful commuting swap within the search range.

    Only swaps gates that *share a qubit* and commute (checked via Qiskit's
    CommutationChecker).  Disjoint-qubit gates execute in parallel on
    hardware (same moment), so reordering them has no physical effect.

    If the two commuting gates are not linearly adjacent, "bubble" one
    gate past the intervening disjoint gates (which is always safe) to
    bring them together, then swap.

    Returns True if a swap was performed, False otherwise.
    """
    for i in range(search_start, search_end):
        ni, qi, pi = tokens[i][0], tokens[i][1], tokens[i][2]
        qi_set = set(qi)
        for j in range(i + 1, search_end):
            nj, qj, pj = tokens[j][0], tokens[j][1], tokens[j][2]
            qj_set = set(qj)
            if qi_set.isdisjoint(qj_set):
                continue  # disjoint swap has no physical effect
            if not _ops_commute(ni, list(qi), pi, nj, list(qj), pj):
                continue

            # Try bubbling gate i forward toward j
            can_bubble_i = all(
                qi_set.isdisjoint(set(tokens[m][1])) for m in range(i + 1, j)
            )
            if can_bubble_i:
                for step in range(i, j - 1):
                    tokens[step], tokens[step + 1] = tokens[step + 1], tokens[step]
                    gate_insts[step], gate_insts[step + 1] = gate_insts[step + 1], gate_insts[step]
                tokens[j - 1], tokens[j] = tokens[j], tokens[j - 1]
                gate_insts[j - 1], gate_insts[j] = gate_insts[j], gate_insts[j - 1]
                return True

            # Try bubbling gate j backward toward i
            can_bubble_j = all(
                qj_set.isdisjoint(set(tokens[m][1])) for m in range(i + 1, j)
            )
            if can_bubble_j:
                for step in range(j, i + 1, -1):
                    tokens[step], tokens[step - 1] = tokens[step - 1], tokens[step]
                    gate_insts[step], gate_insts[step - 1] = gate_insts[step - 1], gate_insts[step]
                tokens[i], tokens[i + 1] = tokens[i + 1], tokens[i]
                gate_insts[i], gate_insts[i + 1] = gate_insts[i + 1], gate_insts[i]
                return True

    return False


class PatternDisruptionPass(TransformationPass):
    """Qiskit TransformationPass that disrupts known problematic patterns.

    This pass implements the online stage of QRisk: after standard
    compilation, it scans the resulting circuit for occurrences of known
    bad patterns and applies targeted commuting gate swaps to break them.

    Usage::

        from quantum.pattern_transform import PatternDisruptionPass
        from qiskit.transpiler import PassManager

        patterns = [
            [("sx", (107,), ()), ("rz", (107,), (0.393,)), ("sx", (108,), ()), ("cz", (108, 107), ())],
        ]
        pm = PassManager([PatternDisruptionPass(patterns)])
        new_circuit = pm.run(circuit)
    """

    def __init__(self, patterns: list[list[tuple]]):
        super().__init__()
        self.patterns = patterns

    def run(self, dag: DAGCircuit) -> DAGCircuit:
        """Run the pass on a DAGCircuit."""
        from qiskit.converters import dag_to_circuit, circuit_to_dag
        circuit = dag_to_circuit(dag)
        new_circuit = disrupt_patterns(circuit, self.patterns)
        return circuit_to_dag(new_circuit)


# ---------------------------------------------------------------------------
# Random commuting swap for variant generation
# ---------------------------------------------------------------------------

def commuting_swap_circuit(
    circuit: QuantumCircuit, n_swaps: int, seed: int,
) -> QuantumCircuit:
    """Apply n random adjacent commuting-gate swaps. Semantically equivalent.

    Used to generate circuit variants with different pattern hit counts
    for evaluation experiments.  Commutation is checked via Qiskit's
    CommutationChecker.
    """
    import random

    skip_ops = {"measure", "barrier", "delay", "reset"}
    gate_insts = []
    measure_insts = []
    for inst in circuit.data:
        if inst.operation.name in skip_ops:
            measure_insts.append(inst)
        else:
            q = {circuit.find_bit(q).index for q in inst.qubits}
            gate_insts.append((inst, q))

    rng = random.Random(seed)
    for _ in range(n_swaps):
        pairs = []
        for k in range(len(gate_insts) - 1):
            inst_a, q_a = gate_insts[k]
            inst_b, q_b = gate_insts[k + 1]
            if _ops_commute(
                inst_a.operation.name, sorted(q_a), tuple(inst_a.operation.params),
                inst_b.operation.name, sorted(q_b), tuple(inst_b.operation.params),
            ):
                pairs.append(k)
        if not pairs:
            break
        k = rng.choice(pairs)
        gate_insts[k], gate_insts[k + 1] = gate_insts[k + 1], gate_insts[k]

    new = circuit.copy_empty_like()
    for inst, _ in gate_insts:
        qargs = [new.qubits[circuit.find_bit(q).index] for q in inst.qubits]
        cargs = [new.clbits[circuit.find_bit(c).index] for c in inst.clbits]
        new.append(inst.operation, qargs, cargs)
    for inst in measure_insts:
        qargs = [new.qubits[circuit.find_bit(q).index] for q in inst.qubits]
        cargs = [new.clbits[circuit.find_bit(c).index] for c in inst.clbits]
        new.append(inst.operation, qargs, cargs)
    return new
