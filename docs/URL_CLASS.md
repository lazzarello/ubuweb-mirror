# URL Class Documentation

## Overview

The `URL` class provides better encapsulation for URL handling and validation throughout the ubuweb-mirror codebase. It replaces raw string and `urllib.parse` usage with a clean, immutable, and feature-rich API.

## Features

- **Immutable**: URL objects are frozen dataclasses and cannot be modified after creation
- **Validation**: Built-in URL validation for scheme, hostname, and structure with clear error messages
  - Rejects empty strings (ValueError)
  - Rejects non-string types (TypeError)
  - Validates scheme format (ValueError for malformed schemes)
- **Normalization**: Automatically adds `https://` scheme if missing (only when no scheme delimiter present)
- **Rich API**: Easy access to URL components (scheme, hostname, path, filename, etc.)
- **Type-safe**: Provides clear type hints for all methods and properties
- **Hashable**: Can be used in sets and as dictionary keys

## Installation

The URL class is part of the `ubu` package and is automatically available:

```python
from ubu import URL, is_valid_url
```

## Basic Usage

### Creating URLs

```python
from ubu import URL

# Create from a full URL
url = URL("https://www.ubu.com/film/video.mp4")

# Scheme is added automatically if missing
url = URL("www.ubu.com/film/video.mp4")  # Becomes https://www.ubu.com/film/video.mp4

# Using the parse classmethod (alternative syntax)
url = URL.parse("https://www.ubu.com/film/")
```

### Error Handling

The URL class validates input and raises exceptions for invalid URLs:

```python
from ubu import URL

# Empty strings raise ValueError
try:
    url = URL("")
except ValueError as e:
    print(f"Error: {e}")  # "URL cannot be empty"

# Non-string types raise TypeError
try:
    url = URL(123)
except TypeError as e:
    print(f"Error: {e}")  # "URL must be a string, got int"

# Malformed schemes raise ValueError
try:
    url = URL("ht!tp://example.com")
except ValueError as e:
    print(f"Error: {e}")  # "Invalid URL scheme: ht!tp"

# Always wrap URL creation in try/except when working with untrusted input
try:
    url = URL(user_input)
    # Use url safely here
except (ValueError, TypeError) as e:
    logging.error(f"Invalid URL: {e}")
    # Handle error appropriately
```

### Accessing URL Components

```python
url = URL("https://www.ubu.com/film/artists/video.mp4?quality=high#section")

# Basic components
print(url.scheme)      # 'https'
print(url.hostname)    # 'www.ubu.com'
print(url.path)        # '/film/artists/video.mp4'
print(url.query)       # 'quality=high'
print(url.fragment)    # 'section'

# Path components
print(url.path_parts)  # ['film', 'artists', 'video.mp4']
print(url.filename)    # 'video.mp4'
print(url.extension)   # '.mp4'
```

### URL Operations

```python
# Join URLs
base = URL("https://www.ubu.com/film/")
url = base.join("artists/artist.html")
# Result: https://www.ubu.com/film/artists/artist.html

# Create from base (classmethod)
url = URL.from_base(base, "artists/artist.html")

# Change scheme
secure_url = url.with_scheme("https")

# Change path
new_url = url.with_path("/new/path.html")
```

### URL Checks

```python
url = URL("https://www.ubu.com/page.html")

# Check if HTML
if url.is_html():
    print("This is an HTML file")

# Check if secure (HTTPS)
if url.is_secure():
    print("This URL uses HTTPS")

# Check if absolute
if url.is_absolute():
    print("This is an absolute URL")

# Validate URL
if url.validate():
    print("URL is valid")
```

### String Conversion

```python
url = URL("https://www.ubu.com/film/")

# Convert to string
url_string = str(url)

# Developer representation
print(repr(url))  # URL('https://www.ubu.com/film/')

# URLs can be compared with strings
assert url == "https://www.ubu.com/film/"
```

### Validation Helper

```python
from ubu import is_valid_url

# Quick validation
if is_valid_url("https://www.ubu.com/film/"):
    print("Valid URL!")
```

## Migration from urllib.parse

### Before (using urllib.parse)

```python
from urllib.parse import urlparse

url_string = "https://www.ubu.com/film/video.mp4"
parsed = urlparse(url_string)
path_parts = parsed.path.split('/')
filename = path_parts[-1]

# Check if HTML
is_html = filename.lower().endswith(('.html', '.htm'))
```

### After (using URL class)

```python
from ubu import URL

url = URL("https://www.ubu.com/film/video.mp4")
filename = url.filename

# Check if HTML
is_html = url.is_html()
```

## Properties Reference

| Property | Type | Description |
|----------|------|-------------|
| `scheme` | `str` | URL scheme (e.g., 'https', 'http') |
| `netloc` | `str` | Network location (hostname and port) |
| `hostname` | `str` | Hostname only |
| `port` | `Optional[int]` | Port number or None |
| `path` | `str` | URL path |
| `path_parts` | `list[str]` | Path split into components |
| `filename` | `str` | Filename from path (last component) |
| `extension` | `str` | File extension including dot |
| `query` | `str` | Query string |
| `fragment` | `str` | Fragment identifier |
| `params` | `str` | Parameters |

## Methods Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `from_base(base, path)` | `URL` | Create URL by joining base and path (classmethod) |
| `parse(url_string)` | `URL` | Parse URL string (classmethod) |
| `join(path)` | `URL` | Join with relative path |
| `with_scheme(scheme)` | `URL` | Return new URL with different scheme |
| `with_path(path)` | `URL` | Return new URL with different path |
| `is_html()` | `bool` | Check if URL points to HTML file |
| `is_secure()` | `bool` | Check if URL uses HTTPS |
| `is_absolute()` | `bool` | Check if URL is absolute |
| `validate()` | `bool` | Validate URL structure |

## Examples from the Codebase

### In models.py (with error handling)

```python
from .url import URL
import logging

def download_work(self):
    if self.download_url is not None:
        response = requests.get(self.download_url, stream=True, timeout=30)
    else:
        logging.info("whoopsy daisy, can't find a download_url")
        self.download_alternate_work()
        return None
    
    if response.url != ERROR_URL:
        try:
            url = URL(self.download_url)
        except (ValueError, TypeError) as e:
            logging.error(f"Invalid download URL '{self.download_url}': {e}")
            return None
        
        filename_base = url.filename
        
        # Check if HTML using URL method
        if url.is_html():
            download_path = HTML_PATH
        else:
            download_path = DOWNLOAD_PATH
```

### In downloader.py (with error handling)

```python
from .url import URL
import logging

# Safely extract filename from URL
try:
    url = URL(work.download_url)
except (ValueError, TypeError) as e:
    logging.error(f"Invalid download URL for {work.name}: {e}")
    stats["errors"] += 1
    continue

filename = url.filename

# Check if HTML file
if url.is_html():
    file_index = html_file_index
else:
    file_index = av_file_index
```

## Benefits

1. **Better Encapsulation**: URL logic is centralized in one class
2. **Type Safety**: Clear types help catch errors at development time
3. **Cleaner Code**: Less manual string manipulation and parsing
4. **Testable**: URL class is thoroughly tested with 24+ test cases
5. **Immutable**: Thread-safe and prevents accidental modifications
6. **Consistent API**: Same interface throughout the codebase

## Testing

The URL class has comprehensive test coverage in `tests/test_url.py`:

```bash
pytest tests/test_url.py -v
```

All 27 tests verify:
- URL creation and parsing
- Component extraction (filename, extension, path parts)
- URL operations (join, with_scheme, with_path)
- Validation and checks (is_html, is_secure, is_absolute)
- Input validation (empty strings, non-string types, malformed schemes)
- Immutability and hashability
- String conversion and comparison

## Related Issues

- **Issue #18**: Build URL object class ✅ Completed

## Future Enhancements

Potential future improvements:
- Query parameter parsing and manipulation
- URL building from components
- Support for relative URLs
- IPv6 hostname support
- Internationalized domain names (IDN)
