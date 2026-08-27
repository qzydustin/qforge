
"""
Python Random Code Mutation Engine

This module provides a lightweight Python mutation system that generates mutants by applying
small edits to source code. It is useful for validating test effectiveness and studying
program robustness.

Main features:
- Abstract mutation operator interface
- Multiple mutation operations (operator replacement, variable renaming, statement deletion, etc.)
- Random traversal engine
- Reproducible execution via random seed control
- Dual usage modes: CLI and API

Author: Zi Yang
"""

import ast
import random
import copy
import sys
import io
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Type, Set
from enum import Enum
from contextlib import redirect_stderr, redirect_stdout


# Default implicit Python runtime globals (whitelist to avoid false positives in semantic checks).
# Includes common typing/dataclasses symbols so strict semantic validation does not incorrectly
# report undefined names when imports are absent.
DEFAULT_PY_GLOBALS = {
    "__name__", "__file__", "__package__", "__doc__", "__builtins__", "__spec__",
    # ---- typing / dataclasses sentinels (annotation/decorator only; safe to ignore in strict checks) ----
    # bare decorator / helper
    "dataclass", "field",
    # common typing aliases
    "Optional", "Tuple", "List", "Dict", "Set", "Any", "Type", "Union",
    "Literal", "Annotated", "Callable", "Iterable", "Protocol", "TypedDict",
    # qualified-module fallbacks & common aliases
    "typing", "dataclasses", "t", "dc"
}

class MutationContext:
    """Mutation context used to carry state during mutation execution."""

    def __init__(self, seed: Optional[int] = None):
        self.random = random.Random(seed)
        self.applied_mutations = []
        self.mutation_count = 0
        self.seed = seed
        self.coverage_info = {}   # coverage information
        self.semantic_info = {}   # semantic information
        # Dependency-guided priority signals (user-provided dependency identifiers from CLI/API)
        self.priority_dependencies: Set[str] = set()

    def record_mutation(self, operator_name: str, node_info: str, line_number: Optional[int] = None):
        """Record an applied mutation.

        Args:
            operator_name: Mutation operator name
            node_info: Human-readable node/mutation description
            line_number: Source line number where the mutation happened
        """
        mutation_record = {
            'operator': operator_name,
            'node': node_info,
            'step': self.mutation_count
        }

        if line_number is not None:
            mutation_record['line'] = line_number

        self.applied_mutations.append(mutation_record)
        self.mutation_count += 1

    # === Scheduler hooks ===
    def _touch_op_stat(self, name: str) -> Dict[str, Any]:
        stat = self._op_stats.get(name)
        if stat is None:
            stat = {"success": 0, "fail": 0}
            self._op_stats[name] = stat
        return stat

    def record_failure(self, operator_name: str):
        """Record a failed attempt of an operator (no mutation applied)."""
        st = self._touch_op_stat(operator_name)
        st["fail"] += 1

    def _record_success_for_scheduler(self, operator_name: str):
        """Update scheduler-facing counters whenever a mutation is successfully recorded."""
        st = self._touch_op_stat(operator_name)
        st["success"] += 1
        # update consecutive streak
        if self._last_op == operator_name:
            self._last_streak += 1
        else:
            self._last_op = operator_name
            self._last_streak = 1


class MutationOperator(ABC):
    """Abstract base class for mutation operators.

    All mutation operators should inherit from this class and implement `apply`.
    """

    # ===== Sentinel/skip helpers (centralized) =====
    @staticmethod
    def _is_dunder(s: Optional[str]) -> bool:
        try:
            return isinstance(s, str) and len(s) >= 4 and s.startswith("__") and s.endswith("__")
        except Exception:
            return False

    @staticmethod
    def _is_const_main(node: ast.AST) -> bool:
        return isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value == "__main__"

    @staticmethod
    def _is_name_dunder_name(node: ast.AST) -> bool:
        return isinstance(node, ast.Name) and node.id == "__name__"

    @staticmethod
    def _is_entrypoint_compare(node: ast.AST) -> bool:
        # Matches: __name__ == "__main__" (or !=), and also the reversed order
        if not isinstance(node, ast.Compare) or len(getattr(node, "comparators", [])) != 1:
            return False
        left = node.left
        right = node.comparators[0]
        pair_ok = (
            (MutationOperator._is_name_dunder_name(left) and MutationOperator._is_const_main(right)) or
            (MutationOperator._is_name_dunder_name(right) and MutationOperator._is_const_main(left))
        )
        if not pair_ok:
            return False
        # Treat any comparator (Eq/NotEq) as an entrypoint guard
        return True

    @staticmethod
    def is_entrypoint_guard(node: ast.AST) -> bool:
        """Return True if the node (or its subtree) contains an entrypoint sentinel like: __name__ == "__main__"."""
        try:
            for n in ast.walk(node):
                if MutationOperator._is_entrypoint_compare(n):
                    return True
            return False
        except Exception:
            return False

    @staticmethod
    def should_skip_node(node: ast.AST) -> bool:
        """Centralized 'do-not-mutate' hook. Extend this when more sentinels are added."""
        return MutationOperator.is_entrypoint_guard(node)

    def __init__(self, name: str, weight: float = 1.0):
        self.name = name
        self.weight = weight

    @abstractmethod
    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        """Apply a mutation.

        Args:
            tree: The AST to mutate
            ctx: Mutation context

        Returns:
            bool: Whether a mutation was successfully applied
        """
        pass

    @abstractmethod
    def can_apply(self, tree: ast.AST) -> bool:
        """Check whether this operator can be applied.

        Args:
            tree: The AST to inspect

        Returns:
            bool: Whether the operator has at least one valid target
        """
        pass

    # ===== Unified dependency-hit helper =====
    @staticmethod
    def _normalize_dep(s: Optional[str]) -> str:
        try:
            return str(s).strip().lower() if isinstance(s, str) else ""
        except Exception:
            return ""

    @staticmethod
    def match_dependencies(node: ast.AST, dependencies: Set[str]) -> bool:
        """Return True if the given AST node matches any identifier in `dependencies`.

        Supported identifiers:
          - Name.id, FunctionDef.name, ClassDef.name, arg.arg, keyword.arg
          - Attribute.attr
          - alias.name (import alias), with dotted-name segment matching
        """
        if not dependencies:
            return False
        deps = {MutationOperator._normalize_dep(d) for d in dependencies}
        try:
            # Direct matches
            if isinstance(node, ast.Name) and MutationOperator._normalize_dep(node.id) in deps:
                return True
            if isinstance(node, ast.Attribute) and MutationOperator._normalize_dep(node.attr) in deps:
                return True
            if isinstance(node, ast.FunctionDef) and MutationOperator._normalize_dep(getattr(node, 'name', '')) in deps:
                return True
            if isinstance(node, ast.ClassDef) and MutationOperator._normalize_dep(getattr(node, 'name', '')) in deps:
                return True
            if isinstance(node, ast.arg) and MutationOperator._normalize_dep(getattr(node, 'arg', '')) in deps:
                return True
            if isinstance(node, ast.keyword) and MutationOperator._normalize_dep(getattr(node, 'arg', '')) in deps:
                return True
            if isinstance(node, ast.alias):
                name = MutationOperator._normalize_dep(getattr(node, 'name', ''))
                if name in deps:
                    return True
                # alias.name may contain dots; match each segment too
                parts = [p.strip() for p in name.split('.') if p.strip()]
                if any(p in deps for p in parts):
                    return True
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and MutationOperator._normalize_dep(func.id) in deps:
                    return True
                if isinstance(func, ast.Attribute) and MutationOperator._normalize_dep(func.attr) in deps:
                    return True
                # Match keyword argument names
                for kw in getattr(node, 'keywords', []) or []:
                    if isinstance(kw, ast.keyword) and MutationOperator._normalize_dep(getattr(kw, 'arg', '')) in deps:
                        return True

            # Subtree scan for better hit coverage
            for n in ast.walk(node):
                if isinstance(n, ast.Name) and MutationOperator._normalize_dep(n.id) in deps:
                    return True
                if isinstance(n, ast.Attribute) and MutationOperator._normalize_dep(n.attr) in deps:
                    return True
                if isinstance(n, ast.arg) and MutationOperator._normalize_dep(getattr(n, 'arg', '')) in deps:
                    return True
                if isinstance(n, ast.keyword) and MutationOperator._normalize_dep(getattr(n, 'arg', '')) in deps:
                    return True
            return False
        except Exception:
            return False


class ArithmeticOperatorMutator(MutationOperator):
    """Arithmetic operator replacement mutator."""

    # Arithmetic operator mapping table
    OPERATOR_MAP = {
        ast.Add: [ast.Sub, ast.Mult, ast.Div],
        ast.Sub: [ast.Add, ast.Mult, ast.Div],
        ast.Mult: [ast.Add, ast.Sub, ast.Div],
        ast.Div: [ast.Add, ast.Sub, ast.Mult],
        ast.Mod: [ast.Add, ast.Sub, ast.Mult],
        ast.Pow: [ast.Mult, ast.Div],
        ast.FloorDiv: [ast.Div, ast.Mult]
    }

    def __init__(self):
        super().__init__("ArithmeticOperatorMutator")
        self.target_nodes = []

    def can_apply(self, tree: ast.AST) -> bool:
        """Check if there are arithmetic operators that can be mutated."""
        self.target_nodes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and type(node.op) in self.OPERATOR_MAP:
                self.target_nodes.append(node)
        return len(self.target_nodes) > 0

    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        """Replace one arithmetic operator with another."""
        if not self.can_apply(tree):
            return False

        # Randomly select a target node
        target_node = ctx.random.choice(self.target_nodes)
        old_op = type(target_node.op)

        # Randomly select a replacement operator
        new_op_class = ctx.random.choice(self.OPERATOR_MAP[old_op])
        target_node.op = new_op_class()

        # Record mutation
        ctx.record_mutation(
            self.name,
            f"Line {getattr(target_node, 'lineno', 'unknown')}: Arithmetic Operator Replacement {old_op.__name__} -> {new_op_class.__name__}",
            getattr(target_node, 'lineno', None)
        )

        return True


class VariableRenameMutator(MutationOperator):
    """Variable rename mutator (scope-consistent version).

    Goal: Within a single function scope, consistently rename a selected "local variable", including:
    - Function parameters (posonlyargs/args/kwonlyargs/vararg/kwarg)
    - All ast.Name references in that function (Load/Store/Del)
    - Store targets produced by for/with/assignments, etc.

    Constraints:
    - Do not enter nested function/class/lambda scopes
    - Do not rename attribute names (obj.attr)
    - Exclude symbols declared as global/nonlocal
    - Do not rename across functions
    """

    def __init__(self):
        super().__init__("VariableRenameMutator")
        # Candidates: [(func_node, var_name)]
        self.candidates: List[Tuple[ast.AST, str]] = []

    # ============== Internal helpers ==============
    @staticmethod
    def _iter_func_nodes(tree: ast.AST) -> List[ast.AST]:
        return [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

    @staticmethod
    def _skip_nested(node: ast.AST) -> bool:
        return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda))

    @staticmethod
    def _collect_global_nonlocal(func: ast.AST) -> Tuple[Set[str], Set[str]]:
        g, nl = set(), set()
        for n in ast.walk(func):
            if isinstance(n, ast.Global):
                g.update(n.names)
            elif isinstance(n, ast.Nonlocal):
                nl.update(n.names)
        return g, nl

    @staticmethod
    def _iter_nodes_in_function(func: ast.AST):
        # Traverse only this function body; skip nested function/class/lambda scopes.
        stack = list(getattr(func, 'body', []))
        while stack:
            n = stack.pop()
            yield n
            if not VariableRenameMutator._skip_nested(n):
                for child in ast.iter_child_nodes(n):
                    stack.append(child)

    @staticmethod
    def _collect_locals_in_function(func: ast.AST) -> Set[str]:
        """Collect local identifiers (Store/Del) within the function body only (excluding parameters)."""
        locals_: Set[str] = set()
        for n in VariableRenameMutator._iter_nodes_in_function(func):
            if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
                locals_.add(n.id)
        return locals_

    def can_apply(self, tree: ast.AST) -> bool:
        """Check whether there are local variables within functions that can be renamed."""
        self.candidates = []
        func_nodes = self._iter_func_nodes(tree)
        for fn in func_nodes:
            globals_, nonlocals_ = self._collect_global_nonlocal(fn)
            locals_ = self._collect_locals_in_function(fn)
            # Filter out built-ins and global/nonlocal symbols
            for name in locals_:
                if name.startswith('__'):
                    continue
                if name in ['print', 'len', 'range', 'str', 'int', 'float', 'dict', 'list', 'set', 'tuple']:
                    continue
                if name in globals_ or name in nonlocals_:
                    continue
                self.candidates.append((fn, name))
        return len(self.candidates) > 0

    class FunctionScopeRenamer(ast.NodeTransformer):
        """Transformer that performs consistent renaming within a specific function scope."""
        def __init__(self, target_func: ast.AST, old: str, new: str, globals_: Set[str], nonlocals_: Set[str]):
            self.target_func = target_func
            self.old = old
            self.new = new
            self.globals_ = set(globals_)
            self.nonlocals_ = set(nonlocals_)
            self.first_renamed_lineno: Optional[int] = None

        # Skip nested scopes
        def visit_ClassDef(self, node: ast.ClassDef):
            return node
        def visit_Lambda(self, node: ast.Lambda):
            return node
        def visit_FunctionDef(self, node: ast.FunctionDef):
            if node is not self.target_func:
                return node
            # Rename parameters
            self._rename_args(node.args)
            node.body = [self.visit(stmt) for stmt in node.body]
            return node
        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            if node is not self.target_func:
                return node
            self._rename_args(node.args)
            node.body = [self.visit(stmt) for stmt in node.body]
            return node

        def _rename_args(self, args: ast.arguments):
            def rename_arg(a: ast.arg):
                if a and a.arg == self.old and self.old not in self.globals_ and self.old not in self.nonlocals_:
                    a.arg = self.new
            for a in getattr(args, 'posonlyargs', []):
                rename_arg(a)
            for a in getattr(args, 'args', []):
                rename_arg(a)
            for a in getattr(args, 'kwonlyargs', []):
                rename_arg(a)
            if getattr(args, 'vararg', None):
                rename_arg(args.vararg)
            if getattr(args, 'kwarg', None):
                rename_arg(args.kwarg)

        def visit_Global(self, node: ast.Global):
            # Track globals so we don't rename them
            self.globals_.update(node.names)
            return node

        def visit_Nonlocal(self, node: ast.Nonlocal):
            self.nonlocals_.update(node.names)
            return node

        def visit_Name(self, node: ast.Name):
            if node.id == self.old and self.old not in self.globals_ and self.old not in self.nonlocals_:
                node.id = self.new
                if self.first_renamed_lineno is None and hasattr(node, 'lineno'):
                    self.first_renamed_lineno = node.lineno
            return node

    class CallKeywordSync(ast.NodeTransformer):
        """Synchronize keyword arguments in calls within the same file.

        When a target function's parameter is renamed from old -> new, update keyword arguments
        in calls within the same module so keyword.arg changes from old to new.

        - Only updates keyword arguments; positional arguments stay unchanged.
        - Matches direct calls by function name (ast.Name) and safe attribute calls where
          Attribute.attr equals the function name.
        - Single-file scope only; does not resolve complex aliasing or cross-module bindings.
        """
        def __init__(self, func_name: str, old_kw: str, new_kw: str):
            self.func_name = func_name
            self.old_kw = old_kw
            self.new_kw = new_kw
            self.updated_lines: List[int] = []

        def visit_Call(self, node: ast.Call):
            try:
                is_target = False
                if isinstance(node.func, ast.Name) and node.func.id == self.func_name:
                    is_target = True
                elif isinstance(node.func, ast.Attribute) and getattr(node.func, 'attr', None) == self.func_name:
                    # Could be a method call; still safe to update keyword name only
                    is_target = True

                if is_target and getattr(node, 'keywords', None):
                    for kw in node.keywords:
                        # kw.arg == None means **kwargs; skip
                        if kw.arg == self.old_kw:
                            kw.arg = self.new_kw
                            if hasattr(node, 'lineno') and isinstance(node.lineno, int):
                                self.updated_lines.append(node.lineno)

                self.generic_visit(node)
                return node
            except Exception:
                return node

    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        """Perform a "pure identifier rename" within a single function scope.

        Note: This variant renames local variable identifiers within the chosen function.
        It does not rename function parameters and does not synchronize call keywords.
        """
        if not self.can_apply(tree):
            return False

        # Coverage-first: if coverage info exists, prefer candidates whose function contains executed lines.
        coverage_lines: Set[int] = set()
        try:
            if hasattr(ctx, 'coverage_info') and ctx.coverage_info:
                coverage_lines = set(ctx.coverage_info)
        except Exception:
            coverage_lines = set()

        # Dependency-guided priority: if ctx.priority_dependencies is non-empty, prefer candidates whose
        # variable name or function name matches the dependency identifiers.
        deps: Set[str] = set()
        try:
            if hasattr(ctx, 'priority_dependencies') and ctx.priority_dependencies:
                deps = {str(d).lower() for d in ctx.priority_dependencies}
        except Exception:
            deps = set()

        def func_has_covered_line(fn: ast.AST) -> bool:
            for n in ast.walk(fn):
                ln = getattr(n, 'lineno', None)
                if isinstance(ln, int) and ln in coverage_lines:
                    return True
            return False

        candidates = list(self.candidates)

        preferred_candidates: List[Tuple[ast.AST, str]] = []
        name_matched: List[Tuple[ast.AST, str]] = []
        func_matched: List[Tuple[ast.AST, str]] = []
        if deps:
            for fn, name in candidates:
                fn_name = getattr(fn, 'name', '')
                if isinstance(name, str) and name.lower() in deps:
                    name_matched.append((fn, name))
                elif isinstance(fn_name, str) and fn_name.lower() in deps:
                    func_matched.append((fn, name))
            preferred_candidates = name_matched if name_matched else func_matched

        def choose_from(cands: List[Tuple[ast.AST, str]]) -> Tuple[ast.AST, str]:
            if coverage_lines:
                covered_cands = [(fn, name) for (fn, name) in cands if func_has_covered_line(fn)]
            else:
                covered_cands = []
            if covered_cands:
                return ctx.random.choice(covered_cands)
            return ctx.random.choice(cands)

        target_func, old_name = choose_from(preferred_candidates or candidates)
        new_name = f"mutated_{old_name}_{ctx.random.randint(1000, 9999)}"

        # Rename identifier within the function scope only (does not modify parameters).
        globals_, nonlocals_ = self._collect_global_nonlocal(target_func)

        class FunctionVarRenamer(ast.NodeTransformer):
            def __init__(self, target_func: ast.AST, old: str, new: str, globals_: Set[str], nonlocals_: Set[str]):
                self.target_func = target_func
                self.old = old
                self.new = new
                self.globals_ = set(globals_)
                self.nonlocals_ = set(nonlocals_)
                self.first_renamed_lineno: Optional[int] = None
            def visit_FunctionDef(self, node: ast.FunctionDef):
                if node is not self.target_func:
                    return node
                node.body = [self.visit(stmt) for stmt in node.body]
                return node
            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
                if node is not self.target_func:
                    return node
                node.body = [self.visit(stmt) for stmt in node.body]
                return node
            def visit_Global(self, node: ast.Global):
                self.globals_.update(node.names)
                return node
            def visit_Nonlocal(self, node: ast.Nonlocal):
                self.nonlocals_.update(node.names)
                return node
            def visit_Name(self, node: ast.Name):
                if node.id == self.old and self.old not in self.globals_ and self.old not in self.nonlocals_:
                    node.id = self.new
                    if self.first_renamed_lineno is None and hasattr(node, 'lineno'):
                        self.first_renamed_lineno = node.lineno
                return node

        renamer = FunctionVarRenamer(target_func, old_name, new_name, globals_, nonlocals_)
        renamer.visit(target_func)

        # Record mutation (does not include call keyword sync info)
        first_line = renamer.first_renamed_lineno or getattr(target_func, 'lineno', None)
        ctx.record_mutation(
            self.name,
            f"Line {first_line or 'unknown'}: Local variable renaming within a function scope {old_name} -> {new_name}",
            first_line
        )
        return True

class ParamRenameMutator(MutationOperator):
    """Function parameter renaming operator (with same-file call keyword synchronization).

    When a dependency hint matches a function parameter (e.g., vip) or the function name (e.g., score_user),
    this operator prefers renaming that parameter, and synchronizes keyword argument names at call sites
    within the same source file.

    Notes:
    - Positional-argument calls are NOT modified.
    - Scope is limited to the same source file only.
    """
    def __init__(self):
        super().__init__("ParamRenameMutator")
        self.candidates: List[Tuple[ast.AST, str]] = []

    @staticmethod
    def _iter_func_nodes(tree: ast.AST) -> List[ast.AST]:
        return [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

    @staticmethod
    def _collect_params(fn: ast.AST) -> List[str]:
        names: List[str] = []
        args = getattr(fn, 'args', None)
        if isinstance(args, ast.arguments):
            for a in getattr(args, 'posonlyargs', []):
                names.append(a.arg)
            for a in getattr(args, 'args', []):
                names.append(a.arg)
            for a in getattr(args, 'kwonlyargs', []):
                names.append(a.arg)
            if getattr(args, 'vararg', None):
                names.append(args.vararg.arg)
            if getattr(args, 'kwarg', None):
                names.append(args.kwarg.arg)
        return names

    def can_apply(self, tree: ast.AST) -> bool:
        self.candidates = []
        for fn in ParamRenameMutator._iter_func_nodes(tree):
            for name in ParamRenameMutator._collect_params(fn):
                if not name or name.startswith('__'):
                    continue
                if name in ['print', 'len', 'range', 'str', 'int', 'float', 'dict', 'list', 'set', 'tuple']:
                    continue
                self.candidates.append((fn, name))
        return len(self.candidates) > 0

    class ParamScopeRenamer(ast.NodeTransformer):
        def __init__(self, target_func: ast.AST, old: str, new: str, globals_: Set[str], nonlocals_: Set[str]):
            self.target_func = target_func
            self.old = old
            self.new = new
            self.globals_ = set(globals_)
            self.nonlocals_ = set(nonlocals_)
            self.first_renamed_lineno: Optional[int] = None

        def visit_ClassDef(self, node: ast.ClassDef):
            return node

        def visit_Lambda(self, node: ast.Lambda):
            return node

        def visit_FunctionDef(self, node: ast.FunctionDef):
            if node is not self.target_func:
                return node
            self._rename_args(node.args)
            node.body = [self.visit(stmt) for stmt in node.body]
            return node

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            if node is not self.target_func:
                return node
            self._rename_args(node.args)
            node.body = [self.visit(stmt) for stmt in node.body]
            return node

        def _rename_args(self, args: ast.arguments):
            def rename_arg(a: ast.arg):
                if a and a.arg == self.old and self.old not in self.globals_ and self.old not in self.nonlocals_:
                    a.arg = self.new
            for a in getattr(args, 'posonlyargs', []):
                rename_arg(a)
            for a in getattr(args, 'args', []):
                rename_arg(a)
            for a in getattr(args, 'kwonlyargs', []):
                rename_arg(a)
            if getattr(args, 'vararg', None):
                rename_arg(args.vararg)
            if getattr(args, 'kwarg', None):
                rename_arg(args.kwarg)

        def visit_Global(self, node: ast.Global):
            self.globals_.update(node.names)
            return node

        def visit_Nonlocal(self, node: ast.Nonlocal):
            self.nonlocals_.update(node.names)
            return node

        def visit_Name(self, node: ast.Name):
            if node.id == self.old and self.old not in self.globals_ and self.old not in self.nonlocals_:
                node.id = self.new
                if self.first_renamed_lineno is None and hasattr(node, 'lineno'):
                    self.first_renamed_lineno = node.lineno
            return node

    class CallKeywordSync(ast.NodeTransformer):
        def __init__(self, func_name: str, old_kw: str, new_kw: str):
            self.func_name = func_name
            self.old_kw = old_kw
            self.new_kw = new_kw
            self.updated_lines: List[int] = []

        def visit_Call(self, node: ast.Call):
            try:
                is_target = False
                if isinstance(node.func, ast.Name) and node.func.id == self.func_name:
                    is_target = True
                elif isinstance(node.func, ast.Attribute) and getattr(node.func, 'attr', None) == self.func_name:
                    is_target = True

                if is_target and getattr(node, 'keywords', None):
                    for kw in node.keywords:
                        if kw.arg == self.old_kw:
                            kw.arg = self.new_kw
                            if hasattr(node, 'lineno') and isinstance(node.lineno, int):
                                self.updated_lines.append(node.lineno)

                self.generic_visit(node)
                return node
            except Exception:
                return node

    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        if not self.can_apply(tree):
            return False

        coverage_lines: Set[int] = set(getattr(ctx, 'coverage_info', set()) or set())
        deps: Set[str] = set(getattr(ctx, 'priority_dependencies', set()) or set())
        candidates = list(self.candidates)

        param_matched: List[Tuple[ast.AST, str]] = []
        func_matched: List[Tuple[ast.AST, str]] = []
        if deps:
            for fn, name in candidates:
                fn_name = getattr(fn, 'name', '')
                if isinstance(name, str) and MutationOperator._normalize_dep(name) in deps:
                    param_matched.append((fn, name))
                elif isinstance(fn_name, str) and MutationOperator._normalize_dep(fn_name) in deps:
                    func_matched.append((fn, name))

        preferred = param_matched if param_matched else func_matched

        def func_has_covered_line(fn: ast.AST) -> bool:
            for n in ast.walk(fn):
                ln = getattr(n, 'lineno', None)
                if isinstance(ln, int) and ln in coverage_lines:
                    return True
            return False

        def choose_from(cands: List[Tuple[ast.AST, str]]) -> Tuple[ast.AST, str]:
            if coverage_lines:
                covered_cands = [(fn, name) for (fn, name) in cands if func_has_covered_line(fn)]
                if covered_cands:
                    return ctx.random.choice(covered_cands)
            return ctx.random.choice(cands)

        target_func, old_name = choose_from(preferred or candidates)
        new_name = f"mutated_{old_name}_{ctx.random.randint(1000, 9999)}"

        globals_, nonlocals_ = VariableRenameMutator._collect_global_nonlocal(target_func)
        renamer = ParamRenameMutator.ParamScopeRenamer(target_func, old_name, new_name, globals_, nonlocals_)
        renamer.visit(target_func)

        func_name = getattr(target_func, 'name', None)
        updated_lines: List[int] = []
        if isinstance(func_name, str) and func_name:
            try:
                sync = ParamRenameMutator.CallKeywordSync(func_name, old_name, new_name)
                sync.visit(tree)
                updated_lines = sync.updated_lines
            except Exception:
                updated_lines = []

        first_line_candidates = [renamer.first_renamed_lineno or getattr(target_func, 'lineno', None)] + (updated_lines[:1] if updated_lines else [])
        first_line = next((ln for ln in first_line_candidates if isinstance(ln, int)), None)

        extra = f"; Synchronously updated call keyword {old_name} -> {new_name}" if updated_lines else ""
        ctx.record_mutation(
            self.name,
            f"Line {first_line or 'unknown'}: Renamed function parameter {old_name} -> {new_name}{extra}",
            first_line
        )
        return True


class KeywordArgValueMutator(MutationOperator):
    """Keyword-argument value mutation operator.

    Approach:
    - Collect keyword arguments from all Call nodes where the value is a bool/int/float constant.
    - If priority_dependencies hits some keyword names (e.g., "vip"), then only mutate those keywords
      ("name-targeted" mutation).
    - If no keyword name is hit by deps, fall back to the generic match_dependencies(kw/call, deps) logic.
    """
    def __init__(self):
        super().__init__("KeywordArgValueMutator", weight=1.2)
        self.candidates: List[Tuple[ast.Call, ast.keyword]] = []

    def can_apply(self, tree: ast.AST) -> bool:
        self.candidates = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                for kw in getattr(node, "keywords", []) or []:
                    val = getattr(kw, "value", None)
                    # Only accept constant bool/int/float, and kw.arg must be a string
                    if (
                        isinstance(val, ast.Constant)
                        and isinstance(val.value, (bool, int, float))
                        and isinstance(kw.arg, str)
                    ):
                        self.candidates.append((node, kw))
        return len(self.candidates) > 0

    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        if not self.can_apply(tree):
            return False

        # Read dependency hints & coverage info from the context
        deps: Set[str] = set(getattr(ctx, "priority_dependencies", set()) or set())
        coverage_lines: Set[int] = set(getattr(ctx, "coverage_info", set()) or set())

        # ===== Dependency-prioritized filtering =====
        pref: List[Tuple[ast.Call, ast.keyword]] = []
        if deps:
            # First, detect keyword names hit by deps (e.g., "vip")
            arg_hit_names: Set[str] = set(
                kw.arg
                for _, kw in self.candidates
                if isinstance(kw, ast.keyword)
                and isinstance(kw.arg, str)
                and kw.arg in deps
            )

            for call, kw in self.candidates:
                hit = False

                if arg_hit_names:
                    # If any "name-hit" keywords exist, restrict selection to those keywords only
                    if isinstance(kw, ast.keyword) and isinstance(kw.arg, str) and kw.arg in arg_hit_names:
                        hit = True
                else:
                    # Otherwise, fall back to AST-level dependency matching (function name / context)
                    if (
                        MutationOperator.match_dependencies(kw, deps)
                        or MutationOperator.match_dependencies(call, deps)
                    ):
                        hit = True

                if hit:
                    pref.append((call, kw))

        # Use dependency-filtered candidates if available; otherwise fall back to all candidates
        cands: List[Tuple[ast.Call, ast.keyword]] = pref if pref else self.candidates

        # ===== Coverage-first: prefer calls on executed lines =====
        if coverage_lines:
            covered: List[Tuple[ast.Call, ast.keyword]] = []
            for call, kw in cands:
                ln = getattr(call, "lineno", None)
                if isinstance(ln, int) and ln in coverage_lines:
                    covered.append((call, kw))
            if covered:
                cands = covered

        if not cands:
            return False

        # Randomly pick a keyword and mutate its value
        call, kw = ctx.random.choice(cands)
        val = kw.value
        old_desc = None

        if isinstance(val, ast.Constant) and isinstance(val.value, bool):
            old_desc = str(val.value)
            val.value = not val.value
        elif isinstance(val, ast.Constant) and isinstance(val.value, int):
            old_desc = str(val.value)
            delta = ctx.random.choice([-1, 1])
            val.value = val.value + delta
        elif isinstance(val, ast.Constant) and isinstance(val.value, float):
            old_desc = str(val.value)
            delta = ctx.random.choice([-0.1, 0.1])
            val.value = round(val.value + delta, 3)
        else:
            # Should not happen because can_apply filters types
            return False

        ln = getattr(call, "lineno", None)
        ctx.record_mutation(
            self.name,
            f"Line {ln or 'unknown'}: Keyword argument value changed {kw.arg} = {old_desc} -> {ast.unparse(kw.value)}",
            ln,
        )
        return True


class AttributeRenameMutator(MutationOperator):
    """Attribute renaming mutation operator.

    When Attribute.attr hits the dependency list, prefer attribute renaming.
    For compatibility: if an enclosing function scope can be found, consistently rewrite the same attribute name
    on the same base variable within that function; otherwise rewrite only the selected node.
    """
    def __init__(self):
        super().__init__("AttributeRenameMutator")
        self.candidates: List[ast.Attribute] = []

    def can_apply(self, tree: ast.AST) -> bool:
        self.candidates = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and isinstance(node.attr, str):
                if not node.attr.startswith('__'):
                    self.candidates.append(node)
        return len(self.candidates) > 0

    @staticmethod
    def _find_enclosing_function(tree: ast.AST, target: ast.AST) -> Optional[ast.AST]:
        for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            for n in ast.walk(fn):
                if n is target:
                    return fn
        return None

    class FunctionAttributeRenamer(ast.NodeTransformer):
        def __init__(self, target_func: ast.AST, base_name: Optional[str], old: str, new: str):
            self.target_func = target_func
            self.base_name = base_name
            self.old = old
            self.new = new
            self.first_renamed_line: Optional[int] = None

        def visit_FunctionDef(self, node: ast.FunctionDef):
            if node is not self.target_func:
                return node
            node.body = [self.visit(stmt) for stmt in node.body]
            return node

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            if node is not self.target_func:
                return node
            node.body = [self.visit(stmt) for stmt in node.body]
            return node

        def visit_Attribute(self, node: ast.Attribute):
            try:
                base_ok = True
                if self.base_name and isinstance(node.value, ast.Name):
                    base_ok = (node.value.id == self.base_name)
                if base_ok and node.attr == self.old:
                    node.attr = self.new
                    if self.first_renamed_line is None and hasattr(node, 'lineno'):
                        self.first_renamed_line = node.lineno
            except Exception:
                pass
            return node

    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        if not self.can_apply(tree):
            return False

        deps = set(getattr(ctx, 'priority_dependencies', set()) or set())
        coverage_lines: Set[int] = set(getattr(ctx, 'coverage_info', set()) or set())

        pref = []
        if deps:
            for attr in self.candidates:
                if MutationOperator.match_dependencies(attr, deps):
                    pref.append(attr)
        cands = pref if pref else self.candidates

        def covered_first(c: List[ast.Attribute]):
            if coverage_lines:
                covered = [a for a in c if isinstance(getattr(a, 'lineno', None), int) and a.lineno in coverage_lines]
                if covered:
                    return covered
            return c

        cands = covered_first(cands)

        target = ctx.random.choice(cands)
        old = target.attr
        new = f"mutated_{old}_{ctx.random.randint(1000, 9999)}"

        # Try best-effort consistent renaming within the enclosing function scope
        base_name = target.value.id if isinstance(target.value, ast.Name) else None
        fn = self._find_enclosing_function(tree, target)
        first_line = getattr(target, 'lineno', None)
        if fn:
            try:
                ren = AttributeRenameMutator.FunctionAttributeRenamer(fn, base_name, old, new)
                ren.visit(fn)
                if isinstance(ren.first_renamed_line, int):
                    first_line = ren.first_renamed_line
            except Exception:
                # Fallback: rewrite only the selected node
                target.attr = new
        else:
            target.attr = new

        ctx.record_mutation(
            self.name,
            f"Line {first_line or 'unknown'}: Rename attribute {old} -> {new}",
            first_line
        )
        return True


class FunctionRenameMutator(MutationOperator):
    """Function name renaming mutation operator.

    When a dependency hint hits the function name or any of its parameter names, prefer renaming the function.
    Also attempts to synchronize call sites in the same file (directly resolvable Name/Attribute calls).
    """
    def __init__(self):
        super().__init__("FunctionRenameMutator")
        self.candidates: List[ast.AST] = []

    def can_apply(self, tree: ast.AST) -> bool:
        self.candidates = []
        for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            name = getattr(fn, 'name', '')
            if isinstance(name, str) and name and not name.startswith('__'):
                self.candidates.append(fn)
        return len(self.candidates) > 0

    @staticmethod
    def _func_has_param_hit(fn: ast.AST, deps: Set[str]) -> bool:
        try:
            if not deps:
                return False
            deps_norm = {MutationOperator._normalize_dep(d) for d in deps}
            args = getattr(fn, 'args', None)
            if not isinstance(args, ast.arguments):
                return False
            for a in getattr(args, 'posonlyargs', []) + getattr(args, 'args', []) + getattr(args, 'kwonlyargs', []):
                if MutationOperator._normalize_dep(getattr(a, 'arg', '')) in deps_norm:
                    return True
            for extra in [getattr(args, 'vararg', None), getattr(args, 'kwarg', None)]:
                if extra and MutationOperator._normalize_dep(getattr(extra, 'arg', '')) in deps_norm:
                    return True
            return False
        except Exception:
            return False

    class CallFunctionNameSync(ast.NodeTransformer):
        def __init__(self, old: str, new: str):
            self.old = old
            self.new = new
            self.updated_lines: List[int] = []

        def visit_Call(self, node: ast.Call):
            try:
                if isinstance(node.func, ast.Name) and node.func.id == self.old:
                    node.func.id = self.new
                    if hasattr(node, 'lineno') and isinstance(node.lineno, int):
                        self.updated_lines.append(node.lineno)
                elif isinstance(node.func, ast.Attribute) and getattr(node.func, 'attr', None) == self.old:
                    node.func.attr = self.new
                    if hasattr(node, 'lineno') and isinstance(node.lineno, int):
                        self.updated_lines.append(node.lineno)
            except Exception:
                pass
            self.generic_visit(node)
            return node

    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        if not self.can_apply(tree):
            return False

        deps = set(getattr(ctx, 'priority_dependencies', set()) or set())
        coverage_lines: Set[int] = set(getattr(ctx, 'coverage_info', set()) or set())

        pref: List[ast.AST] = []
        if deps:
            deps_norm = {MutationOperator._normalize_dep(d) for d in deps}
            for fn in self.candidates:
                fname = getattr(fn, 'name', '')
                if MutationOperator._normalize_dep(fname) in deps_norm:
                    pref.append(fn)
                elif FunctionRenameMutator._func_has_param_hit(fn, deps):
                    pref.append(fn)

        cands = pref if pref else self.candidates

        def covered_first(c: List[ast.AST]):
            if coverage_lines:
                covered = [
                    fn for fn in c
                    if any(
                        isinstance(getattr(n, 'lineno', None), int) and getattr(n, 'lineno', None) in coverage_lines
                        for n in ast.walk(fn)
                    )
                ]
                if covered:
                    return covered
            return c

        cands = covered_first(cands)

        target_fn = ctx.random.choice(cands)
        old = getattr(target_fn, 'name', '')
        new = f"mutated_{old}_{ctx.random.randint(1000, 9999)}"

        # Rename the function definition
        target_fn.name = new

        # Synchronize same-file calls
        try:
            sync = FunctionRenameMutator.CallFunctionNameSync(old, new)
            sync.visit(tree)
            updated_lines = sync.updated_lines
        except Exception:
            updated_lines = []

        first_line = getattr(target_fn, 'lineno', None)
        extra = f"; Synchronously updated calls {old} -> {new}" if updated_lines else ""
        ctx.record_mutation(
            self.name,
            f"Line {first_line or 'unknown'}: Function renaming {old} -> {new}{extra}",
            first_line
        )
        return True

class StatementDeletionMutator(MutationOperator):
    """
    Statement deletion mutation operator with safety guards + dependency/coverage preference.

    Safety goals:
    - Do not delete a statement if it introduces a name for the first time and that name is
      later read before being redefined (prevents NameError).
    - Protect module/class/function docstring as the first body element.
    - Prefer statements that touch priority dependencies.
    - Prefer statements on covered lines when coverage info is available.
    """

    def __init__(self):
        super().__init__("StatementDeletionMutator")
        # Each candidate: (parent_node_with_body, index_in_body, stmt_node)
        self.deletable_statements: List[Tuple[ast.AST, int, ast.AST]] = []

    def can_apply(self, tree: ast.AST) -> bool:
        """Collect deletable statement candidates."""
        self.deletable_statements = []
        for node in ast.walk(tree):
            body = getattr(node, "body", None)
            if isinstance(body, list):
                for i, stmt in enumerate(body):
                    # Only consider simple statements. Skip control blocks and function defs.
                    if isinstance(
                        stmt,
                        (ast.Assign, ast.AugAssign, ast.AnnAssign, ast.Expr, ast.Import, ast.ImportFrom),
                    ):
                        self.deletable_statements.append((node, i, stmt))
        return len(self.deletable_statements) > 0

    @staticmethod
    def _assigned_names(stmt: ast.AST) -> Set[str]:
        """Extract variable names written/defined by this statement (including imports)."""
        names: Set[str] = set()

        def collect(t: ast.AST):
            if isinstance(t, ast.Name):
                names.add(t.id)
            elif isinstance(t, (ast.Tuple, ast.List)):
                for e in t.elts:
                    collect(e)

        if isinstance(stmt, ast.Assign):
            for t in getattr(stmt, "targets", []) or []:
                collect(t)
        elif isinstance(stmt, ast.AugAssign):
            collect(getattr(stmt, "target", None))
        elif isinstance(stmt, ast.AnnAssign):
            collect(getattr(stmt, "target", None))
        elif isinstance(stmt, ast.Import):
            # import inspect / import inspect as ins
            for alias in stmt.names:
                names.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(stmt, ast.ImportFrom):
            # from inspect import signature as sig
            for alias in stmt.names:
                names.add(alias.asname or alias.name)
        return names

    @staticmethod
    def _statement_reads_names(stmt: ast.AST, names: Set[str]) -> bool:
        """Return True if this statement reads any name in `names`."""
        for n in ast.walk(stmt):
            if isinstance(n, ast.Name) and isinstance(getattr(n, "ctx", None), ast.Load) and n.id in names:
                return True
        return False

    @staticmethod
    def _first_defs_in_scope(scope: ast.AST, idx: int, names: Set[str]) -> Set[str]:
        """
        Return the subset of `names` that are first-defined by scope.body[idx]
        (i.e., not assigned/imported earlier within this scope.body).
        """
        first: Set[str] = set()
        for name in names:
            seen_before = False
            for j in range(0, idx):
                if name in StatementDeletionMutator._assigned_names(scope.body[j]):
                    seen_before = True
                    break
            if not seen_before:
                first.add(name)
        return first

    @staticmethod
    def _first_defs_used_later(scope: ast.AST, idx: int, first_defs: Set[str]) -> bool:
        """
        Return True if any first-defined name is read later before being redefined.
        This indicates deleting this statement could cause NameError.
        """
        alive: Set[str] = set(first_defs)
        if not alive:
            return False

        for j in range(idx + 1, len(getattr(scope, "body", []))):
            stmt = scope.body[j]
            if StatementDeletionMutator._statement_reads_names(stmt, alive):
                return True
            alive -= StatementDeletionMutator._assigned_names(stmt)
            if not alive:
                return False
        return False

    # ============================================================
    # Helpers for dependency preference and metadata
    # ============================================================
    @staticmethod
    def _touches_dependency(node: ast.AST, deps: Set[str]) -> bool:
        """Return True if node touches any dependency in deps; if deps empty, always True."""
        if not deps:
            return True
        try:
            return MutationOperator.match_dependencies(node, deps)
        except Exception:
            norm = {MutationOperator._normalize_dep(d) for d in deps}
            for n in ast.walk(node):
                if isinstance(n, ast.Name) and MutationOperator._normalize_dep(n.id) in norm:
                    return True
            return False

    @staticmethod
    def _any_lineno(node: ast.AST) -> Optional[int]:
        """Best-effort: find any lineno within this node/subtree."""
        ln = getattr(node, "lineno", None)
        if isinstance(ln, int):
            return ln
        for n in ast.walk(node):
            ln2 = getattr(n, "lineno", None)
            if isinstance(ln2, int):
                return ln2
        return None

    @staticmethod
    def _ensure_non_empty_body(parent: ast.AST, deleted_stmt: ast.AST) -> bool:
        """If parent.body becomes empty, insert a `pass` (except for Module).

        Returns True if a pass was inserted.
        """
        body = getattr(parent, "body", None)
        if not isinstance(body, list):
            return False

        # Module body can be empty; other suites usually cannot.
        if isinstance(parent, ast.Module):
            return False

        if len(body) > 0:
            return False

        pass_node = ast.Pass()

        # Give the pass a reasonable source location so ast.unparse() works well.
        # Prefer deleted_stmt location; fallback to parent location; final fallback line=1.
        line = getattr(deleted_stmt, "lineno", None)
        col = getattr(deleted_stmt, "col_offset", None)
        if not isinstance(line, int):
            line = getattr(parent, "lineno", None)
        if not isinstance(line, int):
            line = 1
        if not isinstance(col, int):
            col = 0

        pass_node.lineno = line
        pass_node.col_offset = col

        body.append(pass_node)
        ast.fix_missing_locations(pass_node)
        return True

    # ============================================================
    # Main mutation logic
    # ============================================================
    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        if not self.can_apply(tree):
            return False
        ast.fix_missing_locations(tree)
        deps: Set[str] = set(getattr(ctx, "priority_dependencies", set()) or set())
        coverage_lines: Set[int] = set(getattr(ctx, "coverage_info", set()) or set())

        safe: List[Tuple[ast.AST, int, ast.AST]] = []
        for parent, idx, stmt in self.deletable_statements:
            # Skip docstring if it is the first statement in module/class/function.
            if (
                isinstance(stmt, ast.Expr)
                and isinstance(getattr(stmt, "value", None), ast.Constant)
                and isinstance(stmt.value.value, str)
                and idx == 0
                and isinstance(parent, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            ):
                continue

            # Safety: do not delete if it introduces a first definition that is used later.
            assigned = self._assigned_names(stmt)
            first_defs = self._first_defs_in_scope(parent, idx, assigned)
            if self._first_defs_used_later(parent, idx, first_defs):
                continue

            # Dependency preference: skip if unrelated when deps are provided.
            if not self._touches_dependency(stmt, deps):
                continue

            safe.append((parent, idx, stmt))

        if not safe:
            return False

        # Coverage preference: if any safe statement is on an executed line, restrict to those.
        if coverage_lines:
            covered = [t for t in safe if self._any_lineno(t[2]) in coverage_lines]
            if covered:
                safe = covered

        parent_node, stmt_index, stmt = ctx.random.choice(safe)

        # IMPORTANT: capture line number before deleting the node.
        stmt_line = self._any_lineno(stmt)
        del parent_node.body[stmt_index]
        # If we emptied a suite body, insert `pass` to keep syntax valid
        inserted_pass = self._ensure_non_empty_body(parent_node, stmt)

        # Record mutation with a real int line when available.
        # (If stmt_line is None, engine may still try fallbacks; but mutator should provide line whenever possible.)
        stmt_line = self._any_lineno(stmt)
        extra = " (empty suite -> inserted pass)" if inserted_pass else ""
        ctx.record_mutation(
            self.name,
            f"Line {stmt_line or 'unknown'}: delete statement {type(stmt).__name__}{extra}",
            stmt_line,
        )
        return True
class BooleanConditionFlipMutator(MutationOperator):
    """Condition-flip mutation operator.

    Flips boolean conditions, with dependency-prioritized selection support
    (e.g., dep='loyalty_points' or 'vip').
    """

    def __init__(self):
        super().__init__("BooleanConditionFlipMutator")
        self.target_nodes: List[ast.AST] = []
        # Track parent relationships to locate enclosing function, etc.
        self.parent_map: Dict[ast.AST, ast.AST] = {}

    def _build_parent_map(self, tree: ast.AST):
        """Build parent_map: child -> parent."""
        self.parent_map.clear()
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                self.parent_map[child] = parent

    def _enclosing_func_name(self, node: ast.AST) -> Optional[str]:
        """Walk upwards and return the nearest enclosing function name (or None if not inside a function)."""
        cur = node
        visited = set()
        while cur in self.parent_map and cur not in visited:
            visited.add(cur)
            cur = self.parent_map[cur]
            if isinstance(cur, ast.FunctionDef):
                return cur.name
        return None

    def can_apply(self, tree: ast.AST) -> bool:
        """
        Collect boolean-condition nodes that can be flipped:
        - If / While tests (excluding entrypoint sentinels)
        - BoolOp (and/or), excluding any subtree that contains entrypoint sentinels
        """
        self.target_nodes = []
        self._build_parent_map(tree)

        for node in ast.walk(tree):
            # If/While condition: collect when test is not an entrypoint sentinel
            if isinstance(node, (ast.If, ast.While)):
                test = getattr(node, "test", None)
                if test is not None and not MutationOperator.should_skip_node(test):
                    self.target_nodes.append(node)
            # Direct boolean operations: collect only if subtree does not contain entrypoint sentinels
            elif isinstance(node, ast.BoolOp):
                if not MutationOperator.should_skip_node(node):
                    self.target_nodes.append(node)

        return len(self.target_nodes) > 0

    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        """
        Flip boolean conditions with a dependency-prioritized strategy:
        1. If ctx.priority_dependencies is non-empty (e.g., ['loyalty_points'] or ['vip']),
           prefer nodes where:
             - the enclosing function name is in deps (e.g., an if inside loyalty_points),
             - or the node/test contains dependency identifiers.
        2. If no deps match, fall back to all candidates.
        3. If coverage_info is available, further prefer nodes on covered lines.
        """
        if not self.can_apply(tree):
            return False

        deps = set(getattr(ctx, "priority_dependencies", []) or [])
        coverage_lines: Set[int] = set(getattr(ctx, "coverage_info", []) or set())

        candidates: List[ast.AST] = list(self.target_nodes)

        # ------- Dependency-prioritized filtering -------
        if deps:
            dep_matched: List[ast.AST] = []
            for node in candidates:
                func_name = self._enclosing_func_name(node)
                func_hit = func_name in deps if func_name is not None else False

                node_hit = MutationOperator.match_dependencies(node, deps)
                test_hit = False
                if isinstance(node, (ast.If, ast.While)):
                    test = getattr(node, "test", None)
                    if test is not None and MutationOperator.match_dependencies(test, deps):
                        test_hit = True

                if func_hit or node_hit or test_hit:
                    dep_matched.append(node)

            if dep_matched:
                candidates = dep_matched

        # ------- Coverage-first (if coverage_info is present) -------
        if coverage_lines:
            covered = [
                n for n in candidates
                if isinstance(getattr(n, "lineno", None), int)
                and n.lineno in coverage_lines
            ]
            if covered:
                candidates = covered

        if not candidates:
            # Should not happen, but keep a safe fallback
            return False

        target_node = ctx.random.choice(candidates)

        # ------- Apply the actual flip -------
        if isinstance(target_node, (ast.If, ast.While)):
            original_test = target_node.test
            target_node.test = ast.UnaryOp(op=ast.Not(), operand=original_test)
            node_line = getattr(target_node, "lineno", None)
            ctx.record_mutation(
                self.name,
                f"Line {node_line or 'unknown'}: Flip condition in {type(target_node).__name__}",
                node_line,
            )
        elif isinstance(target_node, ast.BoolOp):
            if isinstance(target_node.op, ast.And):
                target_node.op = ast.Or()
                op_change = "And -> Or"
            elif isinstance(target_node.op, ast.Or):
                target_node.op = ast.And()
                op_change = "Or -> And"
            else:
                return False
            node_line = getattr(target_node, "lineno", None)
            ctx.record_mutation(
                self.name,
                f"Line {node_line or 'unknown'}: Flip boolean operator {op_change}",
                node_line,
            )
        else:
            return False

        return True


class LoopBoundaryMutator(MutationOperator):
    """Loop-boundary mutation operator.

    Modifies for/while boundary values (only changes upper bound / comparator value),
    and avoids accidentally changing the range() step.
    """

    def __init__(self):
        super().__init__("LoopBoundaryMutator")
        self.target_nodes = []

    def can_apply(self, tree: ast.AST) -> bool:
        """Check whether there are loop boundaries that can be modified."""
        self.target_nodes = []
        for node in ast.walk(tree):
            # Find range(...) calls in for loops
            if isinstance(node, ast.For) and isinstance(node.iter, ast.Call):
                if isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
                    self.target_nodes.append(node.iter)
            # Find comparison conditions in while loops
            elif isinstance(node, ast.While) and isinstance(node.test, ast.Compare):
                self.target_nodes.append(node.test)
        return len(self.target_nodes) > 0

    @staticmethod
    def _range_stop_index(args: list) -> int:
        """
        Return the index of the stop argument in range(...):
        - range(stop)                -> 0
        - range(start, stop)         -> 1
        - range(start, stop, step)   -> 1   (do NOT touch step = args[2])
        """
        return 0 if len(args) == 1 else 1

    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        """Modify loop boundary."""
        if not self.can_apply(tree):
            return False

        target_node = ctx.random.choice(self.target_nodes)

        # --- Handle for range(...) upper bound ---
        if isinstance(target_node, ast.Call):
            # Must be builtin range
            if not (isinstance(target_node.func, ast.Name) and target_node.func.id == 'range'):
                return False

            if len(target_node.args) >= 1:
                stop_idx = self._range_stop_index(target_node.args)
                stop_node = target_node.args[stop_idx]

                # Randomly +/- 1
                delta = 1 if ctx.random.random() < 0.5 else -1

                # Constant upper bound: change directly; prevent negative for range(stop)
                if isinstance(stop_node, ast.Constant) and isinstance(stop_node.value, int):
                    old_value = stop_node.value
                    new_value = old_value + delta
                    if stop_idx == 0:
                        new_value = max(0, new_value)  # avoid negatives only for range(stop)
                    stop_node.value = new_value

                    node_line = getattr(target_node, 'lineno', None)
                    ctx.record_mutation(
                        self.name,
                        f"Line {node_line or 'unknown'}: Change range upper bound {old_value} -> {new_value}",
                        node_line
                    )
                    return True

                # Non-constant upper bound: wrap as (stop_expr ± 1)
                try:
                    old_src = ast.unparse(stop_node)
                except Exception:
                    old_src = "<expr>"
                new_expr = ast.BinOp(
                    left=stop_node,
                    op=ast.Add() if delta == 1 else ast.Sub(),
                    right=ast.Constant(value=1)
                )
                target_node.args[stop_idx] = new_expr

                node_line = getattr(target_node, 'lineno', None)
                ctx.record_mutation(
                    self.name,
                    f"Line {node_line or 'unknown'}: Range upper bound modification {old_src} {'+' if delta == 1 else '-'} 1",
                    node_line
                )
                return True

        # --- Handle while loop comparator boundary value ---
        elif isinstance(target_node, ast.Compare):
            # Modify the comparator value, not the comparison operator
            if target_node.ops and len(target_node.comparators) >= 1:
                comp = target_node.comparators[0]
                delta = 1 if ctx.random.random() < 0.5 else -1

                if isinstance(comp, ast.Constant) and isinstance(comp.value, int):
                    old_value = comp.value
                    new_value = old_value + delta
                    comp.value = new_value

                    node_line = getattr(target_node, 'lineno', None)
                    ctx.record_mutation(
                        self.name,
                        f"Line {node_line or 'unknown'}: While-loop boundary modification {old_value} -> {new_value}",
                        node_line
                    )
                    return True

                # Non-constant comparator: wrap as (comp ± 1)
                try:
                    old_src = ast.unparse(comp)
                except Exception:
                    old_src = "<expr>"
                new_expr = ast.BinOp(
                    left=comp,
                    op=ast.Add() if delta == 1 else ast.Sub(),
                    right=ast.Constant(value=1)
                )
                target_node.comparators[0] = new_expr

                node_line = getattr(target_node, 'lineno', None)
                ctx.record_mutation(
                    self.name,
                    f"Line {node_line or 'unknown'}: While-loop boundary modification {old_src} {'+' if delta == 1 else '-'} 1",
                    node_line
                )
                return True

        return False


class FunctionCallParameterMutator(MutationOperator):
    """Function-call argument mutation operator.

    Mutates arguments in function calls.
    """

    def __init__(self):
        super().__init__("FunctionCallParameterMutator")
        self.target_nodes = []

    def can_apply(self, tree: ast.AST) -> bool:
        """Check whether there are function calls eligible for argument mutation."""
        self.target_nodes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and len(node.args) >= 2:
                # Only handle calls with multiple positional arguments
                self.target_nodes.append(node)
        return len(self.target_nodes) > 0

    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        """Mutate function-call arguments."""
        if not self.can_apply(tree):
            return False

        target_node = ctx.random.choice(self.target_nodes)

        # Randomly select a mutation type
        mutation_type = ctx.random.choice(['swap', 'duplicate', 'remove'])

        if mutation_type == 'swap' and len(target_node.args) >= 2:
            # Swap the positions of two arguments
            i, j = ctx.random.sample(range(len(target_node.args)), 2)
            target_node.args[i], target_node.args[j] = target_node.args[j], target_node.args[i]

            node_line = getattr(target_node, 'lineno', None)
            ctx.record_mutation(
                self.name,
                f"Line {node_line or 'unknown'}: Swap call arguments {i} <-> {j}",
                node_line
            )
            return True

        elif mutation_type == 'duplicate' and len(target_node.args) >= 1:
            # Duplicate one argument
            idx = ctx.random.randint(0, len(target_node.args) - 1)
            duplicated_arg = copy.deepcopy(target_node.args[idx])
            target_node.args.append(duplicated_arg)

            node_line = getattr(target_node, 'lineno', None)
            ctx.record_mutation(
                self.name,
                f"Line {node_line or 'unknown'}: Duplicate call argument at index {idx}",
                node_line
            )
            return True

        elif mutation_type == 'remove' and len(target_node.args) >= 2:
            # Remove one argument (keep at least one)
            idx = ctx.random.randint(0, len(target_node.args) - 1)
            target_node.args.pop(idx)

            node_line = getattr(target_node, 'lineno', None)
            ctx.record_mutation(
                self.name,
                f"Line {node_line or 'unknown'}: Remove call argument at index {idx}",
                node_line
            )
            return True

        return False
class DataStructureMutator(MutationOperator):
    """
    Data structure mutation operator.

    Mutates container literal types:
      - List  -> Tuple (with a conservative guard for common list-mutating method usage)
      - Tuple -> List
      - Set   -> List
      - Dict  -> swap keys/values (only when lengths match and non-empty)

    Important safety rule:
      - Never mutate nodes that are part of type annotations (arg annotations, AnnAssign annotations,
        function return annotations). This prevents invalid mutants like Dict[[str, float]].
    """

    def __init__(self):
        super().__init__("DataStructureMutator")
        self.target_nodes: List[ast.AST] = []
        self._annotation_nodes: Set[int] = set()

    # -------------------------
    # Helpers
    # -------------------------
    @staticmethod
    def _any_lineno(node: ast.AST) -> Optional[int]:
        """Best-effort: find a lineno on this node or its descendants."""
        ln = getattr(node, "lineno", None)
        if isinstance(ln, int):
            return ln
        for n in ast.walk(node):
            ln2 = getattr(n, "lineno", None)
            if isinstance(ln2, int):
                return ln2
        return None

    @staticmethod
    def _find_parent_ref(tree: ast.AST, target: ast.AST):
        """Find (parent, field_name, index) such that parent.<field_name>[index] is target
        or parent.<field_name> is target.

        Returns:
            (parent_node, parent_field, parent_index)
            - parent_index is None when the field is not a list.
        """
        for parent in ast.walk(tree):
            for field, value in ast.iter_fields(parent):
                if value is target:
                    return parent, field, None
                if isinstance(value, list):
                    for i, item in enumerate(value):
                        if item is target:
                            return parent, field, i
        return None, None, None

    @staticmethod
    def _replace_child(parent: ast.AST, field: str, index: Optional[int], new_node: ast.AST) -> None:
        """Replace a child node on parent."""
        if index is None:
            setattr(parent, field, new_node)
        else:
            lst = getattr(parent, field)
            lst[index] = new_node

    @staticmethod
    def _list_to_tuple_guard(tree: ast.AST, parent_node: ast.AST, target_node: ast.AST) -> bool:
        """Return True if it is safe(ish) to convert a list literal to a tuple.

        Heuristic: if the list literal is assigned to a variable name, and later we see
        common list-mutating methods called on that variable, skip conversion.
        This is conservative and not scope-aware, but filters many incompatible cases.
        """
        guard_methods = {"append", "extend", "insert", "pop", "remove", "clear", "sort"}

        try:
            if not (isinstance(parent_node, ast.Assign) and getattr(parent_node, "value", None) is target_node):
                return True

            # Collect assigned LHS names
            lhs_names = set()
            for t in getattr(parent_node, "targets", []) or []:
                for sub in ast.walk(t):
                    if isinstance(sub, ast.Name):
                        lhs_names.add(sub.id)

            if not lhs_names:
                return True

            assign_line = getattr(parent_node, "lineno", None)

            # Scan for later mutating calls: x.append(...), x.pop(), etc.
            for call in ast.walk(tree):
                if not isinstance(call, ast.Call):
                    continue
                func = call.func
                if not isinstance(func, ast.Attribute):
                    continue
                if func.attr not in guard_methods:
                    continue
                if not isinstance(func.value, ast.Name):
                    continue
                if func.value.id not in lhs_names:
                    continue

                # Rough "later" check using line numbers when available
                call_ln = getattr(call, "lineno", None)
                if isinstance(assign_line, int) and isinstance(call_ln, int) and call_ln >= assign_line:
                    return False

            return True
        except Exception:
            # If anything goes wrong, be conservative and allow the mutation.
            return True

    def _collect_annotation_nodes(self, tree: ast.AST) -> None:
        """Collect all nodes that appear inside type annotation subtrees."""
        self._annotation_nodes = set()

        def mark_subtree(root: Optional[ast.AST]) -> None:
            if root is None:
                return
            for n in ast.walk(root):
                self._annotation_nodes.add(id(n))

        for node in ast.walk(tree):
            # Variable annotations: x: Dict[str, float] = ...
            if isinstance(node, ast.AnnAssign):
                mark_subtree(node.annotation)

            # Function annotations: def f(x: T) -> R
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                mark_subtree(node.returns)
                for a in node.args.posonlyargs:
                    mark_subtree(getattr(a, "annotation", None))
                for a in node.args.args:
                    mark_subtree(getattr(a, "annotation", None))
                for a in node.args.kwonlyargs:
                    mark_subtree(getattr(a, "annotation", None))
                if node.args.vararg is not None:
                    mark_subtree(getattr(node.args.vararg, "annotation", None))
                if node.args.kwarg is not None:
                    mark_subtree(getattr(node.args.kwarg, "annotation", None))

    def _is_in_annotation(self, node: ast.AST) -> bool:
        """Return True if the node is part of an annotation subtree."""
        return id(node) in self._annotation_nodes

    # -------------------------
    # API: can_apply / apply
    # -------------------------
    def can_apply(self, tree: ast.AST) -> bool:
        """Collect candidate container literal nodes with usable line info."""
        self._collect_annotation_nodes(tree)

        self.target_nodes = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.List, ast.Tuple, ast.Set, ast.Dict)):
                # Skip anything inside type annotations (prevents invalid typing mutants).
                if self._is_in_annotation(node):
                    continue

                # Keep only nodes with a discoverable lineno (helps explain + coverage scoring).
                if self._any_lineno(node) is not None:
                    self.target_nodes.append(node)

        return len(self.target_nodes) > 0

    def apply(self, tree: ast.AST, ctx: "MutationContext") -> bool:
        """Apply a data structure mutation."""
        if not self.can_apply(tree):
            return False

        target_node = ctx.random.choice(self.target_nodes)
        old_type = type(target_node).__name__
        node_line = self._any_lineno(target_node)  # Always derive line from the old node.

        parent_node, parent_field, parent_index = self._find_parent_ref(tree, target_node)
        if parent_node is None:
            return False

        new_node: Optional[ast.AST] = None
        new_type: Optional[str] = None

        # ---- List -> Tuple (guarded) ----
        if isinstance(target_node, ast.List):
            if not self._list_to_tuple_guard(tree, parent_node, target_node):
                return False
            new_node = ast.Tuple(elts=target_node.elts, ctx=target_node.ctx)
            new_type = "Tuple"

        # ---- Tuple -> List ----
        elif isinstance(target_node, ast.Tuple):
            new_node = ast.List(elts=target_node.elts, ctx=target_node.ctx)
            new_type = "List"

        # ---- Set -> List ----
        elif isinstance(target_node, ast.Set):
            new_node = ast.List(elts=target_node.elts, ctx=ast.Load())
            new_type = "List"

        # ---- Dict: swap keys/values ----
        elif isinstance(target_node, ast.Dict):
            if len(target_node.keys) == len(target_node.values) and len(target_node.keys) > 0:
                target_node.keys, target_node.values = target_node.values, target_node.keys

                ctx.record_mutation(
                    self.name,
                    f"Line {node_line or 'unknown'}: swap dictionary keys and values",
                    node_line,
                )
                return True
            return False

        if new_node is None:
            return False

        # Preserve location info so downstream tools keep line mapping.
        ast.copy_location(new_node, target_node)
        ast.fix_missing_locations(new_node)

        self._replace_child(parent_node, parent_field, parent_index, new_node)

        ctx.record_mutation(
            self.name,
            f"Line {node_line or 'unknown'}: change data structure {old_type} -> {new_type}",
            node_line,
        )
        return True

class CodeValidator:
    """CodeValidator"""

    @staticmethod
    def validate_syntax(code: str) -> Tuple[bool, Optional[str]]:
        """Check code syntax.

        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"syntax error: {e}"
        except Exception as e:
            return False, f"validation error: {e}"

    @staticmethod
    def validate_semantics(code: str) -> Tuple[bool, List[str]]:
        """Check code semantics.

        Returns:
            Tuple[bool, List[str]]: (is_valid, error_messages)
        """
        try:
            tree = ast.parse(code)
            validator = SemanticValidator()
            errors = validator.validate(tree)
            return len(errors) == 0, errors
        except Exception as e:
            return False, [f"semantic validation error: {e}"]

    @staticmethod
    def validate_execution(code: str, timeout: int = 5) -> Tuple[bool, Optional[str]]:
        """Validate whether code can execute in a restricted environment.

        Args:
            code: Source code string.
            timeout: Timeout seconds (currently unused in this implementation).

        Returns:
            Tuple[bool, Optional[str]]: (is_executable, error_message)
        """
        try:
            # Create a restricted execution environment
            restricted_globals = {
                '__name__': '__main__',
                '__package__': None,
                '__spec__': None,
                '__doc__': None,
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple,
                    'set': set,
                    # If you need to support imports, you can add: '__import__': __import__
                }
            }

            # Capture outputs
            old_stdout = sys.stdout
            old_stderr = sys.stderr

            try:
                sys.stdout = io.StringIO()
                sys.stderr = io.StringIO()

                # Compile and execute code
                compiled_code = compile(code, '<string>', 'exec')
                exec(compiled_code, restricted_globals)

                return True, None

            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

        except NameError as e:
            return False, f"undefined variable or function: {e}"
        except TypeError as e:
            return False, f"type error: {e}"
        except Exception as e:
            return False, f"execution error: {e}"


class SemanticValidator(ast.NodeVisitor):
    """Semantic validator."""

    def __init__(self):
        self.errors: List[str] = []
        self.defined_vars: Set[str] = set()
        self.defined_funcs: Set[str] = set()
        self.used_vars: Set[str] = set()
        self.used_funcs: Set[str] = set()
        self.scope_stack: List[Set[str]] = [set()]  # Scope stack
        self.current_function: Optional[str] = None  # Current function name

    def validate(self, tree: ast.AST) -> List[str]:
        """Validate an AST tree."""
        self.errors = []
        self.defined_vars = set()
        self.defined_funcs = set()
        self.used_vars = set()
        self.used_funcs = set()
        self.scope_stack = [set()]
        self.current_function = None

        # First pass: collect all function/class definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.defined_funcs.add(node.name)
            elif isinstance(node, ast.ClassDef):
                # A class name can also be called like a constructor
                self.defined_funcs.add(node.name)

        # Second pass: check variable/function uses (triggers visit_*)
        self.visit(tree)

        # Builtins and constants - build a full list of Python builtins
        import builtins as python_builtins
        builtin_functions = {
            name for name in dir(python_builtins)
            if not name.startswith('_') and callable(getattr(python_builtins, name, None))
        }

        # Common builtin constants
        builtin_constants = {
            'True', 'False', 'None', 'Ellipsis', 'NotImplemented'
        }

        # Merge all builtin identifiers (plus implicit runtime globals whitelist)
        builtins = (builtin_functions | builtin_constants | DEFAULT_PY_GLOBALS)

        # Check undefined variables (excluding parameters and locals)
        all_defined_vars = self.defined_vars.copy()
        # Merge all variables from all scopes
        for scope in self.scope_stack:
            all_defined_vars.update(scope)

        undefined_vars = self.used_vars - all_defined_vars - builtins
        for var in undefined_vars:
            # Avoid treating function names as variables
            if var not in self.defined_funcs:
                # If it has "mutated_" prefix, it may be a renamed variable
                # Check if its original name exists
                if var.startswith('mutated_') and '_' in var:
                    # Extract original variable name (format: mutated_originalname_xxxx)
                    parts = var.split('_')
                    if len(parts) >= 3:
                        original_name = parts[1]
                        # If original exists, consider it valid
                        if original_name in all_defined_vars or original_name in builtins:
                            continue
                self.errors.append(f"undefined variable: {var}")

        # Check undefined functions
        undefined_funcs = self.used_funcs - self.defined_funcs - builtins
        for func in undefined_funcs:
            # If it has "mutated_" prefix, it may be a renamed function
            if func.startswith('mutated_') and '_' in func:
                # Extract original function name (format: mutated_originalname_xxxx)
                parts = func.split('_')
                if len(parts) >= 3:
                    original_name = parts[1]
                    # If original exists, consider it valid
                    if original_name in self.defined_funcs or original_name in builtins:
                        continue
            self.errors.append(f"undefined function: {func}")

        return self.errors

    # ======================
    # Scope-related visitors
    # ======================
    def visit_FunctionDef(self, node):
        """Visit a function definition."""
        old_function = self.current_function
        self.current_function = node.name

        # Enter a new scope
        self.scope_stack.append(set())

        # Add parameters to the current scope and to global defined-vars
        for arg in node.args.args:
            self.scope_stack[-1].add(arg.arg)
            self.defined_vars.add(arg.arg)  # Parameters also count as defined variables

        # Visit function body
        self.generic_visit(node)

        # Exit scope
        self.scope_stack.pop()
        self.current_function = old_function

    def visit_ClassDef(self, node):
        """Visit a class definition."""
        # Enter a new scope
        self.scope_stack.append(set())

        # Visit class body
        self.generic_visit(node)

        # Exit scope
        self.scope_stack.pop()

    def visit_Import(self, node: ast.Import):
        """Visit an import statement: import inspect / import inspect as ins."""
        for alias in node.names:
            # name = 'inspect' or 'inspect as ins'
            name = alias.asname or alias.name.split('.')[0]
            self.defined_vars.add(name)
            if self.scope_stack:
                self.scope_stack[-1].add(name)
        # Continue traversing children (usually none, but keep it consistent)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Visit a from-import statement: from inspect import signature as sig."""
        for alias in node.names:
            name = alias.asname or alias.name
            self.defined_vars.add(name)
            if self.scope_stack:
                self.scope_stack[-1].add(name)
        self.generic_visit(node)

    def visit_Name(self, node):
        """Visit a name node."""
        if isinstance(node.ctx, ast.Store):
            # Variable assignment
            self.defined_vars.add(node.id)
            # Add to current scope
            if self.scope_stack:
                self.scope_stack[-1].add(node.id)
        elif isinstance(node.ctx, ast.Load):
            # Variable usage - but exclude function names used in calls
            # Record here first; visit_Call will reclassify function names
            self.used_vars.add(node.id)

    def visit_Call(self, node):
        """Visit a function call."""
        if isinstance(node.func, ast.Name):
            # This is a function call; remove it from used_vars and add to used_funcs
            func_name = node.func.id
            self.used_funcs.add(func_name)
            if func_name in self.used_vars:
                self.used_vars.discard(func_name)

        # Visit arguments
        for arg in node.args:
            self.visit(arg)
        for keyword in node.keywords:
            self.visit(keyword.value)


class CoverageGuidedStrategy:
    """Coverage-guided mutation strategy (line-based).

    Uses executed_lines (a set) to prioritize operators whose target nodes/functions
    intersect with covered lines.
    """

    def __init__(self, coverage_data: Optional[Dict] = None):
        # Expect coverage_data like {"executed_lines": set([...])}
        lines = set()
        if coverage_data and isinstance(coverage_data, dict):
            raw = coverage_data.get("executed_lines")
            if isinstance(raw, (set, list)):
                lines = set(raw)
        self.executed_lines: Set[int] = lines

    def _node_lineno_in_coverage(self, node: ast.AST) -> bool:
        ln = getattr(node, "lineno", None)
        return isinstance(ln, int) and ln in self.executed_lines

    def _function_body_has_coverage(self, func: ast.AST) -> bool:
        for n in ast.walk(func):
            ln = getattr(n, "lineno", None)
            if isinstance(ln, int) and ln in self.executed_lines:
                return True
        return False

    def prioritize_operators(self, operators: List[MutationOperator], tree: ast.AST) -> List[MutationOperator]:
        """Sort mutation operators by coverage affinity."""
        operator_scores: List[Tuple[MutationOperator, float]] = []
        for op in operators:
            if not op.can_apply(tree):
                continue

            score = float(op.weight)

            # For operators with target_nodes: count covered targets
            if hasattr(op, 'target_nodes') and isinstance(getattr(op, 'target_nodes'), list):
                covered_targets = 0
                for n in getattr(op, 'target_nodes'):
                    try:
                        if self._node_lineno_in_coverage(n):
                            covered_targets += 1
                    except Exception:
                        pass
                if covered_targets > 0:
                    score *= (1.0 + covered_targets * 0.5)

            # For VariableRenameMutator / ParamRenameMutator: boost if candidate function bodies have coverage
            from_types = (VariableRenameMutator, ParamRenameMutator)
            if isinstance(op, from_types):
                try:
                    covered_funcs = 0
                    for fn, _name in op.candidates:
                        if self._function_body_has_coverage(fn):
                            covered_funcs += 1
                    if covered_funcs > 0:
                        score *= (1.0 + covered_funcs * 0.5)
                except Exception:
                    pass

            operator_scores.append((op, score))

        operator_scores.sort(key=lambda x: x[1], reverse=True)
        return [op for op, _ in operator_scores]


class DependencyGuidedStrategy:
    """Dependency-guided mutation strategy.

    The user provides a list of dependency identifiers (function/variable/attribute names).
    If any operators match these dependencies, restrict each mutation step to those operators;
    otherwise, fall back to the original operator set.
    """

    def __init__(self, dependencies: Optional[List[str]] = None):
        deps: Set[str] = set()
        if dependencies:
            for d in dependencies:
                if isinstance(d, str):
                    s = d.strip().lower()
                    if s:
                        deps.add(s)
        self.dependencies: Set[str] = deps

    @staticmethod
    def _normalize(s: str) -> str:
        return str(s).strip().lower()

    def _node_matches_deps(self, node: ast.AST) -> bool:
        try:
            return MutationOperator.match_dependencies(node, self.dependencies)
        except Exception:
            return False

    def _operator_has_dep_affinity(self, op: MutationOperator, tree: ast.AST) -> bool:
        # Ensure can_apply has been called to populate target_nodes/candidates
        if hasattr(op, 'can_apply') and not op.can_apply(tree):
            return False

        # For operators with target_nodes
        if hasattr(op, 'target_nodes') and isinstance(getattr(op, 'target_nodes'), list):
            for n in getattr(op, 'target_nodes'):
                if MutationOperator.match_dependencies(n, self.dependencies):
                    return True

                # Dependency-hit enhancement: affinity to Assign LHS for data-structure literal mutations
                if isinstance(op, DataStructureMutator):
                    try:
                        for parent in ast.walk(tree):
                            if isinstance(parent, ast.Assign) and getattr(parent, 'value', None) is n:
                                # Collect LHS identifiers (supports unpacking/multi-target)
                                lhs_ids: Set[str] = set()
                                for t in getattr(parent, 'targets', []) or []:
                                    for sub in ast.walk(t):
                                        if isinstance(sub, ast.Name):
                                            lhs_ids.add(MutationOperator._normalize_dep(sub.id))
                                if any(id_ in self.dependencies for id_ in lhs_ids):
                                    return True
                    except Exception:
                        pass

        # Generic handling for operators with candidates (node or node-tuples)
        if hasattr(op, 'candidates') and isinstance(getattr(op, 'candidates'), list):
            try:
                for c in getattr(op, 'candidates'):
                    nodes = []
                    if isinstance(c, ast.AST):
                        nodes.append(c)
                    elif isinstance(c, (tuple, list)):
                        for part in c:
                            if isinstance(part, ast.AST):
                                nodes.append(part)
                    for n in nodes:
                        if MutationOperator.match_dependencies(n, self.dependencies):
                            return True
            except Exception:
                pass

        # VariableRenameMutator affinity (function name / variable name)
        if isinstance(op, VariableRenameMutator):
            try:
                for fn, name in op.candidates:
                    if MutationOperator._normalize_dep(name) in self.dependencies:
                        return True
                    fn_name = getattr(fn, 'name', '')
                    if isinstance(fn_name, str) and MutationOperator._normalize_dep(fn_name) in self.dependencies:
                        return True
            except Exception:
                pass

        # ParamRenameMutator affinity (function name / parameter name)
        if isinstance(op, ParamRenameMutator):
            try:
                for fn, name in op.candidates:
                    if MutationOperator._normalize_dep(name) in self.dependencies:
                        return True
                    fn_name = getattr(fn, 'name', '')
                    if isinstance(fn_name, str) and MutationOperator._normalize_dep(fn_name) in self.dependencies:
                        return True
            except Exception:
                pass

        return False

    def prioritize_operators(self, operators: List[MutationOperator], tree: ast.AST) -> List[MutationOperator]:
        if not self.dependencies:
            return operators

        dep_ops: List[MutationOperator] = []
        for op in operators:
            try:
                if self._operator_has_dep_affinity(op, tree):
                    dep_ops.append(op)
            except Exception:
                continue

        # If any dependency-hitting operators exist, restrict to them for this step
        return dep_ops if dep_ops else operators


class SemanticAwareStrategy:
    """Semantic-aware mutation strategy."""

    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()

    def select_meaningful_mutations(
        self,
        operators: List[MutationOperator],
        tree: ast.AST,
        ctx: MutationContext
    ) -> List[MutationOperator]:
        """Select semantically meaningful mutation operators."""
        semantic_info = self.semantic_analyzer.analyze(tree)

        meaningful_ops = []
        for op in operators:
            if op.can_apply(tree):
                meaningfulness = self._assess_meaningfulness(op, semantic_info, tree)
                if meaningfulness > 0.3:  # Threshold
                    meaningful_ops.append(op)

        return meaningful_ops

    def _assess_meaningfulness(self, operator: MutationOperator, semantic_info: Dict, tree: ast.AST) -> float:
        """Assess semantic meaningfulness of a mutation."""
        base_score = 0.5

        # Adjust score based on operator type and code features
        if isinstance(operator, ArithmeticOperatorMutator):
            # Arithmetic mutations are more meaningful if code contains arithmetic computations
            if semantic_info.get('has_arithmetic', False):
                base_score += 0.3

        elif isinstance(operator, BooleanConditionFlipMutator):
            # Condition flips are more meaningful if code contains conditionals
            if semantic_info.get('has_conditionals', False):
                base_score += 0.4

        elif isinstance(operator, LoopBoundaryMutator):
            # Boundary mutations are more meaningful if code contains loops
            if semantic_info.get('has_loops', False):
                base_score += 0.3

        return min(1.0, base_score)


class SemanticAnalyzer:
    """Semantic analyzer."""

    def analyze(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze semantic features of code."""
        analyzer = SemanticVisitor()
        analyzer.visit(tree)
        return analyzer.get_analysis_result()


class SemanticVisitor(ast.NodeVisitor):
    """Semantic visitor."""

    def __init__(self):
        self.has_arithmetic = False
        self.has_conditionals = False
        self.has_loops = False
        self.has_functions = False
        self.has_classes = False
        self.complexity_score = 0

    def visit_BinOp(self, node):
        """Visit a binary operation."""
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            self.has_arithmetic = True
            self.complexity_score += 1
        self.generic_visit(node)

    def visit_If(self, node):
        """Visit an if statement."""
        self.has_conditionals = True
        self.complexity_score += 2
        self.generic_visit(node)

    def visit_For(self, node):
        """Visit a for loop."""
        self.has_loops = True
        self.complexity_score += 3
        self.generic_visit(node)

    def visit_While(self, node):
        """Visit a while loop."""
        self.has_loops = True
        self.complexity_score += 3
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """Visit a function definition."""
        self.has_functions = True
        self.complexity_score += 2
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Visit a class definition."""
        self.has_classes = True
        self.complexity_score += 4
        self.generic_visit(node)

    def get_analysis_result(self) -> Dict[str, Any]:
        """Return the analysis result."""
        return {
            'has_arithmetic': self.has_arithmetic,
            'has_conditionals': self.has_conditionals,
            'has_loops': self.has_loops,
            'has_functions': self.has_functions,
            'has_classes': self.has_classes,
            'complexity_score': self.complexity_score
        }

        return False


class NumberSignFlipMutator(MutationOperator):
    """
    Numeric sign-flip mutation operator.

    - Target: int / float constants (excluding bool)
    - Behavior: v -> -v
      Examples:
        42      -> -42
        -3.5    -> -(-3.5) == 3.5

    - Dependency/Coverage prioritization:
        1. If ctx.priority_dependencies is provided:
           prefer constants that match dependencies (either the constant itself or its parent node).
        2. If ctx.coverage_info is provided:
           prefer constants on covered lines.
    """

    def __init__(self):
        # You can also add weight: super().__init__("NumberSignFlipMutator", weight=1.1)
        super().__init__("NumberSignFlipMutator")
        # Each candidate is (const_node, parent_node)
        self.candidates: List[Tuple[ast.Constant, Optional[ast.AST]]] = []
        self._parent_map: dict[int, ast.AST] = {}

    # ---------- Internal helpers ----------

    def _build_parent_map(self, tree: ast.AST) -> None:
        """Build child -> parent map for later dependency matching."""
        self._parent_map = {}

        def visit(node: ast.AST):
            for child in ast.iter_child_nodes(node):
                self._parent_map[id(child)] = node
                visit(child)

        visit(tree)

    def _get_parent(self, node: ast.AST) -> Optional[ast.AST]:
        return self._parent_map.get(id(node))

    def _is_numeric_constant(self, node: ast.AST) -> bool:
        """Return True if node is a flippable numeric constant (int/float, but not bool)."""
        if not isinstance(node, ast.Constant):
            return False
        val = node.value
        # bool is a subclass of int, must exclude first
        if isinstance(val, bool):
            return False
        return isinstance(val, (int, float))

    # ---------- MutationOperator API ----------

    def can_apply(self, tree: ast.AST) -> bool:
        """Collect all numeric constants that can be sign-flipped and record their parents."""
        self.candidates = []
        self._build_parent_map(tree)

        for node in ast.walk(tree):
            if not self._is_numeric_constant(node):
                continue
            if MutationOperator.should_skip_node(node):
                continue
            parent = self._get_parent(node)
            self.candidates.append((node, parent))

        return len(self.candidates) > 0

    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        """Pick a candidate by dependency/coverage priority and flip its sign."""
        if not self.can_apply(tree):
            return False

        deps: Set[str] = set(getattr(ctx, "priority_dependencies", set()) or set())
        coverage_lines: Set[int] = set(getattr(ctx, "coverage_info", set()) or set())

        cands: List[Tuple[ast.Constant, Optional[ast.AST]]] = self.candidates

        # 1) Dependency priority: match either the constant node or its parent
        if deps:
            dep_pref: List[Tuple[ast.Constant, Optional[ast.AST]]] = []
            for const_node, parent in cands:
                if MutationOperator.match_dependencies(const_node, deps):
                    dep_pref.append((const_node, parent))
                    continue
                if parent is not None and MutationOperator.match_dependencies(parent, deps):
                    dep_pref.append((const_node, parent))
            if dep_pref:
                cands = dep_pref

        # 2) Coverage priority: prefer constants with lineno in coverage_lines
        if coverage_lines:
            covered: List[Tuple[ast.Constant, Optional[ast.AST]]] = []
            for const_node, parent in cands:
                ln = getattr(const_node, "lineno", None)
                if isinstance(ln, int) and ln in coverage_lines:
                    covered.append((const_node, parent))
            if covered:
                cands = covered

        if not cands:
            return False

        const_node, parent = ctx.random.choice(cands)
        old_val = const_node.value

        try:
            new_val = -old_val
        except Exception:
            return False

        const_node.value = new_val
        lineno = getattr(const_node, "lineno", None)

        # Try to include some context for easier debugging
        try:
            snippet = ast.unparse(parent or const_node)
        except Exception:
            snippet = ""

        ctx.record_mutation(
            self.name,
            f"Line {lineno or 'unknown'}: Numeric constant sign inversion {old_val} -> {new_val}"
            + (f" in `{snippet}`" if snippet else ""),
            lineno,
        )
        return True


class ComparisonOperatorMutator(MutationOperator):
    """Comparison operator replacement mutation operator."""

    OPERATOR_MAP = {
        ast.Eq: [ast.NotEq, ast.Lt, ast.Gt],
        ast.NotEq: [ast.Eq, ast.Lt, ast.Gt],
        ast.Lt: [ast.Gt, ast.LtE, ast.GtE],
        ast.Gt: [ast.Lt, ast.LtE, ast.GtE],
        ast.LtE: [ast.GtE, ast.Lt, ast.Gt],
        ast.GtE: [ast.LtE, ast.Lt, ast.Gt],
    }

    def __init__(self):
        super().__init__("ComparisonOperatorMutator")
        self.target_nodes = []

    def can_apply(self, tree: ast.AST) -> bool:
        """Check if there are comparable operators to mutate (skip entrypoint sentinels, etc.)."""
        self.target_nodes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                # Skip entrypoint sentinels / protected nodes, e.g., if __name__ == "__main__":
                try:
                    if MutationOperator.should_skip_node(node):
                        continue
                except Exception:
                    # Defensive: do not let exceptions break traversal
                    pass
                for op in node.ops:
                    if type(op) in self.OPERATOR_MAP:
                        self.target_nodes.append((node, op))
        return len(self.target_nodes) > 0

    def apply(self, tree: ast.AST, ctx: MutationContext) -> bool:
        if not self.can_apply(tree):
            return False

        # Filter again in case external state changes caused unsafe choices
        eligible: list[tuple[ast.Compare, ast.cmpop]] = []
        for compare_node, old_op in self.target_nodes:
            try:
                if MutationOperator.should_skip_node(compare_node):
                    continue
            except Exception:
                # If an exception happens, treat it as eligible to avoid over-blocking
                pass
            eligible.append((compare_node, old_op))

        if not eligible:
            return False

        # Randomly choose a target
        compare_node, old_op = ctx.random.choice(eligible)
        old_op_type = type(old_op)

        # Randomly choose a replacement operator
        new_op_class = ctx.random.choice(self.OPERATOR_MAP[old_op_type])

        # Replace the operator in-place
        for i, op in enumerate(compare_node.ops):
            if op is old_op:
                compare_node.ops[i] = new_op_class()
                break

        # Record mutation
        node_line = getattr(compare_node, 'lineno', None)
        ctx.record_mutation(
            self.name,
            f"Line {node_line or 'unknown'}: Comparison operator replacement {old_op_type.__name__} -> {new_op_class.__name__}",
            node_line
        )
        return True


@dataclass
class MutationGraph:
    """Mutation graph that manages mutation operators and performs random walks."""

    operators: List[MutationOperator] = field(default_factory=list)
    coverage_strategy: Optional[CoverageGuidedStrategy] = field(default=None)
    semantic_strategy: Optional[SemanticAwareStrategy] = field(default=None)
    dependency_strategy: Optional[DependencyGuidedStrategy] = field(default=None)
    enable_validation: bool = field(default=True)

    def add_operator(self, operator: MutationOperator):
        """Add a mutation operator."""
        self.operators.append(operator)

    def get_applicable_operators(self, tree: ast.AST) -> List[MutationOperator]:
        """Get all applicable mutation operators."""
        return [op for op in self.operators if op.can_apply(tree)]

    def random_walk(self, tree: ast.AST, steps: int, ctx: MutationContext) -> ast.AST:
        """Perform random-walk-based mutation.

        Args:
            tree: The original AST.
            steps: Number of mutation steps.
            ctx: Mutation context.

        Returns:
            The mutated AST.
        """
        mutated_tree = copy.deepcopy(tree)
        successful_mutations = 0

        for step in range(steps):
            applicable_ops = self.get_applicable_operators(mutated_tree)

            if not applicable_ops:
                print(f"Step {step + 1}: No applicable mutation operators, terminating early")
                break

            # Dependency-guided prioritization:
            # If dependency-hitting operators exist, restrict selection to this subset
            if self.dependency_strategy:
                applicable_ops = self.dependency_strategy.prioritize_operators(
                    applicable_ops, mutated_tree
                )

            # Apply coverage-guided mutation strategy
            if self.coverage_strategy:
                applicable_ops = self.coverage_strategy.prioritize_operators(
                    applicable_ops, mutated_tree
                )

            # Apply semantic-aware mutation filtering
            if self.semantic_strategy:
                applicable_ops = self.semantic_strategy.select_meaningful_mutations(
                    applicable_ops, mutated_tree, ctx
                )

            if not applicable_ops:
                print(f"Step {step + 1}: No operators available after strategy filtering")
                continue

            # Select a mutation operator based on weights
            weights = [op.weight for op in applicable_ops]
            selected_op = ctx.random.choices(applicable_ops, weights=weights)[0]

            # Backup the AST before mutation
            backup_tree = copy.deepcopy(mutated_tree) if self.enable_validation else None

            # Apply the mutation
            success = selected_op.apply(mutated_tree, ctx)

            if success and self.enable_validation:
                # Validate the mutated code
                mutated_code = ast.unparse(mutated_tree)
                is_valid, error_msg = self._validate_mutation(mutated_code)

                if not is_valid:
                    print(f"Step {step + 1}: Invalid mutation ({error_msg}), rolling back")
                    # Roll back to the state before mutation
                    mutated_tree = backup_tree
                    # Remove the invalid mutation record
                    if ctx.applied_mutations:
                        ctx.applied_mutations.pop()
                        ctx.mutation_count -= 1
                    continue

            if success:
                successful_mutations += 1
                print(f"Step {step + 1}: Successfully applied {selected_op.name}")
            else:
                print(f"Step {step + 1}: Failed to apply mutation operator {selected_op.name}")

        print(f"Mutation completed: {successful_mutations}/{steps} mutations successfully applied")
        return mutated_tree

    def _validate_mutation(self, code: str) -> Tuple[bool, Optional[str]]:
        """Validate mutated code."""
        # Syntax validation
        syntax_valid, syntax_error = CodeValidator.validate_syntax(code)
        if not syntax_valid:
            return False, f"syntax error: {syntax_error}"

        # Semantic validation
        semantic_valid, semantic_errors = CodeValidator.validate_semantics(code)
        if not semantic_valid:
            return False, f"semantic error: {'; '.join(semantic_errors[:3])}"  # show only first 3 errors

        return True, None


def create_default_mutation_graph() -> MutationGraph:
    """Create the default mutation graph."""
    graph = MutationGraph()

    # Add default mutation operators
    graph.add_operator(ArithmeticOperatorMutator())
    graph.add_operator(VariableRenameMutator())
    graph.add_operator(ParamRenameMutator())
    graph.add_operator(StatementDeletionMutator())
    graph.add_operator(ComparisonOperatorMutator())

    # Add additional mutation operators
    graph.add_operator(BooleanConditionFlipMutator())
    graph.add_operator(LoopBoundaryMutator())
    graph.add_operator(FunctionCallParameterMutator())
    graph.add_operator(DataStructureMutator())
    graph.add_operator(NumberSignFlipMutator())

    return graph


def mutate_code(
    source_code: str,
    steps: int = 3,
    seed: Optional[int] = None,
    custom_operators: Optional[List[MutationOperator]] = None,
    validate: bool = False,
    use_coverage_strategy: bool = False,
    use_semantic_strategy: bool = False,
    coverage_data: Optional[Dict] = None,
    priority_dependencies: Optional[List[str]] = None
) -> Tuple[str, List[Dict]]:
    """Main API to mutate Python source code.

    Args:
        source_code: Source code string.
        steps: Number of mutation steps.
        seed: Random seed.
        custom_operators: Custom mutation operators.
        validate: Whether to enable validation (default: False).
        use_coverage_strategy: Whether to use coverage-guided strategy.
        use_semantic_strategy: Whether to use semantic-aware strategy.
        coverage_data: Coverage data.

    Returns:
        Tuple[str, List[Dict]]: (mutated_code, mutation_records)
    """
    try:
        # Parse source code into an AST
        tree = ast.parse(source_code)

        # Create mutation context
        ctx = MutationContext(seed)

        # Inject coverage info into context for operators to consume
        if coverage_data and isinstance(coverage_data, dict):
            lines = coverage_data.get('executed_lines')
            if isinstance(lines, (set, list)):
                ctx.coverage_info = set(lines)

        # Inject dependency guidance set (case-insensitive)
        if priority_dependencies:
            try:
                deps_norm = {str(d).strip().lower() for d in priority_dependencies if isinstance(d, str) and d.strip()}
                ctx.priority_dependencies = deps_norm
            except Exception:
                ctx.priority_dependencies = set()

        # Create mutation graph
        if custom_operators:
            graph = MutationGraph(enable_validation=validate)
            for op in custom_operators:
                graph.add_operator(op)
        else:
            graph = create_default_mutation_graph()
            graph.enable_validation = validate

        # Configure dependency-guided strategy (highest priority)
        if priority_dependencies:
            graph.dependency_strategy = DependencyGuidedStrategy(priority_dependencies)

        # Configure optional strategies
        if use_coverage_strategy:
            graph.coverage_strategy = CoverageGuidedStrategy(coverage_data)

        if use_semantic_strategy:
            graph.semantic_strategy = SemanticAwareStrategy()

        # Run mutation
        mutated_tree = graph.random_walk(tree, steps, ctx)

        # Convert AST back to source code
        mutated_code = ast.unparse(mutated_tree)

        return mutated_code, ctx.applied_mutations

    except SyntaxError as e:
        raise ValueError(f"original code syntax error: {e}")
    except Exception as e:
        raise RuntimeError(f"error during mutation: {e}")


def smart_mutate_code(
    source_code: str,
    steps: int = 3,
    seed: Optional[int] = None,
    validate: bool = False,
    coverage_data: Optional[Dict] = None,
    priority_dependencies: Optional[List[str]] = None
) -> Tuple[str, List[Dict]]:
    """Smart mutation: combines coverage-guided and semantic-aware strategies.

    Args:
        source_code: Source code string.
        steps: Number of mutation steps.
        seed: Random seed.
        validate: Whether to enable validation (default: False).
        coverage_data: Coverage data.

    Returns:
        Tuple[str, List[Dict]]: (mutated_code, mutation_records)
    """
    return mutate_code(
        source_code=source_code,
        steps=steps,
        seed=seed,
        validate=validate,
        use_coverage_strategy=True,
        use_semantic_strategy=True,
        coverage_data=coverage_data,
        priority_dependencies=priority_dependencies
    )


def analyze_code_complexity(source_code: str) -> Dict[str, int]:
    """Analyze code complexity to guide mutation strategies."""
    try:
        tree = ast.parse(source_code)

        stats = {
            'statements': 0,
            'functions': 0,
            'classes': 0,
            'variables': 0,
            'operators': 0,
            'loops': 0,
            'conditionals': 0
        }

        variables = set()

        for node in ast.walk(tree):
            if isinstance(node, (ast.Assign, ast.AugAssign, ast.Expr)):
                stats['statements'] += 1
            elif isinstance(node, ast.FunctionDef):
                stats['functions'] += 1
            elif isinstance(node, ast.ClassDef):
                stats['classes'] += 1
            elif isinstance(node, ast.Name):
                variables.add(node.id)
            elif isinstance(node, (ast.BinOp, ast.Compare, ast.BoolOp)):
                stats['operators'] += 1
            elif isinstance(node, (ast.For, ast.While)):
                stats['loops'] += 1
            elif isinstance(node, ast.If):
                stats['conditionals'] += 1

        stats['variables'] = len(variables)
        return stats

    except SyntaxError:
        return {}


if __name__ == "__main__":
    # Simple test example
    test_code = '''
def calculate(x, y):
    result = x + y * 2
    if result > 10:
        result = result - 1
    return result

def main():
    a = 5
    b = 3
    print(calculate(a, b))
'''

    print("Original code:")
    print(test_code)
    print("\n" + "=" * 50 + "\n")

    # Run mutations
    mutated_code, mutations = mutate_code(test_code, steps=3, seed=42)

    print("Mutated code:")
    print(mutated_code)
    print("\n" + "=" * 30 + "\n")

    print("Mutation records:")
    for mutation in mutations:
        print(f"Step {mutation['step'] + 1}: {mutation['operator']} - {mutation['node']}")