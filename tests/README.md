# UbuWeb Mirror Test Suite

This directory contains comprehensive tests for the `ubu` module.

## Test Files

- **test_imports.py** - Tests module imports, exports, and basic structure
- **test_models.py** - Tests model classes (Artist, Work, FilmWork, SoundWork, Page)
- **test_downloader.py** - Tests download functions with mocking
- **test_integration.py** - Integration tests verifying components work together
- **conftest.py** - Pytest configuration and fixtures

## Running Tests

### With UV (Recommended)

```bash
# Run all tests with pytest
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=ubu -v

# Run specific test file
uv run pytest tests/test_imports.py -v

# Run integration tests only
uv run pytest tests/ -m integration -v

# Run tests in parallel (if pytest-xdist installed)
uv run pytest tests/ -n auto -v
```

### Without uv (Legacy)

```bash
# With pytest
pytest tests/ -v
```

## Test Coverage

The test suite covers:

### Module Structure (test_imports.py)
- ✓ Module can be imported
- ✓ Version string exists
- ✓ All 17 exports are available
- ✓ Constants have correct types and values
- ✓ Classes are callable
- ✓ Functions are accessible
- ✓ Internal modules are properly encapsulated

### Model Classes (test_models.py)
- ✓ Artist instantiation and attributes
- ✓ Work instantiation and attributes
- ✓ FilmWork inheritance from Work
- ✓ SoundWork inheritance from Work
- ✓ Page instantiation and methods
- ✓ Models are dataclasses
- ✓ Download methods exist

### Downloader Functions (test_downloader.py)
- ✓ All download functions exist
- ✓ URL regex pattern works
- ✓ download_all_works_from structure
- ✓ download_random_work_from structure
- ✓ Error handling is present
- ✓ Logging is configured
- ✓ URL resolution works (mocked)
- ✓ Tweet download structure

### Integration (test_integration.py)
- ✓ Components work together
- ✓ Artist-Work relationships
- ✓ FilmWork specialization
- ✓ SoundWork specialization
- ✓ Constants used by functions
- ✓ Page methods integration
- ✓ Logging configuration

## Dependencies

Tests require pytest (automatically installed with `uv sync`):

```bash
# With uv (recommended)
uv sync  # Installs all dependencies including pytest

# With pip (legacy)
pip install -r requirements-dev.txt
```

## Notes

- Most tests use mocking to avoid network calls
- Tests marked with `@pytest.mark.integration` may have more dependencies
- Tests marked with `@pytest.mark.network` require internet access (none currently)
- Each test file can run independently without pytest
