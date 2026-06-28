# HTML File Separation Feature

## Summary

This feature separates HTML files from audio/video content during downloads. HTML files are now saved to `~/tmp/ubuweb/` while A/V content continues to be saved to `~/jellyfin/ubuweb/`.

## Changes Made

### 1. New Constant: `HTML_PATH`
- Added `HTML_PATH = "/home/lee/tmp/ubuweb/"` to `ubu/constants.py`
- Exported in `ubu/__init__.py` for public API access

### 2. Smart File Routing in `download_work()`
- Modified `ubu/models.py` Work class to check file extensions
- Files ending in `.html` or `.htm` are routed to `HTML_PATH`
- All other files go to `DOWNLOAD_PATH` (A/V content)

### 3. Dual Index Support
- Updated `full_download_run()` in `ubu/downloader.py` to maintain two file indices:
  - `av_file_index`: Tracks existing A/V files in `DOWNLOAD_PATH`
  - `html_file_index`: Tracks existing HTML files in `HTML_PATH`
- Skip-existing feature now checks the appropriate index based on file type

### 4. Migration Script
- Created `migrate_html_files.py` to help existing users migrate
- Supports dry-run mode (default) for safety
- Moves HTML files from A/V directory to dedicated HTML directory

### 5. Documentation
- Updated README.md with new "File Organization" section
- Explains the separation and benefits for media server users

## Benefits

1. **Clean Media Server**: Jellyfin directory only contains playable content
2. **Preserved Data**: HTML files kept in separate location for future reference
3. **Backward Compatible**: Existing installations continue to work
4. **Smart Detection**: Automatically routes files based on extension

## Migration for Existing Users

Moved 3,749 HTML files from `~/jellyfin/ubuweb/` to `~/tmp/ubuweb/`

To migrate in the future, run:
```bash
python migrate_html_files.py              # Preview changes
python migrate_html_files.py --execute    # Execute migration
```

## File Counts After Migration

- A/V files in `~/jellyfin/ubuweb/`: 3,119
- HTML files in `~/tmp/ubuweb/`: 3,749
- Total files: 6,868
