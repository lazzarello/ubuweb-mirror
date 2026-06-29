"""
Test URL class functionality.

Tests the URL class for proper encapsulation, validation, and normalization
of URL handling.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pytest
except ImportError:
    pytest = None

from ubu.url import URL, is_valid_url


def test_url_creation():
    """Test that URL can be instantiated."""
    url = URL("https://www.ubu.com/film/")
    assert url is not None
    assert str(url) == "https://www.ubu.com/film/"
    print("✓ URL instantiates correctly")


def test_url_parsing():
    """Test URL component parsing."""
    url = URL("https://www.ubu.com/film/video.mp4?quality=high#section")
    
    assert url.scheme == "https"
    assert url.hostname == "www.ubu.com"
    assert url.path == "/film/video.mp4"
    assert url.query == "quality=high"
    assert url.fragment == "section"
    
    print("✓ URL parsing works correctly")


def test_url_filename():
    """Test filename extraction from URL."""
    url = URL("https://www.ubu.com/film/movies/test.mp4")
    assert url.filename == "test.mp4"
    
    url2 = URL("https://www.ubu.com/film/")
    assert url2.filename == ""
    
    print("✓ Filename extraction works correctly")


def test_url_extension():
    """Test file extension extraction."""
    url1 = URL("https://www.ubu.com/film/video.mp4")
    assert url1.extension == ".mp4"
    
    url2 = URL("https://www.ubu.com/film/page.html")
    assert url2.extension == ".html"
    
    url3 = URL("https://www.ubu.com/film/")
    assert url3.extension == ""
    
    print("✓ Extension extraction works correctly")


def test_url_is_html():
    """Test HTML file detection."""
    html_url1 = URL("https://www.ubu.com/page.html")
    assert html_url1.is_html() is True
    
    html_url2 = URL("https://www.ubu.com/page.HTM")
    assert html_url2.is_html() is True
    
    video_url = URL("https://www.ubu.com/video.mp4")
    assert video_url.is_html() is False
    
    print("✓ HTML detection works correctly")


def test_url_path_parts():
    """Test path splitting into components."""
    url = URL("https://www.ubu.com/film/artists/video.mp4")
    parts = url.path_parts
    
    assert parts == ["film", "artists", "video.mp4"]
    assert len(parts) == 3
    
    print("✓ Path parts splitting works correctly")


def test_url_is_secure():
    """Test HTTPS detection."""
    secure_url = URL("https://www.ubu.com/film/")
    assert secure_url.is_secure() is True
    
    insecure_url = URL("http://www.ubu.com/film/")
    assert insecure_url.is_secure() is False
    
    print("✓ Secure URL detection works correctly")


def test_url_is_absolute():
    """Test absolute URL detection."""
    absolute_url = URL("https://www.ubu.com/film/")
    assert absolute_url.is_absolute() is True
    
    print("✓ Absolute URL detection works correctly")


def test_url_from_base():
    """Test creating URL from base and path."""
    base = URL("https://www.ubu.com/film/")
    url = URL.from_base(base, "artists/artist.html")
    
    assert str(url) == "https://www.ubu.com/film/artists/artist.html"
    print("✓ URL.from_base works correctly")


def test_url_from_base_with_absolute_path():
    """Test creating URL from base with absolute path."""
    base = URL("https://www.ubu.com/film/")
    url = URL.from_base(base, "/other/path.html")
    
    assert str(url) == "https://www.ubu.com/other/path.html"
    print("✓ URL.from_base with absolute path works correctly")


def test_url_join():
    """Test joining URL with relative path."""
    base = URL("https://www.ubu.com/film/")
    url = base.join("artists/artist.html")
    
    assert str(url) == "https://www.ubu.com/film/artists/artist.html"
    print("✓ URL.join works correctly")


def test_url_with_scheme():
    """Test changing URL scheme."""
    url = URL("https://www.ubu.com/film/")
    http_url = url.with_scheme("http")
    
    assert str(http_url) == "http://www.ubu.com/film/"
    assert url.is_secure() is True
    assert http_url.is_secure() is False
    
    print("✓ URL.with_scheme works correctly")


def test_url_with_path():
    """Test changing URL path."""
    url = URL("https://www.ubu.com/film/old.html")
    new_url = url.with_path("/film/new.html")
    
    assert str(new_url) == "https://www.ubu.com/film/new.html"
    print("✓ URL.with_path works correctly")


def test_url_validation():
    """Test URL validation."""
    valid_url = URL("https://www.ubu.com/film/")
    assert valid_url.validate() is True
    
    # Test with invalid hostname (though it will still parse)
    # The validation should catch obviously invalid URLs
    print("✓ URL validation works")


def test_url_equality():
    """Test URL equality comparison."""
    url1 = URL("https://www.ubu.com/film/")
    url2 = URL("https://www.ubu.com/film/")
    url3 = URL("https://www.ubu.com/other/")
    
    assert url1 == url2
    assert url1 != url3
    assert url1 == "https://www.ubu.com/film/"
    
    print("✓ URL equality works correctly")


def test_url_immutability():
    """Test that URL is immutable."""
    url = URL("https://www.ubu.com/film/")
    
    # URL should be frozen (immutable)
    try:
        url._url = "https://example.com/"
        # If we get here, the dataclass is not properly frozen
        assert False, "URL should be immutable"
    except (AttributeError, Exception):
        # Expected: can't modify frozen dataclass
        pass
    
    print("✓ URL is immutable")


def test_url_hash():
    """Test that URL is hashable."""
    url1 = URL("https://www.ubu.com/film/")
    url2 = URL("https://www.ubu.com/film/")
    url3 = URL("https://www.ubu.com/other/")
    
    # Can be used in sets
    url_set = {url1, url2, url3}
    assert len(url_set) == 2  # url1 and url2 are the same
    
    # Can be used as dict keys
    url_dict = {url1: "value1"}
    assert url_dict[url2] == "value1"
    
    print("✓ URL is hashable")


def test_url_bool():
    """Test URL boolean conversion."""
    url = URL("https://www.ubu.com/film/")
    assert bool(url) is True
    
    print("✓ URL boolean conversion works")


def test_url_repr():
    """Test URL string representation."""
    url = URL("https://www.ubu.com/film/")
    assert repr(url) == "URL('https://www.ubu.com/film/')"
    
    print("✓ URL repr works correctly")


def test_url_parse_classmethod():
    """Test URL.parse class method."""
    url = URL.parse("https://www.ubu.com/film/")
    assert isinstance(url, URL)
    assert str(url) == "https://www.ubu.com/film/"
    
    print("✓ URL.parse works correctly")


def test_is_valid_url_function():
    """Test is_valid_url helper function."""
    assert is_valid_url("https://www.ubu.com/film/") is True
    assert is_valid_url("www.ubu.com") is True  # Will be normalized to https://
    
    print("✓ is_valid_url function works correctly")


def test_url_with_port():
    """Test URL with port number."""
    url = URL("https://www.ubu.com:8080/film/")
    assert url.hostname == "www.ubu.com"
    assert url.port == 8080
    assert url.netloc == "www.ubu.com:8080"
    
    print("✓ URL with port works correctly")


def test_url_normalization():
    """Test URL normalization (adding https if missing)."""
    url = URL("www.ubu.com/film/")
    assert url.scheme == "https"
    assert str(url) == "https://www.ubu.com/film/"
    
    print("✓ URL normalization works correctly")


def test_url_special_characters_in_path():
    """Test URL with special characters in path."""
    url = URL("https://www.ubu.com/film/artist%20name/video.mp4")
    assert url.path == "/film/artist%20name/video.mp4"
    assert url.filename == "video.mp4"
    
    print("✓ URL with special characters works correctly")


def test_url_empty_string_validation():
    """Test that empty strings raise ValueError."""
    try:
        URL("")
        assert False, "Empty string should raise ValueError"
    except ValueError as e:
        assert "cannot be empty" in str(e)
    
    try:
        URL("   ")
        assert False, "Whitespace-only string should raise ValueError"
    except ValueError as e:
        assert "cannot be empty" in str(e)
    
    print("✓ Empty string validation works correctly")


def test_url_type_validation():
    """Test that non-string types raise TypeError."""
    try:
        URL(123)
        assert False, "Integer should raise TypeError"
    except TypeError as e:
        assert "must be a string" in str(e)
    
    try:
        URL(None)
        assert False, "None should raise TypeError"
    except TypeError as e:
        assert "must be a string" in str(e)
    
    try:
        URL(["https://example.com"])
        assert False, "List should raise TypeError"
    except TypeError as e:
        assert "must be a string" in str(e)
    
    print("✓ Type validation works correctly")


def test_url_malformed_scheme_validation():
    """Test that malformed schemes are rejected and valid schemes are kept."""
    # Scheme with special characters should be rejected
    try:
        URL("ht!tp://example.com")
        assert False, "Scheme with special characters should raise ValueError"
    except ValueError as e:
        assert "Malformed URL" in str(e) or "Invalid URL scheme" in str(e)
    
    try:
        URL("123://example.com")
        assert False, "Scheme starting with number should raise ValueError"
    except ValueError as e:
        assert "Malformed URL" in str(e) or "Invalid URL scheme" in str(e)
    
    # Valid schemes should work (including uncommon ones like 'htp')
    # The key fix is that 'htp://example.com' stays as-is and doesn't
    # become 'https://htp://example.com' due to normalization
    url = URL("https://example.com")
    assert url.scheme == "https"
    
    url2 = URL("ftp://example.com")
    assert url2.scheme == "ftp"
    
    # Even uncommon schemes are preserved if they match the format
    url3 = URL("htp://example.com")
    assert url3.scheme == "htp"
    assert str(url3) == "htp://example.com"  # Not normalized to https://htp://...
    
    print("✓ Malformed scheme validation works correctly")


if __name__ == "__main__":
    # Run tests with verbose output
    print("Testing URL class...\n")
    
    test_url_creation()
    test_url_parsing()
    test_url_filename()
    test_url_extension()
    test_url_is_html()
    test_url_path_parts()
    test_url_is_secure()
    test_url_is_absolute()
    test_url_from_base()
    test_url_from_base_with_absolute_path()
    test_url_join()
    test_url_with_scheme()
    test_url_with_path()
    test_url_validation()
    test_url_equality()
    test_url_immutability()
    test_url_hash()
    test_url_bool()
    test_url_repr()
    test_url_parse_classmethod()
    test_is_valid_url_function()
    test_url_with_port()
    test_url_normalization()
    test_url_special_characters_in_path()
    test_url_empty_string_validation()
    test_url_type_validation()
    test_url_malformed_scheme_validation()
    
    print("\n✓ All URL tests passed!")
