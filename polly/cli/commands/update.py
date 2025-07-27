import subprocess
import sys
from colorama import init, Fore, Style
import os

init(autoreset=True)


def run_command(command, description):
    cwd = os.path.expanduser("~")
    print(f"{Fore.CYAN}➤ {description}...", flush=True)
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
                print(output, end="")
        returncode = process.poll()
        if returncode == 0:
            print(f"{Fore.GREEN}✔ {description} completed.")
        else:
            print(f"{Fore.RED}✖ {description} failed.")
            sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}✖ {description} failed.")
        print(f"{Fore.YELLOW}Exception: {e}")
        sys.exit(1)


def update_main():
    print(f"{Fore.MAGENTA}{Style.BRIGHT}Polly Updater\n{'='*30}")
    print(f"{Fore.BLUE}Starting update process...\n")

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
            f"\n{Fore.GREEN}{Style.BRIGHT}✔ Update complete! Polly is now up to date."
        )

    do_update()


if __name__ == "__main__":
    update_main()
