# ANSI color constants
RESET = "\033[0m"
PRIMARY_COLOR = "#4F8EF7"  # Blue
SECONDARY_COLOR = "#F7B32B"  # Orange
SUCCESS_COLOR = "#4ADE80"  # Green
ERROR_COLOR = "#EF4444"  # Red
GREY_COLOR = "#808080"  # Grey
INFO_COLOR = "#06B6D4"  # Cyan
WARNING_COLOR = "#F59E0B"  # Yellow

# Import simple mode utilities
from polly.utils.simple import (
    is_simple_mode,
    get_simple_colors,
    simple_format_message,
    simple_print_header,
)


def hex_to_ansi(hex_color):
    """Convert hex color to ANSI escape sequence."""
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"


def get_colors():
    """Get color codes for consistent styling."""
    if is_simple_mode():
        return get_simple_colors()

    return {
        "primary": hex_to_ansi(PRIMARY_COLOR),
        "secondary": hex_to_ansi(SECONDARY_COLOR),
        "success": hex_to_ansi(SUCCESS_COLOR),
        "error": hex_to_ansi(ERROR_COLOR),
        "grey": hex_to_ansi(GREY_COLOR),
        "info": hex_to_ansi(INFO_COLOR),
        "warning": hex_to_ansi(WARNING_COLOR),
        "reset": RESET,
    }


def format_message(message_type, message):
    """Format a message with appropriate color and symbol."""
    if is_simple_mode():
        return simple_format_message(message_type, message)

    colors = get_colors()

    symbols = {
        "progress": f"{colors['primary']}➤{colors['reset']}",
        "success": f"{colors['success']}✔{colors['reset']}",
        "error": f"{colors['error']}✖{colors['reset']}",
        "info": f"{colors['info']}ℹ{colors['reset']}",
        "warning": f"{colors['warning']}⚠{colors['reset']}",
        "question": f"{colors['primary']}?{colors['reset']}",
    }

    symbol = symbols.get(message_type, "")
    return f"  {symbol} {colors['grey']}{message}{colors['reset']}"


def print_header(title, subtitle=None):
    """Print a formatted header."""
    if is_simple_mode():
        simple_print_header(title, subtitle)
        return

    colors = get_colors()

    if subtitle:
        print(
            f"\n  {colors['primary']}{title}{colors['reset']} {colors['grey']}- {colors['secondary']}{subtitle}{colors['reset']}"
        )
    else:
        print(f"\n  {colors['primary']}{title}{colors['reset']}")

    # Calculate separator length
    total_length = len(title) + (len(subtitle) + 3 if subtitle else 0)
    print(f"  {colors['grey']}{'─' * total_length}{colors['reset']}\n")
