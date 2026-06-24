# UbuWeb Mirror Test Suite

This directory contains comprehensive tests for the `ubu` module.

## Test Files

- **test_imports.py** - Tests module imports, exports, and basic structure
- **test_models.py** - Tests model classes (Artist, Work, FilmWork, SoundWork, Page)
- **test_downloader.py** - Tests download functions with mocking
- **test_integration.py** - Integration tests verifying components work together
- **conftest.py** - Pytest configuration and fixtures

## Running Tests

### Run All Tests

```bash
# Using pytest (recommended)
pytest tests/

# Or with verbose output
pytest tests/ -v

# Run individual test files
.venv/bin/python tests/test_imports.py
.venv/bin/python tests/test_models.py
.venv/bin/python tests/test_downloader.py
.venv/bin/python tests/test_integration.py
```

### Run Specific Test Categories

```bash
# Run only import tests
pytest tests/test_imports.py -v

# Run only model tests
pytest tests/test_models.py -v

# Run integration tests
pytest tests/ -m integration -v

# Skip slow tests
pytest tests/ -m "not slow" -v
```

### Run Tests Without Pytest

Each test file can be run directly as a Python script:

```bash
.venv/bin/python tests/test_imports.py
.venv/bin/python tests/test_models.py
.venv/bin/python tests/test_downloader.py
.venv/bin/python tests/test_integration.py
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

Tests require:
```
pytest
```

Install with:
```bash
.venv/bin/python -m pip install pytest
```

## Notes

- Most tests use mocking to avoid network calls
- Tests marked with `@pytest.mark.integration` may have more dependencies
- Tests marked with `@pytest.mark.network` require internet access (none currently)
- Each test file can run independently without pytest
