"""
Debug mode handling for Polly CLI.
This module manages the global debug mode state for verbose error reporting.
"""

import traceback
import sys

# Global debug mode state
_debug_mode = False


def set_debug_mode(enabled):
    """Set the global debug mode state."""
    global _debug_mode
    _debug_mode = enabled


def is_debug_mode():
    """Check if debug mode is enabled."""
    return _debug_mode


def debug_print(message):
    """Print a debug message if debug mode is enabled."""
    if _debug_mode:
        print(f"DEBUG: {message}", file=sys.stderr)


def format_error_with_debug(basic_error, detailed_error=None, exception=None):
    """
    Format an error message with optional debug information.

    :param basic_error: The basic error message shown to users
    :param detailed_error: Additional error details shown in debug mode
    :param exception: Exception object to show traceback in debug mode
    :return: Formatted error message
    """
    if not _debug_mode:
        return basic_error

    debug_parts = [basic_error]

    if detailed_error:
        debug_parts.append(f"Details: {detailed_error}")

    if exception:
        debug_parts.append(f"Exception: {type(exception).__name__}: {str(exception)}")
        debug_parts.append(f"Traceback:\n{traceback.format_exc()}")

    return "\n".join(debug_parts)


def handle_exception_with_debug(basic_message, exception):
    """
    Handle an exception with appropriate debug information.

    :param basic_message: Basic error message for users
    :param exception: The exception that occurred
    :return: Formatted error message
    """
    if _debug_mode:
        return f"{basic_message}\nException Details: {type(exception).__name__}: {str(exception)}\nTraceback:\n{traceback.format_exc()}"
    else:
        return basic_message
