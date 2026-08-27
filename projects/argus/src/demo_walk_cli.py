#!/usr/bin/env python3
"""Demo CLI for controllable / explainable / reproducible mutation walks.

This script exposes three main demo modes over the same input file:

  1) Random walk:
       --walk random --policy random
  2) Coverage-guided walk:
       --walk guided --policy coverage
  3) Composite guided walk (coverage + semantic + dependency priority):
       --walk guided --policy composite --target-api score_user

Outputs for each run are written to:

  outputs/<policy>/<timestamp>/

with the following files:
  - manifest.json  (run manifest + path + validation metadata)
  - explain.json   (per-step ExplainEvent export)
  - graph.json     (AST graph + highlighted path)
  - graph.html     (lightweight viewer for graph.json)
  - graph_tree_steps.html (tree viewer with step sidebar)
  - mutated.py     (mutated source code)
  - run_manifest.txt (exact command line and parameters)
"""

from __future__ import annotations

import argparse
import inspect
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from codemutationengine.demo_walk_engine import (
    compute_static_executed_lines,
    compute_coverage_hash,
    run_guided_demo,
)
from codemutationengine.utils.coverage_manager import CoverageManager


def _canon_path(p: Path) -> str:
    """Canonical absolute path for stable coverage measurement and key lookup."""
    return os.path.realpath(os.path.abspath(str(p)))


def _collect_executed_lines(input_path: Path, source: str, policy: str) -> Tuple[Set[int], Dict[str, Any]]:
    """Collect executed line numbers + metadata.

    If the `coverage` package is available and policy uses coverage, we run the file once
    under coverage and derive executed lines. Otherwise we fall back to a static approximation
    based on AST statement locations.

    Returns:
        executed_lines: set[int]
        meta: {
          "coverage_source": "coverage" | "static",
          "coverage_percent": float,
          (optional) "coverage_run_error": str,
          (optional) "coverage_fallback_reason": str
        }
    """
    cm = CoverageManager()

    # If the policy doesn't use coverage, avoid runtime measurement.
    if policy not in {"coverage", "composite"}:
        executed_static = compute_static_executed_lines(source)
        return executed_static, {
            "coverage_source": "static",
            "coverage_percent": 0.0,
            "coverage_fallback_reason": f"policy={policy} does not use runtime coverage",
        }

    if not cm.is_available():
        executed_static = compute_static_executed_lines(source)
        return executed_static, {
            "coverage_source": "static",
            "coverage_percent": 0.0,
            "coverage_fallback_reason": "coverage package not available",
        }

    abs_input = cm._canon_path(str(input_path))

    try:
        cm.start()
        run_err = cm.run_file(abs_input)
        cov_json = cm.stop_and_analyze(abs_input)

        extracted = CoverageManager.extract_executed_lines(cov_json, abs_input)
        if extracted:
            key_path, executed_raw = extracted

            executed_int: Set[int] = set()
            for x in executed_raw:
                try:
                    executed_int.add(int(x))
                except Exception:
                    continue

            percent = 0.0
            try:
                key = cm._canon_path(key_path)
                percent = float(cov_json["files"][key]["summary"]["percent"])
            except Exception:
                percent = 0.0

            meta: Dict[str, Any] = {
                "coverage_source": "coverage",
                "coverage_percent": percent,
            }
            if run_err:
                meta["coverage_run_error"] = run_err

            if executed_int:
                return executed_int, meta

            executed_static = compute_static_executed_lines(source)
            meta["coverage_source"] = "static"
            meta["coverage_percent"] = 0.0
            meta["coverage_fallback_reason"] = "runtime coverage returned empty executed_lines"
            return executed_static, meta

        executed_static = compute_static_executed_lines(source)
        return executed_static, {
            "coverage_source": "static",
            "coverage_percent": 0.0,
            "coverage_fallback_reason": "coverage JSON did not contain an entry for the input file",
            **({"coverage_run_error": run_err} if run_err else {}),
        }

    except Exception as e:
        executed_static = compute_static_executed_lines(source)
        return executed_static, {
            "coverage_source": "static",
            "coverage_percent": 0.0,
            "coverage_fallback_reason": f"coverage exception: {type(e).__name__}: {e}",
        }


def _write_json(path: Path, data: Any) -> None:
    """Write JSON to disk (pretty-printed, UTF-8)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


GRAPH_HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>AST Graph Viewer</title>
  <style>
    body { font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 0; }
    header { padding: 12px 16px; background: #f5f5f5; border-bottom: 1px solid #ddd; }
    #meta { font-size: 13px; color: #555; }
    #graph { width: 100vw; height: calc(100vh - 52px); }
    .node circle { stroke: #888; stroke-width: 1px; fill: #fff; }
    .node text { font-size: 11px; pointer-events: none; }
    .node.mutated circle { fill: #ffcc00; stroke: #cc9900; stroke-width: 2px; }
    line.link { stroke: #aaa; stroke-width: 1px; }
  </style>
  <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
  <header>
    <div id="meta">Loading graph metadata...</div>
  </header>
  <svg id="graph"></svg>
  <script>
    const svg = d3.select('#graph');
    const width = window.innerWidth;
    const height = window.innerHeight - 52;
    svg.attr('width', width).attr('height', height);

    fetch('graph.json').then(r => r.json()).then(data => {
      const nodes = data.nodes.map(d => Object.assign({}, d));
      const links = data.edges.map(d => ({ source: d.source, target: d.target }));
      const pathIds = new Set(data.mutation_path || []);

      document.getElementById('meta').textContent = `File: ${data.meta.input_file}  |  Policy: ${data.meta.policy}  |  Walk: ${data.meta.walk}  |  Seed: ${data.meta.seed}`;

      const idToNode = new Map();
      nodes.forEach(n => idToNode.set(n.id, n));
      const simLinks = links
        .map(l => ({ source: idToNode.get(l.source), target: idToNode.get(l.target) }))
        .filter(l => l.source && l.target);

      const simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(simLinks).id(d => d.id).distance(60).strength(0.6))
        .force('charge', d3.forceManyBody().strength(-120))
        .force('center', d3.forceCenter(width / 2, height / 2));

      const link = svg.append('g')
        .attr('stroke', '#aaa')
        .attr('stroke-opacity', 0.6)
        .selectAll('line')
        .data(simLinks)
        .enter().append('line')
        .attr('class', 'link');

      const node = svg.append('g')
        .selectAll('g')
        .data(nodes)
        .enter().append('g')
        .attr('class', d => pathIds.has(d.id) ? 'node mutated' : 'node')
        .call(d3.drag()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended));

      node.append('circle')
        .attr('r', d => pathIds.has(d.id) ? 10 : 6);

      node.append('title').text(d => `${d.type}@${d.lineno || '?'}: ${d.snippet}`);

      node.append('text')
        .attr('x', 10)
        .attr('y', 3)
        .text(d => d.type);

      simulation.on('tick', () => {
        link
          .attr('x1', d => d.source.x)
          .attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x)
          .attr('y2', d => d.target.y);

        node.attr('transform', d => `translate(${d.x},${d.y})`);
      });

      function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
      }

      function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
    }).catch(err => {
      document.getElementById('meta').textContent = 'Failed to load graph.json: ' + err;
    });
  </script>
</body>
</html>
"""


GRAPH_TREE_STEPS_HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AST Graph Viewer</title>
  <style>
    :root{
      --border:#e6e6e6;
      --bg:#fafafa;
      --card:#ffffff;
      --text:#222;
      --mut:#ffcc00;
      --mut-stroke:#cc9900;
      --active:#ff6a00;
      --faint:#bbb;

      --shadow: 0 10px 28px rgba(0,0,0,0.10);
      --shadow-soft: 0 6px 16px rgba(0,0,0,0.06);
      --radius: 12px;
      --radius2: 10px;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono","Courier New", monospace;
    }

    body{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      margin:0; padding:0;
      color:var(--text);
      background:#fff;
    }

    header{
      padding: 10px 14px;
      background:#f5f5f5;
      border-bottom: 1px solid var(--border);
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
    }

    #meta{
      font-size: 13px;
      color:#555;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    #controls{
      display:flex;
      align-items:center;
      gap:12px;
      flex-wrap:wrap;
    }

    #controls label{
      font-size:12px;
      color:#444;
      user-select:none;
      display:flex;
      gap:6px;
      align-items:center;
    }

    #controls input[type="checkbox"]{ transform: translateY(1px); }
    #controls input[type="range"]{ width: 140px; }

    #controls button{
      border: 1px solid var(--border);
      background: #fff;
      border-radius: 10px;
      padding: 4px 10px;
      font-size: 12px;
      cursor: pointer;
      box-shadow: var(--shadow-soft);
    }
    #controls button:hover{ background:#f7f7f7; }

    #container{
      display:flex;
      width:100vw;
      height: calc(100vh - 48px);
    }

    #graphWrap{ flex:1; min-width:0; background:#fff; }
    #graph{ width:100%; height:100%; display:block; }

    #sidebar{
      width: 440px;
      max-width: 50vw;
      border-left: 1px solid var(--border);
      background: var(--bg);
      padding: 12px;
      overflow:auto;
    }

    .sectionTitle{
      margin: 8px 0 10px;
      font-size: 13px;
      font-weight: 750;
      color:#333;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:8px;
    }

    .sectionTitle .left{
      display:flex;
      align-items:center;
      gap:8px;
      min-width: 0;
    }

    .sectionTitle .right{
      display:flex;
      align-items:center;
      gap:8px;
      flex-wrap:wrap;
      justify-content:flex-end;
    }

    .pill{
      font-size: 11px;
      color:#555;
      background:#fff;
      border: 1px solid var(--border);
      padding: 2px 8px;
      border-radius: 999px;
      white-space:nowrap;
    }

    .toolbarBtn{
      border: 1px solid var(--border);
      background:#fff;
      border-radius: 10px;
      padding: 4px 10px;
      font-size: 12px;
      cursor: pointer;
      box-shadow: var(--shadow-soft);
      white-space:nowrap;
    }
    .toolbarBtn:hover{ background:#f7f7f7; }
    .toolbarBtn.primary{
      border-color: rgba(255,106,0,0.25);
      background: rgba(255,106,0,0.08);
      color:#7a3400;
    }

    .panel{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 10px;
      box-shadow: var(--shadow-soft);
    }

    .stepCard{
      background: #fff;
      border: 1px solid var(--border);
      border-radius: var(--radius2);
      padding: 10px;
      margin-bottom: 10px;
      cursor: pointer;
      box-shadow: var(--shadow-soft);
    }
    .stepCard:hover{ border-color:#cfcfcf; }
    .stepCard.active{
      border-color: var(--active);
      box-shadow: 0 0 0 2px rgba(255,106,0,0,0.14), var(--shadow-soft);
    }
    .stepTitle{
      font-weight: 750;
      font-size: 13px;
      margin-bottom: 6px;
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap:10px;
    }
    .stepTitle code{ font-family: var(--mono); font-size: 12.5px; }
    .stepMeta{
      font-size: 12px;
      color:#555;
      line-height: 1.35;
    }
    .stepMeta code{ font-family: var(--mono); font-size: 12px; }

    #details{
      margin-top: 10px;
      background: #fff;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 10px;
      box-shadow: var(--shadow-soft);
    }

    .k{ font-size: 12px; color:#666; margin-top: 10px; }
    .v{ font-size: 13px; white-space: pre-wrap; }
    code{
      font-family: var(--mono);
      font-size: 12px;
    }

    .subtle{
      font-size: 12px;
      color:#666;
    }

    details.accordion{
      border:1px solid var(--border);
      border-radius: var(--radius2);
      padding: 8px 10px;
      margin: 8px 0;
      background:#fff;
      box-shadow: var(--shadow-soft);
    }
    details.accordion > summary{
      cursor:pointer;
      font-size: 12.8px;
      font-weight: 700;
      list-style:none;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
    }
    details.accordion > summary::-webkit-details-marker { display:none; }
    .summaryRight{
      display:flex;
      align-items:center;
      gap:8px;
      color:#666;
      font-weight: 600;
      font-size: 12px;
    }

    .badge{
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 999px;
      border: 1px solid var(--border);
      background:#f9f9f9;
      color:#444;
      white-space:nowrap;
    }
    .badge.orange{
      border-color: rgba(255,106,0,0.25);
      background: rgba(255,106,0,0.08);
      color: #8a3b00;
    }

    .grid2{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .tableWrap{
      width:100%;
      overflow:auto;
      border:1px solid var(--border);
      border-radius: var(--radius2);
      background:#fff;
      box-shadow: var(--shadow-soft);
    }
    table{
      width:100%;
      border-collapse:collapse;
      font-size: 12px;
    }
    th, td{
      padding: 6px 8px;
      border-bottom: 1px solid #eee;
      text-align:left;
      vertical-align:top;
    }
    thead th{
      position: sticky;
      top: 0;
      background:#fcfcfc;
      border-bottom: 1px solid var(--border);
      z-index: 1;
    }
    tr:last-child td{ border-bottom:none; }
    td code{ font-size: 11.5px; }

    tr.selectedRow td{
      background: rgba(255,106,0,0.06);
    }

    .divider{
      height:1px;
      background: var(--border);
      margin: 10px 0;
    }

    /* Graph */
    .link { fill: none; stroke: #999; stroke-opacity: 0.55; stroke-width: 1.2px; }
    .node circle { fill: #fff; stroke: #666; stroke-width: 1.2px; }
    .node text { font-size: 11px; dominant-baseline: middle; }

    .node.faint circle { stroke: var(--faint); }
    .node.faint text { fill: #aaa; }

    .node.mutated circle { fill: var(--mut); stroke: var(--mut-stroke); stroke-width: 2.2px; }
    .node.active circle { stroke: var(--active); stroke-width: 3px; }
    .node.active text { font-weight: 700; }

    /* Node step-count badge on SVG */
    .nodeBadgeCircle{
      fill: rgba(255,106,0,0.92);
      stroke: rgba(255,106,0,0.92);
    }
    .nodeBadgeText{
      fill: #fff;
      font-weight: 800;
      font-size: 10px;
      font-family: var(--mono);
      dominant-baseline: middle;
      text-anchor: middle;
      pointer-events: none;
    }

    #glossary{
      margin-top: 10px;
      background: #fff;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 10px;
      box-shadow: var(--shadow-soft);
    }
    #glossary .row{ font-size: 12px; line-height: 1.35; margin: 4px 0; }
    #glossary .hint{ color:#666; font-size:12px; margin-top:8px; }

    #nodePopup{
      position: fixed;
      z-index: 9999;
      max-width: min(680px, 92vw);
      max-height: 60vh;
      overflow: auto;
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: var(--shadow);
      padding: 10px 12px;
      display: none;
    }
    #nodePopup .hdr{
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap:10px;
      margin-bottom: 8px;
    }
    #nodePopup .title{
      font-size: 13px;
      font-weight: 800;
      line-height: 1.25;
    }
    #nodePopup .close{
      border: 1px solid var(--border);
      background: #f7f7f7;
      border-radius: 10px;
      padding: 2px 8px;
      font-size: 12px;
      cursor: pointer;
      user-select: none;
      white-space: nowrap;
    }
    #nodePopup .row{ margin: 6px 0; }
    #nodePopup .k{ font-size: 12px; color: #666; margin-bottom: 2px; }
    #nodePopup .v{ font-size: 12.5px; white-space: pre-wrap; word-break: break-word; }
    #nodePopup code{ font-family: var(--mono); font-size: 12px; }
  </style>

  <script src="https://d3js.org/d3.v7.min.js"></script>
</head>

<body>
  <header>
    <div id="meta">Loading graph metadata...</div>
    <div id="controls">
      <label><input id="showDetails" type="checkbox" checked />Show detail nodes (Name/Constant/Load/Store...)</label>
      <label><input id="showLabels" type="checkbox" checked />Show labels for important nodes</label>

      <label title="Collapse the tree to improve readability for large ASTs">
        Max depth
        <input id="maxDepth" type="range" min="2" max="40" value="14" />
        <span id="maxDepthVal">14</span>
      </label>

      <label title="Vertical spacing between nodes">
        Y spacing
        <input id="ySpacing" type="range" min="10" max="70" value="22" />
        <span id="ySpacingVal">22</span>
      </label>

      <label title="Horizontal spacing between levels">
        X spacing
        <input id="xSpacing" type="range" min="80" max="280" value="150" />
        <span id="xSpacingVal">150</span>
      </label>

      <button id="fitBtn" type="button" title="Fit the whole tree into view">Fit</button>
      <button id="centerActiveBtn" type="button" title="Center the selected node">Center</button>
    </div>
  </header>

  <div id="container">
    <div id="graphWrap">
      <svg id="graph"></svg>
    </div>

    <aside id="sidebar">
      <div class="sectionTitle">
        <div class="left" style="min-width:0;">
          <span>Steps</span>
          <span id="stepsCount" class="pill">0</span>
          <span id="stepsFilterPill" class="pill" style="display:none;">Filtered</span>
        </div>
        <div class="right">
          <button id="showAllStepsBtn" class="toolbarBtn" type="button" style="display:none;">Show all</button>
          <button id="clearFilterBtn" class="toolbarBtn primary" type="button" style="display:none;">Clear filter</button>
        </div>
      </div>

      <div id="steps" class="panel">Loading explain.json...</div>

      <div class="sectionTitle" style="margin-top:14px;">
        <span>Details</span>
        <span class="pill">Step + Node</span>
      </div>
      <div id="details">
        <div class="v">Select a step or click a node to highlight it and view details.</div>
      </div>

      <div class="sectionTitle" style="margin-top:14px;">
        <span>AST Node Glossary</span>
        <span class="pill">Quick help</span>
      </div>
      <div id="glossary"></div>
    </aside>
  </div>

  <div id="nodePopup" role="dialog" aria-label="AST node details"></div>

  <script>
    const svg = d3.select('#graph');
    const graphWrap = document.getElementById('graphWrap');

    const typeGlossary = {
      "Module": "A Python file/module (the root of the AST).",
      "FunctionDef": "Function definition: def foo(...):",
      "arguments": "Container for function parameters.",
      "arg": "A single function parameter.",
      "If": "If-statement (condition + body).",
      "Assign": "Assignment statement: x = ...",
      "Return": "Return statement: return ...",
      "Expr": "Expression used as a statement (e.g., calling a function without assigning).",
      "Call": "Function call expression: f(...)",
      "Name": "Identifier name (variable/function).",
      "Constant": "Literal value (number/string/bool/None).",
      "BinOp": "Binary operation expression: a + b, a * b, ...",
      "BoolOp": "Boolean operation: and/or between conditions.",
      "Compare": "Comparison: <, >, ==, in, ...",
      "Load": "Context: variable is being read.",
      "Store": "Context: variable is being written.",
      "Add": "Operator +",
      "Sub": "Operator -",
      "Mult": "Operator *",
      "Gt": "Comparison operator >",
      "Lt": "Comparison operator <",
      "Eq": "Comparison operator ==",
      "Or": "Boolean operator or",
      "And": "Boolean operator and",
      "keyword": "Keyword argument in a call: f(x=1)"
    };

    function renderGlossary() {
      const el = document.getElementById('glossary');
      const keys = Object.keys(typeGlossary);
      el.innerHTML = keys.map(k => `<div class="row"><code>${k}</code> — ${typeGlossary[k]}</div>`).join('');
      el.insertAdjacentHTML('beforeend', `<div class="hint">Tip: hover any node to see its line number and code snippet.</div>`);
    }
    renderGlossary();

    function sizeSvg() {
      const w = graphWrap.clientWidth;
      const h = graphWrap.clientHeight;
      svg.attr('width', w).attr('height', h);
      return { w, h };
    }

    const state = {
      rawNodes: [],
      rawEdges: [],
      idToNode: new Map(),
      childrenById: new Map(),
      rootId: null,
      mutationSet: new Set(),

      allEvents: [],
      visibleEvents: [],

      stepCards: [],
      activeNodeId: null,
      activeStepIdx: null,

      showDetails: true,
      showLabels: true,

      maxDepth: 14,
      ySpacing: 22,
      xSpacing: 150,

      g: null,
      nodeSel: null,
      zoom: null,
      activeTransform: null,

      nodeIdToEvents: new Map(),
      nodeIdToStepCount: new Map(),

      stepTraceExpanded: new Set(), // stepKey
      filteredNodeId: null,
      showAllStepsEvenWhenFiltered: false,
    };

    const DETAIL_TYPES = new Set(["Name","Constant","Load","Store","arg","arguments","keyword","Add","Sub","Mult","Gt","Lt","Eq","Or","And"]);
    const IMPORTANT_TYPES = new Set(["Module","FunctionDef","If","Assign","Return","Expr","Call","Compare","BoolOp","BinOp"]);

    function escapeHtml(s) {
      return String(s ?? '')
        .replaceAll('&','&amp;')
        .replaceAll('<','&lt;')
        .replaceAll('>','&gt;')
        .replaceAll('"','&quot;')
        .replaceAll("'",'&#39;');
    }

    function truncate(s, n=34) {
      if (!s) return "";
      s = String(s).replace(/\s+/g,' ').trim();
      return (s.length > n) ? (s.slice(0, n-1) + "…") : s;
    }

    function labelForNode(d) {
      if (!state.showLabels) return "";
      if (IMPORTANT_TYPES.has(d.type) || state.mutationSet.has(d.id) || d.id === state.activeNodeId) {
        if (d.snippet && (d.type === "Assign" || d.type === "Return" || d.type === "If" || d.type === "Expr" || d.type === "Call" || d.type === "FunctionDef")) {
          return truncate(d.snippet, 50);
        }
        if (d.snippet && (d.type === "Name" || d.type === "Constant")) {
          return truncate(d.snippet, 22);
        }
        return d.type;
      }
      return "";
    }

    function formatScores(scores) {
      if (!scores) return 'n/a';
      const parts = [
        ['total', scores.total],
        ['coverage', scores.coverage],
        ['semantic', scores.semantic],
        ['dependency', scores.dependency],
      ];
      return parts.map(([k,v]) => `${k}: ${v}`).join('  |  ');
    }

    function renderScoreReasonsText(reasons) {
      if (!reasons || typeof reasons !== 'object') return 'n/a';
      const lines = Object.entries(reasons).map(([k,v]) => `${k}: ${v}`);
      return lines.length ? lines.join('\n') : 'n/a';
    }

    function hideNodePopup() {
      const pop = document.getElementById('nodePopup');
      pop.style.display = 'none';
      pop.innerHTML = '';
    }

    function showNodePopup(event, nodeData) {
      const pop = document.getElementById('nodePopup');
      const type = nodeData?.type ?? 'n/a';
      const desc = typeGlossary[type] ? (" — " + typeGlossary[type]) : "";
      const line = nodeData?.lineno ?? '?';
      const id = nodeData?.id ?? 'n/a';
      const snippet = nodeData?.snippet ?? '';

      pop.innerHTML = `
        <div class="hdr">
          <div class="title"><code>${escapeHtml(type)}</code>${escapeHtml(desc)}</div>
          <div class="close" id="nodePopupClose">Close</div>
        </div>
        <div class="row"><div class="k">node_id</div><div class="v"><code>${escapeHtml(id)}</code></div></div>
        <div class="row"><div class="k">Line</div><div class="v"><code>${escapeHtml(line)}</code></div></div>
        <div class="row"><div class="k">Full Snippet</div><div class="v"><code>${escapeHtml(snippet)}</code></div></div>
      `;

      pop.style.display = 'block';

      const pad = 12;
      let x = (event.clientX ?? 0) + pad;
      let y = (event.clientY ?? 0) + pad;

      pop.style.left = x + 'px';
      pop.style.top = y + 'px';
      const rect = pop.getBoundingClientRect();

      const vw = window.innerWidth;
      const vh = window.innerHeight;
      if (rect.right > vw - pad) x = Math.max(pad, vw - rect.width - pad);
      if (rect.bottom > vh - pad) y = Math.max(pad, vh - rect.height - pad);
      pop.style.left = x + 'px';
      pop.style.top = y + 'px';

      const closeBtn = document.getElementById('nodePopupClose');
      if (closeBtn) closeBtn.onclick = hideNodePopup;
    }

    document.addEventListener('click', () => hideNodePopup());
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') hideNodePopup(); });

    function buildNodeIdToEvents(events) {
      state.nodeIdToEvents = new Map();
      for (const ev of events || []) {
        const nid = ev?.selected_node?.node_id;
        if (!nid) continue;
        if (!state.nodeIdToEvents.has(nid)) state.nodeIdToEvents.set(nid, []);
        state.nodeIdToEvents.get(nid).push(ev);
      }
      for (const [nid, arr] of state.nodeIdToEvents.entries()) {
        arr.sort((a,b) => (Number(a.step)||0) - (Number(b.step)||0));
      }
      state.nodeIdToStepCount = new Map();
      for (const [nid, arr] of state.nodeIdToEvents.entries()) {
        state.nodeIdToStepCount.set(nid, arr.length);
      }
    }

    function updateStepsHeader() {
      const total = state.allEvents.length;
      const visible = state.visibleEvents.length;

      document.getElementById('stepsCount').textContent = `${visible}/${total}`;

      const filterPill = document.getElementById('stepsFilterPill');
      const showAllBtn = document.getElementById('showAllStepsBtn');
      const clearBtn = document.getElementById('clearFilterBtn');

      const isFiltered = !!state.filteredNodeId && !state.showAllStepsEvenWhenFiltered;

      filterPill.style.display = isFiltered ? '' : 'none';
      showAllBtn.style.display = (!!state.filteredNodeId && !state.showAllStepsEvenWhenFiltered) ? '' : 'none';
      clearBtn.style.display = (!!state.filteredNodeId) ? '' : 'none';

      if (state.filteredNodeId) {
        filterPill.textContent = `Filtered by node ${state.filteredNodeId}`;
      }
    }

    function applyStepsFilterByNode(nodeId) {
      state.filteredNodeId = nodeId;
      state.showAllStepsEvenWhenFiltered = false;

      const related = state.nodeIdToEvents.get(nodeId) || [];
      state.visibleEvents = related.slice();

      buildStepsPanel(state.visibleEvents, true);
      updateStepsHeader();
    }

    function clearStepsFilter() {
      state.filteredNodeId = null;
      state.showAllStepsEvenWhenFiltered = false;
      state.visibleEvents = state.allEvents.slice();
      buildStepsPanel(state.visibleEvents, false);
      updateStepsHeader();
    }

    function showAllStepsTemporarily() {
      state.showAllStepsEvenWhenFiltered = true;
      state.visibleEvents = state.allEvents.slice();
      buildStepsPanel(state.visibleEvents, false);
      updateStepsHeader();
    }

    document.getElementById('showAllStepsBtn').addEventListener('click', () => showAllStepsTemporarily());
    document.getElementById('clearFilterBtn').addEventListener('click', () => clearStepsFilter());

    function buildStepsPanel(events, filtered) {
      const stepsDiv = document.getElementById('steps');
      stepsDiv.innerHTML = '';
      state.stepCards = [];

      if (!events || events.length === 0) {
        stepsDiv.innerHTML = filtered
          ? `<div class="subtle">No steps selected this node (no matching events in explain.json).</div>`
          : `No events found in explain.json`;
        return;
      }

      events.forEach((ev, idx) => {
        const node = ev.selected_node || {};
        const card = document.createElement('div');
        card.className = 'stepCard';

        const total = ev?.scores?.total ?? 'n/a';
        const op = ev.selected_operator || 'n/a';
        const step = ev.step ?? (idx+1);

        card.innerHTML = `
          <div class="stepTitle">
            <span>Step ${escapeHtml(step)}: <code>${escapeHtml(op)}</code></span>
            <span class="badge orange">total=${escapeHtml(total)}</span>
          </div>
          <div class="stepMeta">
            <div><code>node_id=${escapeHtml(node.node_id ?? 'n/a')}</code> · line ${escapeHtml(node.lineno ?? '?')}</div>
            <div style="margin-top:4px;"><code>${escapeHtml(formatScores(ev.scores))}</code></div>
          </div>
        `;

        card.addEventListener('click', () => {
          setActiveStepByEvent(ev, idx);
        });

        stepsDiv.appendChild(card);
        state.stepCards.push(card);
      });

      // Mark active if possible
      if (state.activeStepIdx != null && state.stepCards[state.activeStepIdx]) {
        state.stepCards.forEach((el, i) => el.classList.toggle('active', i === state.activeStepIdx));
      }
    }

    function getStepKey(ev) {
      const s = ev?.step ?? '';
      const op = ev?.selected_operator ?? '';
      const nid = ev?.selected_node?.node_id ?? '';
      return `${s}::${op}::${nid}`;
    }

    function renderSelectionTraceHtml(ev) {
      const trace =
        (ev.retries && ev.retries.final_selection_trace) ||
        ev.selection_trace ||
        null;

      if (!trace) return `<div class="v subtle">n/a</div>`;

      const orderedAll = Array.isArray(trace.ordered) ? trace.ordered : [];
      const stepKey = getStepKey(ev);
      const expanded = state.stepTraceExpanded.has(stepKey);
      const limit = 15;

      const orderedShown = expanded ? orderedAll : orderedAll.slice(0, limit);

      const header = `
        <div class="grid2">
          <div class="panel" style="padding:8px;">
            <div class="k" style="margin-top:0;">Strategy</div>
            <div class="v"><code>${escapeHtml(trace.strategy ?? 'n/a')}</code></div>
          </div>
          <div class="panel" style="padding:8px;">
            <div class="k" style="margin-top:0;">Sampling</div>
            <div class="v"><code>random_draw=${escapeHtml(trace.random_draw ?? 'n/a')}</code></div>
            <div class="v"><code>weight_sum=${escapeHtml(trace.weight_sum ?? 'n/a')}</code></div>
            <div class="v"><code>chosen_index=${escapeHtml(trace.chosen_index ?? 'n/a')}</code></div>
          </div>
        </div>
      `;

      const toggleBtn = (orderedAll.length > limit) ? `
        <div style="margin:8px 0 6px; display:flex; justify-content:flex-end;">
          <button class="toolbarBtn" type="button"
            onclick="window.__toggleTrace('${escapeHtml(stepKey)}')">
            ${expanded ? 'Show Top-15' : `Show all (${orderedAll.length})`}
          </button>
        </div>
      ` : '';

      const chosenIndex = trace.chosen_index;
      const selectedOp = ev?.selected_operator ?? '';

      const rows = orderedShown.map(o => {
        const isSelected =
          (String(o.reason || '').toUpperCase().includes('SELECTED')) ||
          (o.operator === selectedOp) ||
          (chosenIndex != null && String(o.rank) === String(chosenIndex));

        return `
          <tr class="${isSelected ? 'selectedRow' : ''}">
            <td>${escapeHtml(o.rank ?? '')}</td>
            <td><code>${escapeHtml(o.operator ?? '')}</code></td>
            <td>${escapeHtml(o.total_score ?? '')}</td>
            <td>${escapeHtml(o.weight_used ?? '')}</td>
            <td>${escapeHtml(o.reason ?? '')}</td>
          </tr>
        `;
      }).join('');

      const table = `
        <div class="k">Ordered candidates (default Top-15)</div>
        ${toggleBtn}
        <div class="tableWrap">
          <table>
            <thead>
              <tr>
                <th style="min-width:44px;">rank</th>
                <th style="min-width:190px;">operator</th>
                <th style="min-width:70px;">total</th>
                <th style="min-width:70px;">weight</th>
                <th style="min-width:260px;">why</th>
              </tr>
            </thead>
            <tbody>${rows || ''}</tbody>
          </table>
        </div>
      `;

      return `${header}${table}`;
    }

    // Global hook for the inline onclick above
    window.__toggleTrace = (stepKey) => {
      if (state.stepTraceExpanded.has(stepKey)) state.stepTraceExpanded.delete(stepKey);
      else state.stepTraceExpanded.add(stepKey);

      // Re-render the current details pane
      if (state.activeStepIdx != null && state.visibleEvents[state.activeStepIdx]) {
        const ev = state.visibleEvents[state.activeStepIdx];
        document.getElementById('details').innerHTML = renderStepDetails(ev);
      }
    };

    function renderTopCandidatesHtml(ev) {
      const arr = Array.isArray(ev.top_candidates) ? ev.top_candidates : [];
      if (!arr.length) return `<div class="v subtle">n/a</div>`;

      const items = arr.map((c, idx) => {
        const r = c.reason || {};
        const reasonText = [
          r.coverage ? `coverage: ${r.coverage}` : null,
          r.semantic ? `semantic: ${r.semantic}` : null,
          r.dependency ? `dependency: ${r.dependency}` : null,
        ].filter(Boolean).join('\n');

        return `
          <details class="accordion">
            <summary>
              <span>#${idx+1} <code>${escapeHtml(c.operator ?? 'n/a')}</code></span>
              <span class="summaryRight">
                <span class="badge">total=${escapeHtml(c.total_score ?? 'n/a')}</span>
                <span class="badge">cov=${escapeHtml(c.cov_score ?? 'n/a')}</span>
                <span class="badge">sem=${escapeHtml(c.sem_score ?? 'n/a')}</span>
                <span class="badge">dep=${escapeHtml(c.dep_score ?? 'n/a')}</span>
              </span>
            </summary>
            <div class="divider"></div>
            <div class="k" style="margin-top:0;">Reason</div>
            <div class="v"><code>${escapeHtml(reasonText || 'n/a')}</code></div>
          </details>
        `;
      }).join('');

      return `<div>${items}</div>`;
    }

    function renderDiscardedHtml(ev) {
      const disc = ev?.retries && Array.isArray(ev.retries.discarded) ? ev.retries.discarded : [];
      if (!disc.length) return `<div class="v subtle">n/a</div>`;

      const blocks = disc.map((d, i) => {
        const mv = d.mutant_validation || {};
        const trace = d.selection_trace || {};
        return `
          <details class="accordion">
            <summary>
              <span>Discarded #${i+1}</span>
              <span class="summaryRight">
                <span class="badge orange">${escapeHtml(mv.error_type ?? 'error')}</span>
                <span class="badge">stage=${escapeHtml(mv.validation_stage ?? 'n/a')}</span>
              </span>
            </summary>
            <div class="divider"></div>

            <div class="k" style="margin-top:0;">Error</div>
            <div class="v"><code>${escapeHtml(mv.error_msg ?? '')}</code></div>
            <div class="k">Traceback</div>
            <div class="v"><code>${escapeHtml(mv.traceback ?? '')}</code></div>

            <div class="k">Selection trace (this discarded attempt)</div>
            <div class="v"><code>
strategy=${escapeHtml(trace.strategy ?? 'n/a')}
weight_kind=${escapeHtml(trace.weight_kind ?? 'n/a')}
random_draw=${escapeHtml(trace.random_draw ?? 'n/a')}
weight_sum=${escapeHtml(trace.weight_sum ?? 'n/a')}
chosen_index=${escapeHtml(trace.chosen_index ?? 'n/a')}
            </code></div>
          </details>
        `;
      }).join('');

      return `<div>${blocks}</div>`;
    }

    function renderStepDetails(ev) {
      const reasons = (ev.scores && ev.scores.reasons) ? ev.scores.reasons : {};
      const node = ev.selected_node || {};
      const scoresText = formatScores(ev.scores);

      return `
        <div class="sectionTitle" style="margin:0 0 8px;">
          <span>Step Explanation</span>
          <span class="pill">step=${escapeHtml(ev.step ?? 'n/a')}</span>
        </div>

        <div class="panel">
          <div class="k" style="margin-top:0;">Operator</div>
          <div class="v"><code>${escapeHtml(ev.selected_operator || 'n/a')}</code></div>

          <div class="k">Selected AST Node</div>
          <div class="v"><code>node_id=${escapeHtml(node.node_id ?? 'n/a')}</code> <span class="subtle">(line ${escapeHtml(node.lineno ?? '?')})</span></div>

          <div class="k">Snippet</div>
          <div class="v"><code>${escapeHtml(node.snippet || '')}</code></div>

          <div class="k">Scores</div>
          <div class="v"><code>${escapeHtml(scoresText)}</code></div>

          <div class="k">Score reasons</div>
          <div class="v"><code>${escapeHtml(renderScoreReasonsText(reasons))}</code></div>

          <div class="k">Selection strategy</div>
          <div class="v"><code>${escapeHtml(ev.selection_strategy || 'n/a')}</code></div>
        </div>

        <details class="accordion" open>
          <summary>
            <span>Why this operator was chosen (selection trace)</span>
            <span class="summaryRight"><span class="badge">weighted sampling</span></span>
          </summary>
          <div class="divider"></div>
          ${renderSelectionTraceHtml(ev)}
        </details>

        <details class="accordion">
          <summary>
            <span>Top candidates (scoring explanations)</span>
            <span class="summaryRight"><span class="badge">${escapeHtml((ev.top_candidates||[]).length)}</span></span>
          </summary>
          <div class="divider"></div>
          ${renderTopCandidatesHtml(ev)}
        </details>

        <details class="accordion">
          <summary>
            <span>Discarded attempts (if validation failed)</span>
            <span class="summaryRight"><span class="badge">${escapeHtml((ev.retries && ev.retries.discarded ? ev.retries.discarded.length : 0))}</span></span>
          </summary>
          <div class="divider"></div>
          ${renderDiscardedHtml(ev)}
        </details>
      `;
    }

    function renderNodeLinkedSteps(nodeId) {
      const list = state.nodeIdToEvents.get(nodeId) || [];
      if (!list.length) {
        return `
          <div class="panel">
            <div class="k" style="margin-top:0;">Linked steps</div>
            <div class="v subtle">No step in explain.json selected this node as the "selected_node".</div>
          </div>
        `;
      }

      const items = list.map((ev, idx) => {
        const node = ev.selected_node || {};
        return `
          <details class="accordion" ${idx === 0 ? 'open' : ''}>
            <summary>
              <span>Step ${escapeHtml(ev.step ?? 'n/a')} — <code>${escapeHtml(ev.selected_operator ?? 'n/a')}</code></span>
              <span class="summaryRight">
                <span class="badge">line ${escapeHtml(node.lineno ?? '?')}</span>
                <span class="badge orange">total=${escapeHtml(ev.scores?.total ?? 'n/a')}</span>
              </span>
            </summary>
            <div class="divider"></div>
            ${renderStepDetails(ev)}
          </details>
        `;
      }).join('');

      return `
        <div class="sectionTitle" style="margin:10px 0 8px;">
          <span>Why this node matters</span>
          <span class="pill">${escapeHtml(list.length)} linked</span>
        </div>
        ${items}
      `;
    }

    function renderNodeDetails(nodeData) {
      const type = nodeData?.type ?? 'n/a';
      const desc = typeGlossary[type] ? (" — " + typeGlossary[type]) : "";
      const line = nodeData?.lineno ?? '?';
      const id = nodeData?.id ?? 'n/a';
      const snippet = nodeData?.snippet ?? '';

      const details = document.getElementById('details');
      details.innerHTML = `
        <div class="sectionTitle" style="margin:0 0 8px;">
          <span>Node Details</span>
          <span class="pill">node_id=${escapeHtml(id)}</span>
        </div>

        <div class="panel">
          <div class="k" style="margin-top:0;">Type</div>
          <div class="v"><code>${escapeHtml(type)}</code>${escapeHtml(desc)}</div>

          <div class="k">Line</div>
          <div class="v"><code>${escapeHtml(line)}</code></div>

          <div class="k">Full snippet</div>
          <div class="v"><code>${escapeHtml(snippet)}</code></div>

          <div class="k">Tip</div>
          <div class="v subtle">Steps panel is filtered to only show steps related to this node.</div>
        </div>

        ${renderNodeLinkedSteps(id)}
      `;
    }

    function setActiveStepByEvent(ev, idxInVisible) {
      state.activeStepIdx = idxInVisible;

      state.stepCards.forEach((el, i) => el.classList.toggle('active', i === idxInVisible));

      const nodeId = ev.selected_node && ev.selected_node.node_id;
      state.activeNodeId = nodeId ?? null;

      if (state.nodeSel) {
        state.nodeSel.classed('active', d => d.data.id === state.activeNodeId);
        state.nodeSel.select('text').text(d => labelForNode(d.data));
      }

      document.getElementById('details').innerHTML = renderStepDetails(ev);
      centerOnNodeId(state.activeNodeId);
    }

    function buildHierarchyObject(rootId, visited=new Set()) {
      const n = state.idToNode.get(rootId);
      if (!n) return null;
      if (visited.has(rootId)) return { ...n, children: [] };
      visited.add(rootId);
      const childIds = state.childrenById.get(rootId) || [];
      return {
        ...n,
        children: childIds.map(cid => buildHierarchyObject(cid, visited)).filter(Boolean)
      };
    }

    function pruneToDepth(node, maxDepth, depth = 0) {
      if (!node) return null;
      const copy = { ...node };
      if (depth >= maxDepth) {
        copy.children = [];
        return copy;
      }
      if (Array.isArray(copy.children)) {
        copy.children = copy.children
          .map(c => pruneToDepth(c, maxDepth, depth + 1))
          .filter(Boolean);
      } else {
        copy.children = [];
      }
      return copy;
    }

    function getTreeBounds(gSelection) {
      try {
        const b = gSelection.node().getBBox();
        return { x: b.x, y: b.y, w: b.width, h: b.height };
      } catch {
        return { x: 0, y: 0, w: 1, h: 1 };
      }
    }

    function applyZoomToFit(svgSel, gSel) {
      if (!state.zoom) return;
      const { w: width, h: height } = sizeSvg();
      const b = getTreeBounds(gSel);

      const pad = 24;
      const scale = Math.max(0.15, Math.min(6, Math.min(
        (width - pad * 2) / Math.max(1, b.w),
        (height - pad * 2) / Math.max(1, b.h)
      )));

      const tx = (width / 2) - (b.x + b.w / 2) * scale;
      const ty = (height / 2) - (b.y + b.h / 2) * scale;

      const t = d3.zoomIdentity.translate(tx, ty).scale(scale);
      svgSel.transition().duration(250).call(state.zoom.transform, t);
      state.activeTransform = t;
    }

    function centerOnNodeId(nodeId) {
      if (!nodeId || !state.zoom || !state.nodeSel) return;
      const match = state.nodeSel.filter(d => d.data.id === nodeId);
      if (match.empty()) return;

      const { w: width, h: height } = sizeSvg();
      const transform = d3.zoomTransform(svg.node());
      const datum = match.datum();

      const x = datum.y;
      const y = datum.x;

      const tx = width / 2 - (x * transform.k);
      const ty = height / 2 - (y * transform.k);
      const t = d3.zoomIdentity.translate(tx, ty).scale(transform.k);

      svg.transition().duration(250).call(state.zoom.transform, t);
      state.activeTransform = t;
    }

    function redrawTree() {
      sizeSvg();
      svg.selectAll("*").remove();

      const g = svg.append("g");
      state.g = g;

      state.zoom = d3.zoom()
        .scaleExtent([0.15, 6])
        .on("zoom", (event) => {
          g.attr("transform", event.transform);
          state.activeTransform = event.transform;
        });
      svg.call(state.zoom);

      const rootObjRaw = buildHierarchyObject(state.rootId);
      const rootObj = pruneToDepth(rootObjRaw, state.maxDepth);

      const root = d3.hierarchy(rootObj, d => d.children);
      root.each(d => { d.data.__isDetail = DETAIL_TYPES.has(d.data.type); });

      const tree = d3.tree().nodeSize([state.ySpacing, state.xSpacing]);
      tree(root);

      g.append("g")
        .selectAll("path")
        .data(root.links())
        .enter()
        .append("path")
        .attr("class", "link")
        .attr("d", d3.linkHorizontal().x(d => d.y).y(d => d.x));

      const nodes = root.descendants().filter(d => state.showDetails ? true : !d.data.__isDetail);

      const node = g.append("g")
        .selectAll("g")
        .data(nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .classed("mutated", d => state.mutationSet.has(d.data.id))
        .classed("faint", d => d.data.__isDetail && !state.mutationSet.has(d.data.id))
        .classed("active", d => d.data.id === state.activeNodeId)
        .attr("transform", d => `translate(${d.y},${d.x})`);

      node.append("circle")
        .attr("r", d => {
          if (d.data.id === state.activeNodeId) return 8;
          if (state.mutationSet.has(d.data.id)) return 7;
          if (IMPORTANT_TYPES.has(d.data.type)) return 5.5;
          return 3.5;
        });

      node.append("title")
        .text(d => {
          const type = d.data.type;
          const desc = typeGlossary[type] ? (" - " + typeGlossary[type]) : "";
          const line = d.data.lineno ?? "?";
          const code = d.data.snippet ? d.data.snippet.replace(/\s+/g,' ').trim() : "";
          const c = state.nodeIdToStepCount.get(d.data.id) || 0;
          const stepInfo = c ? `\nlinked_steps: ${c}` : '';
          return `${type}${desc}\nline: ${line}${stepInfo}\n${code}`;
        });

      node.append("text")
        .attr("x", 10)
        .attr("y", 0)
        .text(d => labelForNode(d.data));

      // --- (1) Add step-count corner badge on nodes ---
      const badge = node.filter(d => (state.nodeIdToStepCount.get(d.data.id) || 0) > 0);

      const badgeR = 8;
      badge.append("circle")
        .attr("class", "nodeBadgeCircle")
        .attr("cx", 10)
        .attr("cy", -10)
        .attr("r", badgeR);

      badge.append("text")
        .attr("class", "nodeBadgeText")
        .attr("x", 10)
        .attr("y", -10)
        .text(d => {
          const c = state.nodeIdToStepCount.get(d.data.id) || 0;
          return c > 99 ? "99+" : String(c);
        });

      node.on('click', (event, d) => {
        event.stopPropagation();

        state.activeNodeId = d.data.id;
        state.activeStepIdx = null;

        if (state.nodeSel) {
          state.nodeSel.classed('active', n => n.data.id === state.activeNodeId);
          state.nodeSel.select('text').text(n => labelForNode(n.data));
        }

        // --- (2) Filter steps panel to related steps ---
        applyStepsFilterByNode(state.activeNodeId);

        renderNodeDetails(d.data);
        showNodePopup(event, d.data);
      });

      state.nodeSel = node;

      if (state.activeTransform) {
        svg.call(state.zoom.transform, state.activeTransform);
      } else {
        applyZoomToFit(svg, g);
      }
    }

    document.getElementById("showDetails").addEventListener("change", (e) => {
      state.showDetails = e.target.checked;
      state.activeTransform = null;
      redrawTree();
    });

    document.getElementById("showLabels").addEventListener("change", (e) => {
      state.showLabels = e.target.checked;
      if (state.nodeSel) state.nodeSel.select('text').text(d => labelForNode(d.data));
    });

    const maxDepthEl = document.getElementById("maxDepth");
    const maxDepthValEl = document.getElementById("maxDepthVal");
    const ySpacingEl = document.getElementById("ySpacing");
    const ySpacingValEl = document.getElementById("ySpacingVal");
    const xSpacingEl = document.getElementById("xSpacing");
    const xSpacingValEl = document.getElementById("xSpacingVal");

    maxDepthValEl.textContent = String(state.maxDepth);
    ySpacingValEl.textContent = String(state.ySpacing);
    xSpacingValEl.textContent = String(state.xSpacing);

    maxDepthEl.addEventListener("input", (e) => {
      state.maxDepth = parseInt(e.target.value, 10);
      maxDepthValEl.textContent = String(state.maxDepth);
      state.activeTransform = null;
      redrawTree();
    });

    ySpacingEl.addEventListener("input", (e) => {
      state.ySpacing = parseInt(e.target.value, 10);
      ySpacingValEl.textContent = String(state.ySpacing);
      state.activeTransform = null;
      redrawTree();
    });

    xSpacingEl.addEventListener("input", (e) => {
      state.xSpacing = parseInt(e.target.value, 10);
      xSpacingValEl.textContent = String(state.xSpacing);
      state.activeTransform = null;
      redrawTree();
    });

    document.getElementById("fitBtn").addEventListener("click", () => {
      if (state.g) applyZoomToFit(svg, state.g);
    });

    document.getElementById("centerActiveBtn").addEventListener("click", () => {
      centerOnNodeId(state.activeNodeId);
    });

    Promise.all([
      fetch('graph.json').then(r => r.json()),
      fetch('explain.json').then(r => r.json()).catch(() => ({ events: [] })),
    ]).then(([graphData, explainData]) => {
      const meta = graphData.meta || {};
      document.getElementById('meta').textContent =
        `File: ${meta.input_file}  |  Policy: ${meta.policy}  |  Walk: ${meta.walk}  |  Seed: ${meta.seed}  |  View: Tree`;

      state.rawNodes = graphData.nodes || [];
      state.rawEdges = graphData.edges || [];
      state.mutationSet = new Set(graphData.mutation_path || []);

      state.allEvents = (explainData && explainData.events) ? explainData.events : [];
      state.visibleEvents = state.allEvents.slice();

      buildNodeIdToEvents(state.allEvents);

      state.idToNode = new Map();
      state.rawNodes.forEach(n => state.idToNode.set(n.id, n));

      state.childrenById = new Map();
      state.rawEdges.forEach(e => {
        if (!state.childrenById.has(e.source)) state.childrenById.set(e.source, []);
        state.childrenById.get(e.source).push(e.target);
      });

      const sources = new Set(state.rawEdges.map(e => e.source));
      const targets = new Set(state.rawEdges.map(e => e.target));
      const roots = [...sources].filter(x => !targets.has(x));
      state.rootId = roots.length ? roots[0] : (state.rawNodes[0] ? state.rawNodes[0].id : null);

      // Initial steps panel (all)
      buildStepsPanel(state.visibleEvents, false);
      updateStepsHeader();

      redrawTree();

      if (state.allEvents.length > 0) {
        // Default: select the first visible step
        setActiveStepByEvent(state.visibleEvents[0], 0);
      } else {
        renderNodeDetails({ type: "Module", id: state.rootId, lineno: null, snippet: "" });
      }

      window.addEventListener('resize', () => {
        state.activeTransform = null;
        redrawTree();
      });
    }).catch(err => {
      document.getElementById('meta').textContent = 'Failed to load graph data: ' + err;
      document.getElementById('steps').textContent = 'Failed to load explain.json: ' + err;
    });
  </script>
</body>
</html>
"""


def write_graph_tree_steps_html(output_dir: str | Path, filename: str = "graph_tree_steps.html") -> Path:
    """Write the tree-based HTML viewer into the output directory."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    out_path.write_text(GRAPH_TREE_STEPS_HTML_TEMPLATE, encoding="utf-8")
    return out_path


def _filter_kwargs_for_callable(fn: Any, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Return only kwargs that are accepted by the callable's signature."""
    try:
        sig = inspect.signature(fn)
    except Exception:
        return dict(kwargs)
    accepted = set(sig.parameters.keys())
    return {k: v for k, v in kwargs.items() if k in accepted}


def _call_run_guided_demo_compat(**kwargs):
    """Call run_guided_demo with best-effort backward compatibility."""
    try:
        sig = inspect.signature(run_guided_demo)
        params = set(sig.parameters.keys())
    except Exception:
        sig = None
        params = set()

    # Support validate vs enable_validation.
    if sig is not None:
        if "validate" not in params and "enable_validation" in params:
            if "validate" in kwargs:
                kwargs["enable_validation"] = kwargs.pop("validate")

    safe_kwargs = _filter_kwargs_for_callable(run_guided_demo, kwargs)
    return run_guided_demo(**safe_kwargs)


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        description="Demo CLI: controllable / explainable / reproducible mutation walks",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--input", required=True, help="Path to input Python file")
    parser.add_argument("--walk", choices=["random", "guided"], default="random",
                        help="Walk mode: random baseline or guided")
    parser.add_argument("--policy", choices=["random", "coverage", "composite"], default="random",
                        help="Guidance policy")
    parser.add_argument("--steps", type=int, default=8, help="Number of mutation steps")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--target-api", dest="target_api", help="Single target symbol for dependency priority")
    parser.add_argument("--dep-priority", nargs="*", default=None,
                        help="Additional dependency-priority symbols (function/variable names)")

    vg = parser.add_mutually_exclusive_group()
    vg.add_argument("--validate", dest="validate", action="store_true",
                    help="Enable validate/rollback for invalid mutations")
    vg.add_argument("--no-validate", dest="validate", action="store_false",
                    help="Disable validate/rollback (may emit invalid mutated code)")
    parser.set_defaults(validate=True)

    sg = parser.add_mutually_exclusive_group()
    sg.add_argument("--smoke-run", dest="smoke_run", action="store_true",
                    help="Enable smoke-run validation (exec in a subprocess with timeout)")
    sg.add_argument("--no-smoke-run", dest="smoke_run", action="store_false",
                    help="Disable smoke-run validation (parse/compile only)")
    parser.set_defaults(smoke_run=True)

    parser.add_argument("--smoke-timeout-sec", type=float, default=2.0,
                        help="Smoke-run timeout in seconds")

    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    source = input_path.read_text(encoding="utf-8")

    # Normalize policy/walk combinations.
    walk = args.walk
    policy = args.policy
    if walk == "random":
        policy = "random"

    # Coverage for ORIGINAL input (used by the engine as guidance signal).
    executed_lines, cov_meta = _collect_executed_lines(input_path, source, policy)
    coverage_hash = compute_coverage_hash(sorted(executed_lines))

    started_at = datetime.fromtimestamp(time.time()).isoformat()

    # Run the guided demo engine.
    mutated_code, manifest_meta, explain_events, graph_json = _call_run_guided_demo_compat(
        source_code=source,
        input_path=str(input_path),
        walk=walk,
        policy=policy,
        seed=args.seed,
        steps=args.steps,
        coverage_lines=executed_lines,
        target_api=args.target_api,
        extra_dependencies=args.dep_priority,
        validate=args.validate,
        smoke_run=args.smoke_run,
        smoke_timeout_sec=args.smoke_timeout_sec,
    )

    # Output layout: outputs/<policy>/<timestamp>/.
    project_root = Path(__file__).resolve().parent.parent
    out_root = project_root / "outputs" / policy
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = out_root / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    mutated_path = run_dir / "mutated.py"
    mutated_path.write_text(mutated_code, encoding="utf-8")

    # Best-effort coverage for MUTATED output (reporting only).
    mutated_cov_lines: Set[int] = set()
    mutated_cov_meta: Dict[str, Any] = {"coverage_source": "n/a", "coverage_percent": None}
    mutated_cov_hash: Optional[str] = None

    if policy in {"coverage", "composite"}:
        try:
            mutated_cov_lines, mutated_cov_meta = _collect_executed_lines(mutated_path, mutated_code, policy)
            mutated_cov_hash = compute_coverage_hash(sorted(mutated_cov_lines))
        except Exception:
            mutated_cov_lines = set()
            mutated_cov_meta = {"coverage_source": "error", "coverage_percent": 0.0}
            mutated_cov_hash = compute_coverage_hash([])

    # Build manifest without clobbering engine-provided validation fields.
    manifest: Dict[str, Any] = {}
    if isinstance(manifest_meta, dict):
        manifest.update(manifest_meta)

    manifest.update(
        {
            "output_file": str(mutated_path),
            "cli": {
                "seed": args.seed,
                "walk": walk,
                "policy": policy,
                "steps": args.steps,
                "validate": bool(args.validate),
                "smoke_run": bool(args.smoke_run),
                "smoke_timeout_sec": float(args.smoke_timeout_sec),
            },
            "coverage_measurement_original": {
                "coverage_hash": coverage_hash,
                "executed_lines": sorted(executed_lines),
                "coverage_source": cov_meta.get("coverage_source"),
                "coverage_percent": cov_meta.get("coverage_percent"),
                "coverage_run_error": cov_meta.get("coverage_run_error"),
                "coverage_fallback_reason": cov_meta.get("coverage_fallback_reason"),
            },
            "coverage_measurement_mutated": {
                "coverage_hash": mutated_cov_hash,
                "executed_lines": sorted(mutated_cov_lines),
                "coverage_source": mutated_cov_meta.get("coverage_source"),
                "coverage_percent": mutated_cov_meta.get("coverage_percent"),
                "coverage_run_error": mutated_cov_meta.get("coverage_run_error"),
                "coverage_fallback_reason": mutated_cov_meta.get("coverage_fallback_reason"),
            },
            "timestamps": {"started_at": started_at},
        }
    )

    manifest_path = run_dir / "manifest.json"
    _write_json(manifest_path, manifest)

    explain_path = run_dir / "explain.json"
    _write_json(explain_path, {"events": explain_events})

    graph_path = run_dir / "graph.json"
    _write_json(graph_path, graph_json)

    graph_html_path = run_dir / "graph.html"
    graph_html_path.write_text(GRAPH_HTML_TEMPLATE, encoding="utf-8")

    write_graph_tree_steps_html(output_dir=run_dir, filename="graph_tree_steps.html")

    run_manifest_path = run_dir / "run_manifest.txt"
    cmdline = "python " + os.path.relpath(__file__) + " " + " ".join(sys.argv[1:])
    run_manifest_path.write_text(cmdline + "\n", encoding="utf-8")

    manifest.setdefault("timestamps", {})
    manifest["timestamps"]["finished_at"] = datetime.fromtimestamp(time.time()).isoformat()
    _write_json(manifest_path, manifest)

    print(f"Run completed. Outputs written to: {run_dir}")


if __name__ == "__main__":  # pragma: no cover
    main()