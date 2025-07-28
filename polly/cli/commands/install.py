import sys
import argparse
from polly.core import install_package_from_git
from polly.utils import (
    print_header,
    format_message,
    get_colors,
    extract_package_id_from_url,
    is_simple_mode,
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

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return

    repo_url = parsed_args.repo_url

    # Validate that it looks like a git URL
    if not (
        repo_url.startswith(("http://", "https://", "git@"))
        or repo_url.endswith(".git")
        or "/" in repo_url
    ):
        if is_simple_mode():
            print(f"error:Invalid repository URL: {repo_url}")
        else:
            print(format_message("error", f"Invalid repository URL: {repo_url}"))
            print(
                f"  {colors['grey']}Please provide a valid git repository URL{colors['reset']}"
            )
        sys.exit(1)

    # Print header and package info
    if is_simple_mode():
        package_id = extract_package_id_from_url(repo_url)
        print(f"installing:{package_id}")
        print(f"repository:{repo_url}")
    else:
        print_header("Polly", "Package Installation")

        # Show package information
        package_id = extract_package_id_from_url(repo_url)
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
            if is_simple_mode():
                print(f"success:{message}")
                if package_name:
                    print(f"location:/opt/pollypackages/{package_name}")
            else:
                print(format_message("success", message))
                if package_name:
                    print(
                        f"  {colors['grey']}Location: /opt/pollypackages/{package_name}{colors['reset']}\n"
                    )
        else:
            if is_simple_mode():
                print(f"error:{message}")
            else:
                print(format_message("error", message))
            sys.exit(1)

    except KeyboardInterrupt:
        if is_simple_mode():
            print("error:Installation cancelled by user")
        else:
            print(format_message("error", "Installation cancelled by user"))
        sys.exit(1)
    except Exception as e:
        if is_simple_mode():
            print(f"error:Unexpected error during installation: {e}")
        else:
            print(format_message("error", f"Unexpected error during installation: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    install_main()
