"""Tests for qrisk.patterns and qrisk.budget (offline, no IBM)."""

import pytest
from qiskit import QuantumCircuit

from qrisk.budget import BudgetExceeded, QPUBudget
from qrisk.patterns import (
    circuits_equivalent, commuting_swap_circuit, count_linear, count_occurrences, find_matches,
    moment_signature, neutral_swaps, pattern_core, reduce_occurrences, timeline_tokens,
)

PAT = [("rz", [1], []), ("cz", [0, 1], []), ("sx", [1], [])]


def _circuit(interleave: bool) -> QuantumCircuit:
    qc = QuantumCircuit(3, 2)
    qc.rz(0.3, 1)
    if interleave:
        qc.sx(2)          # disjoint gate between pattern gates in linear order
    qc.cz(0, 1)
    qc.sx(1)
    qc.rz(0.7, 1)
    qc.cz(1, 0)           # symmetric cz, reversed operands
    qc.sx(1)
    qc.measure(0, 0)
    qc.measure(1, 1)
    return qc


def test_timeline_match_ignores_disjoint_interleaving():
    plain, inter = _circuit(False), _circuit(True)
    assert count_occurrences(plain, PAT) == 2
    assert count_occurrences(inter, PAT) == 2
    toks, _ = timeline_tokens(inter)
    # The paper's linear matcher is broken by the unrelated sx(2).
    assert count_linear(toks, PAT) == 1


def test_params_only_matter_when_requested():
    qc = _circuit(False)
    exact = [("rz", [1], [0.3]), ("cz", [0, 1], []), ("sx", [1], [])]
    assert count_occurrences(qc, exact, with_params=False) == 2
    assert count_occurrences(qc, exact, with_params=True) == 1


def test_consecutive_on_timeline_required():
    qc = QuantumCircuit(2)
    qc.rz(0.1, 1)
    qc.x(1)               # breaks rz -> cz adjacency on qubit 1
    qc.cz(0, 1)
    qc.sx(1)
    assert count_occurrences(qc, PAT) == 0


def test_reduce_occurrences_preserves_semantics_and_terminates():
    qc = _circuit(True)
    snaps = reduce_occurrences(qc, PAT, seed=3)
    counts = [c for c, _ in snaps]
    assert counts[0] == 2
    assert counts == sorted(counts, reverse=True)
    assert len(set(counts)) == len(counts)            # strictly decreasing
    for _, c in snaps:
        assert circuits_equivalent(qc, c)
        assert dict(c.count_ops()) == dict(qc.count_ops())


def test_neutral_swaps_keep_count():
    qc = _circuit(True)
    v = neutral_swaps(qc, PAT, n_swaps=5, seed=1)
    assert count_occurrences(v, PAT) == count_occurrences(qc, PAT)
    assert circuits_equivalent(qc, v)


def test_pattern_core_prefers_two_qubit_component():
    pattern = [("rz", [5], []), ("sx", [1], []), ("cz", [0, 1], []), ("rz", [0], []), ("sx", [5], [])]
    core = pattern_core(pattern)
    assert {t[0] for t in core} == {"sx", "cz", "rz"}
    assert all(set(t[1]) <= {0, 1} for t in core)


def test_find_matches_rejects_disconnected_pattern():
    with pytest.raises(ValueError):
        find_matches(timeline_tokens(_circuit(False))[0], [("rz", [0], []), ("rz", [2], [])])


def test_moment_signature_detects_physical_change():
    a = _circuit(False)
    snaps = reduce_occurrences(a, PAT, seed=0)
    assert moment_signature(snaps[-1][1]) != moment_signature(snaps[0][1])


def test_commuting_swap_circuit_preserves_semantics():
    qc = _circuit(True)
    v = commuting_swap_circuit(qc, n_swaps=4, seed=2)
    assert circuits_equivalent(qc, v)
    assert dict(v.count_ops()) == dict(qc.count_ops())


def test_budget_guard(tmp_path):
    b = QPUBudget(tmp_path / "ledger.jsonl", cap_seconds=30, default_seconds_per_circuit=10)
    assert b.check(n_circuits=2) == 20
    b.record(12.0, 2, "ibm_fez", "job1")          # measured 6 s/circuit
    assert b.seconds_per_circuit_estimate() == 6.0
    b.check(n_circuits=3)                          # 12 + 18 = 30 <= 30
    with pytest.raises(BudgetExceeded):
        b.check(n_circuits=4)                      # 12 + 24 > 30
    # Persisted across instances.
    assert QPUBudget(tmp_path / "ledger.jsonl", cap_seconds=30).spent_seconds() == 12.0
