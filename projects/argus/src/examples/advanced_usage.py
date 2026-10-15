#!/usr/bin/env python3
"""
Python Random Code Mutation Engine - Advanced Usage Examples

This example demonstrates smart mutation strategies, custom operators, and advanced features.

Author: Zi Yang
"""

import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from random_mutator import (
    mutate_code, smart_mutate_code, MutationOperator, MutationContext,
    ArithmeticOperatorMutator, BooleanConditionFlipMutator,
    LoopBoundaryMutator, DataStructureMutator
)
import ast


class CustomStringMutator(MutationOperator):
    """Example custom mutator that modifies string constants."""
    
    def __init__(self):
        super().__init__("CustomStringMutator")
        self.target_nodes = []
    
    def can_apply(self, tree: ast.AST) -> bool:
        """Check whether there are strings to mutate."""
        self.target_nodes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                self.target_nodes.append(node)
        return len(self.target_nodes) > 0
    
    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        """Mutate string content by adding a prefix."""
        if not self.can_apply(tree):
            return False
        
        target_node = ctx.random.choice(self.target_nodes)
        old_value = target_node.value
        
        # Simple string mutation: add prefix
        new_value = f"mutated_{old_value}"
        target_node.value = new_value
        
        # Record mutation
        line_number = getattr(target_node, 'lineno', None)
        ctx.record_mutation(
            self.name,
            f"Line {line_number or 'unknown'}: String mutation '{old_value}' -> '{new_value}'",
            line_number
        )
        
        return True


def smart_mutation_example():
    """Smart mutation strategy example."""
    print("=== Smart mutation strategy example ===")
    
    # Code containing multiple syntax constructs
    complex_code = """
def process_data(data_list, threshold=10):
    results = {}
    
    for i, item in enumerate(data_list):
        if item > threshold:
            # Handle values greater than threshold
            processed = item * 2
            results[f"item_{i}"] = processed
        elif item == 0:
            # Handle zero values
            results[f"zero_{i}"] = "special"
        else:
            # Handle values less than threshold
            processed = abs(item) + 1
            results[f"small_{i}"] = processed
    
    return results

def analyze_results(results_dict):
    total_items = len(results_dict)
    
    numeric_values = []
    for key, value in results_dict.items():
        if isinstance(value, (int, float)):
            numeric_values.append(value)
    
    if numeric_values:
        avg_value = sum(numeric_values) / len(numeric_values)
        return {
            "total": total_items,
            "numeric_count": len(numeric_values),
            "average": avg_value
        }
    else:
        return {"total": total_items, "numeric_count": 0}

def main():
    test_data = [-5, 0, 3, 15, -2, 20, 0, 8]
    
    # Process data
    results = process_data(test_data, threshold=10)
    print("Processing result:", results)
    
    # Analyze results
    analysis = analyze_results(results)
    print("Analysis result:", analysis)
"""
    
    print("Complex example code:")
    print(complex_code)
    
    # Smart mutation
    print("\nPerforming smart mutation...")
    mutated_code, mutations = smart_mutate_code(
        complex_code,
        steps=5,
        seed=456,
        validate=True
    )
    
    print(f"\nSmart mutation result (total {len(mutations)} steps):")
    for i, mutation in enumerate(mutations, 1):
        line_info = f" (Line {mutation['line']})" if 'line' in mutation else ""
        print(f"{i}. {mutation['operator']}: {mutation['node']}{line_info}")
    
    print("\nCode after smart mutation:")
    print(mutated_code)


def custom_operators_example():
    """Custom operator combination example."""
    print("\n=== Custom operator combination example ===")
    
    # Test code
    test_code = """
def greet_user(name, greeting="Hello"):
    message = f"{greeting}, {name}!"
    print(message)
    return len(message)

def calculate_stats(numbers):
    if not numbers:
        return {"count": 0, "sum": 0, "avg": 0}
    
    total = sum(numbers)
    count = len(numbers)
    average = total / count
    
    return {
        "count": count,
        "sum": total,
        "avg": average
    }

def main():
    greet_user("Alice")
    greet_user("Bob", "Hi")
    
    data = [1, 2, 3, 4, 5]
    stats = calculate_stats(data)
    print("Statistics:", stats)
"""
    
    print("Test code:")
    print(test_code)
    
    # Create custom operator combination
    custom_operators = [
        ArithmeticOperatorMutator(),
        BooleanConditionFlipMutator(),
        DataStructureMutator(),
        CustomStringMutator()  # Our custom mutator
    ]
    
    print(f"\nMutating with {len(custom_operators)} custom operators...")
    
    mutated_code, mutations = mutate_code(
        test_code,
        steps=4,
        seed=789,
        custom_operators=custom_operators,
        validate=True
    )
    
    print(f"\nCustom operators mutation result (total {len(mutations)} steps):")
    for i, mutation in enumerate(mutations, 1):
        line_info = f" (Line {mutation['line']})" if 'line' in mutation else ""
        print(f"{i}. {mutation['operator']}: {mutation['node']}{line_info}")
    
    print("\nMutated code:")
    print(mutated_code)


def specific_operators_example():
    """Demonstration of specific operators."""
    print("\n=== Specific operator effects demo ===")
    
    # Test cases for different operators
    test_cases = [
        {
            "name": "Loop boundary mutation",
            "code": """
def sum_numbers(n):
    total = 0
    for i in range(n):
        total += i
    return total

def print_countdown(start):
    while start > 0:
        print(f"Countdown: {start}")
        start -= 1
""",
            "operators": [LoopBoundaryMutator()]
        },
        {
            "name": "Data structure mutation",
            "code": """
def create_data_structures():
    my_list = [1, 2, 3, 4]
    my_tuple = (5, 6, 7, 8)
    my_dict = {"a": 10, "b": 20, "c": 30}
    my_set = {100, 200, 300}
    
    return my_list, my_tuple, my_dict, my_set
""",
            "operators": [DataStructureMutator()]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("Original code:")
        print(test_case['code'])
        
        mutated_code, mutations = mutate_code(
            test_case['code'],
            steps=2,
            seed=100 + i,
            custom_operators=test_case['operators'],
            validate=True
        )
        
        print(f"\nMutation result (total {len(mutations)} steps):")
        for j, mutation in enumerate(mutations, 1):
            line_info = f" (Line {mutation['line']})" if 'line' in mutation else ""
            print(f"  {j}. {mutation['node']}{line_info}")
        
        print("\nMutated code:")
        print(mutated_code)


def validation_modes_comparison():
    """Validation mode comparison example."""
    print("\n=== Validation modes comparison ===")
    
    # Code that may trigger issues
    risky_code = """
def process_item(item):
    if item is not None:
        result = item.upper()
        return result
    return ""

def main():
    items = ["hello", "world", None, "test"]
    
    for item in items:
        processed = process_item(item)
        if processed:
            print(f"Processed result: {processed}")
"""
    
    print("Test code:")
    print(risky_code)
    
    # Without validation
    print("\n1. Validation disabled:")
    try:
        mutated_unvalidated, mutations_unvalidated = mutate_code(
            risky_code,
            steps=6,
            seed=999,
            validate=False
        )
        
        print(f"Applied {len(mutations_unvalidated)} mutations")
        print("Note: may include invalid mutations")
        
        # Syntax check
        try:
            ast.parse(mutated_unvalidated)
            print("✓ Syntax check passed")
        except SyntaxError as e:
            print(f"✗ Syntax error: {e}")
            
    except Exception as e:
        print(f"Mutation failed: {e}")
    
    # With validation
    print("\n2. Validation enabled:")
    try:
        mutated_validated, mutations_validated = mutate_code(
            risky_code,
            steps=6,
            seed=999,  # same seed
            validate=True
        )
        
        print(f"Applied {len(mutations_validated)} mutations")
        print("✓ All mutations validated")
        
        # Show mutation records under validation mode
        print("\nMutation records under validation mode:")
        for i, mutation in enumerate(mutations_validated, 1):
            line_info = f" (Line {mutation['line']})" if 'line' in mutation else ""
            print(f"  {i}. {mutation['operator']}: {mutation['node']}{line_info}")
            
    except Exception as e:
        print(f"Mutation under validation failed: {e}")


def batch_mutation_simulation():
    """Batch mutation simulation example."""
    print("\n=== Batch mutation simulation example ===")
    
    base_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    
    print("Base code:")
    print(base_code)
    
    print("\nGenerating multiple mutated versions:")
    
    # Generate multiple mutated variants
    variants = []
    for i in range(5):
        mutated_code, mutations = mutate_code(
            base_code,
            steps=2,
            seed=i * 111,  # different seeds
            validate=True
        )
        
        variants.append({
            'seed': i * 111,
            'mutations': len(mutations),
            'operators': [m['operator'] for m in mutations]
        })
        
        print(f"Mutation version {i+1} (seed: {i * 111}):")
        print(f"  Mutation steps: {len(mutations)}")
        print(f"  Operators used: {' -> '.join([m['operator'] for m in mutations])}")
    
    print(f"\nGenerated {len(variants)} different mutation versions in total")


if __name__ == "__main__":
    print("🚀 Python Random Code Mutation Engine - Advanced Usage Examples")
    print("=" * 60)
    
    try:
        smart_mutation_example()
        custom_operators_example()
        specific_operators_example()
        validation_modes_comparison()
        batch_mutation_simulation()
        
        print("\n✅ All advanced examples completed!")
        
        print("\n🎯 Advanced features summary:")
        print("• Smart mutation strategy - combines coverage-guided and semantic-aware")
        print("• Custom mutation operators - extend system capabilities")
        print("• Specific operator combinations - targeted mutations")
        print("• Validation modes comparison - ensure code quality")
        print("• Batch mutation processing - produce diverse test cases")
        
    except Exception as e:
        print(f"\n❌ Advanced examples failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
