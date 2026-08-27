"""Sensitivity analysis: recurrence threshold sweep at 40%, 50%, 60%.

Reads recurrence_matrix.csv and computes how many distinct patterns
pass the recurrence filter at each threshold level, and whether the
verified core patterns survive at each threshold.

Outputs:
  analysis/_out/sensitivity/sensitivity_sweep.csv
  analysis/_out/sensitivity/sensitivity_summary.json
"""

from __future__ import annotations

import csv
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

_REPO_ROOT = Path(__file__).resolve().parent.parent
IN_DIR = _REPO_ROOT / "analysis" / "_out" / "inventory"
OUT_DIR = _REPO_ROOT / "analysis" / "_out" / "sensitivity"

# The two verified core patterns (layer_exact JSON strings)
# We identify them by backend+layout (the only two with db_entries > 0)
VERIFIED_LAYOUTS = {
    ("ibm_fez", "97,106,107,108"),
    ("ibm_marrakesh", "6,7,8,17"),
}


def _norm_backend(b: str) -> str:
    b = (b or "").strip()
    if b.startswith("ibm_"):
        return b
    return f"ibm_{b}" if b else b


def load_recurrence_matrix() -> Tuple[
    Dict[Tuple[str, str, str], Dict[str, bool]],  # (backend, layout, identity) -> {run_date: flagged}
    Dict[Tuple[str, str], List[str]],  # (backend, layout) -> sorted run_dates
]:
    """Load the recurrence matrix from CSV."""
    matrix: Dict[Tuple[str, str, str], Dict[str, bool]] = defaultdict(dict)
    runs: Dict[Tuple[str, str], Set[str]] = defaultdict(set)

    with open(IN_DIR / "recurrence_matrix.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            b = _norm_backend(row["backend"])
            l = row["layout"]
            rd = row["run_date"]
            ident = row["layer_exact"]
            flagged = row["flagged"] == "1"
            matrix[(b, l, ident)][rd] = flagged
            runs[(b, l)].add(rd)

    sorted_runs = {k: sorted(v) for k, v in runs.items()}
    return matrix, sorted_runs


def load_hist_runs() -> Dict[Tuple[str, str], List[str]]:
    """Determine historical (OLD-schema) runs from reports.csv."""
    hist: Dict[Tuple[str, str], Set[str]] = defaultdict(set)
    reports_path = _REPO_ROOT / "analysis" / "_out" / "reports.csv"
    with open(reports_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["schema"] == "OLD":
                b = _norm_backend(row["backend"])
                l = row["layout"]
                rd = row["window_labels_weekly"]
                if rd:
                    hist[(b, l)].add(rd)
    return {k: sorted(v) for k, v in hist.items()}


def sweep_thresholds(
    matrix: Dict[Tuple[str, str, str], Dict[str, bool]],
    runs: Dict[Tuple[str, str], List[str]],
    hist_runs: Dict[Tuple[str, str], List[str]],
    thresholds: List[float] = [0.40, 0.50, 0.60],
) -> List[dict]:
    """For each threshold, count how many patterns pass recurrence filter.

    The recurrence denominator is the HISTORICAL run count for the layout
    (matching the inventory.py logic used for the main paper claims).
    """
    results = []

    for thresh in thresholds:
        total_pass = 0
        total_patterns = 0
        core_preserved = True
        per_layout_rows: List[dict] = []

        # Group identities by (backend, layout)
        by_layout: Dict[Tuple[str, str], List[Tuple[str, Dict[str, bool]]]] = defaultdict(list)
        for (b, l, ident), flagged in matrix.items():
            by_layout[(b, l)].append((ident, flagged))

        for (b, l), ident_list in sorted(by_layout.items()):
            hist_set = set(hist_runs.get((b, l), []))
            n_hist = len(hist_set)
            if n_hist == 0:
                # No historical runs → use all runs as denominator
                all_runs_set = set(runs.get((b, l), []))
                n_denom = len(all_runs_set)
                denom_set = all_runs_set
            else:
                n_denom = n_hist
                denom_set = hist_set

            passing = 0
            for ident, flagged in ident_list:
                # Count how many runs in the denominator set flagged this pattern
                count = sum(1 for rd, f in flagged.items() if f and rd in denom_set)
                freq = count / n_denom if n_denom > 0 else 0
                if freq >= thresh:
                    passing += 1

            total_pass += passing
            total_patterns += len(ident_list)

            # Check if this is a verified layout
            is_verified = (b, l) in VERIFIED_LAYOUTS
            if is_verified:
                # Find the most-frequent pattern (the core)
                best_count = 0
                for ident, flagged in ident_list:
                    count = sum(1 for rd, f in flagged.items() if f and rd in denom_set)
                    if count > best_count:
                        best_count = count
                core_freq = best_count / n_denom if n_denom > 0 else 0
                if core_freq < thresh:
                    core_preserved = False

            per_layout_rows.append({
                "threshold": thresh,
                "backend": b,
                "layout": l,
                "n_denom_runs": n_denom,
                "total_patterns": len(ident_list),
                "patterns_passing": passing,
                "is_verified": is_verified,
            })

        results.extend(per_layout_rows)

    return results


def main() -> None:
    os.chdir(_REPO_ROOT)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    matrix, runs = load_recurrence_matrix()
    hist_runs = load_hist_runs()

    thresholds = [0.40, 0.50, 0.60]
    rows = sweep_thresholds(matrix, runs, hist_runs, thresholds)

    # Write detailed CSV
    cols = ["threshold", "backend", "layout", "n_denom_runs", "total_patterns",
            "patterns_passing", "is_verified"]
    with open(OUT_DIR / "sensitivity_sweep.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    # Build summary
    summary = {}
    for thresh in thresholds:
        t_rows = [r for r in rows if r["threshold"] == thresh]
        total_pass = sum(r["patterns_passing"] for r in t_rows)
        total_patterns = sum(r["total_patterns"] for r in t_rows)
        verified_rows = [r for r in t_rows if r["is_verified"]]
        verified_pass = sum(r["patterns_passing"] for r in verified_rows)

        # Check if cores are preserved
        # The core is the most-frequent pattern per verified layout;
        # if verified_pass > 0 for each verified layout, core is preserved
        cores_preserved = all(r["patterns_passing"] > 0 for r in verified_rows)

        summary[f"{int(thresh*100)}%"] = {
            "threshold": thresh,
            "total_distinct_patterns": total_patterns,
            "patterns_passing": total_pass,
            "patterns_filtered": total_patterns - total_pass,
            "retention_pct": round(total_pass / total_patterns * 100, 1) if total_patterns else 0,
            "verified_cores_preserved": cores_preserved,
            "verified_layouts_passing": verified_pass,
        }

    with open(OUT_DIR / "sensitivity_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("=== Sensitivity Sweep Summary ===")
    for k, v in summary.items():
        print(f"  {k}: {v['patterns_passing']}/{v['total_distinct_patterns']} pass "
              f"({v['retention_pct']}%), cores preserved={v['verified_cores_preserved']}")


if __name__ == "__main__":
    main()
