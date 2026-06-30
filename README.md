# RNA-seq Differential Expression Tutorial

> A reference project showing what a clean, reproducible repository looks like for
> data scientists, bioinformaticians, and ML scientists. The *science* here is a toy
> RNA-seq differential-expression example — the point is the **structure and workflow**,
> not the biology.

[![CI](https://github.com/wgzeng-maker/ds-github-tutorial/actions/workflows/ci.yml/badge.svg)](https://github.com/wgzeng-maker/ds-github-tutorial/actions/workflows/ci.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Why this repo exists

When you (or a collaborator, or *future you* six months from now) open a project, you
should be able to answer three questions in under a minute:

1. **What is this?** → top of this README
2. **How do I set it up?** → [Quickstart](#quickstart)
3. **How is it organized?** → [Project structure](docs/project_structure.md)

Everything in this repo is in service of those three answers.

## Quickstart

```bash
# 1. Clone
git clone https://github.com/wgzeng-maker/ds-github-tutorial.git
cd ds-github-tutorial

# 2. Create the environment (conda/mamba)
conda env create -f environment.yml
conda activate rnaseq-tutorial

# 3. Install the local package in editable mode
pip install -e ".[dev]"

# 4. Run the test suite to confirm everything works
make test

# 5. Run the full pipeline on the bundled toy data
make pipeline
```

## Project structure

```
ds-github-tutorial/
├── data/                # Data lives here — but is NOT committed (see data/README.md)
│   ├── raw/             # Immutable inputs. Never edit by hand.
│   └── processed/       # Derived data. Reproducible from raw/ + code.
├── notebooks/           # Exploration. Numbered, prose-light, not the source of truth.
├── src/rnaseq_tutorial/ # The actual importable, testable Python package.
├── tests/               # Automated tests. CI runs these on every push.
├── scripts/             # Entry-point scripts (download data, run pipeline).
├── docs/                # Longer-form documentation.
├── environment.yml      # Conda environment (system + Python deps).
├── pyproject.toml       # Package metadata + tool config (ruff, pytest).
└── Makefile             # One-word commands for common tasks.
```

See [docs/project_structure.md](docs/project_structure.md) for the reasoning behind each choice.

## The golden rule of reproducible data science

> **Raw data + code = everything else.**

If you ever can't regenerate a result from raw data and committed code, that result
isn't reproducible. This is why `data/processed/` is git-ignored: it's an *output*,
not a *source*. The same logic applies to model checkpoints, figures, and reports.

## License

[MIT](LICENSE) — do whatever you want, no warranty.
