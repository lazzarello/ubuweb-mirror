"""
Configuration for pytest.

This file configures pytest for the ubu test suite.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path so tests can import ubu
sys.path.insert(0, str(Path(__file__).parent.parent))


if pytest:
    def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests that integrate multiple components"
    )
    config.addinivalue_line(
        "markers", "network: marks tests that require network access"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


@pytest.fixture
def mock_artist():
    """Fixture providing a mock Artist object."""
    import ubu
        return ubu.Artist(
            name="Test Artist",
            url="https://www.ubu.com/film/test.html",
            id=1,
            description="A test artist"
        )


    @pytest.fixture
    def mock_work():
    """Fixture providing a mock Work object."""
    import ubu
        return ubu.Work(
            name="Test Work",
            url="https://www.ubu.com/film/test_work.html",
            daterange="2020",
            description="A test work"
        )


    @pytest.fixture
    def mock_page():
        """Fixture providing a Page instance."""
        import ubu
        return ubu.Page()
