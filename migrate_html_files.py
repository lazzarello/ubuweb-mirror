#!/usr/bin/env python
"""
Migration script to move HTML files from A/V directory to HTML directory.

This script helps existing users separate their HTML files from A/V content
after upgrading to the version that separates file types.

Usage:
    python migrate_html_files.py [--dry-run]
"""

import argparse
import shutil
from pathlib import Path
from ubu.constants import DOWNLOAD_PATH, HTML_PATH


def migrate_html_files(dry_run=False):
    """
    Move all HTML files from DOWNLOAD_PATH to HTML_PATH.
    
    Args:
        dry_run: If True, only report what would be moved without moving
    """
    download_dir = Path(DOWNLOAD_PATH)
    html_dir = Path(HTML_PATH)
    
    if not download_dir.exists():
        print(f"Error: Download directory does not exist: {download_dir}")
        return
    
    # Create HTML directory if it doesn't exist
    if not html_dir.exists():
        if dry_run:
            print(f"Would create directory: {html_dir}")
        else:
            html_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {html_dir}")
    
    # Find all HTML files
    html_patterns = ['*.html', '*.htm', '*.HTML', '*.HTM']
    html_files = []
    
    for pattern in html_patterns:
        html_files.extend(download_dir.glob(pattern))
    
    # Also find files with html/htm extension but wrong separator (like "file,html")
    for file in download_dir.iterdir():
        if file.is_file():
            name_lower = file.name.lower()
            # Check for common typos: comma instead of period
            if name_lower.endswith(',html') or name_lower.endswith(',htm'):
                if file not in html_files:
                    html_files.append(file)
    
    if not html_files:
        print("No HTML files found to migrate.")
        return
    
    print(f"\nFound {len(html_files)} HTML file(s) to migrate")
    print(f"From: {download_dir}")
    print(f"To:   {html_dir}\n")
    
    if dry_run:
        print("DRY RUN - No files will be moved\n")
    
    moved_count = 0
    error_count = 0
    
    for html_file in html_files:
        dest = html_dir / html_file.name
        
        try:
            if dry_run:
                print(f"Would move: {html_file.name}")
            else:
                # Check if destination exists
                if dest.exists():
                    print(f"Skipping (already exists): {html_file.name}")
                    continue
                
                shutil.move(str(html_file), str(dest))
                print(f"Moved: {html_file.name}")
                moved_count += 1
        except Exception as e:
            print(f"Error moving {html_file.name}: {e}")
            error_count += 1
    
    print(f"\n{'DRY RUN ' if dry_run else ''}Summary:")
    print(f"  Files {'that would be ' if dry_run else ''}moved: {moved_count if not dry_run else len(html_files)}")
    if error_count > 0:
        print(f"  Errors: {error_count}")


def main():
    parser = argparse.ArgumentParser(
        description='Migrate HTML files from A/V directory to HTML directory',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This script separates HTML files from A/V content by moving them to a
dedicated HTML directory. This ensures your media server (like Jellyfin)
only contains playable audio/video content.

Examples:
  python migrate_html_files.py              # Preview what will be moved
  python migrate_html_files.py --execute    # Actually move the files
        """
    )
    
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually move files (default is dry-run mode)'
    )
    
    args = parser.parse_args()
    
    print("HTML File Migration Tool")
    print("=" * 60)
    
    # By default, run in dry-run mode for safety
    dry_run = not args.execute
    
    migrate_html_files(dry_run=dry_run)
    
    if dry_run:
        print("\nTo actually move these files, run:")
        print("  python migrate_html_files.py --execute")


if __name__ == "__main__":
    main()
