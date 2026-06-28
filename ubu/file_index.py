"""
File index utilities for tracking downloaded files.

Provides functions to scan the download directory and build an in-memory
index of existing files for fast skip-checking during downloads.
"""

from pathlib import Path
from typing import Set
import logging

logger = logging.getLogger(__name__)


class FileIndex:
    """
    Fast in-memory index of downloaded files.

    Loads filenames from the download directory into a set for O(1) lookups.
    """

    def __init__(self, download_path: str):
        """
        Initialize the index by scanning the download directory.

        Args:
            download_path: Path to the directory containing downloaded files
        """
        self.download_path = Path(download_path)
        self.filenames: Set[str] = set()
        self.total_files = 0
        self.total_size = 0

    def build(self) -> "FileIndex":
        """
        Scan the download directory and build the index.

        Returns:
            self for method chaining
        """
        if not self.download_path.exists():
            logger.warning(f"Download path does not exist: {self.download_path}")
            logger.info(f"Creating directory: {self.download_path}")
            self.download_path.mkdir(parents=True, exist_ok=True)
            return self

        if not self.download_path.is_dir():
            raise ValueError(f"Download path is not a directory: {self.download_path}")

        logger.info(f"Scanning {self.download_path} for existing files...")

        for entry in self.download_path.iterdir():
            if entry.is_file():
                self.filenames.add(entry.name)
                self.total_files += 1
                try:
                    self.total_size += entry.stat().st_size
                except OSError:
                    pass  # Skip files we can't stat

        size_gb = self.total_size / (1024**3)
        logger.info(f"Index built: {self.total_files} files ({size_gb:.1f} GB)")

        return self

    def has_file(self, filename: str) -> bool:
        """
        Check if a file exists in the index.

        Args:
            filename: Name of the file to check (just the basename)

        Returns:
            True if file exists, False otherwise
        """
        return filename in self.filenames

    def get_full_path(self, filename: str) -> Path:
        """
        Get the full path for a filename.

        Args:
            filename: Name of the file

        Returns:
            Full Path object
        """
        return self.download_path / filename

    def __len__(self) -> int:
        """Return the number of files in the index."""
        return self.total_files

    def __contains__(self, filename: str) -> bool:
        """Support 'filename in index' syntax."""
        return self.has_file(filename)


def build_file_index(download_path: str) -> FileIndex:
    """
    Convenience function to build a file index.

    Args:
        download_path: Path to the download directory

    Returns:
        FileIndex instance
    """
    return FileIndex(download_path).build()
