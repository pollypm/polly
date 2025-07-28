import subprocess
import sys
import os

# Import simple mode utilities
from polly.utils import is_simple_mode

# ANSI color constants
RESET = "\033[0m"
PRIMARY_COLOR = "#4F8EF7"  # Blue
SECONDARY_COLOR = "#F7B32B"  # Orange
SUCCESS_COLOR = "#4ADE80"  # Green
ERROR_COLOR = "#EF4444"  # Red
GREY_COLOR = "#808080"  # Grey


def hex_to_ansi(hex_color):
    """Convert hex color to ANSI escape sequence."""
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"


def run_command(command, description):
    cwd = os.path.expanduser("~")

    if is_simple_mode():
        print(f"running:{description}")
    else:
        primary = hex_to_ansi(PRIMARY_COLOR)
        success = hex_to_ansi(SUCCESS_COLOR)
        error = hex_to_ansi(ERROR_COLOR)
        grey = hex_to_ansi(GREY_COLOR)
        print(f"  {primary}➤{RESET} {grey}{description}...{RESET}")

    try:
        # Run command and show output live
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            if is_simple_mode():
                print(f"completed:{description}")
            else:
                print(f"  {success}✔{RESET} {grey}{description} completed.{RESET}")
        else:
            if is_simple_mode():
                print(f"failed:{description}")
                print(f"error:{result.stderr}")
            else:
                print(f"  {error}✖{RESET} {grey}{description} failed.{RESET}")
                print(f"  {error}Error:{RESET} {grey}{result.stderr}{RESET}")
            sys.exit(1)

    except Exception as e:
        if is_simple_mode():
            print(f"failed:{description}")
            print(f"error:{e}")
        else:
            print(f"  {error}✖{RESET} {grey}{description} failed.{RESET}")
            print(f"  {error}Exception:{RESET} {grey}{e}{RESET}")
        sys.exit(1)


def update_main():
    if is_simple_mode():
        print("updating:polly")
    else:
        primary = hex_to_ansi(PRIMARY_COLOR)
        secondary = hex_to_ansi(SECONDARY_COLOR)
        grey = hex_to_ansi(GREY_COLOR)
        print(f"\n  {primary}Polly{RESET} {grey}- {secondary}Update{RESET}")
        print(f"  {grey}{'─' * 20}{RESET}\n")

    def do_update():
        run_command(
            "curl -fsSL https://raw.githubusercontent.com/pollypm/polly/main/uninstall.sh | sudo bash",
            "Uninstalling current Polly version",
        )
        run_command(
            "curl -fsSL https://raw.githubusercontent.com/pollypm/polly/main/install.sh | sudo bash",
            "Installing latest Polly version",
        )

        if is_simple_mode():
            print("success:Update complete")
        else:
            success = hex_to_ansi(SUCCESS_COLOR)
            grey = hex_to_ansi(GREY_COLOR)
            print(
                f"\n  {success}✔{RESET} {grey}Update complete! Polly is now up to date.{RESET}\n"
            )

    do_update()


if __name__ == "__main__":
    update_main()
