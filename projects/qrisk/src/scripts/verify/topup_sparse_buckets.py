#!/usr/bin/env python3
"""Top up sparse hit buckets of the candidate groups' verify sets from archive/ directories.

For each candidate group with a variants/verify/selection_manifest.json:
  1. Identify buckets with < 30 variants.
  2. Collect the .qpy files in the bucket's archive/ directory.
  3. Dedupe by (n_swaps, seed) parsed from the qpy filename.
  4. Validate that each candidate actually scores the bucket's hit count
     (re-score against the group's auto-picked pattern, drop mismatches).
  5. Randomly sample up to (30 - current_count) extras from the pool and move
     them back to the bucket dir.
  6. If the bucket is still short, add byte-identical copies (_dupN) of its
     variants, then rewrite selection_manifest.json.

Dry run by default: prints what it would move, copy and rewrite. --apply writes.

Usage: python -m scripts.verify.topup_sparse_buckets [--apply]
"""
from __future__ import annotations

import argparse
import json
import random
import re
import shutil
from pathlib import Path

from qiskit import qpy

from scripts.verify.generate_verify_variants import auto_pick_pattern
from qrisk.paths import CANDIDATE_GROUPS_DIR, data_relative, resolve_stored
from qrisk.tokens import circuit_tokens, count_contiguous

PER_BUCKET = 30
RNG_SEED = 20260628

NAME_RE = re.compile(r"_hit(?P<hit>\d+)_sw(?P<sw>\d+)_s(?P<seed>\d+)\.qpy$")


def parse_qpy_name(p: Path) -> tuple[int, int, int] | None:
    """Return (hit, n_swaps, seed) parsed from the qpy filename, or None."""
    m = NAME_RE.search(p.name)
    if not m:
        return None
    return int(m["hit"]), int(m["sw"]), int(m["seed"])


def rescore(qpy_path: Path, pattern_tokens) -> int:
    """Load qpy, return the pattern hit count."""
    with open(qpy_path, "rb") as f:
        circ = list(qpy.load(f))[0]
    return count_contiguous(circuit_tokens(circ), pattern_tokens)


def topup_group(manifest_path: Path, rng: random.Random, apply: bool, per_bucket: int = PER_BUCKET) -> dict:
    """Top up one manifest's buckets; without ``apply`` nothing is moved, copied or written."""
    verify_dir = manifest_path.parent
    group_dir = verify_dir.parent.parent
    m = json.loads(manifest_path.read_text())
    # The manifest keeps only the :.6g display form of the pattern, so the exact
    # tokens are re-derived the way the generator picked them.
    pattern_tokens = auto_pick_pattern(group_dir)

    summary = {"group": group_dir.name, "buckets": {}}

    for bucket, items in m["selected"].items():
        bucket_dir = verify_dir / bucket
        archive_dir = bucket_dir / "archive"
        bucket_hit = int(bucket.split("_")[1])

        live_keys = {(it["n_swaps"], it["seed"]) for it in items}
        before = len(items)  # items is the manifest's list and grows below

        # Pool of candidates from archive/ — names only; we'll validate by re-scoring.
        archive_pool = []
        if archive_dir.is_dir():
            for qpy_file in archive_dir.glob("*.qpy"):
                parsed = parse_qpy_name(qpy_file)
                if parsed is None:
                    continue
                archive_pool.append((qpy_file, parsed))

        if len(items) >= per_bucket and not archive_pool:
            summary["buckets"][bucket] = {
                "before": len(items), "added": 0, "dup_added": 0,
                "final": len(items),
                "deduped_archive": 0, "archive_pool_size": 0,
                "validated_pool_size": 0,
            }
            continue

        # Dedupe archive by (n_swaps, seed) — keep the first occurrence.
        seen_keys = set(live_keys)
        unique_archive = []
        for path, (_hit, sw, sd) in archive_pool:
            if (sw, sd) in seen_keys:
                continue
            seen_keys.add((sw, sd))
            unique_archive.append(path)
        deduped = len(archive_pool) - len(unique_archive)

        # Validate hit count (re-score) and bucket-membership.
        validated = []
        for path in unique_archive:
            try:
                hits = rescore(path, pattern_tokens)
            except Exception as e:
                print(f"  [skip] {path.name}: load/score error: {e}")
                continue
            if hits != bucket_hit:
                # Mismatch — pattern score disagrees with the filename's hit bucket.
                continue
            validated.append(path)

        needed = max(0, per_bucket - len(items))
        rng.shuffle(validated)
        chosen = validated[:needed]

        # Move chosen back to bucket dir; the rest stay in archive/.
        for src in chosen:
            dst = bucket_dir / src.name
            print(f"  {bucket}: move archive/{src.name} into the bucket")
            if apply:
                shutil.move(str(src), str(dst))
            _, n_swaps, seed = parse_qpy_name(src)
            m["selected"][bucket].append({
                "variant_index": len(m["selected"][bucket]) + 1,
                "n_swaps": n_swaps,
                "seed": seed,
                "qpy_path": data_relative(dst),
                "qpy_name": src.name,
                "op_count": None,
                "total_hits": bucket_hit,
                "distinct_hits": 1 if bucket_hit > 0 else 0,
                "weighted_hits": bucket_hit * len(pattern_tokens),
                "source": "archive_topup",
            })

        # If still short, duplicate existing variants (copy with _dupN suffix)
        # until the bucket reaches PER_BUCKET. The copies are byte-identical to
        # their source, so they score the same hit count by construction.
        dup_added = 0
        if len(m["selected"][bucket]) < per_bucket:
            # Source pool for duplication = everything currently selected.
            pool_for_dup = list(m["selected"][bucket])
            if pool_for_dup:
                dup_idx = 1
                while len(m["selected"][bucket]) < per_bucket:
                    src_item = rng.choice(pool_for_dup)
                    src_name = Path(src_item["qpy_path"]).name
                    dup_name = f"{Path(src_name).stem}_dup{dup_idx}.qpy"  # e.g. ..._hit5_sw200_s1034_dup1.qpy
                    dup_path = bucket_dir / dup_name
                    print(f"  {bucket}: copy {src_name} to {dup_name}")
                    if apply:
                        src_path = resolve_stored(src_item["qpy_path"], verify_dir)
                        if src_path is None:
                            raise FileNotFoundError(f"{src_item['qpy_path']} (listed in {manifest_path})")
                        shutil.copy2(str(src_path), str(dup_path))
                    m["selected"][bucket].append({
                        "variant_index": len(m["selected"][bucket]) + 1,
                        "n_swaps": src_item["n_swaps"],
                        "seed": src_item["seed"],
                        "qpy_path": data_relative(dup_path),
                        "qpy_name": dup_name,
                        "op_count": src_item.get("op_count"),
                        "total_hits": bucket_hit,
                        "distinct_hits": 1 if bucket_hit > 0 else 0,
                        "weighted_hits": bucket_hit * len(pattern_tokens),
                        "source": f"duplicate_of:{src_name}",
                    })
                    dup_idx += 1
                    dup_added += 1

        # Re-number variant_index after appending.
        for idx, it in enumerate(m["selected"][bucket], 1):
            it["variant_index"] = idx

        summary["buckets"][bucket] = {
            "before": before,
            "added": len(chosen),
            "dup_added": dup_added,
            "final": len(m["selected"][bucket]),
            "deduped_archive": deduped,
            "archive_pool_size": len(archive_pool),
            "validated_pool_size": len(validated),
        }

    m["total_selected"] = sum(len(v) for v in m["selected"].values())
    if any(b["added"] or b["dup_added"] for b in summary["buckets"].values()):
        print(f"  rewrite {data_relative(manifest_path)}")
        if apply:
            manifest_path.write_text(json.dumps(m, indent=2))
    return summary


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true",
                    help="move, copy and rewrite the manifests (default: dry run)")
    args = ap.parse_args()

    rng = random.Random(RNG_SEED)
    for manifest_path in sorted(CANDIDATE_GROUPS_DIR.glob("*/variants/verify/selection_manifest.json")):
        print(f"\n=== {manifest_path.parents[2].name} ===")
        summary = topup_group(manifest_path, rng, args.apply)
        for bucket, info in summary["buckets"].items():
            mark = "✓" if info["final"] >= PER_BUCKET else "⚠"
            print(f"  {mark} {bucket}: before={info['before']}, "
                  f"added={info['added']}, dup={info['dup_added']}, "
                  f"final={info['final']}, "
                  f"archive_pool={info['archive_pool_size']}, "
                  f"deduped={info['deduped_archive']}, "
                  f"validated={info['validated_pool_size']}")


if __name__ == "__main__":
    main()