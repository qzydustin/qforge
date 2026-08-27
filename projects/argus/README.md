> **Vendored snapshot.** Source: https://github.com/ucr-riple/Argus @ `4be9881` (fetched 2026-08-27).
> Code lives in [`src/`](src/). Run outputs (`results/`, `result/`) were removed. Original license
> retained in [`LICENSE`](LICENSE).

# Python Random Code Mutation Engine

A lightweight, extensible Python code mutation engine designed for mutation testing, robustness studies, and automated testing. Documentation and diagrams use clean, readable text with basic shapes—no external icon packs—to keep the project consistent and compliant.

## Project Overview

This project generates code mutants by applying small, controllable AST changes to source code, useful for evaluating test effectiveness and program robustness. The system adopts a modular architecture, provides multiple mutation operators and smart strategies, and balances extensibility with ease of use.

### Key Features
- Multiple operators: arithmetic operator replacement, variable renaming, statement deletion, condition flip, loop boundary tweak, function parameter modifications, data structure mutations
- Smart strategies: coverage-guided and semantic-aware, increasing the proportion of effective mutations
- Validation pipeline: syntax, semantics, and (optional) execution validation to filter invalid mutations
- Reproducibility: random seed control
- CLI and API support

## Installation

- Python 3.9+
- Recommended development/testing dependencies:

```bash
pip install -r project/requirements.txt
```

## Quick Start (CLI)

```bash
# Basic mutation
python project/cli.py mutate project/examples/score_user.py --steps 5 --validate --output project/results/out.py

# Smart mutation (coverage + semantics)
python project/cli.py mutate project/examples/score_user.py --steps 10 --smart --validate --verbose --output project/results/out_smart.py

# Specify operators
python project/cli.py mutate project/examples/score_user.py --steps 3 --operators arithmetic boolean loop --validate --output project/results/out_ops.py

# List operators
python project/cli.py list-operators
```

## Coverage-Guided Smart Mutation

The project integrates coverage collection and consumption. In smart mode, lines/functions that are actually executed are preferentially mutated, improving validation signals and reducing mutations on dead code.

- Generate coverage (recommended with --validate):

```bash
python project/cli.py mutate project/examples/score_user.py \
  --steps 20 --validate --smart --verbose --coverage \
  --output project/results/out.py
```

- Consume coverage (use an existing JSON to guide smart mutation):

```bash
python project/cli.py mutate project/examples/score_user.py \
  --steps 20 --validate --smart --verbose \
  --coverage-file project/results/coverage.json \
  --output project/results/out_from_cov.py
```

- Coverage JSON format:

```json
{
  "files": {
    "/abs/path/to/input.py": {
      "executed_lines": [12, 13, 14],
      "missing_lines": [1, 2],
      "summary": {"percent": 85.0}
    }
  }
}
```

- Parameter normalization:
  - Previously non-standard inputs like "coverageFile = xxx.py" are unified as the CLI argument "--coverage-file <path>".
  - If the coverage package is not installed, the CLI prints a friendly notice and skips coverage; install with `pip install coverage` to enable.

## API Overview

### mutate_code(source_code, steps=3, seed=None, custom_operators=None, validate=False, use_coverage_strategy=False, use_semantic_strategy=False, coverage_data=None)
- Returns: mutated_code, mutations
- coverage_data: shaped like {"executed_lines": set([...])} for coverage-guided strategy

### smart_mutate_code(source_code, steps=3, seed=None, validate=False, coverage_data=None)
- Smart mutation: combines coverage-guided and semantic-aware strategies

### analyze_code_complexity(source_code)
- Returns code complexity stats, used to guide step selection

## Tests and Verification

- Unit tests:
  - project/tests/test_core.py
  - project/tests/test_variable_scope_rename.py
  - project/tests/test_coverage_integration.py (coverage integration tests)

- Run tests:

```bash
python project/tests/test_core.py
python project/tests/test_variable_scope_rename.py
python project/tests/test_coverage_integration.py
```

## Contribution and Guidelines

- Documentation and diagrams use clean text and basic shapes; no external icon packs.
- Code quality tools: flake8, black, mypy (optional)

## License and Contact

- Author: Zi Yang
- Feedback: open an Issue in the repository

## Dependency-Guided Mutation

This capability allows the CLI/API to accept a "user-provided dependency list" (function names, variable names, attribute names, keyword argument names, etc.). When a dependency hit occurs, the mutation step prioritizes operators at those locations. If there are no hits, the system safely falls back to the default strategy.

- Behavior and boundaries:
  - When code hits dependencies, a mutation step first chooses operators from the hit set; if not, it falls back to the original strategy (no behavior change).
  - List deduplicated, case-insensitive; whitespace and invalid entries are ignored.
  - If passed entries do not appear in code, the CLI prints a notice and continues (default strategy).
  - Compatible with smart strategies (coverage/semantics): after dependency-priority filtering, coverage and semantic strategies still apply to further sort/filter.

- Identifier types that may match dependencies (unified judgment):
  - Identifiers: Name.id, FunctionDef.name, ClassDef.name, arg.arg, keyword.arg
  - Attributes: Attribute.attr
  - Import aliases: alias.name (matches both the full name and split segments)

- CLI usage examples:

```bash
# Prefer variable renaming at score_user/vip related locations
python project/cli.py mutate project/examples/score_user.py \
  --steps 5 --operators variable --dep-priority vip score_user \
  --output project/results/out_dep.py

# Batch mode: enable dependency priority for all Python files in a directory
python project/cli.py batch-mutate project/examples \
  --output project/results/mutated_examples --steps 3 \
  --dep-priority vip mean
```

- API usage example:

```python
from pathlib import Path
from random_mutator import mutate_code, VariableRenameMutator

code = Path('project/examples/score_user.py').read_text(encoding='utf-8')
mutated, logs = mutate_code(
    code, steps=1, custom_operators=[VariableRenameMutator()],
    priority_dependencies=['vip', 'score_user']
)
print('Dependency-priority observed:', any('Renamed function parameter vip -> mutated_' in m['node'] for m in logs))
```

- Help and notices:
  - CLI `list-operators` includes `--dep-priority` documentation.
  - When dependencies are not present in the code, the CLI prints a notice such as:
    `Notice: The following dependency-guided entries were not found in the code: vip, score_user. They will be handled by the default strategy.`

### Parameter and Call Keyword Synchronization (Same-File Transaction Safety)
- Description: When a dependency-priority hit occurs on a function parameter (e.g., vip) and the parameter is renamed, the system synchronizes all call-site keyword names for that function within the same source file (e.g., `vip=True` becomes `mutated_vip_XXXX=True`) to avoid broken executability or inconsistent semantics. Positional argument calls are unaffected.
- Scope: limited to the same source file; cross-file calls currently remain unchanged (may be extended in future versions).
- Example:

```python
# Definition
def score_user(age, orders, refund_rate, vip=False, region='US'):
    ...
# Call (same file)
sc = score_user(age=n, orders=m, refund_rate=0.1, vip=True, region='EU')
```
When `vip` is included in the dependency list, mutation renames the parameter to something like `mutated_vip_1234`, and updates the call-site keyword to `mutated_vip_1234=True`. If the call uses positional arguments (e.g., `score_user(..., True, 'EU')`), no change is required.

### Multi-Factor Hits (Dependencies Driving Multiple Operators)
- Newly enabled operators consume dependencies:
  - FunctionRenameMutator: when the function name or its parameter names hit, prioritize renaming the function name, and synchronize direct calls within the same file (resolvable Name/Attribute).
  - AttributeRenameMutator: when the attribute name hits, prioritize attribute renaming; within a resolvable function scope, rewrite the same attribute name on the same base variable consistently where possible.
  - KeywordArgValueMutator: when keyword.arg (e.g., vip) hits, prefer small changes to that keyword's value (boolean flip, minor numeric tweak), demonstrating that non-renaming operators can also be dependency-driven.
- Recommended multi-operator demo:

```bash
# Enable variable/keyword/attribute/function simultaneously (function includes parameter rename and function-name rename)
python project/cli.py mutate project/examples/score_user.py \
  --steps 8 --operators variable keyword attribute function \
  --dep-priority vip score_user \
  --output project/results/out_dep_multi.py
```
- Behavior: candidate selection layers follow "dependency-first filtering (hits prioritized) → coverage-guided → semantic-aware → random choice by weight". If `--dep-priority` is not provided, behavior remains unchanged.

### Demo (Dependency-Guided Mutation)
- Demo path: Code-Mutation-Engine/Code-Mutation-Engine/demo/dependency_guided
- Reproduce commands:

```bash
# Single operator: variable renaming + keyword sync
python Code-Mutation-Engine/Code-Mutation-Engine/cli.py mutate Code-Mutation-Engine/Code-Mutation-Engine/demo/dependency_guided/input.py \
  --steps 5 --operators variable --dep-priority vip score_user \
  --output Code-Mutation-Engine/Code-Mutation-Engine/demo/dependency_guided/result.py

# Multi-operator demo: enable multi_operators (generates result_multi.py)
python Code-Mutation-Engine/Code-Mutation-Engine/cli.py mutate Code-Mutation-Engine/Code-Mutation-Engine/demo/dependency_guided/input.py \
  --steps 8 --operators variable keyword attribute function \
  --dep-priority vip score_user \
  --output Code-Mutation-Engine/Code-Mutation-Engine/demo/dependency_guided/result_multi.py
```
- Expected effect: After passing `--dep-priority vip score_user`, identifiers related to `vip` or `score_user` are prioritized for mutation. Besides variable renaming (excluding function parameters) and parameter renaming (with keyword sync), you may observe keyword argument value changes (e.g., `vip=True` flipped to `False`), function-name renaming (synchronized calls in the same file), and attribute renaming with consistent rewrites within scope—forming a "multi-factor hit" demonstration.

## CLI Arguments and Key Options

- mutate subcommand:
  - --steps/-s: number of random-walk steps (default 3)
  - --seed: random seed for reproducibility
  - --output/-o: output file path; prints to console if not specified
  - --operators: operator set; one of arithmetic, variable, deletion, comparison, boolean, loop, function, datastructure, keyword, attribute, func_rename
    - function contains ParamRenameMutator and FunctionRenameMutator
  - --smart: smart strategies (coverage + semantics); can be used with --validate
  - --validate: enable syntax + semantics validation; invalid steps roll back without interrupting the overall process
  - --semantic-strategy: enable semantic-aware strategy in standard mode
  - --dep-priority: dependency priority (function/variable/attribute/keyword names; case-insensitive). When hits exist, choose only from the hit subset; otherwise fall back to the original set
  - --exec-check (new): restricted execution check; if the final artifact fails execution, generate a structured failure report *.fail.json and exit with code 2

- analyze subcommand: outputs syntax statistics and suggested steps
- batch-mutate subcommand: mutate a directory; supports --save-logs to emit per-file *.mutation.json

### Operator Set (operators)
- arithmetic: arithmetic operator replacement
- variable: local variable renaming within function scope (scope consistency; does not rename parameters)
- comparison: comparison operator replacement
- deletion: delete statement
- boolean: condition flip
- loop: loop boundary modification
- function: function parameter renaming (with call keyword sync) + function-name renaming (synchronize direct calls in the same file)
- keyword: keyword argument value changes (boolean flip, numeric tweaks)
- attribute: attribute renaming (perform consistent rewrites within safe scope boundaries)
- datastructure: data structure mutations (List↔Tuple, Set→List, swap dict keys/values) with type guards

### Dependency-Priority Semantics and Boundaries (with enhancements)
- Hit rule: determine dependency presence uniformly on the AST (Name/Attribute/FunctionDef/ClassDef/arg/keyword/alias and subtree scan)
- Enhancement: if the operator is DataStructureMutator and the target node is a literal assigned to `Assign.value`, inspect `Assign.targets` to detect left-hand-side hits (e.g., `nums = [...]`) and treat them as dependency affinity hits
- Fallback rule: when no operators hit dependencies, fall back to the original set to ensure progress
- Boundaries and limitations: no complex data-flow across functions; no resolution of cross-file call bindings; attribute renaming attempts only consistent rewrites in clearly resolvable same-file scopes

## Demo Walk CLI (Controllable / Explainable / Reproducible)

For presentation-style demos with explicit walk modes and rich exports, use the dedicated demo CLI:

```bash
# 1) Random walk (baseline)
python codemutationengine/codemutationengine/demo_walk_cli.py \
  --input codemutationengine/codemutationengine/sample_input.py \
  --walk random --policy random --steps 5 --seed 123

# 2) Coverage-guided walk
python codemutationengine/codemutationengine/demo_walk_cli.py \
  --input codemutationengine/codemutationengine/sample_input.py \
  --walk guided --policy coverage --steps 5 --seed 123

# 3) Composite guided walk (coverage + semantic + dependency priority)
python codemutationengine/codemutationengine/demo_walk_cli.py \
  --input codemutationengine/codemutationengine/sample_input.py \
  --walk guided --policy composite --target-api score_user \
  --steps 5 --seed 123
```

Each run writes a timestamped directory under `outputs/<policy>/` with:

- `mutated.py` – mutated artifact
- `manifest.json` – seed/strategy/coverage-hash/path manifest
- `explain.json` – per-step ExplainEvent export (scores + top-5 candidates)
- `graph.json` and `graph.html` – AST graph with the mutation path highlighted
- `run_manifest.txt` – exact command line for reproducibility
