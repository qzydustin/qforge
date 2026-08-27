#!/usr/bin/env python3
"""
Python Random Code Mutation Engine - Core Test Suite

This test file contains unit tests for the core functionality, ensuring all mutation operators and validation features work properly.

Run:
    python -m pytest tests/test_core.py -v
    or
    python tests/test_core.py

Author: Zi Yang
"""

import unittest
import sys
import ast
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from random_mutator import (
    mutate_code, smart_mutate_code, analyze_code_complexity,
    ArithmeticOperatorMutator, VariableRenameMutator,
    StatementDeletionMutator, BooleanConditionFlipMutator,
    LoopBoundaryMutator, FunctionCallParameterMutator,
    DataStructureMutator, CodeValidator, MutationContext
)


class TestBasicMutation(unittest.TestCase):
    """Basic mutation functionality tests."""
    
    def setUp(self):
        """Prepare fixtures for tests."""
        self.simple_code = """
def add(a, b):
    return a + b

def main():
    result = add(3, 4)
    print(result)
"""
        
    def test_basic_mutation_without_validation(self):
        """Test basic mutation (validation disabled)."""
        mutated_code, mutations = mutate_code(
            self.simple_code,
            steps=2,
            seed=42,
            validate=False
        )
        
        self.assertIsInstance(mutated_code, str)
        self.assertIsInstance(mutations, list)
        self.assertGreaterEqual(len(mutations), 0)  # May be 0 if no applicable mutations
        
    def test_basic_mutation_with_validation(self):
        """Test basic mutation (validation enabled)."""
        mutated_code, mutations = mutate_code(
            self.simple_code,
            steps=3,
            seed=42,
            validate=True
        )
        
        self.assertIsInstance(mutated_code, str)
        self.assertIsInstance(mutations, list)
        
        # Validate syntax of mutated code
        try:
            ast.parse(mutated_code)
        except SyntaxError:
            self.fail("Mutated code has syntax errors")
    
    def test_reproducibility(self):
        """Test reproducibility with a fixed seed."""
        seed = 12345
        
        # First run
        mutated1, mutations1 = mutate_code(
            self.simple_code,
            steps=3,
            seed=seed,
            validate=True
        )
        
        # Second run
        mutated2, mutations2 = mutate_code(
            self.simple_code,
            steps=3,
            seed=seed,
            validate=True
        )
        
        # Results should match exactly
        self.assertEqual(mutated1, mutated2)
        self.assertEqual(len(mutations1), len(mutations2))
        
        for m1, m2 in zip(mutations1, mutations2):
            self.assertEqual(m1['operator'], m2['operator'])


class TestMutationOperators(unittest.TestCase):
    """Mutation operator tests."""
    
    def setUp(self):
        """Prepare mutation context for tests."""
        self.ctx = MutationContext(seed=42)
    
    def test_arithmetic_operator_mutator(self):
        """Test arithmetic operator mutation."""
        code = "result = a + b * c"
        tree = ast.parse(code)
        
        mutator = ArithmeticOperatorMutator()
        can_apply = mutator.can_apply(tree)
        self.assertTrue(can_apply)
        
        # Apply mutation
        success = mutator.apply(tree, self.ctx)
        self.assertTrue(success)
        
        # Check mutation record
        self.assertEqual(len(self.ctx.applied_mutations), 1)
        self.assertEqual(self.ctx.applied_mutations[0]['operator'], 'ArithmeticOperatorMutator')
    
    def test_variable_rename_mutator(self):
        """Test variable renaming mutator (function-scope consistency)."""
        code = """
def foo(x):
    y = x + 5
    if y > 10:
        y = y - 1
    return y
"""
        tree = ast.parse(code)
        
        mutator = VariableRenameMutator()
        can_apply = mutator.can_apply(tree)
        self.assertTrue(can_apply)
        
        # Apply mutation
        success = mutator.apply(tree, self.ctx)
        self.assertTrue(success)
        
        # Check mutation record
        mutations = [m for m in self.ctx.applied_mutations if m['operator'] == 'VariableRenameMutator']
        self.assertGreater(len(mutations), 0)
    
    def test_boolean_condition_flip_mutator(self):
        """Test boolean condition flip mutator."""
        code = """
if x > 0 and y > 0:
    print("positive")
"""
        tree = ast.parse(code)
        
        mutator = BooleanConditionFlipMutator()
        can_apply = mutator.can_apply(tree)
        self.assertTrue(can_apply)
        
        # Apply mutation
        success = mutator.apply(tree, self.ctx)
        self.assertTrue(success)
    
    def test_loop_boundary_mutator(self):
        """Test loop boundary mutation."""
        code = """
for i in range(10):
    print(i)
"""
        tree = ast.parse(code)
        
        mutator = LoopBoundaryMutator()
        can_apply = mutator.can_apply(tree)
        self.assertTrue(can_apply)
        
        # Apply mutation
        success = mutator.apply(tree, self.ctx)
        self.assertTrue(success)
    
    def test_data_structure_mutator(self):
        """Test data structure mutation."""
        code = """
my_list = [1, 2, 3]
my_tuple = (4, 5, 6)
my_dict = {"a": 1, "b": 2}
"""
        tree = ast.parse(code)
        
        mutator = DataStructureMutator()
        can_apply = mutator.can_apply(tree)
        self.assertTrue(can_apply)
        
        # Apply mutation
        success = mutator.apply(tree, self.ctx)
        self.assertTrue(success)


class TestCodeValidation(unittest.TestCase):
    """Code validation tests."""
    
    def test_syntax_validation_valid_code(self):
        """Test syntax validation - valid code."""
        valid_code = """
def hello():
    print("Hello, World!")
    return True
"""
        
        is_valid, error = CodeValidator.validate_syntax(valid_code)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_syntax_validation_invalid_code(self):
        """Test syntax validation - invalid code."""
        invalid_code = """
def hello(:
    print("Hello, World!")
    return True
"""
        
        is_valid, error = CodeValidator.validate_syntax(invalid_code)
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_semantic_validation_valid_code(self):
        """Test semantic validation - valid code."""
        valid_code = """
def calculate(x):
    result = x * 2
    return result

y = 5
output = calculate(y)
print(output)
"""
        
        is_valid, errors = CodeValidator.validate_semantics(valid_code)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_semantic_validation_undefined_variable(self):
        """Test semantic validation - undefined variable."""
        invalid_code = """
def calculate(x):
    result = x * 2
    return result

output = calculate(undefined_var)  # undefined_var is undefined
print(output)
"""
        
        is_valid, errors = CodeValidator.validate_semantics(invalid_code)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Check error message contains the undefined variable
        error_text = ' '.join(errors)
        self.assertIn('undefined_var', error_text)


class TestSmartMutation(unittest.TestCase):
    """Smart mutation strategy tests."""
    
    def test_smart_mutation(self):
        """Test smart mutation functionality."""
        complex_code = """
def fibonacci(n):
    if n <= 1:
        return n
    
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    
    return b

def main():
    result = fibonacci(10)
    print(f"Fibonacci(10) = {result}")
"""
        
        mutated_code, mutations = smart_mutate_code(
            complex_code,
            steps=3,
            seed=789,
            validate=True
        )
        
        self.assertIsInstance(mutated_code, str)
        self.assertIsInstance(mutations, list)
        
        # Validate syntax of mutated code
        try:
            ast.parse(mutated_code)
        except SyntaxError:
            self.fail("Smart mutation produced code with syntax errors")


class TestCodeAnalysis(unittest.TestCase):
    """Code analysis tests."""
    
    def test_analyze_code_complexity(self):
        """Test code complexity analysis."""
        code = """
class Calculator:
    def __init__(self):
        self.value = 0
    
    def add(self, x):
        self.value += x
        return self.value
    
    def multiply(self, x):
        self.value *= x
        return self.value

def main():
    calc = Calculator()
    
    for i in range(5):
        calc.add(i)
    
    if calc.value > 10:
        calc.multiply(2)
    
    return calc.value
"""
        
        stats = analyze_code_complexity(code)
        
        self.assertIsInstance(stats, dict)
        
        # Check required statistics exist
        required_keys = ['statements', 'functions', 'classes', 'variables', 
                        'operators', 'loops', 'conditionals']
        
        for key in required_keys:
            self.assertIn(key, stats)
            self.assertIsInstance(stats[key], int)
            self.assertGreaterEqual(stats[key], 0)
        
        # Validate reasonable ranges
        self.assertGreater(stats['statements'], 0)
        self.assertGreater(stats['functions'], 0)
        self.assertGreater(stats['classes'], 0)


class TestEdgeCases(unittest.TestCase):
    """Edge case tests."""
    
    def test_empty_code(self):
        """Test empty code handling."""
        empty_code = ""
        
        # Should handle empty code without crashing
        mutated_code, mutations = mutate_code(
            empty_code,
            steps=1,
            validate=True
        )
        
        self.assertEqual(mutated_code, empty_code)
        self.assertEqual(len(mutations), 0)
    
    def test_single_statement(self):
        """Test single-statement code."""
        single_statement = "x = 42"
        
        mutated_code, mutations = mutate_code(
            single_statement,
            steps=1,
            seed=123,
            validate=True
        )
        
        self.assertIsInstance(mutated_code, str)
        self.assertIsInstance(mutations, list)
    
    def test_complex_nested_code(self):
        """Test complex nested code."""
        complex_code = """
def outer_function(x):
    def inner_function(y):
        if y > 0:
            for i in range(y):
                if i % 2 == 0:
                    yield i * 2
                else:
                    yield i + 1
        else:
            return []
    
    results = list(inner_function(x))
    
    class ResultProcessor:
        def __init__(self, data):
            self.data = data
        
        def process(self):
            return [item for item in self.data if item > 5]
    
    processor = ResultProcessor(results)
    return processor.process()
"""
        
        # Should handle complex code
        mutated_code, mutations = mutate_code(
            complex_code,
            steps=3,
            seed=456,
            validate=True
        )
        
        self.assertIsInstance(mutated_code, str)
        
        # Validate syntax
        try:
            ast.parse(mutated_code)
        except SyntaxError:
            self.fail("Complex code mutation produced syntax errors")


class TestValidationComparison(unittest.TestCase):
    """Validation mode comparison tests."""
    
    def test_validation_effectiveness(self):
        """Test the effectiveness of validation mode."""
        test_code = """
def calculate_area(radius):
    pi = 3.14159
    area = pi * radius * radius
    return area

def main():
    r = 5
    result = calculate_area(r)
    if result > 50:
        print("Large circle")
    else:
        print("Small circle")
"""
        
        # Mutation without validation
        mutated_unvalidated, mutations_unvalidated = mutate_code(
            test_code,
            steps=5,
            seed=999,
            validate=False
        )
        
        # Mutation with validation
        mutated_validated, mutations_validated = mutate_code(
            test_code,
            steps=5,
            seed=999,
            validate=True
        )
        
        # Validation mode should produce syntactically valid code
        try:
            ast.parse(mutated_validated)
        except SyntaxError:
            self.fail("Validation mode produced code with syntax errors")
        
        # Log test results
        print(f"Unvalidated mode applied {len(mutations_unvalidated)} mutations")
        print(f"Validation mode applied {len(mutations_validated)} mutations")


def run_tests():
    """Run all tests."""
    # Build test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestBasicMutation,
        TestMutationOperators,
        TestCodeValidation,
        TestSmartMutation,
        TestCodeAnalysis,
        TestEdgeCases,
        TestValidationComparison
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return status
    return result.wasSuccessful()


if __name__ == "__main__":
    print("🧪 Python Random Code Mutation Engine - Core Test Suite")
    print("=" * 60)
    
    success = run_tests()
    
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
