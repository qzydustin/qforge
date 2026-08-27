#!/usr/bin/env python3
import os
import sys
import unittest
import subprocess
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from random_mutator import mutate_code, ParamRenameMutator


CODE_WITH_VIP = """
def clamp(upper, lower, value):
    return max(lower, min(upper, value))

def score_user(age, orders, refund_rate, vip=False, region='US'):
    base = age * 0.1 + orders * (1 - refund_rate)
    if vip and region in ['US', 'EU']:
        base = base * 1.2
    if refund_rate > 0.5 or age < 0:
        base = base - 10
    return clamp(100, 0, base)
"""


class TestDependencyPriority(unittest.TestCase):
    def test_priority_variable_rename_prefers_named_dep(self):
        # Dependency list hits vip/score_user; vip should be renamed preferentially
        mutated, logs = mutate_code(
            CODE_WITH_VIP,
            steps=1,
            seed=123,
            custom_operators=[ParamRenameMutator()],
            priority_dependencies=['vip', 'score_user']
        )
        self.assertIsInstance(mutated, str)
        self.assertIsInstance(logs, list)
        # Logs should contain a renaming entry for vip
        self.assertTrue(any('Renamed function parameter vip -> mutated_' in m.get('node', '') for m in logs),
                        'Did not observe dependency-priority vip renaming')

    def test_empty_dep_list_defaults(self):
        mutated, logs = mutate_code(
            CODE_WITH_VIP,
            steps=1,
            seed=123,
            custom_operators=[ParamRenameMutator()],
            priority_dependencies=[]
        )
        self.assertIsInstance(mutated, str)
        self.assertIsInstance(logs, list)

    def test_invalid_dep_inputs_graceful(self):
        # Mixed case and nonexistent entries should still execute; case-insensitive match should hit vip
        mutated, logs = mutate_code(
            CODE_WITH_VIP,
            steps=1,
            seed=123,
            custom_operators=[ParamRenameMutator()],
            priority_dependencies=['', 'NONEXISTENT', ' ViP ']
        )
        self.assertTrue(any('Renamed function parameter vip -> mutated_' in m.get('node', '') or 'Renamed function parameter ViP' in m.get('node', '')
                            for m in logs), 'Case-insensitive dependency matching not effective or execution failed')

    def test_cli_dep_priority_variable_rename(self):
        # Verify --dep-priority behavior via CLI
        CLI = ROOT / 'cli.py'
        EXAMPLE = ROOT / 'examples' / 'score_user.py'
        OUT = ROOT / 'results' / 'out_dep_cli.py'
        os.makedirs(OUT.parent, exist_ok=True)
        if OUT.exists():
            OUT.unlink()
        cmd = [sys.executable, str(CLI), 'mutate', str(EXAMPLE), '--steps', '1', '--operators', 'function',
               '--dep-priority', 'vip', '--output', str(OUT)]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            print(proc.stdout)
            print(proc.stderr)
        self.assertEqual(proc.returncode, 0, 'CLI execution failed')
        self.assertTrue(OUT.exists(), 'CLI output file not generated')
        content = OUT.read_text(encoding='utf-8')
        self.assertTrue(('mutated_vip_' in content) or ('mutated_score_user_' in content), 'CLI did not observe dependency-priority changes to vip or score_user')


if __name__ == '__main__':
    unittest.main(verbosity=2)
