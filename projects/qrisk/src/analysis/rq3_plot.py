"""RQ3 dose-response plots (correct direction: increasing).

Generates boxplot figures showing TVD(noisy, real) vs pattern hit count for
each backend. Y-axis INCREASES for fez/marrakesh (showing the +32%/+80%
effect), flat for kingston.

Outputs:
  figures/scaling_fez.pdf
  figures/scaling_marrakesh.pdf
  figures/scaling_kingston.pdf
  figures/scaling_combined.pdf
"""

from __future__ import annotations

import csv
import os
import sys
from pathlib import Path
from typing import List, Dict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

IN_DIR = _REPO_ROOT / "analysis" / "_out" / "rq3"
FIG_DIR = _REPO_ROOT / "analysis" / "_out" / "figures"


def load_observations() -> List[dict]:
    """Load raw_observations.csv."""
    with open(IN_DIR / "raw_observations.csv", "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def plot_backend(backend: str, obs: List[dict], effect_pct: float, out_path: Path) -> None:
    """Generate one boxplot for a backend."""
    backend_obs = [o for o in obs if o["backend"] == backend]
    if not backend_obs:
        return

    # Group by hit_count
    by_hit = {i: [] for i in range(4)}
    for o in backend_obs:
        hit = int(o["hit_count"])
        tvd = float(o["tvd_noisy_real"])
        by_hit[hit].append(tvd)

    # Prepare data for boxplot
    data = [by_hit[i] for i in range(4)]
    positions = [0, 1, 2, 3]

    fig, ax = plt.subplots(figsize=(6, 4))
    bp = ax.boxplot(data, positions=positions, widths=0.5, patch_artist=True,
                    boxprops=dict(facecolor="#d4e6f1", color="#1a5490"),
                    medianprops=dict(color="#c0392b", linewidth=2),
                    whiskerprops=dict(color="#1a5490"),
                    capprops=dict(color="#1a5490"))

    ax.set_xlabel("Pattern occurrence count", fontsize=11)
    ax.set_ylabel("TVD(noisy, real)", fontsize=11)
    ax.set_xticks(positions)
    ax.set_xticklabels(["0", "1", "2", "3"])
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    # Title with effect size
    backend_label = backend.replace("ibm_", "").capitalize()
    ax.set_title(f"{backend_label}: {effect_pct:+.1f}% effect (hit 0→3)", fontsize=12)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_combined(obs: List[dict], effect_sizes: Dict[str, float], out_path: Path) -> None:
    """Generate combined 3-panel figure."""
    backends = ["ibm_fez", "ibm_marrakesh", "ibm_kingston"]
    labels = ["Fez", "Marrakesh", "Kingston"]

    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)

    for ax, backend, label in zip(axes, backends, labels):
        backend_obs = [o for o in obs if o["backend"] == backend]
        by_hit = {i: [] for i in range(4)}
        for o in backend_obs:
            hit = int(o["hit_count"])
            tvd = float(o["tvd_noisy_real"])
            by_hit[hit].append(tvd)

        data = [by_hit[i] for i in range(4)]
        positions = [0, 1, 2, 3]
        bp = ax.boxplot(data, positions=positions, widths=0.5, patch_artist=True,
                        boxprops=dict(facecolor="#d4e6f1", color="#1a5490"),
                        medianprops=dict(color="#c0392b", linewidth=2),
                        whiskerprops=dict(color="#1a5490"),
                        capprops=dict(color="#1a5490"))

        ax.set_xlabel("Pattern occurrence count", fontsize=10)
        if ax == axes[0]:
            ax.set_ylabel("TVD(noisy, real)", fontsize=10)
        ax.set_xticks(positions)
        ax.set_xticklabels(["0", "1", "2", "3"])
        ax.grid(axis="y", alpha=0.3, linestyle="--")

        effect = effect_sizes.get(backend, 0)
        ax.set_title(f"{label} ({effect:+.1f}%)", fontsize=11)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    os.chdir(_REPO_ROOT)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    obs = load_observations()

    # Compute effect sizes for captions
    effect_sizes = {}
    for backend in ["ibm_fez", "ibm_marrakesh", "ibm_kingston"]:
        backend_obs = [o for o in obs if o["backend"] == backend]
        hit0 = [float(o["tvd_noisy_real"]) for o in backend_obs if int(o["hit_count"]) == 0]
        hit3 = [float(o["tvd_noisy_real"]) for o in backend_obs if int(o["hit_count"]) == 3]
        if hit0 and hit3:
            effect_pct = (np.mean(hit3) - np.mean(hit0)) / np.mean(hit0) * 100
        else:
            effect_pct = 0
        effect_sizes[backend] = effect_pct

    # Individual backend plots
    plot_backend("ibm_fez", obs, effect_sizes["ibm_fez"], FIG_DIR / "scaling_fez.pdf")
    plot_backend("ibm_marrakesh", obs, effect_sizes["ibm_marrakesh"], FIG_DIR / "scaling_marrakesh.pdf")
    plot_backend("ibm_kingston", obs, effect_sizes["ibm_kingston"], FIG_DIR / "scaling_kingston.pdf")

    # Combined plot
    plot_combined(obs, effect_sizes, FIG_DIR / "scaling_combined.pdf")

    print("=== RQ3 Plots Generated ===")
    for backend, eff in effect_sizes.items():
        print(f"  {backend}: {eff:+.1f}%")
    print(f"\nOutputs:")
    for name in ["scaling_fez.pdf", "scaling_marrakesh.pdf", "scaling_kingston.pdf", "scaling_combined.pdf"]:
        print(f"  {FIG_DIR / name}")


if __name__ == "__main__":
    main()
