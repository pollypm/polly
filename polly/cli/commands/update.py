import subprocess
import sys
import os

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
    primary = hex_to_ansi(PRIMARY_COLOR)
    success = hex_to_ansi(SUCCESS_COLOR)
    error = hex_to_ansi(ERROR_COLOR)
    grey = hex_to_ansi(GREY_COLOR)

    print(f"  {primary}➤{RESET} {grey}{description}...{RESET}")
    try:
        # Run command and show output live
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=cwd,
        )
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                # Indent command output for better visual hierarchy
                print(f"    {grey}{output.rstrip()}{RESET}")
        returncode = process.poll()
        if returncode == 0:
            print(f"  {success}✔{RESET} {grey}{description} completed.{RESET}")
        else:
            print(f"  {error}✖{RESET} {grey}{description} failed.{RESET}")
            sys.exit(1)
    except Exception as e:
        print(f"  {error}✖{RESET} {grey}{description} failed.{RESET}")
        print(f"  {error}Exception:{RESET} {grey}{e}{RESET}")
        sys.exit(1)


def update_main():
    primary = hex_to_ansi(PRIMARY_COLOR)
    secondary = hex_to_ansi(SECONDARY_COLOR)
    success = hex_to_ansi(SUCCESS_COLOR)
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
        print(
            f"\n  {success}✔{RESET} {grey}Update complete! Polly is now up to date.{RESET}\n"
        )

    do_update()


if __name__ == "__main__":
    update_main()
