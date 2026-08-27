#!/usr/bin/env python3
import unittest
import sys
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from random_mutator import (
    mutate_code,
    KeywordArgValueMutator,
    AttributeRenameMutator,
    FunctionRenameMutator,
    ParamRenameMutator,
)


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

def pipeline(numbers):
    arr = list(numbers)
    arr2 = sorted(arr)
    info = Info(vip=False)
    acc = len(arr2) + 3
    sc = score_user(age=len(arr2) * 3, orders=int(mean(arr2) or 1), refund_rate=0.1, vip=True, region='EU')
    tmp = acc + len(arr)  # Local variable; if VariableRenameMutator is applied, it will be renamed
    return {'score': sc, 'flag': info.vip, 'acc': acc, 'tmp': tmp}
"""


class TestNoVariableWhenNotEnabled(unittest.TestCase):
    def test_no_variable_rename_when_only_function_keyword_attribute(self):
        # Enable only keyword/attribute/function (function includes ParamRenameMutator and FunctionRenameMutator); do not enable variable.
        mutated, logs = mutate_code(
            SAMPLE_CODE,
            steps=6,
            seed=20251010,
            custom_operators=[
                KeywordArgValueMutator(),
                AttributeRenameMutator(),
                FunctionRenameMutator(),
                ParamRenameMutator(),
            ],
            priority_dependencies=['vip', 'score_user']
        )
        # Should not contain VariableRenameMutator records
        self.assertFalse(any(m.get('operator') == 'VariableRenameMutator' for m in logs),
                         'VariableRenameMutator should not be selected when variable operator is not enabled')
        # At least one record from the enabled set should appear
        enabled_ops = {'KeywordArgValueMutator', 'AttributeRenameMutator', 'FunctionRenameMutator', 'ParamRenameMutator'}
        self.assertTrue(any(m.get('operator') in enabled_ops for m in logs), 'At least one operator from the enabled set should be selected')


if __name__ == '__main__':
    unittest.main(verbosity=2)
