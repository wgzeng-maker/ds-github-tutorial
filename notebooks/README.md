# Notebooks

Notebooks are for **exploration and communication**, not as the source of truth for
logic. The rules of thumb that keep notebooks from becoming a mess:

1. **Number them** so the intended reading order is obvious:
   `01_exploratory_analysis.ipynb`, `02_qc.ipynb`, `03_results_figures.ipynb`.

2. **Import, don't define.** Heavy logic lives in `src/rnaseq_tutorial/` where it can be
   tested. A notebook cell should read like:
   ```python
   from rnaseq_tutorial import simulate_counts, differential_expression
   counts, labels = simulate_counts()
   results = differential_expression(counts, labels)
   ```
   If you find yourself writing a 40-line function in a cell, move it into the package.

3. **Strip outputs before committing.** Cell outputs bloat diffs and leak data. The
   `nbstripout` pre-commit hook (see `.pre-commit-config.yaml`) does this automatically.
   Without it, every re-run makes git think the whole notebook changed.

4. **Notebooks are not pipelines.** When an analysis becomes something you re-run, port
   it to a script in `scripts/` (like `run_pipeline.py`) so it's automatable and testable.

> Why so strict? Notebooks store code *and* output *and* execution order as JSON. That
> makes them great for thinking and terrible for version control unless you tame them.
