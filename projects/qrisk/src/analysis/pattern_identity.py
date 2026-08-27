"""Three-layer pattern identity for QRisk analysis.

Every downstream table keys patterns through one of three identity layers
defined here. The layers are ordered from strictest (exact parameters) to
loosest (structural shape). ``PARAM_TOL`` matches ``quantum.pattern_db._tokens_match``
so that the paper's database identity == code identity.

A *gate token* is normalized to the tuple ``(op, qubits_tuple, params_tuple)``
where ``op`` is the gate name (str), ``qubits_tuple`` is a tuple of physical
qubit indices (ints, in the gate's stored order -- NOT sorted, so two-qubit
gate direction is preserved), and ``params_tuple`` is a tuple of floats rounded
to 6 decimals (empty for parameterless gates).

Layers
------
LAYER_EXACT
    Exact-parameterized token sequence in circuit order. Two reports match
    iff this is identical element-for-element. This is the database key.
LAYER_MOMENT_DAG
    Commutation-normalized: gates that execute in the same ASAP moment (on
    disjoint qubits) may be freely reordered, so the canonical key is
    invariant under intra-moment permutation. Reuses
    ``analyze_pattern_repeats.pattern_to_canonical``.
LAYER_STRUCTURAL
    Physical qubit indices renamed to rank order of first appearance, so the
    same gate topology on different physical qubits counts as one shape.
"""

from __future__ import annotations

from typing import Any, List, Optional, Tuple

# Must match quantum/pattern_db._tokens_match tolerance (1e-5) so that the
# paper's "exact match" definition equals the live database's match definition.
PARAM_TOL = 1e-5

Token = Tuple[str, Tuple[int, ...], Tuple[float, ...]]
Pattern = Tuple[Token, ...]


# ---------------------------------------------------------------------------
# Token normalization (single chokepoint -- fixes the "ignore gate[2]" bug)
# ---------------------------------------------------------------------------

def _to_float(param: Any) -> float:
    """Coerce a parameter value to float; tolerate str/None."""
    try:
        return float(param)
    except (TypeError, ValueError):
        return 0.0


def normalize_token(gate: Any) -> Token:
    """Coerce one gate to the ``(op, qubits, params)`` tuple form.

    Accepts either the NEW-schema list form ``[op, [qubits], [params]]`` or
    the OLD-schema dict form ``{"op": ..., "qubits": [...], "params": [...]}``.
    Parameterless gates (cz, x, sx) carry an empty params tuple.
    """
    if isinstance(gate, dict):
        op = str(gate.get("op") or gate.get("operation") or gate.get("name") or "")
        qubits = tuple(int(q) for q in (gate.get("qubits") or []))
        params = tuple(_to_float(p) for p in (gate.get("params") or []))
    elif isinstance(gate, (list, tuple)):
        op = str(gate[0]) if len(gate) > 0 else ""
        qubits = tuple(int(q) for q in (gate[1] if len(gate) > 1 else []))
        raw_params = gate[2] if len(gate) > 2 else []
        params = tuple(_to_float(p) for p in (raw_params or []))
    else:
        op, qubits, params = "", (), ()
    # Round params to 6 dp for stable hashing; the matching tolerance (1e-5)
    # is enforced separately in tokens_match.
    params = tuple(round(p, 6) for p in params)
    return (op, qubits, params)


def tokens_match(a: Pattern, b: Pattern) -> bool:
    """Exact-match two token sequences under PARAM_TOL (mirrors pattern_db)."""
    if len(a) != len(b):
        return False
    for ta, tb in zip(a, b):
        if ta[0] != tb[0]:
            return False
        if ta[1] != tb[1]:
            return False
        if len(ta[2]) != len(tb[2]):
            return False
        for va, vb in zip(ta[2], tb[2]):
            if abs(va - vb) > PARAM_TOL:
                return False
    return True


def pattern_has_cz(pattern: Pattern) -> bool:
    return any(t[0] == "cz" for t in pattern)


# ---------------------------------------------------------------------------
# Layer 1: EXACT
# ---------------------------------------------------------------------------

def layer_exact(tokens: List[Token]) -> Pattern:
    """Exact-parameterized sequence in circuit order."""
    return tuple(tokens)


# ---------------------------------------------------------------------------
# Layer 2: MOMENT_DAG (commutation-normalized)
# ---------------------------------------------------------------------------

def _pattern_to_canonical_ops(pattern: Pattern) -> List[str]:
    """Reuse analyze_pattern_repeats.pattern_to_canonical.

    That function takes the raw ``[op,[qubits],[params]]`` list form and
    returns ``(canonical_ops, canonical_key, moments)``. We only need the
    canonical_key (a hashable string invariant under intra-moment reorder).
    """
    # Reconstruct the list-form it expects.
    raw = [[t[0], list(t[1]), list(t[2])] for t in pattern]
    from analyze_pattern_repeats import pattern_to_canonical  # local import; heavy
    _, canonical_key, _ = pattern_to_canonical(raw)
    return canonical_key


def layer_moment(pattern: Pattern) -> str:
    """Commutation-normalized key (ASAP layers, sorted within layer)."""
    if not pattern:
        return ""
    return _pattern_to_canonical_ops(pattern)


# ---------------------------------------------------------------------------
# Layer 3: STRUCTURAL (qubits renamed to rank order)
# ---------------------------------------------------------------------------

def structural_normalize_key(canonical_key: str) -> Optional[str]:
    """Rename physical qubits to rank-of-appearance labels.

    Adapted from the closure in analyze_pattern_repeats (line 873). Operates
    on a canonical key string of the form ``"op(q,q) → op(q)"``.
    """
    if not canonical_key:
        return None
    parts = canonical_key.split(" → ")
    qubit_map: dict[str, str] = {}
    next_label = 0
    normalized = []
    for p in parts:
        head, _, rest = p.partition("(")
        qubits_str = rest.rstrip(")")
        qubits = qubits_str.split(",")
        norm_qubits = []
        for q in qubits:
            q = q.strip()
            if q not in qubit_map:
                qubit_map[q] = f"Q{next_label}"
                next_label += 1
            norm_qubits.append(qubit_map[q])
        normalized.append(f"{head}({','.join(norm_qubits)})")
    return " → ".join(normalized)


def layer_structural(pattern: Pattern) -> Optional[str]:
    """Structural shape: physical qubits renamed to rank order."""
    if not pattern:
        return None
    return structural_normalize_key(layer_moment(pattern))


# ---------------------------------------------------------------------------
# Tokenizers: report -> list of per-segment token lists
# ---------------------------------------------------------------------------

def tokenize_new(report: dict) -> List[List[Token]]:
    """NEW schema: ``report['pattern']`` is ONE concatenated token list.

    Returns a single-element list (one pattern). Note the NEW schema stores
    only the single primary pattern; per-segment info lives in segments_info
    and is handled separately by build_dataset for the recurrence matrix.
    """
    raw = report.get("pattern") or []
    if not raw:
        return []
    return [[normalize_token(g) for g in raw]]


def tokenize_old(report: dict) -> List[List[Token]]:
    """OLD schema: ``problematic_details[i].instructions`` -- one token list
    PER flagged segment. Returns one element per segment (never concatenated).
    """
    out: List[List[Token]] = []
    for detail in report.get("problematic_details") or []:
        insts = detail.get("instructions") or []
        if not insts:
            continue
        out.append([normalize_token(g) for g in insts])
    return out


__all__ = [
    "PARAM_TOL",
    "Token",
    "Pattern",
    "normalize_token",
    "tokens_match",
    "pattern_has_cz",
    "layer_exact",
    "layer_moment",
    "layer_structural",
    "structural_normalize_key",
    "tokenize_new",
    "tokenize_old",
]
