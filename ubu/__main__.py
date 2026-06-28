"""UbuWeb Mirror - Main entry point

This module provides the command-line interface for UbuWeb Mirror.

Usage:
    python -m ubu              # Show help
    python -m ubu download     # Download archive
    python -m ubu analyze      # Analyze downloaded content
    python -m ubu report       # Generate report
    ubu                        # Console script (after pip install)
"""

from .cli import main

if __name__ == "__main__":
    main()
