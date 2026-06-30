# Project structure — the reasoning

Every directory here exists to answer one question: *when someone new opens this repo,
can they find what they need and trust that it works?* Here's the why behind each piece.

## `src/rnaseq_tutorial/` — the importable package

The single most impactful habit: **put real logic in an installable package, not in
notebooks.** Code here can be `import`ed, unit-tested, reused across notebooks and
scripts, and reviewed in clean diffs. The `src/` layout (package nested under `src/`)
prevents a classic bug where tests accidentally import from your working directory
instead of the installed package.

## `tests/` — proof it works

Tests are not academic. They are how you and CI know a change didn't silently break
something. A repo with tests + CI earns trust instantly; one without makes every
reviewer nervous. Start small — even one test per module is a huge step up.

## `data/` — present but not committed

See [data/README.md](../data/README.md). The structure is tracked (via `.gitkeep`),
the contents are not. `raw/` is immutable input; `processed/` is regenerable output.

## `notebooks/` — exploration, numbered, output-stripped

See [notebooks/README.md](../notebooks/README.md). Great for thinking and figures,
disciplined so they don't pollute git history.

## `scripts/` — runnable entry points

The bridge between exploration and automation. `download_data.py` and
`run_pipeline.py` are plain, importable scripts that turn the package into an
end-to-end reproducible workflow.

## Root-level config files

| File                      | Job                                                        |
|---------------------------|-----------------------------------------------------------|
| `README.md`               | First thing anyone reads. What / setup / structure.       |
| `pyproject.toml`          | Package metadata + tool config (ruff, pytest) in one place.|
| `environment.yml`         | Reproducible conda env, incl. system/bioinformatics tools.|
| `Makefile`                | Memorable one-word commands for common tasks.             |
| `.gitignore`              | The guardrail that keeps data/secrets/artifacts out.      |
| `.pre-commit-config.yaml` | Local checks that run on every commit.                    |
| `.github/workflows/ci.yml`| Remote checks that run on every push/PR.                  |
| `LICENSE`                 | Tells others (and your institution) how they may use it.  |

## The mental model

```
       you edit code  ──►  pre-commit hooks  ──►  git commit
                                                      │
                                                  git push
                                                      │
                                                      ▼
                                            GitHub Actions CI
                                          (lint + test, 3.11/3.12)
                                                      │
                                          green check ✓ / red X ✗
```

Local hooks catch the cheap stuff instantly; CI is the backstop that runs the full
suite on a clean machine. Together they mean `main` is always in a known-good state.
