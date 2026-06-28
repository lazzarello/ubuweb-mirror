"""
Test file index functionality.

Tests the FileIndex class that tracks existing downloaded files.
"""

import sys
from pathlib import Path
import tempfile

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pytest
except ImportError:
    pytest = None


def test_file_index_creation():
    """Test that FileIndex can be instantiated."""
    import ubu

    with tempfile.TemporaryDirectory() as tmpdir:
        index = ubu.FileIndex(tmpdir)
        assert index is not None
        assert index.download_path == Path(tmpdir)
        assert len(index.filenames) == 0

    print("✓ FileIndex creation works")


def test_file_index_build_empty():
    """Test building index on empty directory."""
    import ubu

    with tempfile.TemporaryDirectory() as tmpdir:
        index = ubu.FileIndex(tmpdir).build()
        assert len(index) == 0
        assert index.total_files == 0
        assert index.total_size == 0

    print("✓ FileIndex handles empty directory")


def test_file_index_build_with_files():
    """Test building index with files present."""
    import ubu

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some test files
        test_files = ["test1.mp4", "test2.avi", "test3.mov"]

        for filename in test_files:
            filepath = Path(tmpdir) / filename
            filepath.write_text("test content")

        index = ubu.FileIndex(tmpdir).build()

        assert len(index) == 3
        assert index.total_files == 3
        assert index.total_size > 0

        for filename in test_files:
            assert index.has_file(filename)
            assert filename in index

    print("✓ FileIndex scans and indexes files")


def test_file_index_has_file():
    """Test file existence checking."""
    import ubu

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a file
        filepath = Path(tmpdir) / "exists.mp4"
        filepath.write_text("content")

        index = ubu.FileIndex(tmpdir).build()

        assert index.has_file("exists.mp4")
        assert not index.has_file("missing.mp4")
        assert "exists.mp4" in index
        assert "missing.mp4" not in index

    print("✓ FileIndex file checking works")


def test_file_index_get_full_path():
    """Test getting full path for a filename."""
    import ubu

    with tempfile.TemporaryDirectory() as tmpdir:
        index = ubu.FileIndex(tmpdir)

        full_path = index.get_full_path("test.mp4")
        assert full_path == Path(tmpdir) / "test.mp4"
        assert isinstance(full_path, Path)

    print("✓ FileIndex path generation works")


def test_build_file_index_function():
    """Test the convenience function."""
    import ubu

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        for i in range(5):
            (Path(tmpdir) / f"file{i}.mp4").write_text("test")

        index = ubu.build_file_index(tmpdir)

        assert isinstance(index, ubu.FileIndex)
        assert len(index) == 5

    print("✓ build_file_index convenience function works")


def test_file_index_nonexistent_directory():
    """Test handling of nonexistent directory."""
    import ubu

    with tempfile.TemporaryDirectory() as tmpdir:
        nonexistent = Path(tmpdir) / "nonexistent"
        index = ubu.FileIndex(str(nonexistent)).build()

        # Should create the directory
        assert nonexistent.exists()
        assert len(index) == 0

    print("✓ FileIndex creates missing directory")


def test_file_index_with_real_jellyfin_path():
    """Test with the actual jellyfin path (read-only check)."""
    import ubu

    jellyfin_path = "/home/lee/jellyfin/ubuweb/"

    if not Path(jellyfin_path).exists():
        print("⚠ Skipping real path test - directory doesn't exist")
        return

    index = ubu.build_file_index(jellyfin_path)

    print(f"  Found {len(index)} files in jellyfin directory")
    print(f"  Total size: {index.total_size / (1024**3):.1f} GB")

    # Check for some known files
    if len(index) > 0:
        print(f"  Sample files: {list(index.filenames)[:3]}")

    print("✓ FileIndex works with production directory")


if __name__ == "__main__":
    # Run tests with verbose output
    print("Testing file index functionality...\n")

    test_file_index_creation()
    test_file_index_build_empty()
    test_file_index_build_with_files()
    test_file_index_has_file()
    test_file_index_get_full_path()
    test_build_file_index_function()
    test_file_index_nonexistent_directory()
    test_file_index_with_real_jellyfin_path()

    print("\n✓ All file index tests passed!")
