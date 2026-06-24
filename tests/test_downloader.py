"""
Test downloader functions.

Tests the high-level download functions without actually downloading files.
Uses mocking where appropriate to avoid network calls.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pytest
except ImportError:
    pytest = None

from unittest.mock import Mock, patch, MagicMock


def test_download_functions_exist():
    """Test that all download functions are accessible."""
    import ubu
    
    assert callable(ubu.download_random_work_from)
    assert callable(ubu.download_all_works_from)
    assert callable(ubu.full_download_run)
    assert callable(ubu.get_url_from_text)
    assert callable(ubu.download_from_tweet)
    
    print("✓ All download functions exist")


def test_get_url_from_text_regex():
    """Test URL extraction from text."""
    import ubu
    import re
    
    # Test the URL regex pattern (we can't easily test the function without network)
    from ubu.downloader import URL_REGEX_STRING
    
    test_urls = [
        "https://www.ubu.com/film/test.html",
        "http://example.com/path",
        "Check out https://ubuweb.com/film/index.html for more",
    ]
    
    for text in test_urls:
        match = re.search(URL_REGEX_STRING, text)
        assert match is not None, f"Failed to match URL in: {text}"
    
    print("✓ URL regex pattern works")


@patch('ubu.downloader.Page')
def test_download_all_works_from_structure(mock_page_class):
    """Test the structure of download_all_works_from without actual downloads."""
    import ubu
    
    # Create mock objects
    mock_page = Mock()
    mock_page_class.return_value = mock_page
    
    mock_work1 = Mock()
    mock_work1.url = "http://example.com/work1"
    mock_work1.download_url = "http://example.com/work1.mp4"
    mock_work1.download_work = Mock()
    
    mock_work2 = Mock()
    mock_work2.url = "http://example.com/work2"
    mock_work2.download_url = None  # This one has no download URL
    
    mock_page.get_artist_works.return_value = [mock_work1, mock_work2]
    
    mock_artist = Mock()
    mock_artist.name = "Test Artist"
    
    # Call the function
    ubu.download_all_works_from(mock_artist)
    
    # Verify it tried to get artist works
    mock_page.get_artist_works.assert_called_once_with(mock_artist)
    
    # Verify it tried to download the work with a download_url
    mock_work1.download_work.assert_called_once()
    
    # Work2 should not have download_work called (no download_url)
    mock_work2.download_work.assert_not_called()
    
    print("✓ download_all_works_from structure is correct")


@patch('ubu.downloader.Page')
@patch('ubu.downloader.random.choice')
def test_download_random_work_from_structure(mock_random, mock_page_class):
    """Test the structure of download_random_work_from."""
    import ubu
    
    # Setup mocks
    mock_page = Mock()
    mock_page_class.return_value = mock_page
    
    mock_artist = Mock()
    mock_artist.name = "Random Artist"
    
    mock_work = Mock()
    mock_work.url = "http://example.com/random"
    mock_work.download_url = "http://example.com/random.mp4"
    mock_work.download_work = Mock()
    
    mock_page.get_artist_works.return_value = [mock_work]
    
    # Make random.choice deterministic
    mock_random.return_value = 0
    
    artists = [mock_artist]
    
    # Call the function
    ubu.download_random_work_from(artists)
    
    # Verify Page was instantiated
    mock_page_class.assert_called_once()
    
    # Verify get_artist_works was called
    mock_page.get_artist_works.assert_called_once()
    
    print("✓ download_random_work_from structure is correct")


def test_download_functions_handle_errors():
    """Test that download functions are designed to handle errors."""
    import ubu
    import inspect
    
    # Check that full_download_run has try/except
    source = inspect.getsource(ubu.full_download_run)
    assert 'try:' in source
    assert 'except' in source
    assert 'logging.error' in source or 'logging' in source
    
    print("✓ Download functions have error handling")


def test_downloader_uses_logging():
    """Test that the downloader module uses logging."""
    import ubu.downloader as downloader
    
    # Check that logging is imported and configured
    assert hasattr(downloader, 'logging')
    
    print("✓ Downloader module uses logging")


@patch('ubu.downloader.requests.get')
def test_get_url_from_text_mock(mock_get):
    """Test get_url_from_text with mocked requests."""
    import ubu
    
    # Mock the response
    mock_response = Mock()
    mock_response.url = "https://www.ubu.com/film/actual_url.html"
    mock_get.return_value = mock_response
    
    text = "Check this out: https://t.co/short"
    result = ubu.get_url_from_text(text)
    
    # Should return the resolved URL
    assert result == "https://www.ubu.com/film/actual_url.html"
    
    # Should have made a request
    mock_get.assert_called_once()
    
    print("✓ get_url_from_text resolves URLs")


@patch('ubu.downloader.Work')
@patch('ubu.downloader.get_url_from_text')
def test_download_from_tweet_structure(mock_get_url, mock_work_class):
    """Test download_from_tweet structure."""
    import ubu
    
    # Setup mocks
    mock_work = Mock()
    mock_work_class.return_value = mock_work
    mock_get_url.return_value = "https://www.ubu.com/film/test.html"
    
    mock_tweet = Mock()
    mock_tweet.text = "New film: https://t.co/abc123"
    
    # Call the function
    ubu.download_from_tweet(mock_tweet)
    
    # Verify URL was extracted
    mock_get_url.assert_called_once_with(mock_tweet.text)
    
    # Verify Work was created
    mock_work_class.assert_called_once()
    
    # Verify download_work was called
    mock_work.download_work.assert_called_once()
    
    print("✓ download_from_tweet structure is correct")


if __name__ == "__main__":
    # Run tests with verbose output
    print("Testing ubu downloader functions...\n")
    
    test_download_functions_exist()
    test_get_url_from_text_regex()
    test_download_all_works_from_structure()
    test_download_random_work_from_structure()
    test_download_functions_handle_errors()
    test_downloader_uses_logging()
    test_get_url_from_text_mock()
    test_download_from_tweet_structure()
    
    print("\n✓ All downloader tests passed!")
