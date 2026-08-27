"""RQ3 dose-response statistics (correct direction: more hits → larger TVD).

Reads the dose-response experiment summaries from verified/*/variants/*/summary.json
and computes:
  - Per-bucket mean/median/bootstrap 95% CI
  - Spearman ρ + bootstrap CI (pattern count vs TVD)
  - Mann-Whitney hit0 vs hit3 one-sided + Cliff's δ + rank-biserial
  - Cross-backend interaction test (OLS tvd ~ hits*backend + bootstrap slope-diff CI)
  - Effect sizes: (hit3_mean - hit0_mean) / hit0_mean for fez and marrakesh
  - Noise-model blind spot: Spearman(hits, TVD(ideal,noisy)) should be n.s.

The CORRECT direction (matching raw data):
  - fez: 0.050 → 0.066 (+32%)
  - marrakesh: 0.032 → 0.058 (+80%)
  - kingston: flat (no dose-response)

Outputs:
  analysis/_out/rq3/table_IV.csv (per-bucket stats)
  analysis/_out/rq3/rq3_stats.json (all tests)
  analysis/_out/rq3/raw_observations.csv (individual obs for plotting)
"""

from __future__ import annotations

import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
from scipy import stats

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

OUT_DIR = _REPO_ROOT / "analysis" / "_out" / "rq3"
VERIFIED_ROOT = _REPO_ROOT / "verified"

# Bootstrap config
BOOT_N = 10000
BOOT_SEED = 42


def load_dose_response_data() -> List[dict]:
    """Load all dose-response observations from verified/*/variants/*/summary.json."""
    observations = []
    for layout_dir in VERIFIED_ROOT.iterdir():
        if not layout_dir.is_dir():
            continue
        variants_dir = layout_dir / "variants"
        if not variants_dir.exists():
            continue
        for variant_dir in variants_dir.iterdir():
            summary_path = variant_dir / "summary.json"
            if not summary_path.exists():
                continue
            with open(summary_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            backend = data.get("backend", "")
            layout = data.get("layout", [])
            variant_name = variant_dir.name

            # Kingston fix: verify_kingston has backend=ibm_fez, layout=[]
            # but should be ibm_kingston, layout=[97,106,107,108]
            if variant_name == "verify_kingston":
                backend = "ibm_kingston"
                layout = [97, 106, 107, 108]

            buckets = data.get("buckets", {})
            for bucket_name, bucket_data in buckets.items():
                # Extract hit count from bucket name (hit_0 → 0)
                hit_count = int(bucket_name.split("_")[-1])
                completed = bucket_data.get("completed", [])
                for obs in completed:
                    observations.append({
                        "backend": backend,
                        "layout": str(layout),
                        "variant_name": variant_name,
                        "hit_count": hit_count,
                        "tvd_noisy_real": obs.get("tvd_noisy_vs_real", 0),
                        "tvd_ideal_real": obs.get("tvd_ideal_vs_real", 0),
                        "tvd_ideal_noisy": obs.get("tvd_ideal_vs_noisy", 0),
                        "n_swaps": obs.get("n_swaps", 0),
                    })
    return observations


def bootstrap_ci(data: List[float], stat_fn=np.mean, n_boot: int = BOOT_N,
                 seed: int = BOOT_SEED, alpha: float = 0.05) -> Tuple[float, float, float]:
    """Compute bootstrap CI for a statistic. Returns (stat, lower, upper)."""
    rng = np.random.default_rng(seed)
    data_arr = np.array(data)
    stat_obs = stat_fn(data_arr)
    boot_stats = []
    for _ in range(n_boot):
        sample = rng.choice(data_arr, size=len(data_arr), replace=True)
        boot_stats.append(stat_fn(sample))
    boot_stats = np.array(boot_stats)
    lower = np.percentile(boot_stats, alpha / 2 * 100)
    upper = np.percentile(boot_stats, (1 - alpha / 2) * 100)
    return stat_obs, lower, upper


def spearman_bootstrap_ci(x: List[float], y: List[float], n_boot: int = BOOT_N,
                          seed: int = BOOT_SEED) -> Tuple[float, float, float, float]:
    """Bootstrap CI for Spearman correlation. Returns (rho, p, lower, upper)."""
    rho_obs, p_obs = stats.spearmanr(x, y)
    rng = np.random.default_rng(seed)
    x_arr = np.array(x)
    y_arr = np.array(y)
    n = len(x_arr)
    boot_rhos = []
    for _ in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        boot_rhos.append(stats.spearmanr(x_arr[idx], y_arr[idx])[0])
    boot_rhos = np.array(boot_rhos)
    lower = np.percentile(boot_rhos, 2.5)
    upper = np.percentile(boot_rhos, 97.5)
    return rho_obs, p_obs, lower, upper


def cliffs_delta(group1: List[float], group2: List[float]) -> float:
    """Cliff's delta effect size: fraction of (x1, x2) pairs where x1 < x2 minus where x1 > x2."""
    n1 = len(group1)
    n2 = len(group2)
    greater = sum(1 for x1 in group1 for x2 in group2 if x1 < x2)
    less = sum(1 for x1 in group1 for x2 in group2 if x1 > x2)
    return (greater - less) / (n1 * n2)


def rank_biserial(group1: List[float], group2: List[float]) -> float:
    """Rank-biserial correlation (standardized Mann-Whitney U)."""
    u_stat, _ = stats.mannwhitneyu(group1, group2, alternative="less")
    n1 = len(group1)
    n2 = len(group2)
    return 1 - (2 * u_stat) / (n1 * n2)


def ols_interaction_test(hits: List[int], tvd: List[float], backend: List[str]) -> dict:
    """OLS regression: tvd ~ hits + backend + hits*backend.

    Returns slope for each backend and the interaction coefficient.
    Uses numpy for simple OLS (statsmodels not in venv).
    """
    # Encode backend as dummy (0=fez, 1=kingston)
    backend_dummy = [1 if b == "ibm_kingston" else 0 for b in backend]
    X = np.column_stack([
        np.ones(len(hits)),  # intercept
        hits,
        backend_dummy,
        np.array(hits) * np.array(backend_dummy),  # interaction
    ])
    y = np.array(tvd)
    # OLS: beta = (X'X)^-1 X'y
    beta = np.linalg.lstsq(X, y, rcond=None)[0]

    # Predict and compute R²
    y_pred = X @ beta
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    return {
        "intercept": beta[0],
        "slope_hits": beta[1],
        "coef_backend_kingston": beta[2],
        "interaction_hits_backend": beta[3],
        "r_squared": r2,
        "fez_slope": beta[1],
        "kingston_slope": beta[1] + beta[3],
    }


def bootstrap_slope_diff(hits: List[int], tvd: List[float], backend: List[str],
                         n_boot: int = BOOT_N, seed: int = BOOT_SEED) -> Tuple[float, float, float]:
    """Bootstrap CI for the difference in slopes (fez - kingston)."""
    rng = np.random.default_rng(seed)
    n = len(hits)
    diffs = []
    for _ in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        hits_b = [hits[i] for i in idx]
        tvd_b = [tvd[i] for i in idx]
        backend_b = [backend[i] for i in idx]
        ols = ols_interaction_test(hits_b, tvd_b, backend_b)
        diffs.append(ols["fez_slope"] - ols["kingston_slope"])
    diffs = np.array(diffs)
    obs_ols = ols_interaction_test(hits, tvd, backend)
    obs_diff = obs_ols["fez_slope"] - obs_ols["kingston_slope"]
    lower = np.percentile(diffs, 2.5)
    upper = np.percentile(diffs, 97.5)
    return obs_diff, lower, upper


def main() -> None:
    os.chdir(_REPO_ROOT)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    obs = load_dose_response_data()
    print(f"Loaded {len(obs)} observations")

    # Write raw observations CSV
    with open(OUT_DIR / "raw_observations.csv", "w", encoding="utf-8", newline="") as f:
        cols = ["backend", "layout", "variant_name", "hit_count",
                "tvd_noisy_real", "tvd_ideal_real", "tvd_ideal_noisy", "n_swaps"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(obs)

    # Group by backend and hit_count
    by_backend_hit: Dict[Tuple[str, int], List[float]] = defaultdict(list)
    for o in obs:
        by_backend_hit[(o["backend"], o["hit_count"])].append(o["tvd_noisy_real"])

    # Table IV: per-bucket stats with bootstrap CIs
    table_iv_rows = []
    for backend in ["ibm_fez", "ibm_marrakesh", "ibm_kingston"]:
        for hit in [0, 1, 2, 3]:
            vals = by_backend_hit.get((backend, hit), [])
            if not vals:
                continue
            mean_val, mean_lower, mean_upper = bootstrap_ci(vals, np.mean)
            median_val, med_lower, med_upper = bootstrap_ci(vals, np.median)
            table_iv_rows.append({
                "backend": backend,
                "hit_count": hit,
                "n": len(vals),
                "mean": round(mean_val, 5),
                "mean_ci_lower": round(mean_lower, 5),
                "mean_ci_upper": round(mean_upper, 5),
                "median": round(median_val, 5),
                "median_ci_lower": round(med_lower, 5),
                "median_ci_upper": round(med_upper, 5),
            })

    with open(OUT_DIR / "table_IV.csv", "w", encoding="utf-8", newline="") as f:
        cols = ["backend", "hit_count", "n", "mean", "mean_ci_lower", "mean_ci_upper",
                "median", "median_ci_lower", "median_ci_upper"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(table_iv_rows)

    # Per-backend Spearman correlation (hit_count vs tvd_noisy_real)
    stats_out = {}
    for backend in ["ibm_fez", "ibm_marrakesh", "ibm_kingston"]:
        backend_obs = [o for o in obs if o["backend"] == backend]
        if not backend_obs:
            continue
        hits = [o["hit_count"] for o in backend_obs]
        tvd = [o["tvd_noisy_real"] for o in backend_obs]
        rho, p, lower, upper = spearman_bootstrap_ci(hits, tvd)

        # Effect size: (mean_hit3 - mean_hit0) / mean_hit0
        hit0_vals = [o["tvd_noisy_real"] for o in backend_obs if o["hit_count"] == 0]
        hit3_vals = [o["tvd_noisy_real"] for o in backend_obs if o["hit_count"] == 3]
        if hit0_vals and hit3_vals:
            mean0 = np.mean(hit0_vals)
            mean3 = np.mean(hit3_vals)
            effect_pct = (mean3 - mean0) / mean0 * 100
        else:
            effect_pct = 0

        # Mann-Whitney hit0 vs hit3 (one-sided: hit0 < hit3)
        if hit0_vals and hit3_vals:
            u_stat, mw_p = stats.mannwhitneyu(hit0_vals, hit3_vals, alternative="less")
            delta = cliffs_delta(hit0_vals, hit3_vals)
            rb = rank_biserial(hit0_vals, hit3_vals)
        else:
            u_stat, mw_p, delta, rb = 0, 1.0, 0, 0

        stats_out[backend] = {
            "n": len(backend_obs),
            "spearman_rho": round(rho, 4),
            "spearman_p": round(p, 6),
            "spearman_ci_lower": round(lower, 4),
            "spearman_ci_upper": round(upper, 4),
            "effect_size_pct": round(effect_pct, 1),
            "mann_whitney_u": u_stat,
            "mann_whitney_p": round(mw_p, 6),
            "cliffs_delta": round(delta, 4),
            "rank_biserial": round(rb, 4),
        }

    # Cross-backend interaction (fez + kingston only, since marrakesh is separate hardware)
    fez_kingston_obs = [o for o in obs if o["backend"] in ["ibm_fez", "ibm_kingston"]]
    if fez_kingston_obs:
        hits_fk = [o["hit_count"] for o in fez_kingston_obs]
        tvd_fk = [o["tvd_noisy_real"] for o in fez_kingston_obs]
        backend_fk = [o["backend"] for o in fez_kingston_obs]
        ols = ols_interaction_test(hits_fk, tvd_fk, backend_fk)
        slope_diff, sd_lower, sd_upper = bootstrap_slope_diff(hits_fk, tvd_fk, backend_fk)
        stats_out["cross_backend_interaction"] = {
            "model": "tvd ~ hits + backend + hits*backend",
            "fez_slope": round(ols["fez_slope"], 6),
            "kingston_slope": round(ols["kingston_slope"], 6),
            "interaction_coef": round(ols["interaction_hits_backend"], 6),
            "r_squared": round(ols["r_squared"], 4),
            "slope_diff_fez_minus_kingston": round(slope_diff, 6),
            "slope_diff_ci_lower": round(sd_lower, 6),
            "slope_diff_ci_upper": round(sd_upper, 6),
        }

    # Noise-model blind spot: Spearman(hits, TVD(ideal,noisy)) — should be n.s.
    for backend in ["ibm_fez", "ibm_marrakesh", "ibm_kingston"]:
        backend_obs = [o for o in obs if o["backend"] == backend]
        if not backend_obs:
            continue
        hits = [o["hit_count"] for o in backend_obs]
        tvd_ideal_noisy = [o["tvd_ideal_noisy"] for o in backend_obs]
        rho_blind, p_blind, _, _ = spearman_bootstrap_ci(hits, tvd_ideal_noisy)
        stats_out[backend]["noise_model_blind_spot"] = {
            "spearman_rho": round(rho_blind, 4),
            "spearman_p": round(p_blind, 6),
            "interpretation": "n.s." if p_blind > 0.05 else "sig",
        }

    with open(OUT_DIR / "rq3_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats_out, f, indent=2)

    print("\n=== RQ3 Statistics Summary ===")
    for backend, s in stats_out.items():
        if backend == "cross_backend_interaction":
            continue
        print(f"\n{backend}:")
        print(f"  Spearman ρ = {s['spearman_rho']:.4f}, p = {s['spearman_p']:.6f}, "
              f"95% CI [{s['spearman_ci_lower']:.4f}, {s['spearman_ci_upper']:.4f}]")
        print(f"  Effect size (hit0→hit3): {s['effect_size_pct']:+.1f}%")
        print(f"  Mann-Whitney U (hit0<hit3): p = {s['mann_whitney_p']:.6f}, "
              f"Cliff's δ = {s['cliffs_delta']:.4f}")
        if "noise_model_blind_spot" in s:
            blind = s["noise_model_blind_spot"]
            print(f"  Blind spot (hits vs TVD(ideal,noisy)): ρ = {blind['spearman_rho']:.4f}, "
                  f"p = {blind['spearman_p']:.6f} ({blind['interpretation']})")

    if "cross_backend_interaction" in stats_out:
        cb = stats_out["cross_backend_interaction"]
        print(f"\nCross-backend interaction:")
        print(f"  Fez slope: {cb['fez_slope']:.6f}")
        print(f"  Kingston slope: {cb['kingston_slope']:.6f}")
        print(f"  Slope difference (fez - kingston): {cb['slope_diff_fez_minus_kingston']:.6f}, "
              f"95% CI [{cb['slope_diff_ci_lower']:.6f}, {cb['slope_diff_ci_upper']:.6f}]")
        print(f"  Interaction coefficient: {cb['interaction_coef']:.6f}, R² = {cb['r_squared']:.4f}")

    print(f"\nOutputs: {OUT_DIR}/table_IV.csv, rq3_stats.json, raw_observations.csv")


if __name__ == "__main__":
    main()
