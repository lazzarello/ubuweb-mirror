"""
URL class for better encapsulation of URL handling and validation.

This module provides a URL class that replaces raw string and urllib.parse usage
throughout the codebase, offering better validation, normalization, and a cleaner API.
"""

from urllib.parse import urlparse, urlunparse, urljoin
from dataclasses import dataclass
from typing import Optional
import re


@dataclass(frozen=True)
class URL:
    """
    Immutable URL class that encapsulates URL handling and validation.
    
    Attributes:
        _url: The complete URL string (private)
        _parsed: Parsed URL components (private)
    
    Examples:
        >>> url = URL("https://www.ubu.com/film/video.mp4")
        >>> url.scheme
        'https'
        >>> url.hostname
        'www.ubu.com'
        >>> url.filename
        'video.mp4'
        >>> str(url)
        'https://www.ubu.com/film/video.mp4'
    """
    
    _url: str
    _parsed: object = None
    
    def __post_init__(self):
        """Validate and parse the URL after initialization."""
        # Type validation
        if not isinstance(self._url, str):
            raise TypeError(f"URL must be a string, got {type(self._url).__name__}")
        
        # Empty string validation
        if not self._url or not self._url.strip():
            raise ValueError("URL cannot be empty")
        
        # Parse the URL
        parsed = urlparse(self._url)
        
        # Store parsed result using object.__setattr__ since dataclass is frozen
        object.__setattr__(self, '_parsed', parsed)
        
        # If '://' is present, validate the scheme
        if '://' in self._url:
            if not parsed.scheme:
                # urlparse didn't recognize a scheme, likely malformed
                raise ValueError(f"Malformed URL: contains '://' but no valid scheme")
            # Validate scheme format (must be alphanumeric + plus/dot/hyphen)
            valid_scheme_pattern = r'^[a-zA-Z][a-zA-Z0-9+.\-]*$'
            if not re.match(valid_scheme_pattern, parsed.scheme):
                raise ValueError(f"Invalid URL scheme: {parsed.scheme}")
        
        # If no scheme provided and no '://' present, assume https
        if not self._parsed.scheme and '://' not in self._url:
            normalized_url = f"https://{self._url}"
            parsed = urlparse(normalized_url)
            object.__setattr__(self, '_url', normalized_url)
            object.__setattr__(self, '_parsed', parsed)
    
    @classmethod
    def from_base(cls, base: 'URL', path: str) -> 'URL':
        """
        Create a URL by joining a base URL with a relative path.
        
        Args:
            base: Base URL object
            path: Relative or absolute path to join
            
        Returns:
            New URL object with joined path
            
        Examples:
            >>> base = URL("https://www.ubu.com/film/")
            >>> url = URL.from_base(base, "artists/artist.html")
            >>> str(url)
            'https://www.ubu.com/film/artists/artist.html'
        """
        joined = urljoin(str(base), path)
        return cls(joined)
    
    @classmethod
    def parse(cls, url_string: str) -> 'URL':
        """
        Parse a URL string and return a URL object.
        
        Args:
            url_string: URL string to parse
            
        Returns:
            URL object
        """
        return cls(url_string)
    
    @property
    def scheme(self) -> str:
        """Return the URL scheme (e.g., 'https', 'http')."""
        return self._parsed.scheme
    
    @property
    def netloc(self) -> str:
        """Return the network location (hostname and port)."""
        return self._parsed.netloc
    
    @property
    def hostname(self) -> str:
        """Return the hostname."""
        return self._parsed.hostname or ''
    
    @property
    def port(self) -> Optional[int]:
        """Return the port number or None."""
        return self._parsed.port
    
    @property
    def path(self) -> str:
        """Return the URL path."""
        return self._parsed.path
    
    @property
    def path_parts(self) -> list[str]:
        """
        Return the path split into components.
        
        Returns:
            List of path components (excluding empty strings)
        """
        return [part for part in self.path.split('/') if part]
    
    @property
    def filename(self) -> str:
        """
        Return the filename from the URL path.
        
        Returns:
            Filename (last component of path), or empty string if no filename
            
        Examples:
            >>> url = URL("https://example.com/path/to/file.mp4")
            >>> url.filename
            'file.mp4'
        """
        # If path ends with /, there's no filename
        if self.path.endswith('/'):
            return ''
        parts = self.path_parts
        # Check if the last part looks like a filename (has an extension)
        # or return it anyway as it might be a filename without extension
        return parts[-1] if parts else ''
    
    @property
    def extension(self) -> str:
        """
        Return the file extension including the dot.
        
        Returns:
            File extension (e.g., '.mp4', '.html'), or empty string if none
        """
        filename = self.filename
        if '.' in filename:
            return '.' + filename.rsplit('.', 1)[1]
        return ''
    
    @property
    def query(self) -> str:
        """Return the query string."""
        return self._parsed.query
    
    @property
    def fragment(self) -> str:
        """Return the fragment identifier."""
        return self._parsed.fragment
    
    @property
    def params(self) -> str:
        """Return the parameters."""
        return self._parsed.params
    
    def is_html(self) -> bool:
        """
        Check if the URL points to an HTML file.
        
        Returns:
            True if extension is .html or .htm, False otherwise
        """
        ext = self.extension.lower()
        return ext in ('.html', '.htm')
    
    def is_secure(self) -> bool:
        """
        Check if the URL uses HTTPS.
        
        Returns:
            True if scheme is 'https', False otherwise
        """
        return self.scheme == 'https'
    
    def is_absolute(self) -> bool:
        """
        Check if the URL is absolute (has a scheme and netloc).
        
        Returns:
            True if URL is absolute, False otherwise
        """
        return bool(self.scheme and self.netloc)
    
    def with_scheme(self, scheme: str) -> 'URL':
        """
        Return a new URL with a different scheme.
        
        Args:
            scheme: New scheme (e.g., 'https', 'http')
            
        Returns:
            New URL object with updated scheme
        """
        parsed = self._parsed
        new_url = urlunparse((
            scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
        return URL(new_url)
    
    def with_path(self, path: str) -> 'URL':
        """
        Return a new URL with a different path.
        
        Args:
            path: New path
            
        Returns:
            New URL object with updated path
        """
        parsed = self._parsed
        new_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
        return URL(new_url)
    
    def join(self, path: str) -> 'URL':
        """
        Join this URL with a relative path.
        
        Args:
            path: Relative or absolute path to join
            
        Returns:
            New URL object with joined path
        """
        return URL.from_base(self, path)
    
    def validate(self) -> bool:
        """
        Validate that the URL is well-formed.
        
        Returns:
            True if URL is valid, False otherwise
        """
        # Must have a scheme and netloc for absolute URLs
        if not self.is_absolute():
            return False
        
        # Hostname should not be empty
        if not self.hostname:
            return False
        
        # Basic hostname validation (allows letters, numbers, dots, hyphens)
        hostname_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        if not re.match(hostname_pattern, self.hostname):
            return False
        
        return True
    
    def __str__(self) -> str:
        """Return the URL as a string."""
        return self._url
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"URL('{self._url}')"
    
    def __eq__(self, other) -> bool:
        """Compare URLs for equality."""
        if isinstance(other, URL):
            return self._url == other._url
        if isinstance(other, str):
            return self._url == other
        return False
    
    def __hash__(self) -> int:
        """Return hash of the URL string."""
        return hash(self._url)
    
    def __bool__(self) -> bool:
        """Return True if URL is not empty."""
        return bool(self._url)


def is_valid_url(url_string: str) -> bool:
    """
    Check if a string is a valid URL.
    
    Args:
        url_string: String to validate
        
    Returns:
        True if string is a valid URL, False otherwise
        
    Examples:
        >>> is_valid_url("https://www.ubu.com/film/")
        True
        >>> is_valid_url("not a url")
        False
    """
    try:
        url = URL(url_string)
        return url.validate()
    except (ValueError, TypeError):
        return False
