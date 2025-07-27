import subprocess
import sys
from colorama import init, Fore, Style

init(autoreset=True)


def run_command(command, description):
    print(f"{Fore.CYAN}➤ {description}...", end="", flush=True)
    try:
        # Run command silently
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            print(f"\r{Fore.GREEN}✔ {description} completed.")
        else:
            print(f"\r{Fore.RED}✖ {description} failed.")
            print(f"{Fore.YELLOW}Error: {result.stderr.decode().strip()}")
            sys.exit(1)
    except Exception as e:
        print(f"\r{Fore.RED}✖ {description} failed.")
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
