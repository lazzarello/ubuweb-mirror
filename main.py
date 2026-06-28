"""UbuWeb Mirror - Main entry point

This script provides the command-line interface for UbuWeb Mirror.

Usage:
    python main.py              # Show help
    python main.py download     # Download archive
    python main.py analyze      # Analyze downloaded content
    python main.py report       # Generate report
    python main.py random       # Download random work
"""

from ubu.cli import main

if __name__ == "__main__":
    main()
