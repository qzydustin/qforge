"""Pattern inventory + recurrence recompute.

Reads the tidy tables from analysis/_out/ and produces:
- table_I.csv      : corrected inventory across ALL layouts (real per-layout
                     run counts; candidate counts; pass-50%; DB entries).
- table_III.csv    : recurrence for the 2 verified layouts (core + neighbors,
                     historical vs recent runs; kept/drop at 50%).
- db_count.json    : authoritative verified-DB entry count.
- recurrence_matrix.csv : per-(backend,layout,segment,layer_exact) x run flagged matrix.

Window unit: one DDMin RUN (a distinct execution date). The 50% recurrence
denominator is the number of runs that (backend, layout) actually has.
"""

from __future__ import annotations

import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

IN_DIR = _REPO_ROOT / "analysis" / "_out"
OUT_DIR = IN_DIR / "inventory"


def _norm_backend(b: str) -> str:
    """Canonical long backend name (ibm_fez / ibm_marrakesh / ibm_kingston)."""
    b = (b or "").strip()
    if b.startswith("ibm_"):
        return b
    return f"ibm_{b}" if b else b


def _load(name: str) -> List[dict]:
    with open(IN_DIR / name, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _verified_patterns() -> Dict[Tuple[str, str], List[dict]]:
    """Read the two bad_pattern_memory.json files for the verified cores."""
    out: Dict[Tuple[str, str], List[dict]] = {}
    for p in [
        _REPO_ROOT / "verified" / "grover3-fez-O3-97_106_107_108" / "bad_pattern_memory.json",
        _REPO_ROOT / "verified" / "marrakesh_6_7_8_17" / "bad_pattern_memory.json",
    ]:
        d = json.load(open(p, "r", encoding="utf-8"))
        layout = ",".join(str(q) for q in d.get("layout", []))
        out[(_norm_backend(d.get("backend")), layout)] = d.get("patterns", []) or []
    return out


def build_recurrence_matrix() -> Tuple[dict, dict]:
    """Build the per-(backend,layout,segment,layer_exact) x run flagged matrix.

    Returns (matrix, runs_per_layout) where
      matrix[(b,l)][identity] = {run_date: bool_flagged}
      runs_per_layout[(b,l)]  = sorted list of distinct run dates.
    """
    reports = _load("reports.csv")
    segments = _load("segments.csv")

    # Distinct run date per report (use the weekly date = exact execution date).
    run_date_by_path = {r["report_path"]: r["window_labels_weekly"] for r in reports}
    schema_by_path = {r["report_path"]: r["schema"] for r in reports}
    runs_per_layout: Dict[Tuple[str, str], List[str]] = defaultdict(list)
    hist_runs: Dict[Tuple[str, str], List[str]] = defaultdict(list)  # OLD-schema runs
    rec_runs: Dict[Tuple[str, str], List[str]] = defaultdict(list)   # NEW-schema runs
    for r in reports:
        key = (_norm_backend(r["backend"]), r["layout"])
        rd = r["window_labels_weekly"]
        if rd and rd not in runs_per_layout[key]:
            runs_per_layout[key].append(rd)
            if r["schema"] == "OLD":
                hist_runs[key].append(rd)
            else:
                rec_runs[key].append(rd)
    for d in (runs_per_layout, hist_runs, rec_runs):
        for k in d:
            d[k].sort()

    # identity = layer_exact (the strict DB key). Only non-restored rows
    # represent what the tool actually returned.
    matrix: Dict[Tuple[str, str], Dict[str, Dict[str, bool]]] = defaultdict(lambda: defaultdict(dict))
    for s in segments:
        if s["restored"] == "True":
            continue
        key = (_norm_backend(s["backend"]), s["layout"])
        ident = s["layer_exact"]
        if not ident or ident == "[]":
            continue
        rd = run_date_by_path.get(s["report_path"], "")
        if not rd:
            continue
        matrix[key][ident][rd] = True

    return matrix, dict(runs_per_layout), dict(hist_runs), dict(rec_runs)


def _gate_type_projection(layer_exact_str: str) -> str:
    """Human-readable gate-type-only projection for Table I readability."""
    try:
        toks = json.loads(layer_exact_str)
    except json.JSONDecodeError:
        return ""
    names = [t[0] for t in toks]
    return " → ".join(names)


def recompute_table_I(matrix, runs_per_layout, hist_runs) -> List[dict]:
    """Inventory across ALL layouts. One row per (backend, layout)."""
    verified = _verified_patterns()
    rows: List[dict] = []
    for (b, l), idents in sorted(matrix.items()):
        n_runs = len(runs_per_layout.get((b, l), []))
        n_hist = len(hist_runs.get((b, l), []))
        # candidate distinct exact identities observed at least once
        per_ident_runs = {ident: len(d) for ident, d in idents.items()}
        candidate_count = len(per_ident_runs)
        # pass 50% over THIS layout's HISTORICAL run count (the longitudinal panel)
        pass50 = [ident for ident, d in idents.items()
                  if n_hist and sum(1 for rd in d if rd in set(hist_runs.get((b, l), []))) / n_hist >= 0.5]
        # is this a verified layout?
        vpat = verified.get((b, l))
        db_entries = len([p for p in vpat if p.get("verified")]) if vpat else 0
        # pick the most recurrent fragment for the projection column
        if per_ident_runs:
            best = max(per_ident_runs.items(), key=lambda kv: kv[1])
            frag = _gate_type_projection(best[0])
            frag_freq = f"{best[1]}/{n_runs}"
        else:
            frag, frag_freq = "", ""
        rows.append({
            "backend": b,
            "layout": l,
            "n_runs": n_runs,
            "n_hist_runs": n_hist,
            "candidate_count": candidate_count,
            "pass_50_count": len(pass50),
            "db_entries": db_entries,
            "top_fragment_projection": frag,
            "top_fragment_freq": frag_freq,
        })
    return rows


def recompute_table_III(matrix, runs_per_layout, hist_runs, rec_runs) -> List[dict]:
    """Recurrence for the 2 verified layouts: core + neighbors, kept/drop.

    Reports core frequency on the HISTORICAL panel (the 10-ish OLD-schema
    runs that the '8/10' and '10/10' claims refer to) AND on the RECENT panel
    (where the cores vanished -- the pattern-lifetime finding).
    """
    verified = _verified_patterns()
    rows = []
    for (b, l), vpat in verified.items():
        idents = matrix.get((b, l), {})
        hist_set = set(hist_runs.get((b, l), []))
        rec_set = set(rec_runs.get((b, l), []))
        n_hist = len(hist_set)
        n_rec = len(rec_set)
        per_ident_hist = {ident: sum(1 for rd in d if rd in hist_set) for ident, d in idents.items()}
        per_ident_rec = {ident: sum(1 for rd in d if rd in rec_set) for ident, d in idents.items()}
        kept = sum(1 for ident, c in per_ident_hist.items() if n_hist and c / n_hist >= 0.5)
        drop = len(per_ident_hist) - kept
        # the verified core = the most-frequent exact fragment on the historical panel
        if per_ident_hist:
            best_ident = max(per_ident_hist.items(), key=lambda kv: kv[1])[0]
            core_proj = _gate_type_projection(best_ident)
            core_hist = f"{per_ident_hist[best_ident]}/{n_hist}"
            core_rec = f"{per_ident_rec.get(best_ident, 0)}/{n_rec}"
        else:
            core_proj, core_hist, core_rec = "", "", ""
        rows.append({
            "backend": b,
            "layout": l,
            "n_hist_runs": n_hist,
            "n_rec_runs": n_rec,
            "core_projection": core_proj,
            "core_freq_historical": core_hist,
            "core_freq_recent": core_rec,
            "distinct_fragments": len(per_ident_hist),
            "kept_50pct_hist": kept,
            "dropped_hist": drop,
        })
    return rows


def database_entry_count() -> dict:
    verified = _verified_patterns()
    total = 0
    detail = {}
    for (b, l), vpat in verified.items():
        n = len([p for p in vpat if p.get("verified")])
        detail[f"{b}/{l}"] = n
        total += n
    return {"verified_db_entries": total, "per_layout": detail}


def write_matrix_csv(matrix, runs_per_layout) -> None:
    rows = []
    for (b, l), idents in sorted(matrix.items()):
        runs = runs_per_layout.get((b, l), [])
        for ident, flagged in idents.items():
            for rd in runs:
                rows.append({
                    "backend": b, "layout": l, "run_date": rd,
                    "layer_exact": ident,
                    "flagged": "1" if flagged.get(rd) else "0",
                })
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "recurrence_matrix.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["backend", "layout", "run_date", "layer_exact", "flagged"])
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    os.chdir(_REPO_ROOT)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    matrix, runs_per_layout, hist_runs, rec_runs = build_recurrence_matrix()

    # Table I
    t1 = recompute_table_I(matrix, runs_per_layout, hist_runs)
    with open(OUT_DIR / "table_I.csv", "w", encoding="utf-8", newline="") as f:
        cols = ["backend", "layout", "n_runs", "n_hist_runs", "candidate_count",
                "pass_50_count", "db_entries", "top_fragment_projection", "top_fragment_freq"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in t1:
            w.writerow({k: r.get(k, "") for k in cols})

    # Table III
    t3 = recompute_table_III(matrix, runs_per_layout, hist_runs, rec_runs)
    with open(OUT_DIR / "table_III.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["backend", "layout", "n_hist_runs", "n_rec_runs",
                                          "core_projection", "core_freq_historical",
                                          "core_freq_recent", "distinct_fragments",
                                          "kept_50pct_hist", "dropped_hist"])
        w.writeheader()
        w.writerows(t3)

    # DB count
    dbc = database_entry_count()
    with open(OUT_DIR / "db_count.json", "w", encoding="utf-8") as f:
        json.dump(dbc, f, indent=2)

    write_matrix_csv(matrix, runs_per_layout)

    print("=== db_count ===")
    print(json.dumps(dbc, indent=2))
    print("\n=== Table III (verified layouts) ===")
    for r in t3:
        print(f"  {r['backend']:13} hist={r['n_hist_runs']:2} rec={r['n_rec_runs']:2} "
              f"core={r['core_projection']:25} hist_freq={r['core_freq_historical']:8} "
              f"rec_freq={r['core_freq_recent']:8} distinct={r['distinct_fragments']} "
              f"kept@50%={r['kept_50pct_hist']} drop={r['dropped_hist']}")
    print(f"\n=== Table I: {len(t1)} layouts ===")
    for r in t1:
        print(f"  {r['backend']:11} lay={r['layout']:18} runs={r['n_runs']:2} hist={r['n_hist_runs']:2} "
              f"cand={r['candidate_count']} pass50={r['pass_50_count']} db={r['db_entries']}  "
              f"{r['top_fragment_projection']:30} {r['top_fragment_freq']}")


if __name__ == "__main__":
    main()
