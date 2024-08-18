# Contributing

Create focused changes that pair behavioral modifications with their tests. Avoid mixing broad formatting, unrelated refactors, and feature work in the same commit.

Before submitting a change, run:

```bash
python scripts/verify_reproducibility.py
ruff check .
mypy src
pytest -q
pip-audit -r requirements.lock
```

Commit messages should describe the behavior changed, for example:

```text
feat(reconciliation): support grouped settlement matching
fix(import): reject duplicate statement line keys
perf(reporting): avoid repeated case scans per account
```

Do not add synthetic padding comments, fabricated contributors, backdated commits, or meaningless commit bursts. Repository history should reflect actual engineering work.
