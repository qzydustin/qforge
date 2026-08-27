#!/usr/bin/env python3
"""
Python Random Code Mutation Engine - Basic Usage Examples

This example shows how to use the Python API to perform basic code mutation operations.

Author: Zi Yang
"""

import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from random_mutator import mutate_code, analyze_code_complexity


def basic_mutation_example():
    """Basic mutation example."""
    print("=== Basic mutation example ===")
    
    # Example code
    source_code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        if num > 0:
            total += num
    return total

def main():
    data = [1, -2, 3, 4, -5]
    result = calculate_sum(data)
    print(f"Sum of positive numbers: {result}")
"""
    
    print("Original code:")
    print(source_code)
    
    # Perform mutation
    mutated_code, mutations = mutate_code(
        source_code,
        steps=3,
        seed=42,
        validate=True
    )
    
    print(f"\nMutation result (total {len(mutations)} steps):")
    for i, mutation in enumerate(mutations, 1):
        line_info = f" (Line {mutation['line']})" if 'line' in mutation else ""
        print(f"{i}. {mutation['operator']}: {mutation['node']}{line_info}")
    
    print("\nMutated code:")
    print(mutated_code)


def code_analysis_example():
    """Code analysis example."""
    print("\n=== Code analysis example ===")
    
    # Slightly more complex code
    complex_code = """
class NumberProcessor:
    def __init__(self):
        self.processed_count = 0
    
    def process_list(self, numbers):
        result = []
        
        for i, num in enumerate(numbers):
            if num % 2 == 0:
                processed = num * 2
            else:
                processed = num + 1
            
            result.append(processed)
            self.processed_count += 1
        
        return result
    
    def get_statistics(self):
        return {"processed": self.processed_count}

def main():
    processor = NumberProcessor()
    
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    processed = processor.process_list(test_data)
    
    print("Processed result:", processed)
    print("Statistics:", processor.get_statistics())
"""
    
    print("Analyzing code:")
    print(complex_code)
    
    # Analyze code complexity
    stats = analyze_code_complexity(complex_code)
    
    print("\nComplexity analysis result:")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Suggest mutation steps based on complexity
    complexity_score = (
        stats['statements'] + 
        stats['operators'] * 2 + 
        stats['loops'] * 3 + 
        stats['conditionals'] * 2
    )
    suggested_steps = max(1, min(10, complexity_score // 5))
    
    print(f"\nSuggested number of mutation steps: {suggested_steps}")
    
    # Mutate using suggested steps
    mutated_code, mutations = mutate_code(
        complex_code,
        steps=suggested_steps,
        seed=123,
        validate=True
    )
    
    print(f"\nMutation result based on analysis (total {len(mutations)} steps):")
    for i, mutation in enumerate(mutations, 1):
        line_info = f" (Line {mutation['line']})" if 'line' in mutation else ""
        print(f"{i}. {mutation['operator']}: {mutation['node']}{line_info}")


def reproducibility_example():
    """Reproducibility example."""
    print("\n=== Reproducibility example ===")
    
    test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    for i in range(8):
        print(f"fib({i}) = {fibonacci(i)}")
"""
    
    print("Test code:")
    print(test_code)
    
    # Mutate multiple times using the same seed
    seed = 999
    print(f"\nMutating three times using seed {seed}:")
    
    for run in range(3):
        mutated_code, mutations = mutate_code(
            test_code,
            steps=2,
            seed=seed,
            validate=True
        )
        
        mutation_summary = [m['operator'] for m in mutations]
        print(f"Run {run + 1}: {' -> '.join(mutation_summary)} (total {len(mutations)} steps)")
    
    print("\nResults should be identical, demonstrating reproducibility!")


if __name__ == "__main__":
    print("🚀 Python Random Code Mutation Engine - Basic Usage Examples")
    print("=" * 60)
    
    try:
        basic_mutation_example()
        code_analysis_example()
        reproducibility_example()
        
        print("\n✅ All examples completed!")
        
    except Exception as e:
        print(f"\n❌ Examples failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
