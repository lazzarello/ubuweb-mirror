"""
Test model classes and their instantiation.

Tests that model classes (Artist, Work, FilmWork, SoundWork, Page)
can be instantiated and have the expected attributes.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pytest
except ImportError:
    pytest = None


def test_artist_creation():
    """Test that Artist can be instantiated."""
    import ubu

    artist = ubu.Artist()
    assert artist is not None
    assert hasattr(artist, "name")
    assert hasattr(artist, "url")
    assert hasattr(artist, "id")
    assert hasattr(artist, "description")
    assert hasattr(artist, "born")
    assert hasattr(artist, "broken")
    assert hasattr(artist, "dmca")

    print("✓ Artist class instantiates correctly")


def test_artist_with_values():
    """Test Artist with provided values."""
    import ubu

    artist = ubu.Artist(
        name="Test Artist",
        url="https://example.com/artist",
        id=42,
        description="A test artist",
        born=1970,
        broken=False,
        dmca=False,
    )

    assert artist.name == "Test Artist"
    assert artist.url == "https://example.com/artist"
    assert artist.id == 42
    assert artist.description == "A test artist"
    assert artist.born == 1970
    assert artist.broken is False
    assert artist.dmca is False

    print("✓ Artist accepts and stores values correctly")


def test_work_creation():
    """Test that Work can be instantiated."""
    import ubu

    work = ubu.Work()
    assert work is not None
    assert hasattr(work, "name")
    assert hasattr(work, "daterange")
    assert hasattr(work, "description")
    assert hasattr(work, "url")
    assert hasattr(work, "download_url")
    assert hasattr(work, "artist")

    print("✓ Work class instantiates correctly")


def test_work_with_values():
    """Test Work with provided values."""
    import ubu

    artist = ubu.Artist(name="Test Artist")
    work = ubu.Work(
        name="Test Work",
        daterange="2020-2021",
        description="A test work",
        url="https://example.com/work",
        download_url="https://example.com/work.mp4",
    )
    work.artist = artist  # Set artist after creation

    assert work.name == "Test Work"
    assert work.daterange == "2020-2021"
    assert work.description == "A test work"
    assert work.url == "https://example.com/work"
    assert work.download_url == "https://example.com/work.mp4"
    assert work.artist == artist

    print("✓ Work accepts and stores values correctly")


def test_filmwork_creation():
    """Test that FilmWork can be instantiated."""
    import ubu

    filmwork = ubu.FilmWork()
    assert filmwork is not None
    assert isinstance(filmwork, ubu.Work)  # Should inherit from Work
    assert hasattr(filmwork, "get_media_url")

    print("✓ FilmWork class instantiates correctly")


def test_filmwork_inherits_work():
    """Test that FilmWork inherits from Work."""
    import ubu

    filmwork = ubu.FilmWork(name="Test Film")
    assert isinstance(filmwork, ubu.Work)
    assert filmwork.name == "Test Film"
    assert hasattr(filmwork, "download_url")

    print("✓ FilmWork inherits Work attributes")


def test_soundwork_creation():
    """Test that SoundWork can be instantiated."""
    import ubu

    soundwork = ubu.SoundWork()
    assert soundwork is not None
    assert isinstance(soundwork, ubu.Work)  # Should inherit from Work
    assert hasattr(soundwork, "get_media_url")
    assert hasattr(soundwork, "download_work")

    print("✓ SoundWork class instantiates correctly")


def test_soundwork_inherits_work():
    """Test that SoundWork inherits from Work."""
    import ubu

    soundwork = ubu.SoundWork(name="Test Sound")
    assert isinstance(soundwork, ubu.Work)
    assert soundwork.name == "Test Sound"
    assert hasattr(soundwork, "url")

    print("✓ SoundWork inherits Work attributes")


def test_page_creation():
    """Test that Page can be instantiated."""
    import ubu

    page = ubu.Page()
    assert page is not None
    assert hasattr(page, "get_tables")
    assert hasattr(page, "get_links")
    assert hasattr(page, "get_artists")
    assert hasattr(page, "get_artist_works")
    assert hasattr(page, "get_artist_description")

    print("✓ Page class instantiates correctly")


def test_page_methods_are_callable():
    """Test that Page methods are callable."""
    import ubu

    page = ubu.Page()
    assert callable(page.get_tables)
    assert callable(page.get_links)
    assert callable(page.get_artists)
    assert callable(page.get_artist_works)
    assert callable(page.get_artist_description)

    print("✓ Page methods are callable")


def test_work_has_download_methods():
    """Test that Work has download-related methods."""
    import ubu

    work = ubu.Work()
    assert hasattr(work, "download_work")
    assert hasattr(work, "download_alternate_work")
    assert callable(work.download_work)
    assert callable(work.download_alternate_work)

    print("✓ Work has download methods")


def test_models_are_dataclasses():
    """Test that Artist and Work are dataclasses."""
    import ubu
    from dataclasses import is_dataclass

    assert is_dataclass(ubu.Artist)
    assert is_dataclass(ubu.Work)
    assert is_dataclass(ubu.FilmWork)
    assert is_dataclass(ubu.SoundWork)

    print("✓ Model classes are dataclasses")


if __name__ == "__main__":
    # Run tests with verbose output
    print("Testing ubu model classes...\n")

    test_artist_creation()
    test_artist_with_values()
    test_work_creation()
    test_work_with_values()
    test_filmwork_creation()
    test_filmwork_inherits_work()
    test_soundwork_creation()
    test_soundwork_inherits_work()
    test_page_creation()
    test_page_methods_are_callable()
    test_work_has_download_methods()
    test_models_are_dataclasses()

    print("\n✓ All model tests passed!")
