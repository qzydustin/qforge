#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from pathlib import Path
import unittest

ROOT = Path(__file__).parent.parent
CLI = ROOT / 'cli.py'
EXAMPLE = ROOT / 'examples' / 'score_user.py'
RESULTS = ROOT / 'results'
COVERAGE_JSON = RESULTS / 'coverage.json'
OUT_COV = RESULTS / 'out_from_cov.py'

class TestCoverageIntegration(unittest.TestCase):
    def setUp(self):
        os.makedirs(RESULTS, exist_ok=True)
        # Clean up old files
        for p in [COVERAGE_JSON, OUT_COV]:
            try:
                if Path(p).exists():
                    Path(p).unlink()
            except Exception:
                pass

    def _run_cli(self, args):
        cmd = [sys.executable, str(CLI)] + args
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            print(proc.stdout)
            print(proc.stderr)
        return proc

    def test_generate_coverage_json_with_validate(self):
        proc = self._run_cli([
            'mutate', str(EXAMPLE),
            '--steps', '20', '--validate', '--smart', '--verbose', '--coverage',
            '--output', str(RESULTS / 'out.py')
        ])
        self.assertEqual(proc.returncode, 0, 'CLI execution failed (generate coverage)')
        self.assertTrue(COVERAGE_JSON.exists(), 'Coverage file not generated')
        try:
            data = json.loads(COVERAGE_JSON.read_text(encoding='utf-8'))
        except Exception as e:
            self.fail(f'Coverage JSON parsing failed: {e}')
        abs_path = str(EXAMPLE.resolve())
        self.assertIn('files', data)
        self.assertIn(abs_path, data['files'])
        executed = data['files'][abs_path].get('executed_lines', [])
        self.assertIsInstance(executed, list)

    def test_consume_coverage_json_in_smart_mode(self):
        # If previous test did not generate coverage, generate it first
        if not COVERAGE_JSON.exists():
            _ = self._run_cli([
                'mutate', str(EXAMPLE),
                '--steps', '10', '--validate', '--smart', '--coverage',
                '--output', str(RESULTS / 'out_tmp.py')
            ])
        proc = self._run_cli([
            'mutate', str(EXAMPLE),
            '--steps', '20', '--validate', '--smart', '--verbose',
            '--coverage-file', str(COVERAGE_JSON),
            '--output', str(OUT_COV)
        ])
        self.assertEqual(proc.returncode, 0, 'CLI execution failed (consume coverage)')
        self.assertTrue(OUT_COV.exists(), 'Coverage-guided output file not generated')

if __name__ == '__main__':
    unittest.main(verbosity=2)
