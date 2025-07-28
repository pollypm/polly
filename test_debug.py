#!/usr/bin/env python3

"""
Test script to verify debug mode functionality in Polly Package Manager
"""

import sys
import os

# Add the project root to sys.path so we can import polly modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from polly.utils.debug import (
    set_debug_mode,
    is_debug_mode,
    debug_print,
    format_error_with_debug,
    handle_exception_with_debug,
)


def test_debug_functionality():
    """Test the debug functionality"""
    print("Testing debug functionality...\n")

    # Test 1: Debug mode off
    print("1. Testing with debug mode OFF:")
    set_debug_mode(False)
    print(f"   Debug mode: {is_debug_mode()}")
    debug_print("This debug message should NOT appear")
    basic_error = format_error_with_debug("Basic error message", "Detailed error info")
    print(f"   Error message: {basic_error}")
    print()

    # Test 2: Debug mode on
    print("2. Testing with debug mode ON:")
    set_debug_mode(True)
    print(f"   Debug mode: {is_debug_mode()}")
    debug_print("This debug message SHOULD appear")
    detailed_error = format_error_with_debug(
        "Basic error message", "Detailed error info"
    )
    print(f"   Error message: {detailed_error}")
    print()

    # Test 3: Exception handling
    print("3. Testing exception handling:")
    try:
        raise ValueError("Test exception")
    except Exception as e:
        error_with_traceback = handle_exception_with_debug("Something went wrong", e)
        print(f"   Exception message: {error_with_traceback}")
    print()

    print("Debug functionality test completed!")


if __name__ == "__main__":
    test_debug_functionality()
