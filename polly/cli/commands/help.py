import os
import sys
import threading
import time

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

# Pre-compute ANSI colors to avoid repeated hex conversion
PRIMARY_ANSI = "\033[38;2;79;142;247m"  # #4F8EF7
SECONDARY_ANSI = "\033[38;2;247;179;43m"  # #F7B32B
GREY_ANSI = "\033[38;2;128;128;128m"  # #808080

# Cache for ASCII art
_ascii_art_cache = None


def display_help_with_live_updates():
    """Display help and update version info in real-time."""
    ascii_art = get_cached_ascii_art()

    # Get current version immediately (fast file read)
    try:
        current_ver = get_current_version()[:7]
    except:
        current_ver = "Unknown"

    # Initial display with placeholders
    def create_help_text(current, latest="fetching...", status="checking..."):
        return f"""{PRIMARY_ANSI}Polly {GREY_ANSI}- {SECONDARY_ANSI}Help
{GREY_ANSI}Version {current} (Latest: {PRIMARY_ANSI}{latest}{GREY_ANSI})
{GREY_ANSI}Updates Available: {PRIMARY_ANSI}{status}{GREY_ANSI}

{SECONDARY_ANSI}Usage:
  {PRIMARY_ANSI}polly {GREY_ANSI}<command> [options]

{SECONDARY_ANSI}Available Commands:
  {PRIMARY_ANSI}help        {GREY_ANSI}Show this help message
  {PRIMARY_ANSI}update      {GREY_ANSI}Update Polly to the latest version
  {PRIMARY_ANSI}install     {GREY_ANSI}Install a Polly package
  {PRIMARY_ANSI}uninstall   {GREY_ANSI}Uninstall a Polly package
  {PRIMARY_ANSI}list        {GREY_ANSI}List installed Polly packages
  {PRIMARY_ANSI}search      {GREY_ANSI}Search for Polly packages
  {PRIMARY_ANSI}inspect     {GREY_ANSI}Show information about a Polly package
  {PRIMARY_ANSI}upgrade     {GREY_ANSI}Upgrade Polly packages

{SECONDARY_ANSI}For more information, visit: {PRIMARY_ANSI}https://github.com/pollypm/polly
"""

    # Display initial help immediately
    def display_help(help_text):
        art_lines = ascii_art.splitlines()
        help_lines = help_text.splitlines()

        max_lines = max(len(art_lines), len(help_lines))
        art_lines += [""] * (max_lines - len(art_lines))
        help_lines += [""] * (max_lines - len(help_lines))

        spacing = "   "
        print("\n")
        for art, help_line in zip(art_lines, help_lines):
            print(f"  {art:<40}{RESET}{spacing}{help_line}{RESET}")
        print("\n")

    # Show initial help immediately
    initial_help = create_help_text(current_ver)
    display_help(initial_help)

    # Background thread to fetch and update version info
    def fetch_and_update():
        try:
            latest_ver = latest_version()[:7]
            update_req = update_required()
            update_status = (
                f"Yes {GREY_ANSI}({PRIMARY_ANSI}use {SECONDARY_ANSI}polly update{GREY_ANSI})"
                if update_req
                else "No"
            )

            # Clear screen and redisplay with updated info
            print("\033[H\033[2J", end="")  # Clear screen and move cursor to top
            updated_help = create_help_text(current_ver, latest_ver, update_status)
            display_help(updated_help)

        except Exception:
            # If network fails, just leave the initial display
            pass

    # Start background update
    threading.Thread(target=fetch_and_update, daemon=True).start()


def get_cached_ascii_art():
    """Get ASCII art with caching."""
    global _ascii_art_cache
    if _ascii_art_cache is None:
        ascii_art_path = os.path.join(os.path.dirname(__file__), "../polly.txt")
        try:
            with open(ascii_art_path, "r", encoding="utf-8") as f:
                _ascii_art_cache = f.read()
        except FileNotFoundError:
            _ascii_art_cache = "[ASCII art not found]"
    return _ascii_art_cache


def help_main():
    """Display the help message with ASCII art and live updates."""
    display_help_with_live_updates()
