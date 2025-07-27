import os
import sys

# Add project root to sys.path for imports
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from polly.core import update_required, latest_version, get_current_version
except ImportError:
    # Fallback functions if core module is not available
    def update_required():
        return False

    def latest_version():
        return "Unknown"

    def get_current_version():
        return "Unknown"


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


def display_help():
    """Display the help message with ASCII art."""
    ascii_art_path = os.path.join(os.path.dirname(__file__), "../polly.txt")
    ascii_art = read_ascii_art(ascii_art_path)

    help_text = """{p}Polly {g}- {s}Help
{g}Version {version} (Latest: {p}{latest_version}{g})
{g}Updates Available: {p}{update_required}{g}

{s}Usage:
  {p}polly {g}<command> [options]

{s}Available Commands:
  {p}help        {g}Show this help message
  {p}install     {g}Install a Polly package
  {p}uninstall   {g}Uninstall a Polly package
  {p}list        {g}List installed Polly packages
  {p}search      {g}Search for Polly packages
  {p}inspect     {g}Show information about a Polly package
  {p}upgrade     {g}Upgrade Polly packages

{s}For more information, visit: {p}https://github.com/pollypm/polly
"""

    art_lines = ascii_art.splitlines()
    help_lines = help_text.splitlines()

    # Ensure both lists have the same length
    max_lines = max(len(art_lines), len(help_lines))
    art_lines += [""] * (max_lines - len(art_lines))
    help_lines += [""] * (max_lines - len(help_lines))

    # Color setup
    spacing = "   "
    primary_color = hex_to_ansi(PRIMARY_COLOR)
    secondary_color = hex_to_ansi(SECONDARY_COLOR)
    grey_color = hex_to_ansi("#808080")

    # Format update status
    update_status = (
        f"Yes {grey_color}({primary_color}use {secondary_color}polly update{grey_color})"
        if update_required()
        else "No"
    )

    print("\n")
    for art, help_line in zip(art_lines, help_lines):
        # Replace color placeholders and version info
        formatted_help = (
            help_line.replace("{p}", primary_color)
            .replace("{s}", secondary_color)
            .replace("{g}", grey_color)
            .replace("{latest_version}", latest_version())
            .replace("{version}", get_current_version())
            .replace("{update_required}", update_status)
        )

        print(f"  {art:<40}{RESET}{spacing}{formatted_help}{RESET}")
    print("\n")


if __name__ == "__main__":
    display_help()
