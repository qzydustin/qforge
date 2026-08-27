"""Minimality analysis for DDMin candidate sets.

Reads ddmin_steps.csv and determines whether each final candidate set is
provably 1-minimal (removing any single segment still triggers the oracle).

1-minimality evidence comes from:
  - kept=1: trivially 1-minimal (single segment, nothing to remove)
  - final action='sufficient': algorithm exhaustively tested individual complements
    and confirmed the set cannot be further reduced.
  - final action='test_complement' with kept>1: algorithm narrowed to the final
    set in that step but did NOT verify all remaining elements individually —
    still compact, not provably 1-minimal.

Outputs:
  analysis/_out/minimality/minimality.csv
  analysis/_out/minimality/minimality_summary.json
"""

from __future__ import annotations

import csv
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parent.parent
IN_DIR = _REPO_ROOT / "analysis" / "_out"
OUT_DIR = IN_DIR / "minimality"


def load_steps() -> Dict[str, List[dict]]:
    """Load ddmin_steps.csv grouped by report_path."""
    by_report: Dict[str, List[dict]] = {}
    with open(IN_DIR / "ddmin_steps.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            by_report.setdefault(row["report_path"], []).append(row)
    return by_report


def classify_minimality(steps: List[dict]) -> dict:
    """Classify one DDMin run's minimality status.

    Returns dict with keys: report_path, final_kept, final_action,
    minimality_class, is_1_minimal.
    """
    if not steps:
        return {}
    last = steps[-1]
    kept = int(last["kept"])
    action = last["action"]
    path = last["report_path"]

    # Reports where DDMin didn't run (baseline ratio below threshold)
    if kept >= 100:
        return {
            "report_path": path,
            "final_kept": kept,
            "final_action": action,
            "minimality_class": "no_reduction",
            "is_1_minimal": False,
            "ddmin_ran": False,
        }

    # Trivially 1-minimal: only 1 segment remains
    if kept == 1:
        return {
            "report_path": path,
            "final_kept": kept,
            "final_action": action,
            "minimality_class": "trivial_1_minimal",
            "is_1_minimal": True,
            "ddmin_ran": True,
        }

    # Multi-segment result with exhaustive confirmation
    if action == "sufficient":
        return {
            "report_path": path,
            "final_kept": kept,
            "final_action": action,
            "minimality_class": "confirmed_1_minimal",
            "is_1_minimal": True,
            "ddmin_ran": True,
        }

    # Multi-segment result without exhaustive confirmation
    return {
        "report_path": path,
        "final_kept": kept,
        "final_action": action,
        "minimality_class": "compact_not_confirmed",
        "is_1_minimal": False,
        "ddmin_ran": True,
    }


def compute_minimality() -> List[dict]:
    """Classify all DDMin runs and return per-report rows."""
    by_report = load_steps()
    results = []
    for path in sorted(by_report.keys()):
        steps = by_report[path]
        row = classify_minimality(steps)
        if row:
            results.append(row)
    return results


def summarize(results: List[dict]) -> dict:
    """Produce aggregate summary statistics."""
    active = [r for r in results if r["ddmin_ran"]]
    total_active = len(active)
    no_reduction = len(results) - total_active

    class_counts = Counter(r["minimality_class"] for r in active)
    trivial = class_counts.get("trivial_1_minimal", 0)
    confirmed = class_counts.get("confirmed_1_minimal", 0)
    compact = class_counts.get("compact_not_confirmed", 0)

    return {
        "total_reports": len(results),
        "ddmin_ran": total_active,
        "no_reduction": no_reduction,
        "trivial_1_minimal": trivial,
        "confirmed_1_minimal": confirmed,
        "compact_not_confirmed": compact,
        "total_with_1_minimality_evidence": trivial + confirmed,
        "pct_1_minimal_of_active": round(
            (trivial + confirmed) / total_active * 100, 1
        ) if total_active else 0,
        "pct_compact_of_active": round(
            compact / total_active * 100, 1
        ) if total_active else 0,
        "verdict": (
            "1-minimal"
            if compact == 0
            else "1-minimal for {}/{} ({:.0f}%); remaining {} are compact".format(
                trivial + confirmed, total_active,
                (trivial + confirmed) / total_active * 100,
                compact,
            )
        ),
        "algorithm_ensure_label": "1-minimal" if compact / total_active < 0.10 else "compact",
    }


def main() -> None:
    os.chdir(_REPO_ROOT)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    results = compute_minimality()
    summary = summarize(results)

    # Write per-report CSV
    cols = ["report_path", "final_kept", "final_action", "minimality_class",
            "is_1_minimal", "ddmin_ran"]
    with open(OUT_DIR / "minimality.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in results:
            w.writerow({k: r.get(k, "") for k in cols})

    # Write summary JSON
    with open(OUT_DIR / "minimality_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("=== Minimality Summary ===")
    print(json.dumps(summary, indent=2))
    print(f"\nVerdict: {summary['verdict']}")
    print(f"Algorithm \\ENSURE label: {summary['algorithm_ensure_label']}")


if __name__ == "__main__":
    main()
