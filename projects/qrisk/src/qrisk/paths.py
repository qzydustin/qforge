"""Repository layout. The only module that knows where things live.

Paths written into generated files (reports.csv, summary.md, ...) are
relative to DATA_DIR, so moving the checkout never changes an output.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = REPO_ROOT / "data"
ARTIFACTS_DIR = DATA_DIR / "artifacts"                  # compile groups and the original DDMin reports
CANDIDATE_GROUPS_DIR = DATA_DIR / "candidate_groups"    # candidate groups and their verify variants
VERIFIED_DIR = DATA_DIR / "verified"                    # the two verified layouts (RQ3)
DERIVED_DIR = DATA_DIR / "derived"                      # tables and figures built by analysis/
RESULTS_DIR = DATA_DIR / "results"                      # RQ4 cross-algorithm runs

CONFIG_DIR = REPO_ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "quantum_config.json"
CONFIG_EXAMPLE = CONFIG_DIR / "quantum_config.example.json"

# Raw DDMin report roots, in the order build_dataset walks them.
REPORT_ROOTS = (ARTIFACTS_DIR, CANDIDATE_GROUPS_DIR, VERIFIED_DIR)


def data_relative(path: str | Path) -> str:
    """Path as stored in generated files: relative to DATA_DIR when inside it."""
    p = Path(path).resolve()
    try:
        return p.relative_to(DATA_DIR).as_posix()
    except ValueError:
        return p.as_posix()


def resolve_arg(path: str | Path) -> Path:
    """A command-line path: as given when it exists, else relative to DATA_DIR."""
    path = Path(path)
    return path if path.exists() else DATA_DIR / path


def resolve_stored(path: str | Path, manifest_dir: Path) -> Path | None:
    """Locate a qpy_path stored in a verify manifest.

    Manifests may store the path absolute or relative to DATA_DIR; the variant
    itself always sits in <manifest dir>/<bucket>/<file>, so that is the last
    resort.
    """
    path = Path(path)
    for candidate in (path, DATA_DIR / path, manifest_dir.joinpath(*path.parts[-2:])):
        if candidate.is_file():
            return candidate
    return None
