#!/usr/bin/env python3
"""
CoverageManager: Lightweight coverage management utility.

Responsibilities:
- Start/stop coverage sessions
- Run a specified input file under coverage
- Export a unified JSON format:
  {
    "files": {
      "<canonical_abs_path>": {
        "executed_lines": [int, ...],
        "missing_lines": [int, ...],
        "summary": {"percent": float}
      }
    }
  }

Design notes:
- Do NOT rely on Coverage(include=[abs_path]) because path canonicalization and
  runtime import mechanics can cause the file to be excluded unexpectedly.
- Instead, measure everything in the short run, then filter by file path when
  extracting/analyzing.
"""
from __future__ import annotations

import json
import os
import runpy
import sys
from typing import Any, Dict, Optional, Tuple


class CoverageManager:
    def __init__(self):
        self._cov = None
        self._available = self._check_available()

    @staticmethod
    def _check_available() -> bool:
        try:
            import coverage  # type: ignore
            return True
        except Exception:
            return False

    def is_available(self) -> bool:
        return self._available

    @staticmethod
    def _canon_path(path: str) -> str:
        """Return a canonical absolute path used consistently across the pipeline."""
        return os.path.realpath(os.path.abspath(path))

    def start(self, include_path: Optional[str] = None):
        """Start a coverage session.

        IMPORTANT:
        We intentionally do NOT pass `include=[...]` here. The include filter is strict
        and can easily exclude the target file due to path normalization differences.
        We measure everything in this short run and filter later when extracting.
        """
        if not self._available:
            return None

        import coverage  # type: ignore

        # Measure everything. We'll filter by file path later.
        self._cov = coverage.Coverage(data_file=None)
        self._cov.start()
        return self._cov

    def run_file(self, input_file: str) -> Optional[str]:
        """Run the specified Python file inside the active coverage session.

        We mimic `python file.py` behavior by:
        - setting CWD to the script directory
        - setting sys.path[0] to the script directory
        - setting sys.argv like a real script run

        IMPORTANT:
        - DO NOT pop sys.modules["__main__"] here.
          When the CLI itself is executed via `python -m ...`, removing __main__
          can break runpy's internal save/restore logic and raise KeyError('__main__').

        Returns:
            None if the run finished (or SystemExit), otherwise an error string.
        """
        if not self._cov:
            return "coverage-not-started"

        abs_path = self._canon_path(input_file)
        script_dir = os.path.dirname(abs_path)

        old_cwd = os.getcwd()
        old_sys_path = list(sys.path)
        old_argv = list(sys.argv)
        old_main = sys.modules.get("__main__")  # keep a handle just in case

        try:
            os.chdir(script_dir)

            # Ensure sys.path[0] points to the script directory
            if sys.path:
                sys.path[0] = script_dir
            else:
                sys.path.insert(0, script_dir)

            # Mimic argv
            sys.argv = [abs_path]

            # Run as "__main__" so that `if __name__ == "__main__":` executes.
            runpy.run_path(abs_path, run_name="__main__")
            return None

        except SystemExit:
            return None

        except Exception as e:
            return f"{type(e).__name__}: {e}"

        finally:
            # Restore environment
            try:
                os.chdir(old_cwd)
            except Exception:
                pass
            sys.path[:] = old_sys_path
            sys.argv[:] = old_argv

            # Safety: if __main__ disappeared, restore it
            if "__main__" not in sys.modules and old_main is not None:
                sys.modules["__main__"] = old_main

    def stop_and_analyze(self, input_file: str) -> Dict[str, Any]:
        """Stop coverage and analyze the specified file, returning standardized JSON data.

        Primary source of executed lines:
            coverage_data.lines(file)  (raw executed lines, most reliable)
        Secondary source:
            analysis2(file)            (missing lines + statement list)
        """
        if not self._cov:
            return {"files": {}}

        abs_path = self._canon_path(input_file)

        self._cov.stop()
        try:
            # Finalize internal data so get_data() is usable.
            self._cov.save()
        except Exception:
            pass

        executed_lines = []
        missing_lines = []
        percent = 0.0

        # 1) Raw executed lines from collected data (most reliable)
        try:
            data = self._cov.get_data()
            executed_lines = sorted(list(data.lines(abs_path) or []))
        except Exception:
            executed_lines = []

        # 2) Best-effort statement list + missing lines from analysis2()
        try:
            _filename, statements, _excluded, missing, _executed_stmt = self._cov.analysis2(abs_path)
            total = len(statements) if statements else 0
            exec_count = len(executed_lines) if executed_lines else 0
            percent = (exec_count / total * 100.0) if total > 0 else 0.0
            missing_lines = sorted(list(missing or []))
        except Exception:
            # If analysis2 fails, still return raw executed lines; percent may be unknown.
            percent = 0.0
            missing_lines = []

        return {
            "files": {
                abs_path: {
                    "executed_lines": executed_lines,
                    "missing_lines": missing_lines,
                    "summary": {"percent": round(percent, 2)},
                }
            }
        }

    @staticmethod
    def save_json(data: Dict[str, Any], output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_json(path: str) -> Dict[str, Any]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"files": {}}

    @staticmethod
    def extract_executed_lines(cov_json: Dict[str, Any], input_file: str) -> Optional[Tuple[str, set]]:
        """Extract executed_lines for the specified file from the coverage JSON.

        Returns:
            (canonical_abs_path, executed_set) or None
        """
        if not cov_json or "files" not in cov_json:
            return None

        abs_path = os.path.realpath(os.path.abspath(input_file))

        # Direct lookup by canonical path
        file_entry = cov_json["files"].get(abs_path)

        if not file_entry:
            # Try canonicalized-key mapping
            canon_to_original = {os.path.realpath(os.path.abspath(k)): k for k in cov_json["files"].keys()}
            original_key = canon_to_original.get(abs_path)
            if original_key:
                file_entry = cov_json["files"].get(original_key)
                abs_path = os.path.realpath(os.path.abspath(original_key))

        if not file_entry:
            # Last resort: match by basename
            fname = os.path.basename(abs_path)
            for k, v in cov_json["files"].items():
                if os.path.basename(k) == fname:
                    file_entry = v
                    abs_path = os.path.realpath(os.path.abspath(k))
                    break

        if not file_entry:
            return None

        executed_raw = file_entry.get("executed_lines", [])
        executed = set(executed_raw if isinstance(executed_raw, list) else [])
        return abs_path, executed