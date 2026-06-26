#!/usr/bin/env python3
"""
Test script to verify the skip-existing-files feature works.

This demonstrates how the file index speeds up incremental downloads.
"""

import ubu

def test_index_performance():
    """Test how fast the index builds and checks files."""
    import time
    
    print("Testing file index performance...")
    print("=" * 60)
    
    # Build the index
    start = time.time()
    index = ubu.build_file_index(ubu.DOWNLOAD_PATH)
    elapsed = time.time() - start
    
    print(f"✓ Built index of {len(index)} files in {elapsed:.2f} seconds")
    print(f"  Total size: {index.total_size / (1024**3):.1f} GB")
    print(f"  Average: {len(index)/elapsed:.0f} files/second")
    print()
    
    # Test lookup speed
    print("Testing lookup performance...")
    sample_files = list(index.filenames)[:100] if len(index) > 0 else []
    
    start = time.time()
    for filename in sample_files:
        _ = index.has_file(filename)
    elapsed = time.time() - start
    
    if sample_files:
        print(f"✓ Checked {len(sample_files)} files in {elapsed:.4f} seconds")
        print(f"  Average: {len(sample_files)/elapsed:.0f} lookups/second")
    
    print()
    return index


def show_sample_files(index, n=10):
    """Show a sample of files in the index."""
    if len(index) == 0:
        print("No files in index")
        return
    
    print(f"Sample of {min(n, len(index))} files:")
    print("-" * 60)
    for i, filename in enumerate(list(index.filenames)[:n], 1):
        full_path = index.get_full_path(filename)
        try:
            size_mb = full_path.stat().st_size / (1024**2)
            print(f"{i:2d}. {filename[:50]:<50} {size_mb:>8.1f} MB")
        except:
            print(f"{i:2d}. {filename}")
    print()


def simulate_skip_check():
    """Simulate checking if files would be skipped."""
    print("Simulating skip-existing check...")
    print("=" * 60)
    
    index = ubu.build_file_index(ubu.DOWNLOAD_PATH)
    
    # Test with some example URLs (these are made up for demonstration)
    test_filenames = [
        "zizek!.avi",  # Should exist
        "new_unreleased_film.mp4",  # Should not exist
        "40jahrevideokunst.de_Abramovic-Ulay_City-of-Angels_1983.mp4",  # Should exist
    ]
    
    for filename in test_filenames:
        if index.has_file(filename):
            print(f"✓ Would SKIP: {filename} (already downloaded)")
        else:
            print(f"→ Would DOWNLOAD: {filename} (not in archive)")
    
    print()


def main():
    print("\n")
    print("=" * 60)
    print("UBUWEB FILE INDEX - SKIP EXISTING FILES TEST")
    print("=" * 60)
    print()
    
    # Test performance
    index = test_index_performance()
    
    # Show sample
    show_sample_files(index, n=15)
    
    # Simulate skip logic
    simulate_skip_check()
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✓ File index is ready for incremental downloads")
    print(f"✓ {len(index)} existing files will be skipped")
    print(f"✓ Only new/missing files will be downloaded")
    print()
    print("To run a full catch-up download:")
    print("  uv run python main.py")
    print()


if __name__ == "__main__":
    main()
