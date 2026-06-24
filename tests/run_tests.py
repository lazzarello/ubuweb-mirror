#!/usr/bin/env python3
"""
Run all ubu module tests.

This script runs all test files in the tests/ directory and reports results.
Can be used as an alternative to pytest.
"""

import sys
import importlib.util
from pathlib import Path


def run_test_file(test_file):
    """
    Run a test file and return success status.
    
    Args:
        test_file: Path to the test file
        
    Returns:
        bool: True if all tests passed, False otherwise
    """
    print(f"\n{'='*70}")
    print(f"Running: {test_file.name}")
    print(f"{'='*70}\n")
    
    try:
        # Import and run the test module
        spec = importlib.util.spec_from_file_location(test_file.stem, test_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all test files."""
    tests_dir = Path(__file__).parent
    test_files = sorted(tests_dir.glob("test_*.py"))
    
    if not test_files:
        print("No test files found!")
        sys.exit(1)
    
    print(f"Found {len(test_files)} test files")
    
    results = {}
    for test_file in test_files:
        results[test_file.name] = run_test_file(test_file)
    
    # Print summary
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}\n")
    
    passed = sum(1 for v in results.values() if v)
    failed = len(results) - passed
    
    for test_file, success in results.items():
        status = "✓ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_file}")
    
    print(f"\n{passed} passed, {failed} failed out of {len(results)} test files\n")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("✓ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
