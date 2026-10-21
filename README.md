Graphviz diagrams for the explanatory comment on sympy/sympy#30571 (Lark LaTeX parser).
Render with `dot -Tpng -Gdpi=96 name.dot -o name.png`. Not meant to be merged.

`spans/`: parse trees of example expressions with the substring every node covers, for the
second comment. Regenerate with the repository on `PYTHONPATH` and the branch of the PR checked out:
`python spans/render.py spans spans/figs.json`.
