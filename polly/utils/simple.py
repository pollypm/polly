"""
Simple mode handling for Polly CLI.
This module manages the global simple mode state for unformatted output.
"""

# Global simple mode state
_simple_mode = False


def set_simple_mode(enabled):
    """Set the global simple mode state."""
    global _simple_mode
    _simple_mode = enabled


def is_simple_mode():
    """Check if simple mode is enabled."""
    return _simple_mode


def get_simple_colors():
    """Get empty color codes for simple mode."""
    return {
        "primary": "",
        "secondary": "",
        "success": "",
        "error": "",
        "grey": "",
        "info": "",
        "warning": "",
        "reset": "",
    }


def simple_format_message(message_type, message):
    """Format a message in simple mode (no colors or symbols)."""
    return message


def simple_print_header(title, subtitle=None):
    """Print a simple header without formatting."""
    if subtitle:
        print(f"{title} - {subtitle}")
    else:
        print(title)
