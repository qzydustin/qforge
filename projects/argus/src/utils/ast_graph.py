from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ASTGraph:
    """Simple AST graph representation for visualization.

    Attributes:
        nodes: List of node records, each containing:
            - id: stable integer node id
            - type: AST node type name
            - lineno: optional line number
            - col_offset: optional column offset
            - snippet: short unparsed code snippet for the node
        edges: Parent-child edges using node ids.
        lineno_to_node_ids: Mapping from line number to sorted list of node ids.
    """

    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, int]]
    lineno_to_node_ids: Dict[int, List[int]]


def _safe_unparse(node: ast.AST) -> str:
    """Best-effort ast.unparse with graceful fallback."""
    try:
        snippet = ast.unparse(node)  # type: ignore[attr-defined]
    except Exception:
        snippet = type(node).__name__
    text = str(snippet).replace("\n", " ")
    if len(text) > 120:
        return text[:117] + "..."
    return text


def build_ast_graph(source_code: str) -> ASTGraph:
    """Build a simple AST graph from source code.

    The graph is stable and deterministic for the same input source.
    Node ids are assigned in pre-order traversal.
    """
    tree = ast.parse(source_code)

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, int]] = []
    lineno_to_node_ids: Dict[int, List[int]] = {}

    counter = 1

    def visit(node: ast.AST, parent_id: Optional[int]) -> int:
        nonlocal counter
        node_id = counter
        counter += 1

        lineno = getattr(node, "lineno", None)
        col = getattr(node, "col_offset", None)
        record: Dict[str, Any] = {
            "id": node_id,
            "type": type(node).__name__,
            "lineno": lineno,
            "col_offset": col,
            "snippet": _safe_unparse(node),
        }
        nodes.append(record)

        if isinstance(lineno, int):
            lineno_to_node_ids.setdefault(lineno, []).append(node_id)

        if parent_id is not None:
            edges.append({"source": parent_id, "target": node_id})

        for child in ast.iter_child_nodes(node):
            visit(child, node_id)

        return node_id

    visit(tree, None)

    # Ensure deterministic ordering within each line bucket
    for line, ids in lineno_to_node_ids.items():
        ids.sort()

    return ASTGraph(nodes=nodes, edges=edges, lineno_to_node_ids=lineno_to_node_ids)


def map_lineno_to_node_id(graph: ASTGraph, lineno: Optional[int]) -> Optional[int]:
    """Return a stable node id for a given line number.

    If multiple nodes share the same line, the smallest node id is used.
    """
    if lineno is None:
        return None
    ids = graph.lineno_to_node_ids.get(lineno)
    if not ids:
        return None
    return ids[0]


def export_graph_json(graph: ASTGraph, mutation_path: List[int], meta: Dict[str, Any]) -> Dict[str, Any]:
    """Build the JSON-serializable graph structure used by graph.html."""
    return {
        "nodes": graph.nodes,
        "edges": graph.edges,
        "mutation_path": mutation_path,
        "meta": meta,
    }
