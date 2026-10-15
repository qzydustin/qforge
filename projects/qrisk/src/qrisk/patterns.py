"""
Qubit-timeline pattern matching and semantics-preserving gate swaps.

``qrisk.tokens.count_contiguous`` looks for a *contiguous run in the linear
instruction list*.  Linear order between gates on disjoint qubits is arbitrary
(it has no physical meaning), so two circuits that execute identically can
differ in linear hits.  That is acceptable within one compiled circuit, but
not when comparing *different* algorithms.

This module matches a pattern on the circuit's **qubit timelines**: an
occurrence is an injective mapping of pattern gates to circuit gates such that,
on every qubit the pattern touches, the pattern's gates appear *consecutively
and in the same order* on that qubit's timeline, and multi-qubit gates are the
same instruction on all of their qubits.  This is exactly the structure a
DDMin segment captures (all gates on those qubits within a moment window) and
is invariant to reordering of gates on disjoint qubits.

Tokens are ``qrisk.tokens`` tokens with ``cz`` qubits sorted (cz is
symmetric).  Parameters are ignored unless ``with_params=True``.

Also provides:
  * ``pattern_core``: the largest connected component of a DDMin pattern
    (preferring components that contain a two-qubit gate).
  * ``reduce_occurrences`` / ``neutral_swaps``: commuting swaps that remove
    occurrences one at a time, or keep the count (RQ4 dose-response variants).
  * ``commuting_swap_circuit``: random adjacent commuting swaps (RQ3 verify variants).
  * ``circuits_equivalent``: unitary check on the active qubits.

Commutation is checked via Qiskit's ``CommutationChecker``.
"""

from __future__ import annotations

import random
from typing import Dict, Iterable, List, Sequence, Tuple

from qiskit import QuantumCircuit
from qiskit.circuit.commutation_library import SessionCommutationChecker
from qiskit.circuit.library import get_standard_gate_name_mapping

from .partition import SKIP_OPS, assign_moments
from .tokens import Token, normalize_params, token_from_instruction, token_from_report_gate, tokens_match

SYMMETRIC_GATES = frozenset(["cz"])

_GATE_MAP = get_standard_gate_name_mapping()


# ---------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------

def _symmetric(tok: Token) -> Token:
    name, qubits, params = tok
    return (name, tuple(sorted(qubits)) if name in SYMMETRIC_GATES else qubits, params)


def normalize_pattern(pattern: Sequence) -> List[Token]:
    """Report gates or tokens (``[name, qubits, params?]`` or dict form) as matcher tokens."""
    return [_symmetric(token_from_report_gate(tok)) for tok in pattern]


def timeline_tokens(circuit: QuantumCircuit) -> Tuple[List[Token], List]:
    """Gate tokens in linear order plus the matching CircuitInstructions."""
    insts = [inst for inst in circuit.data if inst.operation.name not in SKIP_OPS]
    return [_symmetric(token_from_instruction(circuit, inst)) for inst in insts], insts


def _tok_eq(a: Token, b: Token, with_params: bool) -> bool:
    if with_params:
        return tokens_match(a, b)
    return a[0] == b[0] and a[1] == b[1]


def gate_type_key(pattern: Sequence) -> str:
    """Parameter-free display key, e.g. ``rz(47) → cz(46,47) → sx(47)``."""
    toks = normalize_pattern(pattern)
    return " → ".join(f"{n}({','.join(map(str, q))})" for n, q, _ in toks)


# ---------------------------------------------------------------------------
# Components / core
# ---------------------------------------------------------------------------

def pattern_components(pattern: Sequence) -> List[List[Token]]:
    """Split a pattern into qubit-connected components (order preserved)."""
    toks = normalize_pattern(pattern)
    parent: Dict[int, int] = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for _, qubits, _ in toks:
        for q in qubits[1:]:
            parent[find(q)] = find(qubits[0])
        find(qubits[0])
    groups: Dict[int, List[Token]] = {}
    for tok in toks:
        groups.setdefault(find(tok[1][0]), []).append(tok)
    return list(groups.values())


def pattern_core(pattern: Sequence) -> List[Token]:
    """Largest connected component, preferring ones with a multi-qubit gate."""
    comps = pattern_components(pattern)
    if not comps:
        return []
    return max(comps, key=lambda c: (any(len(t[1]) > 1 for t in c), len(c)))


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

def _timelines(tokens: Sequence[Token]) -> Tuple[Dict[int, List[int]], Dict[Tuple[int, int], int]]:
    lines: Dict[int, List[int]] = {}
    pos: Dict[Tuple[int, int], int] = {}
    for i, (_, qubits, _) in enumerate(tokens):
        for q in qubits:
            pos[(q, i)] = len(lines.setdefault(q, []))
            lines[q].append(i)
    return lines, pos


def find_matches(
    tokens: Sequence[Token],
    pattern: Sequence,
    with_params: bool = False,
) -> List[frozenset]:
    """All timeline occurrences of a *connected* pattern in a token list.

    Returns a list of frozensets of linear gate indices (one per occurrence).
    """
    pat = normalize_pattern(pattern)
    if not pat:
        return []
    if len(pattern_components(pat)) != 1:
        raise ValueError("find_matches needs a qubit-connected pattern; use pattern_core() first")

    p_lines, _ = _timelines(pat)
    c_lines, c_pos = _timelines(tokens)
    matches = set()

    for c0, ctok in enumerate(tokens):
        if not _tok_eq(pat[0], ctok, with_params):
            continue
        mapping = {0: c0}
        queue = [0]
        done_q = set()
        ok = True
        while queue and ok:
            pi = queue.pop()
            ci = mapping[pi]
            for q in pat[pi][1]:
                if q in done_q:
                    continue
                done_q.add(q)
                if q not in c_lines:
                    ok = False
                    break
                offset = c_pos[(q, ci)] - p_lines[q].index(pi)
                for k, pj in enumerate(p_lines[q]):
                    at = offset + k
                    if at < 0 or at >= len(c_lines[q]):
                        ok = False
                        break
                    cj = c_lines[q][at]
                    if not _tok_eq(pat[pj], tokens[cj], with_params):
                        ok = False
                        break
                    if pj in mapping:
                        if mapping[pj] != cj:
                            ok = False
                            break
                    else:
                        mapping[pj] = cj
                        queue.append(pj)
                if not ok:
                    break
        if ok and len(mapping) == len(pat) and len(set(mapping.values())) == len(pat):
            matches.add(frozenset(mapping.values()))
    return sorted(matches, key=min)


def count_occurrences(circuit_or_tokens, pattern: Sequence, with_params: bool = False) -> int:
    tokens = circuit_or_tokens
    if isinstance(circuit_or_tokens, QuantumCircuit):
        tokens, _ = timeline_tokens(circuit_or_tokens)
    return len(find_matches(tokens, pattern, with_params=with_params))


def count_linear(tokens: Sequence[Token], pattern: Sequence, with_params: bool = False) -> int:
    """The paper's matcher: contiguous run in the linear gate list."""
    pat = normalize_pattern(pattern)
    n = len(pat)
    return sum(
        1 for i in range(len(tokens) - n + 1)
        if all(_tok_eq(pat[k], tokens[i + k], with_params) for k in range(n))
    )


def occurrence_depths(circuit: QuantumCircuit, pattern: Sequence, with_params: bool = False) -> List[float]:
    """Relative depth (0 = start, 1 = end) of each occurrence's first moment."""
    tokens, _ = timeline_tokens(circuit)
    moments = assign_moments(circuit)
    # linear gate index -> moment
    order = sorted(
        ((inst["index"], m) for m, insts in moments.items() for inst in insts),
        key=lambda x: x[0],
    )
    gate_moment = [m for _, m in order]
    total = max(1, max(moments) if moments else 1)
    return [min(gate_moment[i] for i in occ) / total
            for occ in find_matches(tokens, pattern, with_params)]


# ---------------------------------------------------------------------------
# Commuting swaps
# ---------------------------------------------------------------------------

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
    gate_a = _make_gate(name_a, params_a)
    gate_b = _make_gate(name_b, params_b)
    if gate_a is None or gate_b is None:
        return False
    try:
        return SessionCommutationChecker.commute(gate_a, qubits_a, [], gate_b, qubits_b, [])
    except Exception:
        return False


def _rebuild(circuit: QuantumCircuit, gate_insts: Sequence) -> QuantumCircuit:
    """``gate_insts`` in the given order, then the circuit's measure/barrier/... in theirs."""
    new = circuit.copy_empty_like()
    for inst in gate_insts:
        new.append(inst.operation,
                   [new.qubits[circuit.find_bit(q).index] for q in inst.qubits],
                   [new.clbits[circuit.find_bit(c).index] for c in inst.clbits])
    for inst in circuit.data:
        if inst.operation.name in SKIP_OPS:
            new.append(inst.operation,
                       [new.qubits[circuit.find_bit(q).index] for q in inst.qubits],
                       [new.clbits[circuit.find_bit(c).index] for c in inst.clbits])
    return new


def commuting_swap_circuit(
    circuit: QuantumCircuit, n_swaps: int, seed: int,
) -> QuantumCircuit:
    """Apply n random swaps of linearly adjacent commuting gates. Semantically equivalent.

    Used by the RQ3 verify experiment to generate variants with different
    pattern hit counts.
    """
    gate_insts = []
    for inst in circuit.data:
        if inst.operation.name not in SKIP_OPS:
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

    return _rebuild(circuit, [inst for inst, _ in gate_insts])


def _timeline_adjacent_pairs(tokens: Sequence[Token], involved: Iterable[int]) -> List[Tuple[int, int]]:
    """Pairs (a, b), a before b, adjacent on some qubit timeline, touching ``involved``."""
    lines, pos = _timelines(tokens)
    involved = set(involved)
    pairs = set()
    for i in involved:
        for q in tokens[i][1]:
            p = pos[(q, i)]
            if p > 0:
                pairs.add((lines[q][p - 1], i))
            if p + 1 < len(lines[q]):
                pairs.add((i, lines[q][p + 1]))
    return sorted(pairs)


def _try_swap(tokens: List[Token], insts: List, a: int, b: int) -> bool:
    """Swap timeline-adjacent commuting gates a<b in linear order, preserving
    the relative order of every other gate on shared qubits."""
    ta, tb = tokens[a], tokens[b]
    if not _ops_commute(ta[0], list(ta[1]), ta[2], tb[0], list(tb[1]), tb[2]):
        return False
    qa, qb = set(ta[1]), set(tb[1])
    between = range(a + 1, b)
    if all(qa.isdisjoint(tokens[m][1]) for m in between):
        # move a to just after b
        tokens.insert(b, tokens.pop(a))
        insts.insert(b, insts.pop(a))
        return True
    if all(qb.isdisjoint(tokens[m][1]) for m in between):
        # move b to just before a
        tokens.insert(a, tokens.pop(b))
        insts.insert(a, insts.pop(b))
        return True
    return False


def reduce_occurrences(
    circuit: QuantumCircuit,
    pattern: Sequence,
    seed: int = 0,
    with_params: bool = False,
    max_steps: int = 500,
) -> List[Tuple[int, QuantumCircuit]]:
    """Greedily remove occurrences with commuting swaps.

    Returns ``[(count, circuit), ...]`` snapshots starting from the input and
    ending at the lowest count reached.  Each accepted swap strictly lowers
    the occurrence count, so the loop always terminates.
    """
    rng = random.Random(seed)
    tokens, insts = timeline_tokens(circuit)
    count = len(find_matches(tokens, pattern, with_params))
    # Rebuild the starting point too, so every snapshot has the same
    # barrier/measurement placement (mid-circuit barriers move to the end;
    # DDMin's oracle circuits drop them the same way).
    snapshots = [(count, _rebuild(circuit, insts))]
    steps = 0
    while count > 0 and steps < max_steps:
        steps += 1
        occs = find_matches(tokens, pattern, with_params)
        rng.shuffle(occs)
        improved = False
        # Try every occurrence (random order) before giving up: some
        # occurrences have no breaking commuting swap, others do.
        for occ in occs:
            pairs = _timeline_adjacent_pairs(tokens, occ)
            rng.shuffle(pairs)
            for a, b in pairs:
                t2, i2 = list(tokens), list(insts)
                if not _try_swap(t2, i2, a, b):
                    continue
                new_count = len(find_matches(t2, pattern, with_params))
                if new_count < count:
                    tokens, insts, count = t2, i2, new_count
                    snapshots.append((count, _rebuild(circuit, insts)))
                    improved = True
                    break
            if improved:
                break
        if not improved:
            break
    return snapshots


def neutral_swaps(
    circuit: QuantumCircuit,
    pattern: Sequence,
    n_swaps: int,
    seed: int,
    with_params: bool = False,
) -> QuantumCircuit:
    """Apply up to ``n_swaps`` random timeline-adjacent commuting swaps that do
    NOT change the pattern's occurrence count (diversifies variants within a
    bucket without confounding the dose)."""
    rng = random.Random(seed)
    tokens, insts = timeline_tokens(circuit)
    target = len(find_matches(tokens, pattern, with_params))
    done = 0
    attempts = 0
    while done < n_swaps and attempts < n_swaps * 20:
        attempts += 1
        a = rng.randrange(len(tokens))
        pairs = _timeline_adjacent_pairs(tokens, [a])
        if not pairs:
            continue
        x, y = rng.choice(pairs)
        t2, i2 = list(tokens), list(insts)
        if not _try_swap(t2, i2, x, y):
            continue
        if len(find_matches(t2, pattern, with_params)) != target:
            continue
        tokens, insts = t2, i2
        done += 1
    return _rebuild(circuit, insts)


# ---------------------------------------------------------------------------
# Circuit comparison
# ---------------------------------------------------------------------------

def moment_signature(circuit: QuantumCircuit) -> Tuple:
    """Physical schedule fingerprint: sorted gate tokens per ASAP moment."""
    moments = assign_moments(circuit)
    return tuple(
        tuple(sorted((i["operation"], tuple(i["qubits"]), normalize_params(i["params"])) for i in moments[m]))
        for m in sorted(moments)
    )


def circuits_equivalent(a: QuantumCircuit, b: QuantumCircuit) -> bool:
    """Unitary equivalence on the active qubits (measurements/barriers ignored)."""
    from qiskit.quantum_info import Operator

    def compact(c: QuantumCircuit, active: List[int]) -> QuantumCircuit:
        idx = {q: k for k, q in enumerate(active)}
        out = QuantumCircuit(len(active))
        for inst in c.data:
            if inst.operation.name in SKIP_OPS:
                continue
            out.append(inst.operation, [idx[c.find_bit(q).index] for q in inst.qubits])
        return out

    active = sorted({
        c.find_bit(q).index
        for c in (a, b) for inst in c.data if inst.operation.name not in SKIP_OPS
        for q in inst.qubits
    })
    if len(active) > 10:
        raise ValueError("too many active qubits for a unitary check")
    return Operator(compact(a, active)).equiv(Operator(compact(b, active)))
