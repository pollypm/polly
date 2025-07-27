# ANSI color constants
RESET = "\033[0m"
PRIMARY_COLOR = "#4F8EF7"  # Blue
SECONDARY_COLOR = "#F7B32B"  # Orange
SUCCESS_COLOR = "#4ADE80"  # Green
ERROR_COLOR = "#EF4444"  # Red
GREY_COLOR = "#808080"  # Grey
INFO_COLOR = "#06B6D4"  # Cyan
WARNING_COLOR = "#F59E0B"  # Yellow


def hex_to_ansi(hex_color):
    """Convert hex color to ANSI escape sequence."""
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"


def get_colors():
    """Get color codes for consistent styling."""
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


def format_message(message_type, message, simple_mode=False):
    """Format a message with appropriate color and symbol."""
    if simple_mode:
        # Simple plain text format for system integration
        if message_type == "error":
            return f"ERROR: {message}"
        elif message_type == "success":
            return f"SUCCESS: {message}"
        elif message_type == "warning":
            return f"WARNING: {message}"
        elif message_type == "info":
            return f"INFO: {message}"
        elif message_type == "progress":
            return f"PROGRESS: {message}"
        else:
            return message
    
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


def print_header(title, subtitle=None, simple_mode=False):
    """Print a formatted header."""
    if simple_mode:
        # Simple plain text header for system integration
        if subtitle:
            print(f"{title} - {subtitle}")
        else:
            print(title)
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
