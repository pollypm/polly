import sys
import argparse
from polly.core import uninstall_package
from polly.utils import (
    print_header,
    format_message,
    get_colors,
    get_package_names,
    is_simple_mode,
)


def uninstall_main(args=None):
    """Main function for the uninstall command."""
    colors = get_colors()

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Uninstall an installed package", prog="polly uninstall"
    )
    parser.add_argument("package_name", help="Name of the package to uninstall")
    parser.add_argument(
        "-y", "--yes", action="store_true", help="Skip confirmation prompt"
    )

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return

    package_name = parsed_args.package_name
    skip_confirmation = parsed_args.yes

    # Check if package is installed
    installed_packages = get_package_names()
    if package_name not in installed_packages:
        if is_simple_mode():
            print(f"error:Package '{package_name}' is not installed")
        else:
            print(format_message("error", f"Package '{package_name}' is not installed"))
            print(
                f"  {colors['grey']}Use 'polly list' to see installed packages{colors['reset']}"
            )
        sys.exit(1)

    # Print header and package info
    if is_simple_mode():
        print(f"uninstalling:{package_name}")
    else:
        print_header("Polly", "Package Uninstallation")
        print(
            f"  {colors['info']}Package:{colors['reset']} {colors['grey']}{package_name}{colors['reset']}\n"
        )

    # Confirmation prompt (skip in simple mode)
    if not skip_confirmation and not is_simple_mode():
        print(
            f"  {colors['warning']}?{colors['reset']} {colors['grey']}Are you sure you want to uninstall '{package_name}'? (y/N):{colors['reset']} ",
            end="",
        )
        response = input().strip().lower()
        if response not in ["y", "yes"]:
            print(f"  {colors['grey']}Uninstallation cancelled{colors['reset']}")
            return
        print()

    # Uninstall the package
    try:
        success, message = uninstall_package(package_name)

        if success:
            if is_simple_mode():
                print(f"success:{message}")
            else:
                print(format_message("success", message))
        else:
            if is_simple_mode():
                print(f"error:{message}")
            else:
                print(format_message("error", message))
            sys.exit(1)

    except KeyboardInterrupt:
        if is_simple_mode():
            print("error:Uninstallation cancelled by user")
        else:
            print(format_message("error", "Uninstallation cancelled by user"))
        sys.exit(1)
    except Exception as e:
        if is_simple_mode():
            print(f"error:Unexpected error during uninstallation: {e}")
        else:
            print(
                format_message("error", f"Unexpected error during uninstallation: {e}")
            )
        sys.exit(1)


if __name__ == "__main__":
    uninstall_main()
