#!/usr/bin/env python3
"""
Python Random Code Mutation Engine - Command-Line Interface

Provides a CLI to perform code mutation operations, supporting file I/O, batch processing, and related workflows.

Usage examples:
    python cli.py mutate input.py --steps 5 --seed 42 --output mutated.py
    python cli.py analyze input.py
    python cli.py batch-mutate src/ --output mutated_src/ --steps 3

Author: Zi Yang
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional, List

from random_mutator import (
    mutate_code, analyze_code_complexity, smart_mutate_code,
    ArithmeticOperatorMutator, VariableRenameMutator,
    StatementDeletionMutator, ComparisonOperatorMutator,
    BooleanConditionFlipMutator, LoopBoundaryMutator,
    DataStructureMutator,
    FunctionRenameMutator, AttributeRenameMutator, KeywordArgValueMutator, ParamRenameMutator,
    CodeValidator
)
from utils.coverage_manager import CoverageManager


def read_file(file_path: str) -> str:
    """Read file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' does not exist")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to read file '{file_path}': {e}")
        sys.exit(1)


def write_file(file_path: str, content: str):
    """Write content to a file."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error: Failed to write file '{file_path}': {e}")
        sys.exit(1)


def _collect_coverage_if_requested(args) -> Optional[set]:
    """Collect or load coverage based on CLI arguments. Return executed_lines set or None."""
    abs_input = os.path.abspath(args.input)
    project_root = Path(__file__).resolve().parent
    default_cov_output = str(project_root / 'results' / 'coverage.json')

    executed_lines: Optional[set] = None

    # Collect coverage
    if getattr(args, 'coverage', False):
        cm = CoverageManager()
        if not cm.is_available():
            print("Notice: 'coverage' library not installed, skipping coverage collection (pip install coverage to enable).")
        else:
            try:
                cm.start(include_path=abs_input)
                # Collect execution coverage for the input file
                cm.run_file(abs_input)
                cov_json = cm.stop_and_analyze(abs_input)
                cov_output_path = args.coverage_file or default_cov_output
                CoverageManager.save_json(cov_json, cov_output_path)
                print(f"Coverage file generated: {cov_output_path}")
                extracted = CoverageManager.extract_executed_lines(cov_json, abs_input)
                if extracted:
                    _path, executed_lines = extracted
            except Exception as e:
                print(f"Coverage collection failed: {e}")

    # Load coverage JSON
    elif getattr(args, 'coverage_file', None):
        cov_json = CoverageManager.load_json(args.coverage_file)
        extracted = CoverageManager.extract_executed_lines(cov_json, abs_input)
        if extracted:
            _path, executed_lines = extracted
        else:
            print(f"Notice: No record for {abs_input} in the coverage file; smart strategy will not use coverage.")

    return executed_lines


# ===== Dependency-guided helper functions =====

def _normalize_dependencies(dep_list: Optional[List[str]]) -> List[str]:
    """Normalize dependency identifiers provided by the user (deduplicate, strip, lower)."""
    if not dep_list:
        return []
    seen = set()
    result: List[str] = []
    for d in dep_list:
        if isinstance(d, str):
            s = d.strip()
            if not s:
                continue
            norm = s.lower()
            if norm not in seen:
                seen.add(norm)
                result.append(norm)
    return result


def _collect_identifiers_from_code(source_code: str) -> set:
    """Parse source code and collect function names, class names, variable names, attribute names, and call names, used to hint unmatched dependency entries."""
    import ast
    try:
        tree = ast.parse(source_code)
    except Exception:
        return set()
    id_set = set()
    for n in ast.walk(tree):
        try:
            if isinstance(n, ast.FunctionDef):
                id_set.add(str(n.name).lower())
            elif isinstance(n, ast.ClassDef):
                id_set.add(str(n.name).lower())
            elif isinstance(n, ast.Name):
                id_set.add(str(n.id).lower())
            elif isinstance(n, ast.Attribute):
                id_set.add(str(n.attr).lower())
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
                id_set.add(str(n.func.id).lower())
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                id_set.add(str(n.func.attr).lower())
        except Exception:
            continue
    return id_set


def mutate_command(args):
    """Execute mutation command."""
    print(f"Mutating file: {args.input}")
    
    # Read source code
    source_code = read_file(args.input)
    
    # Coverage collection/consumption
    executed_lines = _collect_coverage_if_requested(args)
    coverage_data = {"executed_lines": executed_lines} if executed_lines else None

    # Create custom operator list (if specified)
    custom_operators = None
    if args.operators:
        operator_map = {
            'arithmetic': ArithmeticOperatorMutator,
            'variable': VariableRenameMutator,
            'deletion': StatementDeletionMutator,
            'comparison': ComparisonOperatorMutator,
            'boolean': BooleanConditionFlipMutator,
            'loop': LoopBoundaryMutator,
            'function': None,  # Special handling: includes both parameter renaming (ParamRenameMutator) and function name renaming
            'datastructure': DataStructureMutator,
            'keyword': KeywordArgValueMutator,
            'attribute': AttributeRenameMutator,
            'func_rename': FunctionRenameMutator
        }
        
        custom_operators = []
        for op_name in args.operators:
            if op_name in operator_map:
                if op_name == 'function':
                    # Include both parameter renaming (with keyword sync) and function name renaming operators
                    custom_operators.append(ParamRenameMutator())
                    custom_operators.append(FunctionRenameMutator())
                else:
                    ctor = operator_map[op_name]
                    if ctor is not None:
                        custom_operators.append(ctor())
            else:
                print(f"Warning: Unknown mutation operator '{op_name}'")
    
    # Dependency-guided: preprocessing and hints
    user_dep = _normalize_dependencies(getattr(args, 'dep_priority', None))
    if user_dep:
        try:
            identifiers = _collect_identifiers_from_code(source_code)
            unmatched = [d for d in user_dep if d not in identifiers]
            if unmatched:
                print(f"Notice: The following dependency-guided entries were not found in the code: {', '.join(unmatched)}. They will be handled by the default strategy.")
        except Exception:
            pass

    try:
        # Choose mutation mode
        if hasattr(args, 'smart') and args.smart:
            # Smart mutation mode (coverage-guided + semantic)
            print("Using smart mutation strategy")
            mutated_code, mutations = smart_mutate_code(
                source_code, 
                steps=args.steps, 
                seed=args.seed,
                validate=getattr(args, 'validate', False),
                coverage_data=coverage_data,
                priority_dependencies=user_dep
            )
        else:
            # Standard mutation mode
            mutated_code, mutations = mutate_code(
                source_code, 
                steps=args.steps, 
                seed=args.seed,
                custom_operators=custom_operators,
                validate=getattr(args, 'validate', False),
                use_coverage_strategy=bool(coverage_data),
                use_semantic_strategy=getattr(args, 'semantic_strategy', False),
                coverage_data=coverage_data,
                priority_dependencies=user_dep
            )
        
        # Output results
        if args.output:
            write_file(args.output, mutated_code)
            print(f"Mutated code saved to: {args.output}")
            # New: collect coverage for the mutated artifact (separate from input)
            if getattr(args, 'coverage', False):
                try:
                    cm2 = CoverageManager()
                    if cm2.is_available():
                        abs_output = os.path.abspath(args.output)
                        cm2.start(include_path=abs_output)
                        cm2.run_file(abs_output)
                        cov_json2 = cm2.stop_and_analyze(abs_output)
                        mutated_cov_output = args.coverage_file or str(Path(__file__).resolve().parent / 'results' / 'coverage_mutated.json')
                        CoverageManager.save_json(cov_json2, mutated_cov_output)
                        print(f"Coverage for mutated artifact generated: {mutated_cov_output}")
                    else:
                        print("Notice: 'coverage' library not installed, skipping coverage collection.")
                except Exception as e:
                    print(f"Coverage collection for mutated artifact failed: {e}")
        else:
            print("\nMutated code:")
            print("=" * 50)
            print(mutated_code)
        # Restricted execution validation (optional)
        if getattr(args, 'exec_check', False):
            ok, err = CodeValidator.validate_execution(mutated_code)
            if not ok:
                # Build failure report
                fail_report = {
                    'input_file': args.input,
                    'output_file': args.output,
                    'steps': args.steps,
                    'seed': args.seed,
                    'operators': args.operators,
                    'dep_priority': user_dep,
                    'mode': 'smart' if getattr(args, 'smart', False) else 'standard',
                    'error': err
                }
                # Save failure report to the same directory as output (or default results/)
                base_fail = 'results/out'
                try:
                    out_path = args.output if args.output else base_fail + '.py'
                    fail_path = str(Path(out_path).with_suffix('.fail.json'))
                    os.makedirs(os.path.dirname(fail_path), exist_ok=True)
                    with open(fail_path, 'w', encoding='utf-8') as f:
                        json.dump(fail_report, f, ensure_ascii=False, indent=2)
                    print(f"Execution validation failed; report generated: {fail_path}")
                except Exception as e2:
                    print(f"Execution validation failed, and writing report also failed: {e2}")
                sys.exit(2)
        
        # Display mutation records
        if args.verbose:
            print(f"\nMutation records (total {len(mutations)} steps):")
            print("-" * 40)
            for i, mutation in enumerate(mutations, 1):
                line_info = f" (Line {mutation['line']})" if 'line' in mutation else ""
                print(f"{i}. {mutation['operator']}: {mutation['node']}{line_info}")
        
        # Persist mutation records
        if args.log:
            log_data = {
                'input_file': args.input,
                'output_file': args.output,
                'steps': args.steps,
                'seed': args.seed,
                'operators': args.operators,
                'mutations': mutations,
                'mode': 'smart' if getattr(args, 'smart', False) else 'standard'
            }
            
            with open(args.log, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
            print(f"Mutation log saved to: {args.log}")
            
    except Exception as e:
        print(f"Mutation failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def analyze_command(args):
    """Execute analysis command."""
    print(f"Analyzing file: {args.input}")
    
    # Read source code
    source_code = read_file(args.input)
    
    try:
        # Analyze code complexity
        stats = analyze_code_complexity(source_code)
        
        if not stats:
            print("Error: Code analysis failed; possible syntax errors")
            sys.exit(1)
        
        print("\nCode complexity analysis:")
        print("=" * 30)
        print(f"Number of statements: {stats['statements']}")
        print(f"Number of functions: {stats['functions']}")
        print(f"Number of classes: {stats['classes']}")
        print(f"Number of variables: {stats['variables']}")
        print(f"Number of operators: {stats['operators']}")
        print(f"Number of loops: {stats['loops']}")
        print(f"Number of conditionals: {stats['conditionals']}")
        
        # Suggest mutation steps
        complexity_score = (
            stats['statements'] + 
            stats['operators'] * 2 + 
            stats['loops'] * 3 + 
            stats['conditionals'] * 2
        )
        
        suggested_steps = max(1, min(10, complexity_score // 5))
        print(f"\nSuggested number of mutation steps: {suggested_steps}")
        
        # Write analysis to file
        if args.output:
            analysis_data = {
                'file': args.input,
                'complexity': stats,
                'suggested_steps': suggested_steps
            }
            
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, ensure_ascii=False, indent=2)
            print(f"Analysis result saved to: {args.output}")
            
    except Exception as e:
        print(f"Analysis failed: {e}")
        sys.exit(1)


def batch_mutate_command(args):
    """Execute batch mutation command."""
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist")
        sys.exit(1)
    
    # Locate all Python files
    python_files = list(input_dir.rglob("*.py"))
    
    if not python_files:
        print(f"Warning: No Python files found in directory '{input_dir}'")
        return
    
    print(f"Found {len(python_files)} Python files; starting batch mutation...")
    
    success_count = 0
    failed_files = []
    
    for py_file in python_files:
        try:
            # Compute relative path
            rel_path = py_file.relative_to(input_dir)
            output_file = output_dir / rel_path
            
            print(f"Processing: {rel_path}")
            
            # Read source code
            source_code = read_file(str(py_file))
            
            # Dependency-guided: preprocessing (batch)
            user_dep = _normalize_dependencies(getattr(args, 'dep_priority', None))
            if user_dep:
                try:
                    identifiers = _collect_identifiers_from_code(source_code)
                    unmatched = [d for d in user_dep if d not in identifiers]
                    if unmatched:
                        print(f"  Notice: Dependency entries not present in this file: {', '.join(unmatched)}")
                except Exception:
                    pass
            
            # Perform mutation
            mutated_code, mutations = mutate_code(
                source_code, 
                steps=args.steps, 
                seed=args.seed if args.seed else None,
                validate=getattr(args, 'validate', False),
                priority_dependencies=user_dep
            )
            
            # Save mutated code
            write_file(str(output_file), mutated_code)
            
            # Save mutation log
            if args.save_logs:
                log_file = output_file.with_suffix('.mutation.json')
                log_data = {
                    'source_file': str(rel_path),
                    'steps': args.steps,
                    'seed': args.seed,
                    'mutations': mutations
                }
                
                with open(log_file, 'w', encoding='utf-8') as f:
                    json.dump(log_data, f, ensure_ascii=False, indent=2)
            
            success_count += 1
            
        except Exception as e:
            print(f"  Failed: {e}")
            failed_files.append(str(rel_path))
    
    print(f"\nBatch mutation completed:")
    print(f"Succeeded: {success_count} files")
    print(f"Failed: {len(failed_files)} files")
    
    if failed_files:
        print("\nFailed files:")
        for file in failed_files:
            print(f"  - {file}")


def list_operators_command(args):
    """List all available mutation operators."""
    print("Available mutation operators:")
    print("=" * 30)
    
    operators = [
        ("arithmetic", "ArithmeticOperatorMutator", "Arithmetic operator replacement (+, -, *, /)"),
        ("variable", "VariableRenameMutator", "Variable renaming (pure variable identifiers; excludes function parameters)"),
        ("deletion", "StatementDeletionMutator", "Statement deletion"),
        ("comparison", "ComparisonOperatorMutator", "Comparison operator replacement (==, !=, <, >)"),
        ("boolean", "BooleanConditionFlipMutator", "Condition flip (if condition -> if not condition)"),
        ("loop", "LoopBoundaryMutator", "Loop boundary modification (range(n) -> range(n±1))"),
        ("function", "ParamRenameMutator + FunctionRenameMutator", "Function-related: parameter renaming (with keyword sync) and function name renaming (synchronized calls within same file)"),
        ("keyword", "KeywordArgValueMutator", "Keyword argument value changes (boolean flip, minor numeric tweaks; dependencies can hit keyword.arg)"),
        ("attribute", "AttributeRenameMutator", "Attribute renaming (rewrite consistently by scope and base variable where possible)"),
        ("datastructure", "DataStructureMutator", "Data structure mutations (List↔Tuple, swap dict keys/values)")
    ]
    
    for short_name, class_name, description in operators:
        print(f"{short_name:15} - {description}")
        print(f"{'':15}   Class: {class_name}")
        print()
    
    print("Smart and coverage options:")
    print("=" * 30)
    print("--smart              - Enable smart mutation strategy (combines coverage-guided and semantic-aware)")
    print("--validate           - Enable code validity validation")
    print("--coverage           - Collect coverage for input file (saved to project/results/coverage.json)")
    print("--coverage-file PATH - Load (or override when generating) coverage JSON to guide smart mutation")
    print("--semantic-strategy  - Use semantic-aware strategy (in standard mode)")
    print("--dep-priority DEPS  - Dependency-guided priority (function/variable/attribute names; case-insensitive)")


def main():
    """Main entrypoint."""
    parser = argparse.ArgumentParser(
        description="Python Random Code Mutation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s mutate input.py --steps 5 --seed 42 --output mutated.py
  %(prog)s analyze input.py --output analysis.json
  %(prog)s batch-mutate src/ --output mutated_src/ --steps 3
  %(prog)s list-operators
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # mutate command
    mutate_parser = subparsers.add_parser('mutate', help='Mutate a single Python file')
    mutate_parser.add_argument('input', help='Input Python file path')
    mutate_parser.add_argument('--steps', '-s', type=int, default=3, 
                              help='Number of mutation steps (default: 3)')
    mutate_parser.add_argument('--seed', type=int, 
                              help='Random seed (for reproducibility)')
    mutate_parser.add_argument('--output', '-o', 
                              help='Output file path (prints to console if not specified)')
    mutate_parser.add_argument('--operators', nargs='+', 
                              choices=['arithmetic', 'variable', 'deletion', 'comparison', 
                                     'boolean', 'loop', 'function', 'datastructure', 'keyword', 'attribute', 'func_rename'],
                              help='Specify mutation operators to use')
    mutate_parser.add_argument('--verbose', '-v', action='store_true',
                              help='Show detailed mutation records')
    mutate_parser.add_argument('--log', help='Save mutation log to JSON file')
    
    # Advanced options
    mutate_parser.add_argument('--smart', action='store_true',
                              help='Enable smart mutation strategy (combines coverage-guided and semantic-aware)')
    mutate_parser.add_argument('--validate', action='store_true',
                              help='Enable code validity validation')
    mutate_parser.add_argument('--coverage', action='store_true',
                              help='Collect input file coverage and save JSON (default: project/results/coverage.json)')
    mutate_parser.add_argument('--coverage-file',
                              help='Coverage JSON file path (load to guide smart mutation; used as output path when combined with --coverage)')
    mutate_parser.add_argument('--semantic-strategy', action='store_true',
                              help='Use semantic-aware strategy (in standard mode)')
    mutate_parser.add_argument('--dep-priority', nargs='+',
                              help='Dependency-guided priority: pass identifiers (function/variable/attribute names) to prioritize mutation at these dependency-related locations (case-insensitive)')
    mutate_parser.add_argument('--exec-check', action='store_true',
                              help='Enable restricted execution validation; on failure, generate .fail.json and exit with code 2')
    
    # analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze Python code complexity')
    analyze_parser.add_argument('input', help='Input Python file path')
    analyze_parser.add_argument('--output', '-o', 
                               help='Output analysis results to JSON file')
    
    # batch-mutate command
    batch_parser = subparsers.add_parser('batch-mutate', help='Batch mutate Python files')
    batch_parser.add_argument('input_dir', help='Input directory path')
    batch_parser.add_argument('--output_dir', '-o', required=True,
                             help='Output directory path')
    batch_parser.add_argument('--steps', '-s', type=int, default=3,
                             help='Number of mutation steps (default: 3)')
    batch_parser.add_argument('--seed', type=int,
                             help='Random seed (for reproducibility)')
    batch_parser.add_argument('--save-logs', action='store_true',
                             help='Save mutation log for each file')
    batch_parser.add_argument('--dep-priority', nargs='+',
                             help='Dependency-guided priority: pass identifiers (function/variable/attribute names) to prioritize dependency-related locations (case-insensitive) in batch mode')
    
    # list-operators command
    list_parser = subparsers.add_parser('list-operators', help='List all available mutation operators')
    
    # Parse args
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Dispatch
    if args.command == 'mutate':
        mutate_command(args)
    elif args.command == 'analyze':
        analyze_command(args)
    elif args.command == 'batch-mutate':
        batch_mutate_command(args)
    elif args.command == 'list-operators':
        list_operators_command(args)


if __name__ == "__main__":
    main()
