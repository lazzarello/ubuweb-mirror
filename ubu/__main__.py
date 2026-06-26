"""UbuWeb Mirror - Main entry point

This module runs a full download/sync of the UbuWeb film archive.
By default, it skips files that already exist in the download directory.

Usage:
    python -m ubu              # Skip existing files (default)
    python -m ubu --no-skip    # Re-check all files
    ubu-download               # Console script (after pip install)
"""

import sys
import argparse
from . import full_download_run, DOWNLOAD_PATH


def main():
    """
    Main function - runs full archive download with skip-existing enabled.
    """
    parser = argparse.ArgumentParser(
        description='UbuWeb Mirror - Archive UbuWeb film content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ubu-download                 Download new files, skip existing (default)
  ubu-download --no-skip       Force re-check all files
  python -m ubu                Same as ubu-download

The script builds an index of existing files and only downloads new content.
        """
    )
    
    parser.add_argument(
        '--no-skip',
        action='store_true',
        help='Disable skip-existing feature and re-check all files'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    args = parser.parse_args()
    
    skip_existing = not args.no_skip
    
    if skip_existing:
        print("Running with skip-existing ENABLED (will skip downloaded files)")
    else:
        print("Running with skip-existing DISABLED (will re-check all files)")
    
    print(f"Download path: {DOWNLOAD_PATH}")
    print()
    
    # Run the full download
    full_download_run(skip_existing=skip_existing)


if __name__ == "__main__":
    main()
