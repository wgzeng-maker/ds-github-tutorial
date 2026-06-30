# Contributing

This file tells collaborators (and future-you) how to work in the repo. Even a solo
project benefits from writing the workflow down once.

## The branch + PR workflow

Never commit straight to `main`. Instead:

```bash
# 1. Start from an up-to-date main
git checkout main
git pull

# 2. Create a descriptively-named branch
git checkout -b feature/add-volcano-plot      # or fix/cpm-divide-by-zero

# 3. Make changes, committing in small logical chunks
git add src/rnaseq_tutorial/plots.py
git commit -m "Add volcano plot helper"

# 4. Push the branch
git push -u origin feature/add-volcano-plot

# 5. Open a pull request
gh pr create --fill        # or open it in the GitHub web UI
```

CI runs automatically on the PR. Once it's green and reviewed, **squash and merge**,
then delete the branch.

## Why branches + PRs even when solo?

- `main` always stays working and deployable.
- Every change gets a CI run before it lands.
- The PR is a written record of *why* a change happened — invaluable months later.
- It's the exact workflow you'll use on any team, so the habit pays off.

## Commit messages

- Imperative mood: "Add CPM normalization", not "Added" / "Adds".
- First line under ~50 chars; add a body if the *why* needs explaining.

## Before you push

```bash
make format   # auto-fix style
make lint     # confirm it's clean
make test     # confirm tests pass
```

(Or let the pre-commit hooks and CI do it for you — but locally is faster to iterate.)

## Working with a coding agent (e.g. Claude Code)

A few habits make agent-assisted work smooth and safe:

- **Let the agent work on a branch**, then review its PR — same as a human collaborator.
- **Read the diff before merging.** The agent explains its reasoning; you stay the
  decision-maker, especially for anything touching data or results.
- **Keep changes small and scoped.** "Add a volcano plot function with a test" is a
  great agent task; "redo the whole analysis" is not.
- **Tests + CI are your safety net.** They catch an agent's mistakes the same way they
  catch yours.
