# Migration to UV

This project has been migrated to use [uv](https://github.com/astral-sh/uv) for dependency management as of commit `[current]`.

## What Changed?

### New Files
- **pyproject.toml** - Modern Python project configuration
- **uv.lock** - Lock file ensuring reproducible builds (committed to git)

### Modified Files
- **requirements.txt** - Still maintained for backward compatibility
- **requirements-dev.txt** - Still maintained for backward compatibility
- **ubu/models.py** - Fixed imports to use relative imports (`.constants`)

### Dependencies Now in pyproject.toml
All dependencies are now declared in `pyproject.toml`:
```toml
[project]
dependencies = [
    "requests",
    "requests-html",
    "lxml[html-clean]",
    "beautifulsoup4",
    "tqdm",
    "youtube-dl",
    "tweepy",
]

[dependency-groups]
dev = [
    "pytest>=7.0.0",
    "pytest-mock>=3.0.0",
]
```

## Why UV?

1. **Speed** - 10-100x faster than pip
2. **Reliability** - Deterministic dependency resolution
3. **Modern** - Built-in virtual environment management
4. **Compatible** - Works with existing pip/requirements.txt workflows

## Migration Commands

### For New Contributors
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup project
git clone <repo>
cd ubuweb-mirror
uv sync
```

### For Existing Contributors
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Pull latest changes
git pull origin create-module

# Sync dependencies (replaces pip install -r requirements.txt)
uv sync
```

### Running Commands
```bash
# Old way
source .venv/bin/activate
python main.py
python tests/run_tests.py
pytest tests/

# New way (no activation needed!)
uv run python main.py
uv run python tests/run_tests.py
uv run pytest tests/
```

## Backward Compatibility

The project still supports traditional pip workflows:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
python main.py
```

Both `requirements.txt` and `requirements-dev.txt` are maintained for users who prefer pip.

## Lock File

**Important:** `uv.lock` is committed to git. This ensures:
- Reproducible builds across all environments
- Exact dependency versions for everyone
- No surprises from dependency updates
- Easier debugging and security auditing

## Testing

All 40 tests pass with uv:
```bash
uv run pytest tests/ -v
# ============================== 40 passed in 0.28s ==============================
```

## Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [pyproject.toml specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
- [PEP 735 - Dependency Groups](https://peps.python.org/pep-0735/)
