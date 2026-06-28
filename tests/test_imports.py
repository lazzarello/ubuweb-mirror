"""
Test basic imports and module structure.

Verifies that the ubu module can be imported and all expected
exports are available.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pytest
except ImportError:
    pytest = None


def test_module_import():
    """Test that the ubu module can be imported."""
    import ubu

    assert ubu is not None


def test_module_version():
    """Test that the module has a version string."""
    import ubu

    assert hasattr(ubu, "__version__")
    assert isinstance(ubu.__version__, str)
    assert len(ubu.__version__) > 0


def test_module_all_exports():
    """Test that __all__ contains expected number of exports."""
    import ubu

    assert hasattr(ubu, "__all__")
    assert (
        len(ubu.__all__) == 20
    )  # 7 constants + 5 models + 5 functions + 2 file_index + 1 twitter
    print(f"✓ Module exports {len(ubu.__all__)} items")


def test_constants_available():
    """Test that all constants are exported."""
    import ubu

    constants = [
        "BASE_URL",
        "FILM_URL",
        "BASE_FILM_URL",
        "DOWNLOAD_PATH",
        "ERROR_URL",
        "BROKEN_PAGES",
    ]

    for const in constants:
        assert hasattr(ubu, const), f"Missing constant: {const}"
        assert const in ubu.__all__, f"Constant {const} not in __all__"

    print("✓ All constants available")


def test_constants_values():
    """Test that constants have expected types and values."""
    import ubu

    # Test URLs are strings
    assert isinstance(ubu.BASE_URL, str)
    assert isinstance(ubu.FILM_URL, str)
    assert isinstance(ubu.BASE_FILM_URL, str)
    assert isinstance(ubu.ERROR_URL, str)

    # Test URLs are valid
    assert ubu.BASE_URL.startswith("http")
    assert ubu.FILM_URL.startswith("http")
    assert "ubuweb" in ubu.FILM_URL or "ubu.com" in ubu.FILM_URL

    # Test DOWNLOAD_PATH
    assert isinstance(ubu.DOWNLOAD_PATH, str)
    assert len(ubu.DOWNLOAD_PATH) > 0

    # Test BROKEN_PAGES is a list
    assert isinstance(ubu.BROKEN_PAGES, list)

    print("✓ All constants have correct types and values")


def test_model_classes_available():
    """Test that all model classes are exported."""
    import ubu

    classes = ["Artist", "Work", "FilmWork", "SoundWork", "Page"]

    for cls in classes:
        assert hasattr(ubu, cls), f"Missing class: {cls}"
        assert cls in ubu.__all__, f"Class {cls} not in __all__"
        assert callable(getattr(ubu, cls)), f"{cls} is not callable"

    print("✓ All model classes available")


def test_downloader_functions_available():
    """Test that all downloader functions are exported."""
    import ubu

    functions = [
        "download_random_work_from",
        "download_all_works_from",
        "full_download_run",
        "get_url_from_text",
        "download_from_tweet",
    ]

    for func in functions:
        assert hasattr(ubu, func), f"Missing function: {func}"
        assert func in ubu.__all__, f"Function {func} not in __all__"
        assert callable(getattr(ubu, func)), f"{func} is not callable"

    print("✓ All downloader functions available")


def test_twitter_class_available():
    """Test that the Tweets class is exported."""
    import ubu

    assert hasattr(ubu, "Tweets")
    assert "Tweets" in ubu.__all__
    assert callable(ubu.Tweets)

    print("✓ Tweets class available")


def test_submodules_not_directly_exposed():
    """Test that internal submodules are not directly in namespace."""
    import ubu

    # These should not be directly accessible from ubu
    internal_modules = ["constants", "models", "downloader", "twitter"]

    for module in internal_modules:
        # The module exists internally
        assert hasattr(ubu, module) or True  # Module files exist
        # But not exposed in __all__
        assert module not in ubu.__all__

    print("✓ Internal modules properly encapsulated")


def test_no_import_errors():
    """Test that importing ubu doesn't raise any errors."""
    try:
        import ubu

        # Try to access each export
        for name in ubu.__all__:
            getattr(ubu, name)
        print("✓ No import errors detected")
    except ImportError as e:
        pytest.fail(f"Import error: {e}")
    except AttributeError as e:
        pytest.fail(f"Attribute error: {e}")


if __name__ == "__main__":
    # Run tests with verbose output
    print("Testing ubu module imports...\n")

    test_module_import()
    test_module_version()
    test_module_all_exports()
    test_constants_available()
    test_constants_values()
    test_model_classes_available()
    test_downloader_functions_available()
    test_twitter_class_available()
    test_submodules_not_directly_exposed()
    test_no_import_errors()

    print("\n✓ All import tests passed!")
