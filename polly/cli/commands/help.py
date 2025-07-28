import os
import sys
import shutil

# Add project root to sys.path for imports
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from polly.core import (
        update_required,
        latest_version,
        get_current_version,
        get_recent_commit_messages,
    )
except ImportError:
    # Fallback functions if core module is not available
    def update_required():
        return False

    def latest_version():
        return "Unknown"

    def get_current_version():
        return "Unknown"

    def get_recent_commit_messages():
        return []


# Import simple mode utilities
from polly.utils import is_simple_mode


# ANSI color constants
RESET = "\033[0m"
PRIMARY_COLOR = "#4F8EF7"  # Blue
SECONDARY_COLOR = "#F7B32B"  # Orange


def hex_to_ansi(hex_color):
    """Convert hex color to ANSI escape sequence."""
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"


def read_ascii_art(file_path):
    """Read ASCII art from file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "[ASCII art not found]"


def get_terminal_width():
    """Get terminal width, with fallback for narrow terminals."""
    try:
        terminal_size = shutil.get_terminal_size()
        return terminal_size.columns
    except (OSError, AttributeError):
        return 80  # Default fallback


def should_hide_ascii_art(terminal_width):
    """Determine if ASCII art should be hidden based on terminal width."""
    # ASCII art is approximately 50 characters wide, help text needs ~40 more
    # Add some margin for spacing
    return terminal_width < 100


def create_simple_header():
    """Create a simple text header for narrow terminals."""
    return """┌─ Polly Package Manager ─┐
│        Help Menu        │
└─────────────────────────┘"""


def help_simple():
    """Display help in simple mode for external applications."""
    print("commands:help,update,install,uninstall,list,inspect,upgrade")
    print(f"version:{get_current_version()[:7]}")
    print(f"latest_version:{latest_version()[:7]}")
    print(f"update_available:{update_required()}")


def help_main():
    """Display the help message with ASCII art."""
    # Check if in simple mode
    if is_simple_mode():
        help_simple()
        return

    terminal_width = get_terminal_width()
    hide_ascii_art = should_hide_ascii_art(terminal_width)

    if hide_ascii_art:
        # Use simple header for narrow terminals
        ascii_art = create_simple_header()
    else:
        # Use full ASCII art for wider terminals
        ascii_art_path = os.path.join(os.path.dirname(__file__), "../polly.txt")
        ascii_art = read_ascii_art(ascii_art_path)

    # Check for updates and get commit messages
    has_updates = update_required()
    recent_commits = get_recent_commit_messages() if has_updates else []

    # Build commit messages section
    commit_section = ""
    if has_updates and recent_commits:
        commit_section = "\n\n  {s}Recent Changes:"
        # Show max 5 commits
        display_commits = recent_commits[:5]
        for commit in display_commits:
            commit_section += "\n    {g}• " + commit

        # Show "X more" if there are additional commits
        if len(recent_commits) > 5:
            remaining = len(recent_commits) - 5
            commit_section += "\n    {g}• + " + str(remaining) + " more"

    help_text = """{p}Polly {g}- {s}Help
{g}Version {version} (Latest: {p}{latest_version}{g})
{g}Updates Available: {p}{update_required}{g}{commit_messages}

{s}Usage:
  {p}polly {g}<command> [options]

{s}Available Commands:
  {p}help        {g}Show this help message
  {p}update      {g}Update Polly to the latest version
  {p}install     {g}Install a Polly package
  {p}uninstall   {g}Uninstall a Polly package
  {p}list        {g}List installed Polly packages
  {p}inspect     {g}Show information about a Polly package
  {p}upgrade     {g}Upgrade Polly packages

{s}For more information, visit: {p}https://github.com/pollypm/polly
"""

    # Color setup
    primary_color = hex_to_ansi(PRIMARY_COLOR)
    secondary_color = hex_to_ansi(SECONDARY_COLOR)
    grey_color = hex_to_ansi("#808080")

    # Format update status
    update_status = (
        f"Yes {grey_color}({primary_color}use {secondary_color}polly update{grey_color})"
        if update_required()
        else "No"
    )

    if hide_ascii_art:
        # Simple layout for narrow terminals
        print("\n")

        # Display the simple header with colors
        header_lines = ascii_art.splitlines()
        for line in header_lines:
            colored_line = line.replace(
                "Polly Package Manager", f"{primary_color}Polly Package Manager{RESET}"
            )
            colored_line = colored_line.replace(
                "Help Menu", f"{secondary_color}Help Menu{RESET}"
            )
            print(f"  {colored_line}")

        print()

        # Display help text without side-by-side layout
        help_lines = help_text.splitlines()
        for help_line in help_lines:
            formatted_help = (
                help_line.replace("{commit_messages}", commit_section)
                .replace("{p}", primary_color)
                .replace("{s}", secondary_color)
                .replace("{g}", grey_color)
                .replace("{latest_version}", latest_version()[:7])
                .replace("{version}", get_current_version()[:7])
                .replace("{update_required}", update_status)
            )
            print(f"  {formatted_help}{RESET}")
    else:
        # Original side-by-side layout for wider terminals
        art_lines = ascii_art.splitlines()
        help_lines = help_text.splitlines()

        # Ensure both lists have the same length
        max_lines = max(len(art_lines), len(help_lines))
        art_lines += [""] * (max_lines - len(art_lines))
        help_lines += [""] * (max_lines - len(help_lines))

        spacing = "   "

        print("\n")
        for art, help_line in zip(art_lines, help_lines):
            # Replace color placeholders and version info
            formatted_help = (
                help_line.replace("{p}", primary_color)
                .replace("{s}", secondary_color)
                .replace("{g}", grey_color)
                .replace("{latest_version}", latest_version()[:7])
                .replace("{version}", get_current_version()[:7])
                .replace("{update_required}", update_status)
                .replace("{commit_messages}", commit_section)
            )

            print(f"  {art:<40}{RESET}{spacing}{formatted_help}{RESET}")

    print("\n")


if __name__ == "__main__":
    help_main()
