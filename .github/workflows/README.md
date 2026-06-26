# GitHub Actions CI/CD

This repository uses GitHub Actions for continuous integration.

## Workflows

### Test Workflow (`.github/workflows/test.yml`)

Runs on every push to `main` and `create-module` branches, and on all pull requests.

**Matrix Testing:**
- Python 3.10
- Python 3.11
- Python 3.12

**Steps:**
1. Checkout code
2. Set up Python
3. Install `uv` (with caching enabled)
4. Install dependencies with `uv sync`
5. Run custom test runner: `uv run python tests/run_tests.py`
6. Run pytest: `uv run pytest tests/ -v`

### Lint Workflow (`.github/workflows/lint.yml`)

Runs basic sanity checks:

**Steps:**
1. Verify `uv.lock` is up to date
2. Install dependencies
3. Test that `import ubu` works
4. Verify FileIndex can be created

## Running Locally

To run the same tests locally:

```bash
# Install dependencies
uv sync

# Run tests (matches CI)
uv run python tests/run_tests.py

# Or with pytest
uv run pytest tests/ -v
```

## Badge Status

Add to README.md:

```markdown
![Test](https://github.com/lazzarello/ubuweb-mirror/actions/workflows/test.yml/badge.svg)
![Lint](https://github.com/lazzarello/ubuweb-mirror/actions/workflows/lint.yml/badge.svg)
```

## Notes

- Tests do not require network access (all HTTP calls are mocked)
- Tests do not require the `/home/lee/jellyfin/ubuweb/` directory
- FileIndex tests create temporary directories for testing
- All 48 tests should pass on all Python versions
