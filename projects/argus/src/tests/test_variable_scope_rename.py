#!/usr/bin/env python3
import unittest
import ast
from pathlib import Path
import sys

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from random_mutator import VariableRenameMutator, ParamRenameMutator, MutationContext

class TestFunctionScopeVariableRename(unittest.TestCase):
    def setUp(self):
        self.ctx = MutationContext(seed=1234)

    def _get_function_by_name(self, tree, name):
        for n in ast.walk(tree):
            if isinstance(n, ast.FunctionDef) and n.name == name:
                return n
        return None

    def test_parameter_and_internal_references_are_consistently_renamed(self):
        code = """
def clamp(upper, lower, value):
    return max(lower, min(upper, value))

def score_user(age, orders, refund_rate, vip=False, region='US'):
    base = age * 0.1 + orders * (1 - refund_rate)
    if vip and region in ['US', 'EU']:
        base = base * 1.2
    user = type('U', (), {})()
    user.vip = vip  # Attribute should not be renamed
    if refund_rate > 0.5 or age < 0:
        base = base - 10
    return clamp(100, 0, base)
"""
        tree = ast.parse(code)
        mutator = ParamRenameMutator()
        self.assertTrue(mutator.can_apply(tree))

        # Locate score_user and its candidate parameter vip
        # Take the matching candidate from the list and force random.choice to return it
        candidates = mutator.candidates  # Populated by can_apply
        score_func = self._get_function_by_name(tree, 'score_user')
        target = None
        for fn, name in candidates:
            if fn is score_func and name == 'vip':
                target = (fn, name)
                break
        self.assertIsNotNone(target, 'Did not find vip parameter candidate of score_user')

        # Monkey-patch random.choice to return the specified candidate
        original_choice = self.ctx.random.choice
        try:
            self.ctx.random.choice = lambda seq: target
            success = mutator.apply(tree, self.ctx)
            self.assertTrue(success)
        finally:
            self.ctx.random.choice = original_choice

        # Assert: no ast.Name with old name vip remains inside score_user
        score_func_after = self._get_function_by_name(tree, 'score_user')
        self.assertIsNotNone(score_func_after)

        vip_name_nodes = [n for n in ast.walk(score_func_after) if isinstance(n, ast.Name) and n.id == 'vip']
        self.assertEqual(len(vip_name_nodes), 0, 'Old variable name vip should not remain inside the function')

        # Parameter has been renamed
        args_all = list(getattr(score_func_after.args, 'posonlyargs', [])) + list(score_func_after.args.args) + list(score_func_after.args.kwonlyargs)
        if score_func_after.args.vararg:
            args_all.append(score_func_after.args.vararg)
        if score_func_after.args.kwarg:
            args_all.append(score_func_after.args.kwarg)
        renamed_arg = [a.arg for a in args_all]
        self.assertTrue(any(a.startswith('mutated_vip_') for a in renamed_arg), 'vip parameter was not renamed')

        # Attribute user.vip should not be renamed
        attr_nodes = [n for n in ast.walk(score_func_after) if isinstance(n, ast.Attribute) and n.attr == 'vip']
        self.assertGreaterEqual(len(attr_nodes), 1, 'Attribute name vip should remain unchanged')

    def test_no_cross_function_rename(self):
        code = """
def a(v):
    return v + 1

def b(x):
    y = x + 2
    return y
"""
        tree = ast.parse(code)
        mutator = VariableRenameMutator()
        self.assertTrue(mutator.can_apply(tree))

        # Force renaming of variable y in function b
        candidates = mutator.candidates
        fn_b = self._get_function_by_name(tree, 'b')
        target = None
        for fn, name in candidates:
            if fn is fn_b and name == 'y':
                target = (fn, name)
                break
        self.assertIsNotNone(target)

        original_choice = self.ctx.random.choice
        try:
            self.ctx.random.choice = lambda seq: target
            self.assertTrue(mutator.apply(tree, self.ctx))
        finally:
            self.ctx.random.choice = original_choice

        # Validate: function a's parameter v should remain unchanged
        fn_a = self._get_function_by_name(tree, 'a')
        self.assertIsNotNone(fn_a)
        self.assertEqual(fn_a.args.args[0].arg, 'v')

if __name__ == '__main__':
    unittest.main(verbosity=2)
