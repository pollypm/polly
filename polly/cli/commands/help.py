import os
import sys
import threading
from functools import lru_cache
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

# Cache for version info with timeout
_version_cache = {"data": None, "timestamp": 0, "timeout": 300}  # 5 minute cache


def get_version_info_cached():
    """Get version info with caching to avoid repeated network calls."""
    current_time = time.time()

    # Check if cache is still valid
    if (
        _version_cache["data"] is not None
        and current_time - _version_cache["timestamp"] < _version_cache["timeout"]
    ):
        return _version_cache["data"]

    # Try to get fresh data with a short timeout
    try:
        current_ver = get_current_version()[:7]
        latest_ver = "..."  # Placeholder while loading
        update_status = "..."  # Placeholder while loading

        # Start background thread to fetch latest version
        def fetch_latest():
            try:
                latest = latest_version()[:7]
                update_req = update_required()
                update_text = (
                    f"Yes {GREY_ANSI}({PRIMARY_ANSI}use {SECONDARY_ANSI}polly update{GREY_ANSI})"
                    if update_req
                    else "No"
                )
                # Update cache with real data
                _version_cache["data"] = {
                    "current": current_ver,
                    "latest": latest,
                    "update_status": update_text,
                }
                _version_cache["timestamp"] = time.time()
            except:
                pass  # Fail silently

        # If we have old cached data, use it while updating in background
        if _version_cache["data"] is not None:
            threading.Thread(target=fetch_latest, daemon=True).start()
            return _version_cache["data"]

        # For first time, return basic info immediately
        basic_data = {
            "current": current_ver,
            "latest": "fetching...",
            "update_status": "checking...",
        }

        # Start background fetch
        threading.Thread(target=fetch_latest, daemon=True).start()
        return basic_data

    except Exception:
        # Fallback to basic info
        return {"current": "Unknown", "latest": "Unknown", "update_status": "Unknown"}


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
    """Display the help message with ASCII art."""
    ascii_art = get_cached_ascii_art()

    # Get version info (with smart caching to avoid delays)
    version_info = get_version_info_cached()
    current_ver = version_info["current"]
    latest_ver = version_info["latest"]
    update_status = version_info["update_status"]

    help_text = f"""{PRIMARY_ANSI}Polly {GREY_ANSI}- {SECONDARY_ANSI}Help
{GREY_ANSI}Version {current_ver} (Latest: {PRIMARY_ANSI}{latest_ver}{GREY_ANSI})
{GREY_ANSI}Updates Available: {PRIMARY_ANSI}{update_status}{GREY_ANSI}

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

    art_lines = ascii_art.splitlines()
    help_lines = help_text.splitlines()

    # Ensure both lists have the same length
    max_lines = max(len(art_lines), len(help_lines))
    art_lines += [""] * (max_lines - len(art_lines))
    help_lines += [""] * (max_lines - len(help_lines))

    # Print with minimal processing
    spacing = "   "
    print("\n")
    for art, help_line in zip(art_lines, help_lines):
        print(f"  {art:<40}{RESET}{spacing}{help_line}{RESET}")
    print("\n")
