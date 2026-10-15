"""IBM Quantum account and execution settings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from qrisk.paths import CONFIG_EXAMPLE, CONFIG_FILE


def load_config(path: str | Path | None = None, *, backend: Optional[str] = None,
                example: bool = False) -> Dict[str, Any]:
    """Read the config file (default CONFIG_FILE).

    ``example=True`` reads CONFIG_EXAMPLE instead, so offline runs never open
    the file that holds the tokens. ``backend`` replaces ibm_quantum.backend
    in the returned dict; the file is not modified.
    """
    path = Path(CONFIG_EXAMPLE if example else (path or CONFIG_FILE))
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}. Copy {CONFIG_EXAMPLE.name} "
                                f"to {CONFIG_FILE.name} and add your token.")
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"{path} is not valid JSON (line {e.lineno}, column {e.colno}): {e.msg}. "
                         f"Check for a missing quote/comma or a line break inside a value.") from None
    if backend:
        cfg["ibm_quantum"]["backend"] = backend
    return cfg
