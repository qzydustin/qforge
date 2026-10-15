#!/usr/bin/env python3
import ast
import sys
import unittest
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from random_mutator import mutate_code, ParamRenameMutator

CODE_PARAM_AND_CALL = """
# Simplified utility function
def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x

# Target function with vip parameter
def score_user(age, orders, refund_rate, vip=False, region="US"):
    base = age * 0.1 + orders * (1 - refund_rate)
    if vip and region in ("US", "EU"):
        base = base * 1.2
    if refund_rate > 0.5 or age < 0:
        base = base - 10
    return clamp(base, 0, 100)

# Calls in the same file (both keyword and positional forms)
def pipeline(numbers):
    arr = list(numbers)
    arr2 = sorted(arr)
    sc_kw = score_user(age=len(arr2) * 3, orders=int(len(arr2) or 1), refund_rate=0.1, vip=True, region="EU")
    sc_pos = score_user(30, 10, 0.2, True, "US")
    return sc_kw + sc_pos
"""

class TestParamKeywordSync(unittest.TestCase):
    def test_keyword_sync_on_param_rename(self):
        # Hitting dependencies vip/score_user triggers parameter renaming and call keyword synchronization
        mutated, logs = mutate_code(
            CODE_PARAM_AND_CALL,
            steps=1,
            seed=9527,
            custom_operators=[ParamRenameMutator()],
            priority_dependencies=["vip", "score_user"],
        )
        self.assertIsInstance(mutated, str)
        # Parameter in function definition should be renamed
        self.assertIn("def score_user(", mutated)
        self.assertIn("mutated_vip_", mutated, "Function parameter vip was not renamed")
        # Keyword in call within the same file should be synchronized
        self.assertIn("score_user(age=", mutated)
        self.assertIn("mutated_vip_", mutated, "Call keyword was not synchronized to the new name")
        # Old keyword name should not remain
        self.assertNotIn("vip=True,", mutated, "Old call keyword name still present; not synchronized")

    def test_positional_call_unchanged(self):
        mutated, logs = mutate_code(
            CODE_PARAM_AND_CALL,
            steps=1,
            seed=13579,
            custom_operators=[ParamRenameMutator()],
            priority_dependencies=["vip", "score_user"],
        )
        # Parse AST and check two calls: one keyword form, one positional form
        tree = ast.parse(mutated)
        calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "score_user"]
        self.assertEqual(len(calls), 2, "Expected two calls to score_user")
        # Keyword call should include the renamed keyword
        kw_call = next((c for c in calls if any(k.arg for k in c.keywords)), None)
        self.assertIsNotNone(kw_call, "Keyword-form call not found")
        self.assertTrue(any(k.arg and k.arg.startswith("mutated_vip_") for k in kw_call.keywords), "Keyword-form did not synchronize vip name")
        # Positional call unaffected (should not create/modify keywords)
        pos_call = next((c for c in calls if not c.keywords), None)
        self.assertIsNotNone(pos_call, "Positional call not found or incorrectly rewritten to keyword form")

    def test_case_insensitive_and_nonexistent_dep(self):
        mutated, logs = mutate_code(
            CODE_PARAM_AND_CALL,
            steps=1,
            seed=24680,
            custom_operators=[ParamRenameMutator()],
            priority_dependencies=[" ViP ", "SCORE_USER", "nonexistent"],
        )
        # Should still trigger vip rename and keyword sync
        self.assertIn("mutated_vip_", mutated)
        self.assertNotIn("vip=True,", mutated)

if __name__ == "__main__":
    unittest.main(verbosity=2)
