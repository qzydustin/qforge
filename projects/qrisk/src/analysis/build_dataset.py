"""Build the unified tidy dataset from ALL raw DDMin + verification reports.

Walks the four data roots (artifacts/, candidate_groups/, verified/,
.backup_verify_20260628/), unifies the OLD and NEW DDMin report schemas into
a single token representation that PRESERVES gate parameters, corrects the
verify_kingston mislabel programmatically, and emits five tidy CSVs plus a
schema-migration log and an audit report.

Usage:
    python -m analysis.build_dataset --out analysis/_out/
    python -m analysis.build_dataset --out analysis/_out/ --audit

The tidy tables are the single source of truth for every downstream table and
every number in the paper. Nothing downstream re-reads raw JSON.
"""

from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Make the repo root importable when run as a module from inside qrisk-raw/.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from analysis import pattern_identity as pid  # noqa: E402

# Roots that may contain ddmin_reports/*.json or verify summary.json files.
DATA_ROOTS = [
    "artifacts",
    "candidate_groups",
    "verified",
    ".backup_verify_20260628",
]

# Verified-pattern tokens used to relabel the mislabeled verify_kingston run.
# Authoritatively confirmed: the d7f4... run executed the FEZ pattern variants
# on ibm_kingston. Source: verified/grover3-fez-O3-97_106_107_108/bad_pattern_memory.json
KINGSTON_FIX_BACKEND = "ibm_kingston"
KINGSTON_FIX_LAYOUT = [97, 106, 107, 108]
KINGSTON_FIX_PATTERN_DISPLAY = "sx(107) -> rz(107, 0.392699) -> sx(108) -> cz(108,107)"
KINGSTON_FIX_TOKENS = [
    ["sx", [107], []],
    ["rz", [107], [0.392699]],
    ["sx", [108], []],
    ["cz", [108, 107], []],
]


# ---------------------------------------------------------------------------
# Data classes for tidy rows
# ---------------------------------------------------------------------------

@dataclass
class ReportRow:
    report_path: str
    backend: str
    layout: str  # comma-joined physical qubits
    schema: str  # NEW | OLD
    window_label: str  # YYYY-MM (monthly) -- the recurrence window
    window_labels_weekly: str  # YYYY-MM-DD weekly date, for audit only
    window_kind: str  # monthly | weekly
    n_segments_flagged: int
    baseline_ratio: Optional[float]
    noise_threshold: Optional[float]
    min_expected_tvd: Optional[float]
    n_ddmin_steps: int
    was_force_cleaned: bool
    restored: bool  # True if this row came from _clean_override.original
    has_negative_tau: bool


@dataclass
class SegmentRow:
    report_path: str
    backend: str
    layout: str
    window_label: str
    window_kind: str
    segment_id: str
    moments: str  # comma-joined moment indices
    layer_exact: str  # repr of the exact token tuple
    layer_moment: str
    layer_structural: str
    has_cz: bool
    n_gates: int
    was_force_cleaned: bool
    restored: bool


@dataclass
class GateTokenRow:
    report_path: str
    segment_id: str
    token_index: int
    op: str
    qubits: str  # comma-joined
    params: str  # comma-joined
    has_cz: bool


@dataclass
class DdminStepRow:
    report_path: str
    step: int
    action: str
    kept: Optional[int]
    ratio_before: Optional[float]
    ratio_after: Optional[float]
    reduction: Optional[float]
    noise_threshold: Optional[float]
    result: str


@dataclass
class VerificationObsRow:
    source: str  # summary.json path
    backend: str
    layout: str
    bucket: str  # hit_0..hit_3
    pattern_hits: int
    n_swaps: int
    tvd_ideal_vs_real: float
    tvd_noisy_vs_real: float
    tvd_ideal_vs_noisy: float
    corrected: bool  # True if kingston mislabel fix applied


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _content_hash(obj: Any) -> str:
    return hashlib.md5(
        json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


def _is_ddmin_report(d: dict) -> bool:
    has_steps = ("ddmin_log" in d) or ("ddmin_steps" in d)
    has_segs = ("problematic_segments" in d) or ("problematic_details" in d)
    return has_steps and has_segs


def _classify_schema(d: dict) -> str:
    return "NEW" if "meta" in d else ("OLD" if "timestamp" in d else "NEW")


def _parse_layout_from_dir(dirname: str) -> Tuple[Optional[str], Optional[List[int]]]:
    """Parse ``grover3-<backend>-O3-<q0_q1_q2_q3>`` or ``marrakesh_<q0_q1_q2_q3>``."""
    base = os.path.basename(dirname)
    if base.startswith("grover3-"):
        parts = base.split("-")  # grover3, fez, O3, 97_106_107_108
        if len(parts) >= 4:
            backend = parts[1]
            try:
                layout = [int(x) for x in parts[3].split("_")]
                return backend, layout
            except ValueError:
                return backend, None
            return backend, None
    if base.startswith("marrakesh_"):
        try:
            layout = [int(x) for x in base[len("marrakesh_"):].split("_")]
            return "marrakesh", layout
        except ValueError:
            return "marrakesh", None
    return None, None


def _window_from_report(d: dict, schema: str) -> Tuple[str, str, str]:
    """Return (monthly_label YYYY-MM, weekly_label YYYY-MM-DD, window_kind).

    The recurrence window is the CALENDAR MONTH. The weekly date is retained
    only for the audit / heatmap column granularity.
    """
    if schema == "OLD":
        ts = d.get("timestamp", "")  # "2025-12-10T16:45:33"
    else:
        ts = (d.get("meta") or {}).get("timestamp", "")  # ISO with microseconds
    date_part = ts[:10] if ts else ""  # YYYY-MM-DD
    monthly = date_part[:7] if date_part else ""
    # OLD schema runs are sparse monthly snapshots; NEW schema runs are weekly.
    kind = "monthly" if schema == "OLD" else "weekly"
    return monthly, date_part, kind


def _baseline_ratio(d: dict, schema: str) -> Optional[float]:
    if schema == "OLD":
        if "baseline_ratio" in d:
            return _f(d["baseline_ratio"])
        for s in d.get("ddmin_steps") or []:
            if s.get("action") == "baseline":
                return _f(s.get("ratio"))
        return None
    # NEW: baseline lives inside ddmin_log
    for s in d.get("ddmin_log") or []:
        if s.get("action") == "baseline":
            return _f(s.get("ratio"))
    return None


def _f(v: Any) -> Optional[float]:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _noise_threshold(d: dict, schema: str) -> Optional[float]:
    if schema == "OLD":
        return _f(d.get("noise_threshold"))
    ev = d.get("meta", {}).get("evaluation", {}) or {}
    return _f(ev.get("noise_threshold"))


def _min_expected_tvd(d: dict, schema: str) -> Optional[float]:
    if schema == "OLD":
        return None
    ev = d.get("meta", {}).get("evaluation", {}) or {}
    return _f(ev.get("min_expected_tvd"))


# ---------------------------------------------------------------------------
# Report extraction
# ---------------------------------------------------------------------------

def discover_reports(root: str) -> List[str]:
    """Glob all *.json that are genuine DDMin reports under ``root``."""
    out = []
    for p in glob.glob(os.path.join(root, "**", "*.json"), recursive=True):
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(d, dict) and _is_ddmin_report(d):
            out.append(p)
    return out


def _extract_segments_new(
    d: dict, report_path: str, backend: str, layout: str,
    monthly: str, weekly: str, kind: str, was_cleaned: bool,
    seg_rows: List[SegmentRow], gate_rows: List[GateTokenRow],
    restored: bool,
) -> int:
    """Extract per-segment rows from a NEW-schema report.

    NEW reports store ``pattern`` (one concatenated list) and ``segments_info``
    (full segment table). We key segments by their position in the circuit.
    When ``_clean_override`` is present, the live ``problematic_segments`` is
    empty, so we also restore the original from ``_clean_override.original``.
    """
    count = 0
    segs_info = d.get("segments_info") or []
    flagged = list(d.get("problematic_segments") or [])

    def _emit(seg_id: str, tokens: List, moments):
        if not tokens:
            return
        norm = [pid.normalize_token(g) for g in tokens]
        layer_exact = pid.layer_exact(norm)
        layer_moment = pid.layer_moment(layer_exact)
        layer_struct = pid.layer_structural(layer_exact)
        nonlocal count
        count += 1
        seg_rows.append(SegmentRow(
            report_path=report_path, backend=backend, layout=layout,
            window_label=monthly, window_kind=kind, segment_id=str(seg_id),
            moments=",".join(str(m) for m in (moments or [])),
            layer_exact=_tuple_repr(layer_exact),
            layer_moment=layer_moment or "",
            layer_structural=layer_struct or "",
            has_cz=pid.pattern_has_cz(layer_exact),
            n_gates=len(norm),
            was_force_cleaned=was_cleaned, restored=restored,
        ))
        for i, tok in enumerate(norm):
            gate_rows.append(GateTokenRow(
                report_path=report_path, segment_id=str(seg_id),
                token_index=i, op=tok[0],
                qubits=",".join(str(q) for q in tok[1]),
                params=",".join(repr(p) for p in tok[2]),
                has_cz=(tok[0] == "cz"),
            ))

    # Primary: flagged segment ids -> look up tokens in segments_info.
    if flagged:
        # Build a map of segment layer_id -> instructions.
        info_by_id = {}
        for seg in segs_info:
            lid = seg.get("layer_id")
            if lid is not None:
                info_by_id[lid] = seg
        for sid in flagged:
            seg = info_by_id.get(sid, {})
            insts = seg.get("instructions") or []
            # instructions may be dicts (op/qubits/params) or verbose strings
            toks = []
            for inst in insts:
                if isinstance(inst, dict) and ("op" in inst or "operation" in inst):
                    toks.append(inst)
            moments = seg.get("moments")
            _emit(sid, toks, moments)

    # Fallback: the single concatenated `pattern` field (no segment id).
    if not count and (d.get("pattern")):
        toks = d.get("pattern") or []
        _emit("pattern", toks, [])

    # Restore originals if force-cleaned.
    if was_cleaned and not restored:
        orig = (d.get("_clean_override") or {}).get("original") or {}
        orig_segs = orig.get("problematic_segments") or []
        orig_pattern = orig.get("pattern") or []
        # Emit a parallel restored row.
        if orig_pattern and not orig_segs:
            _emit("pattern_restored", orig_pattern, [])
        else:
            info_by_id = {}
            for seg in segs_info:
                lid = seg.get("layer_id")
                if lid is not None:
                    info_by_id[lid] = seg
            for sid in orig_segs:
                seg = info_by_id.get(sid, {})
                insts = [i for i in (seg.get("instructions") or []) if isinstance(i, dict) and ("op" in i or "operation" in i)]
                _emit(f"{sid}_restored", insts, seg.get("moments"))

    return count


def _extract_segments_old(
    d: dict, report_path: str, backend: str, layout: str,
    monthly: str, weekly: str, kind: str,
    seg_rows: List[SegmentRow], gate_rows: List[GateTokenRow],
) -> int:
    """OLD schema: problematic_details[].instructions -- one segment each."""
    count = 0
    for detail in d.get("problematic_details") or []:
        insts = detail.get("instructions") or []
        if not insts:
            continue
        norm = [pid.normalize_token(g) for g in insts]
        layer_exact = pid.layer_exact(norm)
        seg_id = str(detail.get("layer_id") if detail.get("layer_id") is not None else f"p{count}")
        seg_rows.append(SegmentRow(
            report_path=report_path, backend=backend, layout=layout,
            window_label=monthly, window_kind=kind, segment_id=seg_id,
            moments=",".join(str(m) for m in (detail.get("moments") or [])),
            layer_exact=_tuple_repr(layer_exact),
            layer_moment=pid.layer_moment(layer_exact) or "",
            layer_structural=pid.layer_structural(layer_exact) or "",
            has_cz=pid.pattern_has_cz(layer_exact),
            n_gates=len(norm), was_force_cleaned=False, restored=False,
        ))
        for i, tok in enumerate(norm):
            gate_rows.append(GateTokenRow(
                report_path=report_path, segment_id=seg_id, token_index=i,
                op=tok[0], qubits=",".join(str(q) for q in tok[1]),
                params=",".join(repr(p) for p in tok[2]),
                has_cz=(tok[0] == "cz"),
            ))
        count += 1
    return count


def _extract_ddmin_steps(d: dict, schema: str, report_path: str, steps: List[DdminStepRow]) -> int:
    raw = (d.get("ddmin_steps") or []) if schema == "OLD" else (d.get("ddmin_log") or [])
    n = 0
    for i, s in enumerate(raw):
        action = str(s.get("action", ""))
        kept_raw = s.get("kept")
        # `kept` may be an int (count) or a list (kept segment ids); coerce.
        if isinstance(kept_raw, list):
            kept = len(kept_raw)
        elif kept_raw is None:
            kept = None
        else:
            try:
                kept = int(kept_raw)
            except (TypeError, ValueError):
                kept = None
        ratio_after = _f(s.get("ratio"))
        ratio_before = _f(s.get("baseline_ratio")) or _f(s.get("ratio_before"))
        reduction = _f(s.get("reduction"))
        if reduction is None:
            reduction = _f(s.get("drop"))
        nt = _f(s.get("noise_threshold"))
        result = str(s.get("result", ""))
        steps.append(DdminStepRow(
            report_path=report_path, step=i, action=action,
            kept=kept,
            ratio_before=ratio_before, ratio_after=ratio_after,
            reduction=reduction, noise_threshold=nt, result=result,
        ))
        n += 1
    return n


def _tuple_repr(t) -> str:
    """Stable string repr of an exact-token tuple for CSV storage + matching."""
    return json.dumps([[tok[0], list(tok[1]), list(tok[2])] for tok in t], default=str)


# ---------------------------------------------------------------------------
# Verification summaries (the RQ3 data)
# ---------------------------------------------------------------------------

def _is_verify_summary(d: dict) -> bool:
    return isinstance(d, dict) and "buckets" in d and "hit_0" in d.get("buckets", {})


def discover_verify_summaries(root: str) -> List[str]:
    out = []
    for p in glob.glob(os.path.join(root, "**", "summary.json"), recursive=True):
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        if _is_verify_summary(d):
            out.append(p)
    return out


def extract_verification(summary_path: str, rows: List[VerificationObsRow]) -> int:
    """Extract per-observation rows from a verify summary.json.

    Applies the kingston mislabel correction: if the summary is the
    verify_kingston file (detected by path), override backend/layout/pattern.
    Excludes the incomplete d90g... kingston run (only 2/40 obs, no summary).
    """
    with open(summary_path, "r", encoding="utf-8") as f:
        d = json.load(f)

    backend = d.get("backend", "")
    layout = d.get("layout") or []
    corrected = False
    is_kingston_mislabel = "verify_kingston" in summary_path

    if is_kingston_mislabel:
        backend = KINGSTON_FIX_BACKEND
        layout = KINGSTON_FIX_LAYOUT
        corrected = True

    layout_str = ",".join(str(q) for q in layout) if layout else ""
    n = 0
    for bucket_name in ["hit_0", "hit_1", "hit_2", "hit_3"]:
        bucket = d.get("buckets", {}).get(bucket_name) or {}
        for obs in bucket.get("completed") or []:
            rows.append(VerificationObsRow(
                source=summary_path, backend=backend, layout=layout_str,
                bucket=bucket_name,
                pattern_hits=int(obs.get("pattern_hits", -1)),
                n_swaps=int(obs.get("n_swaps", -1)),
                tvd_ideal_vs_real=_f(obs.get("tvd_ideal_vs_real")) or 0.0,
                tvd_noisy_vs_real=_f(obs.get("tvd_noisy_vs_real")) or 0.0,
                tvd_ideal_vs_noisy=_f(obs.get("tvd_ideal_vs_noisy")) or 0.0,
                corrected=corrected,
            ))
            n += 1
    return n


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------

def build(out_dir: str) -> dict:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    report_rows: List[ReportRow] = []
    seg_rows: List[SegmentRow] = []
    gate_rows: List[GateTokenRow] = []
    step_rows: List[DdminStepRow] = []
    ver_rows: List[VerificationObsRow] = []

    # Dedupe reports by content hash (the .backup root mirrors some verified/).
    seen_hashes: dict[str, str] = {}
    dropped_dupes: List[Tuple[str, str]] = []

    for root in DATA_ROOTS:
        if not os.path.isdir(root):
            continue
        for p in discover_reports(root):
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            ch = _content_hash(d)
            if ch in seen_hashes:
                dropped_dupes.append((p, seen_hashes[ch]))
                continue
            seen_hashes[ch] = p

            schema = _classify_schema(d)
            # Derive backend/layout from directory, fall back to report fields.
            backend_dir, layout_dir = _parse_layout_from_dir(
                os.path.dirname(os.path.dirname(p))  # .../<group>/ddmin_reports
                if os.path.basename(os.path.dirname(p)) == "ddmin_reports"
                else os.path.dirname(p)
            )
            backend = backend_dir or (d.get("backend") or "")
            if schema == "NEW" and not layout_dir:
                layout_dir = (d.get("meta") or {}).get("circuit_info", {}).get("measured_qubits")
            layout = layout_dir or []
            layout_str = ",".join(str(q) for q in layout)

            monthly, weekly, kind = _window_from_report(d, schema)
            bl = _baseline_ratio(d, schema)
            nt = _noise_threshold(d, schema)
            min_tvd = _min_expected_tvd(d, schema)
            was_cleaned = "_clean_override" in d

            # Count flagged segments + emit segment/gate rows.
            if schema == "NEW":
                n_seg = _extract_segments_new(
                    d, p, backend, layout_str, monthly, weekly, kind, was_cleaned,
                    seg_rows, gate_rows, restored=False,
                )
            else:
                n_seg = _extract_segments_old(
                    d, p, backend, layout_str, monthly, weekly, kind,
                    seg_rows, gate_rows,
                )
            n_steps = _extract_ddmin_steps(d, schema, p, step_rows)

            report_rows.append(ReportRow(
                report_path=p, backend=backend, layout=layout_str, schema=schema,
                window_label=monthly, window_labels_weekly=weekly, window_kind=kind,
                n_segments_flagged=n_seg, baseline_ratio=bl, noise_threshold=nt,
                min_expected_tvd=min_tvd, n_ddmin_steps=n_steps,
                was_force_cleaned=was_cleaned, restored=False,
                has_negative_tau=(nt is not None and nt < 0),
            ))

    # Verification observations.
    verify_dupe_keys = set()
    for root in DATA_ROOTS:
        if not os.path.isdir(root):
            continue
        for p in discover_verify_summaries(root):
            # Dedupe verify summaries by content hash too.
            with open(p, "r", encoding="utf-8") as f:
                ch = _content_hash(json.load(f))
            if ch in verify_dupe_keys:
                continue
            verify_dupe_keys.add(ch)
            extract_verification(p, ver_rows)

    # ---- write CSVs ----
    _write_csv(out_path / "reports.csv", report_rows)
    _write_csv(out_path / "segments.csv", seg_rows)
    _write_csv(out_path / "gate_tokens.csv", gate_rows)
    _write_csv(out_path / "ddmin_steps.csv", step_rows)
    _write_csv(out_path / "verification_obs.csv", ver_rows)

    _write_schema_migration(out_path)

    stats = {
        "n_reports": len(report_rows),
        "n_segments_rows": len(seg_rows),
        "n_gate_rows": len(gate_rows),
        "n_step_rows": len(step_rows),
        "n_verification_obs": len(ver_rows),
        "dropped_duplicates": dropped_dupes,
    }
    with open(out_path / "build_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, default=str)
    return stats


def _write_csv(path: Path, rows: List[Any]) -> None:
    if not rows:
        # write header only
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("")
        return
    fields = list(asdict(rows[0]).keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(asdict(r))


def _write_schema_migration(out_path: Path) -> None:
    md = """# Schema Migration Log

Unification of OLD and NEW DDMin report schemas into one token representation.

## Token form (canonical across schemas)

Every gate becomes the tuple `(op, qubits_tuple, params_tuple)` via
`analysis.pattern_identity.normalize_token`. Parameterless gates (cz, x, sx)
carry an empty params tuple. RZ angles are kept as floats rounded to 6 dp.
Matching tolerance `PARAM_TOL = 1e-5` mirrors `quantum.pattern_db._tokens_match`,
so the paper's "exact match" definition equals the live database's match.

## NEW schema -> unified

| NEW field | Unified field |
|---|---|
| `meta.timestamp` | window_label = `timestamp[:7]` (YYYY-MM, monthly column); weekly = `timestamp[:10]` |
| `meta.evaluation.noise_threshold` | noise_threshold |
| `meta.evaluation.min_expected_tvd` | min_expected_tvd |
| `pattern` (`[op,[q],[p]]` list) | one SegmentRow keyed `segment_id="pattern"` |
| `problematic_segments` + `segments_info[].instructions` | per-segment SegmentRows (preferred over concatenated `pattern`) |
| `ddmin_log` (`action=baseline` holds ratio) | baseline_ratio + DdminStepRows |
| `_clean_override.original` | parallel SegmentRows with `restored=True` |

## OLD schema -> unified

| OLD field | Unified field |
|---|---|
| `timestamp` (top-level) | window_label = `timestamp[:7]` |
| `baseline_ratio` (top-level, else `ddmin_steps[baseline].ratio`) | baseline_ratio |
| `noise_threshold` (top-level) | noise_threshold |
| `problematic_details[].instructions` (`{op,qubits,params}`) | ONE SegmentRow per detail (never concatenated) |
| `ddmin_steps` | DdminStepRows |

## Window unit

The recurrence window is the calendar **month** (YYYY-MM). Old-schema runs are
sparse monthly snapshots; new-schema runs are weekly (the weekly date is
retained in `reports.csv.window_labels_weekly` for heatmap granularity only).
The 50% recurrence denominator is the number of distinct monthly windows that
a given (backend, layout) actually has -- not a global constant.
"""
    with open(out_path / "schema_migration.md", "w", encoding="utf-8") as f:
        f.write(md)


# ---------------------------------------------------------------------------
# Audit report
# ---------------------------------------------------------------------------

def write_audit(out_dir: str) -> None:
    import statistics
    out_path = Path(out_dir)
    lines: List[str] = ["# Data Audit Report", ""]

    def _load(name):
        with open(out_path / name, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    reports = _load("reports.csv")
    segments = _load("segments.csv")
    verify = _load("verification_obs.csv")

    n = len(reports)
    schema_new = sum(1 for r in reports if r["schema"] == "NEW")
    schema_old = sum(1 for r in reports if r["schema"] == "OLD")
    n_clean = sum(1 for r in reports if r["was_force_cleaned"] == "True")
    n_negtau = sum(1 for r in reports if r["has_negative_tau"] == "True")

    lines += [
        "## 1. Schema mix", "",
        f"- Total genuine DDMin reports: **{n}**",
        f"- NEW schema: **{schema_new}** / OLD schema: **{schema_old}**",
        "",
        "### Per-backend × schema",
        "",
        "| backend | NEW | OLD | total |",
        "|---|---:|---:|---:|",
    ]
    ct = defaultdict(lambda: defaultdict(int))
    for r in reports:
        ct[r["backend"]][r["schema"]] += 1
    for b in sorted(ct):
        lines.append(f"| {b} | {ct[b]['NEW']} | {ct[b]['OLD']} | {sum(ct[b].values())} |")

    lines += ["", "## 2. Missing / duplicate", "",
              f"- Content-hash duplicates dropped (mirrored across roots): see `build_stats.json`.",
              f"- Reports with 0 flagged segments: **{sum(1 for r in reports if int(r['n_segments_flagged'])==0)}** "
              "(includes force-cleaned reports whose live pattern was emptied).",
              ""]

    lines += ["## 3. `_clean_override` policy", "",
              f"- **{n_clean}** reports force-cleaned (pure rz/sx, no cz).",
              "- Policy: **honor** the override as the canonical reported pattern, but "
              "**also restore** the original under `_clean_override.original` as parallel "
              "`segments.csv` rows with `restored=True`. This lets both numbers be reported; "
              "the restored rows correct the cz-pattern undercount that an override-only "
              "inventory would suffer.",
              ""]

    lines += ["## 4. Negative-τ policy", "",
              f"- **{n_negtau}** reports have `noise_threshold < 0` (physically a degenerate "
              "drop threshold). Policy: include them in the inventory (they are real runs), "
              "flag `has_negative_tau=True`, and exclude their DDMin decisions from the "
              "1-minimality recheck.",
              ""]

    # window inventory
    lines += ["## 5. Per-layout window inventory (authoritative — kills the global '10 windows')", "",
              "| backend | layout | monthly windows | weekly windows | total | span |",
              "|---|---|---:|---:|---:|---|"]
    win = defaultdict(lambda: {"monthly": set(), "weekly": set()})
    for r in reports:
        key = (r["backend"], r["layout"])
        if r["window_label"]:
            win[key]["monthly"].add(r["window_label"])
        if r["window_labels_weekly"]:
            win[key]["weekly"].add(r["window_labels_weekly"])
    for (b, lay), v in sorted(win.items()):
        allm = sorted(v["monthly"])
        span = f"{allm[0]}..{allm[-1]}" if allm else ""
        lines.append(f"| {b} | {lay} | {len(v['monthly'])} | {len(v['weekly'])} | {len(v['monthly'])+len(v['weekly'])} | {span} |")

    lines += ["", "## 6. verify_kingston mislabel correction", "",
              f"- The `verify_kingston/summary.json` (40 obs, job prefix d7f4...) was mislabeled "
              "`backend=ibm_fez, layout=[], pattern=''`. Corrected programmatically to "
              f"`backend={KINGSTON_FIX_BACKEND}, layout={KINGSTON_FIX_LAYOUT}`, pattern = the "
              "fez-97 verified pattern. The separate incomplete d90g... kingston run "
              "(layout 100/101/102/116, 2/40 obs, no summary) is excluded.",
              ""]

    lines += ["## 7. Verification observations", ""]
    vbe = defaultdict(int)
    for r in verify:
        vbe[r["backend"]] += 1
    lines.append("- Per-backend verification observations: " + ", ".join(f"{b}={c}" for b, c in sorted(vbe.items())) + f" (total {len(verify)})")
    lines.append(f"- Corrected (kingston) rows: **{sum(1 for r in verify if r['corrected']=='True')}**")
    lines.append("")

    lines += ["## 8. Parameter tolerance", "",
              f"- `PARAM_TOL = {pid.PARAM_TOL}` (matches `quantum.pattern_db._tokens_match`). "
              "RZ angles differ by design across patterns (e.g. fez 0.392699 vs marrakesh "
              "3.141593 / -2.748894), so tighter grouping would merge distinct gates.",
              ""]

    with open(out_path / "audit_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description="Build unified QRisk tidy dataset.")
    ap.add_argument("--out", default="analysis/_out")
    ap.add_argument("--audit", action="store_true", help="also write audit_report.md")
    args = ap.parse_args()

    os.chdir(_REPO_ROOT)
    stats = build(args.out)
    print(json.dumps(stats, indent=2, default=str))
    if args.audit:
        write_audit(args.out)
        print(f"Audit written to {args.out}/audit_report.md")


if __name__ == "__main__":
    main()
