# Contributing to Open Product Format

Thanks for helping improve OPF.

## Quick start

```bash
git clone https://github.com/eidos-agi/opf.git
cd opf
python -m pip install -e ".[dev]"
```

## Development checks

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
python -m opf.validate --selftest
```

Keep concepts atomic, preserve stable IDs, and add a validator rule only for an
observed failure. New validation branches require a focused regression test.

## Pull requests

- Keep each change focused.
- Update `CHANGELOG.md` for user-visible changes.
- Run the development checks before opening a pull request.
- Explain any schema compatibility impact.

Open an issue with the intended outcome, observed behavior, and a minimal
reproduction when possible.
