"""Gate tokens: the one representation of a gate shared by DDMin reports,
circuits, the RQ3 verify scoring and the analysis tables.

A token is ``(name, qubits, params)``. Qubits keep their stored order, so a
two-qubit gate's direction survives; params are floats rounded to 6 dp.

Pattern identity has three levels, strictest first:

* the token sequence itself: ``count_contiguous`` compares tokens exactly,
  ``tokens_match`` allows ``PARAM_TOL`` on params;
* ``canonical_key``: ASAP moments with the gates sorted inside each moment,
  so reordering gates on disjoint qubits leaves the key unchanged;
* ``structural_key``: the canonical key with qubits renamed Q0, Q1, ... in
  order of appearance, so the same shape on other physical qubits matches.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from qiskit import QuantumCircuit

from .partition import SKIP_OPS

PARAM_TOL = 1e-5

Token = Tuple[str, Tuple[int, ...], Tuple]


def normalize_params(params: Optional[Iterable]) -> Tuple:
    """Floats rounded to 6 dp; a value float() rejects (an unbound parameter) is kept as str."""
    out = []
    for p in params or ():
        try:
            out.append(round(float(p), 6))
        except (TypeError, ValueError):
            out.append(str(p))
    return tuple(out)


def token_from_instruction(circuit: QuantumCircuit, inst) -> Token:
    return (
        inst.operation.name,
        tuple(circuit.find_bit(q).index for q in inst.qubits),
        normalize_params(getattr(inst.operation, "params", [])),
    )


def circuit_tokens(circuit: QuantumCircuit) -> List[Token]:
    """Gate tokens in linear order; measure, barrier, delay and reset are skipped."""
    return [token_from_instruction(circuit, inst) for inst in circuit.data
            if inst.operation.name not in SKIP_OPS]


def token_from_report_gate(gate) -> Token:
    """A gate as stored in a DDMin report.

    NEW schema: ``[op, [qubits], [params]]`` in ``pattern``, and
    ``{"operation": ..., "qubits": ..., "params": ...}`` in ``segments_info``.
    OLD schema: ``{"op": ..., "qubits": ..., "params": ...}``.
    """
    if isinstance(gate, dict):
        name = gate.get("op") or gate.get("operation") or gate.get("name") or ""
        qubits, params = gate.get("qubits"), gate.get("params")
    else:
        name, qubits = gate[0], gate[1]
        params = gate[2] if len(gate) > 2 else ()
    return (str(name), tuple(int(q) for q in qubits or ()), normalize_params(params))


def tokens_match(a: Token, b: Token) -> bool:
    """Same gate on the same qubits with params equal within PARAM_TOL."""
    if a[0] != b[0] or tuple(a[1]) != tuple(b[1]) or len(a[2]) != len(b[2]):
        return False
    for x, y in zip(a[2], b[2]):
        try:
            if abs(float(x) - float(y)) > PARAM_TOL:
                return False
        except (TypeError, ValueError):
            if str(x) != str(y):
                return False
    return True


def count_contiguous(sequence: Sequence[Token], pattern: Sequence[Token]) -> int:
    """Occurrences of ``pattern`` as a contiguous run of ``sequence``, tokens compared exactly.

    This is the pattern-hit count the RQ3 verify manifests were scored with.
    """
    n = len(pattern)
    target = tuple(pattern)
    return sum(1 for i in range(len(sequence) - n + 1) if tuple(sequence[i:i + n]) == target)


def asap_moments(tokens: Iterable[Sequence]) -> List[Tuple[str, ...]]:
    """Gates as ``name(q,...)`` strings grouped into ASAP moments, sorted inside each moment.

    Qubits are sorted inside each gate: the key records which gates share a
    moment, not a two-qubit gate's direction.
    """
    next_free: Dict[int, int] = defaultdict(int)
    moments: Dict[int, List[str]] = defaultdict(list)
    for tok in tokens:
        qubits = sorted(tok[1])
        moment = max(next_free[q] for q in qubits)
        for q in qubits:
            next_free[q] = moment + 1
        moments[moment].append(f"{tok[0]}({','.join(map(str, qubits))})")
    return [tuple(sorted(moments[m])) for m in sorted(moments)]


def canonical_key(tokens: Iterable[Sequence]) -> str:
    """The moments flattened, e.g. ``cz(130,131) → sx(131) → x(130)``; "" for no gates."""
    return " → ".join(gate for moment in asap_moments(tokens) for gate in moment)


def structural_key(key: str) -> Optional[str]:
    """A ``canonical_key`` with qubits renamed Q0, Q1, ... by first appearance; None for ""."""
    if not key:
        return None
    labels: Dict[str, str] = {}
    gates = []
    for gate in key.split(" → "):
        name, _, qubits = gate.partition("(")
        renamed = [labels.setdefault(q.strip(), f"Q{len(labels)}") for q in qubits.rstrip(")").split(",")]
        gates.append(f"{name}({','.join(renamed)})")
    return " → ".join(gates)


def pattern_has_cz(tokens: Iterable[Sequence]) -> bool:
    return any(tok[0] == "cz" for tok in tokens)
