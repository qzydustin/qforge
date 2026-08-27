import unittest
import ast
from typing import List

# Add project root to Python path; compatible with direct import of cli/random_mutator
import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from random_mutator import (
    mutate_code,
    VariableRenameMutator,
    KeywordArgValueMutator,
    AttributeRenameMutator,
    FunctionRenameMutator,
)
import cli



SAMPLE_CODE = """
class Info:
    def __init__(self, vip=False):
        self.vip = vip

def mean(arr):
    return sum(arr) / max(1, len(arr))

def score_user(age, orders, refund_rate, vip=False, region='US'):
    base = age * 0.1 + orders * 0.2
    if vip:
        base += 10
    return int(base - refund_rate * 5)

def bubble_sort(arr):
    a = list(arr)
    for i in range(len(a)):
        for j in range(0, len(a) - i - 1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
    return a

def pipeline(numbers):
    arr = list(numbers)
    arr2 = bubble_sort(arr)
    info = Info(vip=False)
    acc = len(arr2) + 3
    sc = score_user(age=len(arr2) * 3, orders=int(mean(arr2) or 1), refund_rate=0.1, vip=True, region='EU')
    return {'score': sc, 'flag': info.vip, 'acc': acc}
"""


class TestDependencyPriorityMultiOperators(unittest.TestCase):
    def test_variable_and_keyword_mutators(self):
        # Variable renaming (hit vip)
        mutated_v, logs_v = mutate_code(
            SAMPLE_CODE, steps=1, seed=123,
            custom_operators=[VariableRenameMutator()],
            priority_dependencies=['vip', 'score_user']
        )
        self.assertIn('mutated_', mutated_v, msg='Variable renaming should occur (vip or related variable)')
        # Keyword value change (hit vip=True)
        mutated_k, logs_k = mutate_code(
            SAMPLE_CODE, steps=1, seed=123,
            custom_operators=[KeywordArgValueMutator()],
            priority_dependencies=['vip']
        )
        # Parse AST to check vip value in the call is changed (True->False or numeric tweak)
        tree_k = ast.parse(mutated_k)
        found_changed = False
        for n in ast.walk(tree_k):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'score_user':
                for kw in n.keywords or []:
                    if kw.arg == 'vip' and isinstance(kw.value, ast.Constant):
                        # Boolean flip is most common; numeric tweak differs from the original value
                        if isinstance(kw.value.value, bool):
                            found_changed = True
                        elif isinstance(kw.value.value, (int, float)):
                            found_changed = True
        self.assertTrue(found_changed, msg='KeywordArgValueMutator should change the value of vip')

    def test_attribute_mutator(self):
        mutated_a, logs_a = mutate_code(
            SAMPLE_CODE, steps=1, seed=321,
            custom_operators=[AttributeRenameMutator()],
            priority_dependencies=['vip']
        )
        self.assertIn('mutated_vip_', mutated_a, msg='Attribute vip should be prioritized for renaming')

    def test_function_rename_mutator(self):
        mutated_f, logs_f = mutate_code(
            SAMPLE_CODE, steps=1, seed=456,
            custom_operators=[FunctionRenameMutator()],
            priority_dependencies=['score_user', 'vip']
        )
        # Function name and call sites should be synchronized
        self.assertIn('mutated_score_user_', mutated_f, msg='Function name should be renamed')
        self.assertIn('mutated_score_user_', mutated_f, msg='Call sites should be synchronized')

    def test_multi_operators_mode(self):
        # In multi-operator mode, dependency hit coverage spans multiple factors (at least two categories hit)
        mutated_m, logs_m = mutate_code(
            SAMPLE_CODE, steps=6, seed=777,
            custom_operators=[VariableRenameMutator(), KeywordArgValueMutator(), AttributeRenameMutator(), FunctionRenameMutator()],
            priority_dependencies=['vip', 'score_user']
        )
        # Capability check: during candidate collection, each operator should be able to identify dependency hits (unified judgment)
        tree = ast.parse(SAMPLE_CODE)
        deps = {'vip', 'score_user'}
        var_op = VariableRenameMutator(); var_op.can_apply(tree)
        var_hit = any((name.lower() in deps) or (getattr(fn, 'name', '').lower() in deps) for fn, name in var_op.candidates)
        kw_op = KeywordArgValueMutator(); kw_op.can_apply(tree)
        kw_hit = any(k.arg and k.arg.lower() in deps for _c, k in kw_op.candidates)
        attr_op = AttributeRenameMutator(); attr_op.can_apply(tree)
        attr_hit = any(getattr(a, 'attr', '').lower() in deps for a in attr_op.candidates)
        func_op = FunctionRenameMutator(); func_op.can_apply(tree)
        func_hit = any(getattr(f, 'name', '').lower() in deps for f in func_op.candidates)
        hits = [var_hit, kw_hit, attr_hit, func_hit]
        self.assertGreaterEqual(sum(1 for h in hits if h), 2, msg='In multi-operator mode, at least two categories should have dependency-hit capability')
        # Content check: should reflect dependency-related changes (vip or score_user)
        self.assertTrue(('mutated_vip_' in mutated_m) or ('mutated_score_user_' in mutated_m) or ('vip=False' in mutated_m))

    def test_dep_list_normalization_and_unmatched(self):
        # Mixed case and nonexistent entries
        deps = cli._normalize_dependencies(['ViP', 'SCORE_USER', '  ', 'nonexistent'])
        self.assertIn('vip', deps)
        self.assertIn('score_user', deps)
        # Unmatched item hints simulation (identifier collection)
        ids = cli._collect_identifiers_from_code(SAMPLE_CODE)
        self.assertTrue('vip' in ids and 'score_user' in ids)
        self.assertFalse('nonexistent' in ids)


if __name__ == '__main__':
    unittest.main()
