"""
Test validation of the download process and error handling.

This module tests that the download process handles errors gracefully
and produces expected results.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pytest
except ImportError:
    pytest = None

from unittest.mock import Mock, patch
import ubu


def test_get_links_returns_empty_list_on_404():
    """Test that get_links returns empty list (not None) when page is 404."""
    from ubu.models import Page

    page = Page()

    # Mock requests.get to return a 404-like response
    with patch("ubu.models.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.url = "https://www.ubu.com/film/nonexistent.html"
        mock_response.content = b"<html><body>404 Not Found</body></html>"
        mock_get.return_value = mock_response

        # Mock get_tables to return empty list (no tables on 404 page)
        with patch.object(page, "get_tables", return_value=[]):
            result = page.get_links("https://www.ubu.com/film/nonexistent.html")

            # Should return empty list, not None
            assert result is not None
            assert isinstance(result, list)
            assert len(result) == 0

    print("✓ get_links returns empty list on 404")


def test_get_links_handles_insufficient_tables():
    """Test that get_links handles pages with fewer than 2 tables."""
    from ubu.models import Page

    page = Page()

    with patch("ubu.models.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.url = "https://www.ubu.com/film/test.html"
        mock_response.content = (
            b"<html><body><table><tr><td>Only one table</td></tr></table></body></html>"
        )
        mock_get.return_value = mock_response

        # Mock get_tables to return a list with only 1 table (need 2)
        mock_table = Mock()
        with patch.object(page, "get_tables", return_value=[mock_table]):
            result = page.get_links("https://www.ubu.com/film/test.html")

            # Should return empty list
            assert result is not None
            assert isinstance(result, list)
            assert len(result) == 0

    print("✓ get_links handles insufficient tables")


def test_get_artist_works_handles_empty_links():
    """Test that get_artist_works handles empty links list gracefully."""
    from ubu.models import Page, Artist

    page = Page()
    artist = Artist()
    artist.name = "Test Artist"
    artist.url = "https://www.ubu.com/film/test.html"

    # Mock get_links to return empty list
    with patch.object(page, "get_links", return_value=[]):
        works = page.get_artist_works(artist)

        # Should return empty list, not crash
        assert isinstance(works, list)
        assert len(works) == 0

    print("✓ get_artist_works handles empty links")


def test_get_artist_works_handles_one_link():
    """Test that get_artist_works handles a single link without crashing."""
    from ubu.models import Page, Artist

    page = Page()
    artist = Artist()
    artist.name = "Test Artist"
    artist.url = "https://www.ubu.com/film/test.html"

    # Create a mock link
    mock_link = Mock()
    mock_link.text = "Test Work"
    mock_link.__getitem__ = Mock(return_value="test_work.html")

    # Mock get_links to return list with one link
    with patch.object(page, "get_links", return_value=[mock_link]):
        works = page.get_artist_works(artist)

        # Should handle gracefully (pop only once, not crash)
        assert isinstance(works, list)
        # After popping once, should be empty
        assert len(works) == 0

    print("✓ get_artist_works handles single link")


def test_get_artist_works_handles_two_links():
    """Test that get_artist_works pops first two links (nav bar)."""
    from ubu.models import Page, Artist

    page = Page()
    artist = Artist()
    artist.name = "Test Artist"
    artist.url = "https://www.ubu.com/film/test.html"

    # Create mock links
    mock_links = []
    for i in range(4):
        mock_link = Mock()
        mock_link.text = f"Link {i}"
        mock_link.__getitem__ = Mock(return_value=f"link{i}.html")
        mock_links.append(mock_link)

    # Mock get_links
    with patch.object(page, "get_links", return_value=mock_links):
        works = page.get_artist_works(artist)

        # Should have 2 works (4 - 2 nav links)
        assert isinstance(works, list)
        assert len(works) == 2
        assert works[0].name == "Link 2"
        assert works[1].name == "Link 3"

    print("✓ get_artist_works correctly removes nav links")


def test_work_download_url_is_attribute_not_method():
    """Test that Work.download_url is an attribute, not a method."""
    from ubu.models import Work

    work = Work()

    # Should be able to set directly
    work.download_url = "https://www.ubu.com/film/test.mp4"
    assert work.download_url == "https://www.ubu.com/film/test.mp4"

    # Should NOT have set_download_url method
    assert not hasattr(work, "set_download_url") or not callable(
        getattr(work, "set_download_url", None)
    )

    print("✓ Work.download_url is attribute, not method")


def test_full_download_run_handles_invalid_pages():
    """Test that full_download_run handles invalid pages without crashing."""

    # Mock Page class
    with patch("ubu.downloader.Page") as mock_page_class:
        mock_page = Mock()
        mock_page_class.return_value = mock_page

        # Create mock artists - one valid, one with 404 page
        mock_artist1 = Mock()
        mock_artist1.name = "Valid Artist"
        mock_artist1.url = "https://www.ubu.com/film/valid.html"

        mock_artist2 = Mock()
        mock_artist2.name = "Invalid Artist"
        mock_artist2.url = "https://www.ubu.com/film/404.html"

        mock_page.get_artists.return_value = [mock_artist1, mock_artist2]

        # Mock get_artist_works - valid artist has work, invalid has none
        mock_work = Mock()
        mock_work.url = "https://www.ubu.com/film/work.html"
        mock_work.download_url = None

        def mock_get_artist_works(artist):
            if artist.name == "Valid Artist":
                return [mock_work]
            else:
                return []  # Invalid artist returns empty list

        mock_page.get_artist_works = mock_get_artist_works

        # Mock build_file_index
        with patch("ubu.downloader.build_file_index") as mock_build:
            mock_index = Mock()
            mock_index.__len__ = Mock(return_value=0)
            mock_build.return_value = mock_index

            # Should not raise exception
            try:
                ubu.full_download_run(skip_existing=True)
                success = True
            except Exception as e:
                success = False
                print(f"Exception raised: {e}")

            assert success, "full_download_run should handle invalid pages gracefully"

    print("✓ full_download_run handles invalid pages")


def test_download_summary_stats():
    """Test that full_download_run produces expected statistics structure."""
    import io
    import sys

    with patch("ubu.downloader.Page") as mock_page_class:
        mock_page = Mock()
        mock_page_class.return_value = mock_page

        # Create mock artists
        mock_artist = Mock()
        mock_artist.name = "Test Artist"
        mock_page.get_artists.return_value = [mock_artist]

        # Create mock work
        mock_work = Mock()
        mock_work.url = "https://www.ubu.com/film/work.html"
        mock_work.download_url = "https://www.ubu.com/film/work.mp4"
        mock_work.download_work = Mock()

        mock_page.get_artist_works.return_value = [mock_work]

        # Mock build_file_index
        with patch("ubu.downloader.build_file_index") as mock_build:
            mock_index = Mock()
            mock_index.__len__ = Mock(return_value=0)
            mock_index.has_file = Mock(return_value=False)
            mock_build.return_value = mock_index

            # Capture stdout
            captured_output = io.StringIO()
            sys.stdout = captured_output

            try:
                ubu.full_download_run(skip_existing=True)
            finally:
                sys.stdout = sys.__stdout__

            output = captured_output.getvalue()

            # Check that summary contains expected keys
            assert "DOWNLOAD SUMMARY" in output
            assert "Artists processed:" in output
            assert "Works found:" in output
            assert "Files skipped" in output
            assert "Files downloaded:" in output
            assert "Errors:" in output

    print("✓ full_download_run produces expected summary")


def test_download_path_exists():
    """Test that DOWNLOAD_PATH constant points to a valid location."""
    from ubu.constants import DOWNLOAD_PATH
    from pathlib import Path

    # DOWNLOAD_PATH should be defined
    assert DOWNLOAD_PATH is not None
    assert isinstance(DOWNLOAD_PATH, str)
    assert len(DOWNLOAD_PATH) > 0

    # If path doesn't exist, that's okay - it will be created
    # Just verify it's a valid path format
    path = Path(DOWNLOAD_PATH)
    assert path is not None

    print("✓ DOWNLOAD_PATH is defined")


if __name__ == "__main__":
    # Run tests with verbose output
    print("Testing download validation and error handling...\n")

    test_get_links_returns_empty_list_on_404()
    test_get_links_handles_insufficient_tables()
    test_get_artist_works_handles_empty_links()
    test_get_artist_works_handles_one_link()
    test_get_artist_works_handles_two_links()
    test_work_download_url_is_attribute_not_method()
    test_full_download_run_handles_invalid_pages()
    test_download_summary_stats()
    test_download_path_exists()

    print("\n✓ All validation tests passed!")
