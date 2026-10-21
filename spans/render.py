"""Draw the parse trees of LaTeX examples with the substring every node covers.

For each example this writes, in the output directory:

* ``<name>.dot`` / ``<name>.png``: one picture holding, for each reading, the
  parse tree (every node labelled with its rule or terminal, the substring it
  covers and the character range) and a chart laying the nodes over the
  characters of the input.
* ``<name>.txt``: the same information as an indented span listing, for a
  ``<details>`` block in the comment.
"""
import html
import json
import subprocess
import sys
from pathlib import Path

import lark
from lark.visitors import CollapseAmbiguities

from sympy.parsing.latex.lark import parse_latex_lark_all
from sympy.parsing.latex.lark.latex_parser import (
    LarkLaTeXParser, _node_spans, _parallel_readings)

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

NEW_RULES = {
    "relation_chain", "membership", "unary_sign", "number_set",
    "factors_after_argument", "power_with_subscript",
    "inverse_function_applied", "function_power", "named_function",
    "leibniz_fraction", "argument_superscript",
}
CHANGED_RULES = {
    "adjacent_expressions", "function_argument", "superscript", "add", "sub",
    "degree", "trigonometric_function", "trigonometric_function_power", "log",
    "fraction", "latex_string", "number",
}

COLOURS = {
    "token": "#e8e8e8",
    "ambig": "#f4b6b6",
    "new": "#c8e6c9",
    "changed": "#fff3b0",
    "rule": "#dbe9f6",
}

parser = LarkLaTeXParser(transform=False)


def colour_of(node):
    if isinstance(node, lark.Token):
        return COLOURS["token"]
    name = str(node.data)
    if name == "_ambig":
        return COLOURS["ambig"]
    if name in NEW_RULES:
        return COLOURS["new"]
    if name in CHANGED_RULES:
        return COLOURS["changed"]
    return COLOURS["rule"]


def name_of(node):
    if isinstance(node, lark.Token):
        if node.type.startswith("__ANON"):
            return repr(str(node))
        return node.type
    return str(node.data)


def raw_tree(s):
    return parser._parse(s)


def readings(s):
    trees = CollapseAmbiguities().transform(raw_tree(s))
    return _parallel_readings(trees)


def esc(text):
    return html.escape(text, quote=True)


# --- the tree -----------------------------------------------------------------

def tree_dot(tree, s, prefix, lines):
    span_of, _ = _node_spans(tree)
    counter = [0]
    leaves = []

    def visit(node):
        ident = f"{prefix}n{counter[0]}"
        counter[0] += 1
        if isinstance(node, lark.Token):
            leaves.append(ident)
        a, b = span_of[id(node)]
        text = s[a:b]
        name = name_of(node)
        colour = colour_of(node)
        if isinstance(node, lark.Token):
            label = (f'<<table border="0" cellborder="0" cellspacing="0" cellpadding="1">'
                     f'<tr><td><font point-size="9" color="#555555">{esc(name)}</font></td></tr>'
                     f'<tr><td><font face="DejaVu Sans Mono" point-size="11"><b>{esc(text)}</b></font></td></tr>'
                     f'<tr><td><font point-size="8" color="#888888">{a}:{b}</font></td></tr></table>>')
            shape = "box"
        else:
            label = (f'<<table border="0" cellborder="0" cellspacing="0" cellpadding="1">'
                     f'<tr><td><b>{esc(name)}</b></td></tr>'
                     f'<tr><td><font face="DejaVu Sans Mono" point-size="10">{esc(text)}</font></td></tr>'
                     f'<tr><td><font point-size="8" color="#888888">{a}:{b}</font></td></tr></table>>')
            shape = "box" if name != "_ambig" else "octagon"
        lines.append(f'  {ident} [label={label}, shape={shape}, style="filled,rounded", fillcolor="{colour}"];')
        if isinstance(node, lark.Tree):
            for child in node.children:
                child_id = visit(child)
                lines.append(f"  {ident} -> {child_id};")
        return ident

    return visit(tree), leaves


# --- the chart ----------------------------------------------------------------

def chart_rows(tree, s):
    """Rows of (start, end, name, colour) per depth, the root being depth 0."""
    span_of, _ = _node_spans(tree)
    rows = {}

    def visit(node, depth):
        a, b = span_of[id(node)]
        rows.setdefault(depth, []).append((a, b, name_of(node), colour_of(node)))
        if isinstance(node, lark.Tree):
            for child in node.children:
                visit(child, depth + 1)

    visit(tree, 0)
    return [rows[d] for d in sorted(rows)]


def chart_dot(tree, s, ident, lines):
    n = len(s)
    cells = []
    header = "".join(
        f'<td border="1" bgcolor="#ffffff"><font face="DejaVu Sans Mono" point-size="12">'
        f'<b>{esc(c) if c != " " else "&nbsp;"}</b></font></td>' for c in s)
    cells.append(f"<tr>{header}</tr>")
    positions = "".join(
        f'<td border="0"><font point-size="7" color="#888888">{i}</font></td>' for i in range(n))
    cells.append(f"<tr>{positions}</tr>")
    for row in chart_rows(tree, s):
        tds = []
        cursor = 0
        for a, b, name, colour in sorted(row):
            if a > cursor:
                tds.append(f'<td border="0" colspan="{a - cursor}"></td>')
            tds.append(f'<td border="1" colspan="{b - a}" bgcolor="{colour}">'
                       f'<font point-size="9">{esc(name)}</font></td>')
            cursor = b
        if cursor < n:
            tds.append(f'<td border="0" colspan="{n - cursor}"></td>')
        cells.append(f"<tr>{''.join(tds)}</tr>")
    table = (f'<<table border="0" cellborder="0" cellspacing="0" cellpadding="3">'
             f'{"".join(cells)}</table>>')
    lines.append(f'  {ident} [shape=plaintext, label={table}];')


# --- the span listing ---------------------------------------------------------

def listing(tree, s):
    span_of, _ = _node_spans(tree)
    out = []

    def visit(node, depth):
        a, b = span_of[id(node)]
        out.append(f"{a:>2}:{b:<3} {'  ' * depth}{name_of(node):<24} {s[a:b]!r}")
        if isinstance(node, lark.Tree):
            for child in node.children:
                visit(child, depth + 1)

    visit(tree, 0)
    return "\n".join(out)


# --- the figures ---------------------------------------------------------------

def marked_tree(s):
    tree = raw_tree(s)
    for fraction in tree.find_data("fraction"):
        parser.transformer._mark_leibniz_notation(fraction)
    return tree


def figure(name, inputs, raw=False, title=None, marked=False):
    lines = ["digraph G {", '  graph [fontname="DejaVu Sans", fontsize=12, labelloc=t, nodesep=0.15, ranksep=0.35, compound=true];',
             '  node [fontname="DejaVu Sans", fontsize=10];', '  edge [arrowhead=none, color="#777777"];']
    if title:
        lines.append(f'  label=<<b>{esc(title)}</b>>;')
    text = []
    k = 0
    for s in inputs:
        if marked:
            trees = [marked_tree(s)]
            results = parse_latex_lark_all(s)
            captions = [f"{s}   after _mark_leibniz_notation   =   {results[0]}"]
        elif raw:
            trees = [raw_tree(s)]
            results = parse_latex_lark_all(s)
            captions = [f"parse tree of {s}   (before CollapseAmbiguities)"]
        else:
            trees = readings(s)
            results = parse_latex_lark_all(s)
            captions = [f"{s}   reading {i + 1} of {len(trees)}: {results[i] if i < len(results) else '?'}"
                        for i in range(len(trees))]
            if len(trees) == 1:
                captions = [f"{s}   =   {results[0]}"]
        text.append(f"{s}\n  readings: {results}")
        for tree, caption in zip(trees, captions):
            prefix = f"c{k}"
            lines.append(f'  subgraph cluster_{prefix} {{')
            lines.append(f'    label=<<font face="DejaVu Sans Mono">{esc(caption)}</font>>; labeljust=l; style="rounded"; color="#bbbbbb"; margin=12;')
            root, leaves = tree_dot(tree, s, prefix, lines)
            if not raw:
                chart_dot(tree, s, f"{prefix}chart", lines)
                for leaf in leaves:
                    lines.append(f'  {leaf} -> {prefix}chart [style=invis, weight=0];')
            lines.append("  }")
            text.append(f"\n--- {caption}\n{listing(tree, s)}")
            k += 1
    lines.append("}")
    (OUT / f"{name}.dot").write_text("\n".join(lines), encoding="utf-8")
    (OUT / f"{name}.txt").write_text("\n".join(text) + "\n", encoding="utf-8")
    subprocess.run(["dot", "-Tpng", "-Gdpi=96", str(OUT / f"{name}.dot"), "-o", str(OUT / f"{name}.png")], check=True)
    print(name, "ok")


FIGURES = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
for spec in FIGURES:
    figure(spec["name"], spec["inputs"], raw=spec.get("raw", False), title=spec.get("title"), marked=spec.get("marked", False))
