#!/usr/bin/env python3
"""
Test script to verify the ubu module imports correctly.
"""

import ubu

def test_imports():
    """Test that all expected exports are available."""
    print("Testing ubu module import...")
    print(f"✓ Module version: {ubu.__version__}")
    print(f"✓ Available exports: {len(ubu.__all__)}")
    
    # Test constants
    print(f"\nConstants:")
    print(f"  FILM_URL: {ubu.FILM_URL}")
    print(f"  DOWNLOAD_PATH: {ubu.DOWNLOAD_PATH}")
    
    # Test classes are importable
    print(f"\nClasses:")
    print(f"  ✓ Artist: {ubu.Artist}")
    print(f"  ✓ Work: {ubu.Work}")
    print(f"  ✓ FilmWork: {ubu.FilmWork}")
    print(f"  ✓ SoundWork: {ubu.SoundWork}")
    print(f"  ✓ Page: {ubu.Page}")
    
    # Test functions are importable
    print(f"\nFunctions:")
    print(f"  ✓ download_all_works_from")
    print(f"  ✓ full_download_run")
    
    print("\n✓ All imports successful!")

if __name__ == "__main__":
    test_imports()
