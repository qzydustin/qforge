"""Recurrence heatmap: fragment × window presence/absence matrix.

Produces per-verified-layout heatmap data and matplotlib figures showing
which pattern fragments appeared in which execution windows. The May–Jun
zero-columns visualize the pattern-lifetime finding (cores vanish in the
recent weekly runs).

Outputs:
  analysis/_out/heatmap/heatmap_fez.csv
  analysis/_out/heatmap/heatmap_marrakesh.csv
  figures/heatmap_fez.pdf
  figures/heatmap_marrakesh.pdf
"""

from __future__ import annotations

import csv
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_REPO_ROOT = Path(__file__).resolve().parent.parent
IN_DIR = _REPO_ROOT / "analysis" / "_out" / "inventory"
OUT_DIR = _REPO_ROOT / "analysis" / "_out" / "heatmap"
FIG_DIR = _REPO_ROOT / "analysis" / "_out" / "figures"

VERIFIED = [
    {"backend": "ibm_fez", "layout": "97,106,107,108", "label": "fez"},
    {"backend": "ibm_marrakesh", "layout": "6,7,8,17", "label": "marrakesh"},
]


def _norm_backend(b: str) -> str:
    b = (b or "").strip()
    if b.startswith("ibm_"):
        return b
    return f"ibm_{b}" if b else b


def _gate_type_proj(layer_exact_str: str) -> str:
    """Short gate-type-only projection for heatmap y-axis labels."""
    try:
        toks = json.loads(layer_exact_str)
    except (json.JSONDecodeError, TypeError):
        return layer_exact_str[:30]
    names = [t[0] for t in toks]
    return "→".join(names)


def load_matrix_for_layout(
    backend: str, layout: str
) -> Tuple[List[str], List[str], Dict[str, Dict[str, bool]]]:
    """Load recurrence_matrix.csv filtered to one (backend, layout).

    Returns (sorted_run_dates, sorted_identities, ident_to_run_flagged).
    """
    run_dates: Set[str] = set()
    ident_data: Dict[str, Dict[str, bool]] = defaultdict(dict)

    with open(IN_DIR / "recurrence_matrix.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            b = _norm_backend(row["backend"])
            l = row["layout"]
            if b != backend or l != layout:
                continue
            rd = row["run_date"]
            ident = row["layer_exact"]
            flagged = row["flagged"] == "1"
            run_dates.add(rd)
            ident_data[ident][rd] = flagged

    sorted_dates = sorted(run_dates)
    # Sort identities by total frequency (most frequent first)
    sorted_idents = sorted(
        ident_data.keys(),
        key=lambda i: sum(1 for v in ident_data[i].values() if v),
        reverse=True,
    )
    return sorted_dates, sorted_idents, ident_data


def write_heatmap_csv(
    dates: List[str],
    idents: List[str],
    data: Dict[str, Dict[str, bool]],
    path: Path,
) -> None:
    """Write a fragment×window CSV (1/0 matrix)."""
    cols = ["identity", "gate_projection"] + dates
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for ident in idents:
            row = {
                "identity": ident,
                "gate_projection": _gate_type_proj(ident),
            }
            for d in dates:
                row[d] = "1" if data[ident].get(d) else "0"
            w.writerow(row)


def plot_heatmap(
    dates: List[str],
    idents: List[str],
    data: Dict[str, Dict[str, bool]],
    title: str,
    out_path: Path,
) -> None:
    """Generate a matplotlib heatmap figure."""
    n_idents = len(idents)
    n_dates = len(dates)
    if n_idents == 0 or n_dates == 0:
        return

    # Build binary matrix (rows=fragments, cols=dates)
    mat = np.zeros((n_idents, n_dates), dtype=int)
    for i, ident in enumerate(idents):
        for j, d in enumerate(dates):
            if data[ident].get(d):
                mat[i, j] = 1

    fig, ax = plt.subplots(figsize=(max(6, n_dates * 0.6), max(3, n_idents * 0.4)))
    cmap = plt.cm.colors.ListedColormap(["#f0f0f0", "#2166ac"])
    ax.imshow(mat, aspect="auto", cmap=cmap, interpolation="nearest")

    # X-axis: run dates (shortened)
    date_labels = [d[5:] for d in dates]  # drop year prefix
    ax.set_xticks(range(n_dates))
    ax.set_xticklabels(date_labels, rotation=45, ha="right", fontsize=7)

    # Y-axis: gate-type projections
    y_labels = [_gate_type_proj(ident)[:35] for ident in idents]
    ax.set_yticks(range(n_idents))
    ax.set_yticklabels(y_labels, fontsize=7)

    ax.set_xlabel("Execution window")
    ax.set_ylabel("Pattern fragment (gate types)")
    ax.set_title(title, fontsize=10)

    # Grid lines between cells
    ax.set_xticks(np.arange(-0.5, n_dates, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n_idents, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=0.5)
    ax.tick_params(which="minor", size=0)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    os.chdir(_REPO_ROOT)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    for v in VERIFIED:
        backend = v["backend"]
        layout = v["layout"]
        label = v["label"]

        dates, idents, data = load_matrix_for_layout(backend, layout)
        print(f"\n=== {label} ({backend}, {layout}) ===")
        print(f"  Run dates: {len(dates)}")
        print(f"  Distinct fragments: {len(idents)}")

        # Write CSV
        write_heatmap_csv(dates, idents, data, OUT_DIR / f"heatmap_{label}.csv")

        # Plot
        title = f"Pattern recurrence: {label} [{layout}]"
        plot_heatmap(dates, idents, data, title, FIG_DIR / f"heatmap_{label}.pdf")
        print(f"  → {FIG_DIR / f'heatmap_{label}.pdf'}")

    print("\nDone.")


if __name__ == "__main__":
    main()
