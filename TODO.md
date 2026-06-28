# UbuWeb Mirror - TODO

## High Priority

### Add FilmWork and SoundWork Classes
Extend the Work base class to support specialized handling for film and sound media types.
- [ ] Create FilmWork subclass inheriting from Work
- [ ] Create SoundWork subclass inheriting from Work
- [ ] Add type-specific validation and metadata handling
- [ ] Update tests

**Related files:** `models.py`

### Write Log Parser for Failed Downloads
Build a tool to analyze download logs and identify failed downloads for retry/investigation.
- [ ] Parse log files to extract download failures
- [ ] Generate report of failed URLs
- [ ] Optionally support retry mechanism

**Related files:** New module, logging in `models.py`

### Add SQLite ORM/Database Layer
Include an ORM or database layer for tracking downloads, metadata, and state.
- [ ] Evaluate ORM options (SQLAlchemy, Peewee, etc.)
- [ ] Design schema for artists, works, downloads
- [ ] Implement database integration
- [ ] Add migration system

**Related files:** New module, refactor `models.py`

## Medium Priority

### Improve Artist Identification System
Build a better system to uniquely identify artists than array indexes based on DOM `<a>` tag order.
- [ ] Design stable artist ID system (URL-based? name-based?)
- [ ] Refactor code to use new IDs
- [ ] Handle edge cases (renamed artists, redirects)
- [ ] Update tests

**Related files:** `models.py`

### Partial Download System
Implement detection and handling of partial/incomplete downloads.
- [ ] Check file size against Content-Length header
- [ ] Resume interrupted downloads
- [ ] Mark partial files for re-download
- [ ] Integration with file_index.py skip logic

**Related files:** `models.py:81`, `file_index.py`  
**Note:** Currently `file_index.py` skips existing files but doesn't validate completeness

### Extract Description Text from DOM
Build conventions to extract untagged "description" text for artists and works.
- [ ] Identify description text patterns (siblings to `<table>` tags?)
- [ ] Implement extraction logic with word count threshold
- [ ] Handle edge cases and noise
- [ ] Store descriptions in metadata

**Related files:** `models.py`

### Log Analysis Tool
Write a tool to graph and analyze download statistics from logs.
- [ ] Parse logs for download metrics
- [ ] Generate statistics (speed, success rate, etc.)
- [ ] Create visualizations/graphs
- [ ] Export reports

**Related files:** New module

## Low Priority

### Refactor Page Model
Refactor Page class to only accept URL objects for all methods.
- [ ] Build URL class (see next item)
- [ ] Update Page to accept URL objects only
- [ ] Remove artist object parameter handling
- [ ] Consider Page base class with subclasses for different page types

**Related files:** `models.py:123`

### Build URL Object
Create a URL class to encapsulate URL handling and validation.
- [ ] Design URL class interface
- [ ] Migrate from string/urllib.parse usage
- [ ] Add validation and normalization
- [ ] Update all URL handling code

**Related files:** `models.py:125`

### Broken Links Model Extension
Extend broken links and zero-content pages model to always represent accurate broken state.
- [ ] Track broken links persistently
- [ ] Differentiate types of failures (404, timeout, zero bytes)
- [ ] Generate reports of broken content
- [ ] Historical tracking of link health

**Related files:** New module or extend `models.py`

### Email Notification System
Add system to email site maintainers about broken links/issues.
- [ ] Collect broken link/content reports
- [ ] Format notification email
- [ ] Configure SMTP/email sending
- [ ] Schedule periodic reports

**Note:** Original TODO mentions "Kenny G (NOT the WFMU person)" - verify correct contact

## Future Enhancements

### Concurrent Download Optimization
Optimize checking for existing downloads concurrently.
- [ ] Design concurrent file checking strategy
- [ ] Avoid race conditions
- [ ] Handle filesystem locking

**Related files:** `models.py`, `file_index.py`

### Concurrent Downloads
Implement parallel/concurrent downloading of multiple works.
- [ ] Design concurrent download architecture
- [ ] Add rate limiting
- [ ] Handle failures gracefully
- [ ] Configurable concurrency level

### Alternative Writing Algorithms
Try different writing algorithms rather than linear order of `<a>` elements in DOM.
- [ ] Research optimal traversal strategies
- [ ] Implement alternative algorithms
- [ ] Benchmark and compare performance

### Command Line Arguments
Add command line arguments using the `click` library.
- [ ] Define CLI interface
- [ ] Implement argument parsing with click
- [ ] Add help documentation
- [ ] Support common operations (download, analyze, report)

### Develop Reading Chapter
Extend support for the reading/text section of UbuWeb.
- [ ] Analyze reading section structure
- [ ] Implement reading-specific parsing
- [ ] Handle text/PDF downloads
- [ ] Add tests for reading content

## Completed

- [x] DMCA magic string removal (models.py:151) - Removed obsolete commented code

## Obsolete

- ~~Twitter Tweet Caching~~ - Twitter API shut down, see `TWITTER_DEPRECATION.md`
