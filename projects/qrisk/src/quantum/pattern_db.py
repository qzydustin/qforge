"""
Pattern database for QRisk.

Manages the bad_pattern_memory.json file that stores persistent
problematic gate sequences discovered by DDMin across calibration windows.
Also provides token/scoring utilities used by circuit analysis scripts.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from qiskit import QuantumCircuit


def load_pattern_db(path: str | Path) -> Dict[str, Any]:
    """Load a bad_pattern_memory.json file."""
    path = Path(path)
    if not path.exists():
        return {
            "schema_version": 1,
            "layout_name": "",
            "backend": "",
            "target_layout": [],
            "patterns": [],
        }
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_pattern_db(db: Dict[str, Any], path: str | Path) -> None:
    """Save the pattern database to a JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)
        f.write("\n")


def _tokens_match(a: list, b: list) -> bool:
    """Check if two token lists represent the same pattern."""
    if len(a) != len(b):
        return False
    for ta, tb in zip(a, b):
        # Each token is [gate_name, [qubits], [params]]
        if ta[0] != tb[0]:
            return False
        if list(ta[1]) != list(tb[1]):
            return False
        # Compare params with tolerance for floats
        pa = ta[2] if len(ta) > 2 else []
        pb = tb[2] if len(tb) > 2 else []
        if len(pa) != len(pb):
            return False
        for va, vb in zip(pa, pb):
            try:
                if abs(float(va) - float(vb)) > 1e-5:
                    return False
            except (TypeError, ValueError):
                if str(va) != str(vb):
                    return False
    return True


def _make_pattern_id(tokens: list, existing_ids: set) -> str:
    """Generate a unique pattern ID from its tokens."""
    all_qubits = set()
    ops = []
    for tok in tokens:
        ops.append(tok[0])
        all_qubits.update(tok[1])
    qubits_str = "_".join(str(q) for q in sorted(all_qubits))
    ops_str = "_".join(ops)
    base = f"p_len{len(tokens)}_{ops_str}_q{qubits_str}"
    if base not in existing_ids:
        return base
    idx = 2
    while f"{base}_{idx}" in existing_ids:
        idx += 1
    return f"{base}_{idx}"


def add_pattern(
    db: Dict[str, Any],
    pattern_tokens: list,
    backend: str,
    run_timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    """Add a candidate pattern to the database.

    If the pattern already exists (same tokens), increment its evidence
    count and record the new observation.  Otherwise create a new entry.

    Args:
        db: The pattern database dict.
        pattern_tokens: List of [gate_name, [qubits], [params]] tokens.
        backend: Backend name (e.g. ``"ibm_fez"``).
        run_timestamp: ISO timestamp of the DDMin run.

    Returns:
        The updated database dict.
    """
    if not pattern_tokens:
        return db

    run_timestamp = run_timestamp or datetime.now().isoformat()

    # Normalize tokens to lists
    tokens = []
    for tok in pattern_tokens:
        tokens.append([
            tok[0],
            list(tok[1]) if not isinstance(tok[1], list) else tok[1],
            list(tok[2]) if len(tok) > 2 and not isinstance(tok[2], list) else (tok[2] if len(tok) > 2 else []),
        ])

    # Look for existing match
    for entry in db.get("patterns", []):
        if _tokens_match(entry["tokens"], tokens):
            evidence = entry.setdefault("evidence", {"observations": []})
            observations = evidence.setdefault("observations", [])
            observations.append({
                "timestamp": run_timestamp,
                "backend": backend,
            })
            evidence["run_count"] = len(observations)
            return db

    # New pattern
    existing_ids = {p["id"] for p in db.get("patterns", [])}
    pattern_id = _make_pattern_id(tokens, existing_ids)

    db.setdefault("patterns", []).append({
        "id": pattern_id,
        "length": len(tokens),
        "tokens": tokens,
        "evidence": {
            "run_count": 1,
            "observations": [{
                "timestamp": run_timestamp,
                "backend": backend,
            }],
        },
    })

    if not db.get("backend"):
        db["backend"] = backend

    return db


def promote_patterns(db: Dict[str, Any], min_runs: int = 2) -> List[Dict[str, Any]]:
    """Return patterns that have been independently rediscovered in >= min_runs.

    These patterns are considered persistent hardware effects suitable
    for use in the online pattern-guided compilation stage.
    """
    promoted = []
    for entry in db.get("patterns", []):
        run_count = entry.get("evidence", {}).get("run_count", 0)
        if run_count >= min_runs:
            promoted.append(entry)
    return promoted


# ---------------------------------------------------------------------------
# Token / fingerprint / scoring utilities
# ---------------------------------------------------------------------------

def normalize_token(circuit: QuantumCircuit, inst) -> tuple:
    """Convert a circuit instruction to a (name, qubits, params) token."""
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


def token_sequence(circuit: QuantumCircuit) -> list[tuple]:
    """Extract the normalized token sequence from a circuit (excluding non-gate ops)."""
    seq = []
    for inst in circuit.data:
        if inst.operation.name in {"measure", "barrier", "delay", "reset"}:
            continue
        seq.append(normalize_token(circuit, inst))
    return seq


def count_pattern_hits(sequence: list[tuple], pattern: list[tuple]) -> int:
    """Count how many times *pattern* appears as a contiguous subsequence."""
    n = len(pattern)
    target = tuple(pattern)
    return sum(1 for i in range(len(sequence) - n + 1) if tuple(sequence[i:i + n]) == target)


def fingerprint(sequence: list[tuple]) -> str:
    """Deterministic string fingerprint for a token sequence."""
    return json.dumps(sequence, separators=(",", ":"))


def load_patterns(memory_path: str | Path) -> list[dict]:
    """Load patterns from a bad_pattern_memory.json as a list of {id, tokens} dicts."""
    memory_path = Path(memory_path)
    with memory_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    patterns = []
    for item in data["patterns"]:
        patterns.append({
            "id": item["id"],
            "tokens": [
                (token[0], tuple(token[1]), tuple(token[2]))
                for token in item["tokens"]
            ],
        })
    return patterns


def score_variant(sequence: list[tuple], bad_patterns: list[dict]) -> dict:
    """Score a token sequence against known bad patterns."""
    breakdown = {}
    total_hits = 0
    distinct_hits = 0
    weighted_hits = 0
    for item in bad_patterns:
        count = count_pattern_hits(sequence, item["tokens"])
        breakdown[item["id"]] = count
        total_hits += count
        if count > 0:
            distinct_hits += 1
            weighted_hits += count * len(item["tokens"])
    max_len_hit = max(
        (len(item["tokens"]) for item in bad_patterns if breakdown[item["id"]] > 0),
        default=0,
    )
    return {
        "total_hits": total_hits,
        "distinct_hits": distinct_hits,
        "weighted_hits": weighted_hits,
        "max_len_hit": max_len_hit,
        "breakdown": breakdown,
    }
