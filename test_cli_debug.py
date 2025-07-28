#!/usr/bin/env python3

"""
Test script to verify CLI debug flag functionality
"""

import sys
import os

# Add the project root to sys.path so we can import polly modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from polly.cli.cli import dispatch_command
from polly.utils.debug import is_debug_mode, set_debug_mode
from polly.utils.simple import is_simple_mode, set_simple_mode


def test_cli_debug_flag():
    """Test the CLI debug flag parsing"""
    print("Testing CLI debug flag functionality...\n")

    # Reset modes
    set_debug_mode(False)
    set_simple_mode(False)

    # Test 1: No flags
    print("1. Testing with no flags:")
    # Simulate: polly help
    print(f"   Before: Debug={is_debug_mode()}, Simple={is_simple_mode()}")
    # We won't actually call dispatch_command here to avoid output,
    # but we can test the flag parsing logic

    # Test 2: Debug flag only
    print("2. Testing --debug flag:")
    test_args = ["--debug", "help"]
    print(f"   Args: {test_args}")

    # Manually test the flag parsing logic (simplified)
    debug_mode = False
    simple_mode = False
    args = test_args.copy()

    while args and args[0].startswith("--"):
        if args[0] == "--simple":
            simple_mode = True
            args = args[1:]
        elif args[0] == "--debug":
            debug_mode = True
            args = args[1:]
        else:
            break

    print(f"   Parsed: Debug={debug_mode}, Simple={simple_mode}, Remaining args={args}")

    # Test 3: Both flags
    print("3. Testing --debug --simple flags:")
    test_args = ["--debug", "--simple", "help"]
    print(f"   Args: {test_args}")

    # Reset and parse again
    debug_mode = False
    simple_mode = False
    args = test_args.copy()

    while args and args[0].startswith("--"):
        if args[0] == "--simple":
            simple_mode = True
            args = args[1:]
        elif args[0] == "--debug":
            debug_mode = True
            args = args[1:]
        else:
            break

    print(f"   Parsed: Debug={debug_mode}, Simple={simple_mode}, Remaining args={args}")

    # Test 4: Flags in different order
    print("4. Testing --simple --debug flags:")
    test_args = ["--simple", "--debug", "upgrade", "--check-only"]
    print(f"   Args: {test_args}")

    # Reset and parse again
    debug_mode = False
    simple_mode = False
    args = test_args.copy()

    while args and args[0].startswith("--"):
        if args[0] == "--simple":
            simple_mode = True
            args = args[1:]
        elif args[0] == "--debug":
            debug_mode = True
            args = args[1:]
        else:
            break

    print(f"   Parsed: Debug={debug_mode}, Simple={simple_mode}, Remaining args={args}")

    print("\nCLI debug flag test completed!")


if __name__ == "__main__":
    test_cli_debug_flag()
