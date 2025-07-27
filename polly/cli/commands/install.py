import sys
import argparse
from polly.core import install_package_from_git
from polly.utils import (
    print_header,
    format_message,
    get_colors,
    extract_package_id_from_url,
)


def install_main(args=None):
    """Main function for the install command."""
    colors = get_colors()

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Install a package from a git repository", prog="polly install"
    )
    parser.add_argument("repo_url", help="Git repository URL of the package to install")
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Output in simple plain text format for system integration",
    )

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return

    repo_url = parsed_args.repo_url
    simple_mode = parsed_args.simple

    # Validate that it looks like a git URL
    if not (
        repo_url.startswith(("http://", "https://", "git@"))
        or repo_url.endswith(".git")
        or "/" in repo_url
    ):
        print(format_message("error", f"Invalid repository URL: {repo_url}", simple_mode))
        if not simple_mode:
            print(
                f"  {colors['grey']}Please provide a valid git repository URL{colors['reset']}"
            )
        sys.exit(1)

    # Print header (unless in simple mode)
    if not simple_mode:
        print_header("Polly", "Package Installation")

    # Show package information
    package_id = extract_package_id_from_url(repo_url)
    if simple_mode:
        print(f"PACKAGE_ID|{package_id}")
        print(f"REPOSITORY|{repo_url}")
    else:
        print(
            f"  {colors['info']}Package ID:{colors['reset']} {colors['grey']}{package_id}{colors['reset']}"
        )
        print(
            f"  {colors['info']}Repository:{colors['reset']} {colors['grey']}{repo_url}{colors['reset']}\n"
        )

    # Install the package
    try:
        success, message, package_name = install_package_from_git(repo_url)

        if success:
            print(format_message("success", message, simple_mode))
            if package_name:
                if simple_mode:
                    print(f"LOCATION|/opt/pollypackages/{package_name}")
                else:
                    print(
                        f"  {colors['grey']}Location: /opt/pollypackages/{package_name}{colors['reset']}\n"
                    )
        else:
            print(format_message("error", message, simple_mode))
            sys.exit(1)

    except KeyboardInterrupt:
        print(format_message("error", "Installation cancelled by user", simple_mode))
        sys.exit(1)
    except Exception as e:
        print(format_message("error", f"Unexpected error during installation: {e}", simple_mode))
        sys.exit(1)


if __name__ == "__main__":
    install_main()
