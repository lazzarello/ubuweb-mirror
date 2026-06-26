"""UbuWeb Mirror - Main entry point

This script runs a full download/sync of the UbuWeb film archive.
By default, it skips files that already exist in the download directory.

Usage:
    python main.py              # Skip existing files (default)
    python main.py --no-skip    # Re-check all files
"""

import ubu
import sys


def main():
    """
    Main function - runs full archive download with skip-existing enabled.
    """
    # Check for --no-skip flag
    skip_existing = True
    if '--no-skip' in sys.argv:
        skip_existing = False
        print("Running with skip-existing DISABLED (will re-check all files)")
    else:
        print("Running with skip-existing ENABLED (will skip downloaded files)")
    
    print(f"Download path: {ubu.DOWNLOAD_PATH}")
    print()
    
    # Run the full download
    ubu.full_download_run(skip_existing=skip_existing)


if __name__ == "__main__":
    main()
