import sys
import json
import argparse
from polly.core import inspect_package
from polly.utils import (
    print_header,
    format_message,
    get_colors,
    format_size,
    is_simple_mode,
)


def display_inspection_data_simple(data):
    """Display inspection data in simple mode for external tools."""
    print(f"name:{data['name']}")
    print(f"location:{data['path']}")
    print(f"installed:{data['stats']['install_date']}")
    print(f"size:{format_size(data['stats']['size'])}")
    print(f"file_count:{data['stats']['file_count']}")

    # Install commands
    metadata = data["metadata"]
    if "install_commands" in metadata:
        install_commands = metadata["install_commands"]
        if install_commands:
            print(f"install_commands:{','.join(install_commands)}")
            
    # Uninstall commands
    if "uninstall_commands" in metadata:
        uninstall_commands = metadata["uninstall_commands"]
        if uninstall_commands:
            print(f"uninstall_commands:{','.join(uninstall_commands)}")

    # Additional metadata
    if "version" in metadata:
        print(f"version:{metadata['version']}")

    if "description" in metadata:
        print(f"description:{metadata['description']}")

    if "author" in metadata:
        print(f"author:{metadata['author']}")

    if "homepage" in metadata:
        print(f"homepage:{metadata['homepage']}")


def display_inspection_data(data):
    """Display the package inspection data in a formatted way."""
    colors = get_colors()

    # Basic information
    print(
        f"  {colors['info']}Package Name:{colors['reset']} {colors['primary']}{data['name']}{colors['reset']}"
    )
    print(
        f"  {colors['info']}Location:{colors['reset']} {colors['grey']}{data['path']}{colors['reset']}"
    )
    print(
        f"  {colors['info']}Installed:{colors['reset']} {colors['grey']}{data['stats']['install_date']}{colors['reset']}"
    )
    print(
        f"  {colors['info']}Size:{colors['reset']} {colors['grey']}{format_size(data['stats']['size'])}{colors['reset']}"
    )
    print(
        f"  {colors['info']}Files:{colors['reset']} {colors['grey']}{data['stats']['file_count']:,}{colors['reset']}"
    )

    # Install commands
    metadata = data["metadata"]
    if "install_commands" in metadata:
        install_commands = metadata["install_commands"]
        if isinstance(install_commands, list) and install_commands:
            print(f"\n  {colors['info']}Install Commands:{colors['reset']}")
            for i, command in enumerate(install_commands, 1):
                print(f"    {colors['grey']}{i}. {command}{colors['reset']}")

    # Uninstall commands if available
    if "uninstall_commands" in metadata:
        uninstall_commands = metadata["uninstall_commands"]
        if isinstance(uninstall_commands, list) and uninstall_commands:
            print(f"\n  {colors['info']}Uninstall Commands:{colors['reset']}")
            for i, command in enumerate(uninstall_commands, 1):
                print(f"    {colors['grey']}{i}. {command}{colors['reset']}")

    # Git information if available
    if data["git_info"]:
        git_info = data["git_info"]
        print(f"\n  {colors['info']}Git Information:{colors['reset']}")
        if "origin" in git_info:
            print(f"    {colors['grey']}Origin: {git_info['origin']}{colors['reset']}")
        if "branch" in git_info:
            print(f"    {colors['grey']}Branch: {git_info['branch']}{colors['reset']}")
        if "last_commit" in git_info:
            commit = git_info["last_commit"]
            print(
                f"    {colors['grey']}Last Commit: {commit['hash']} - {commit['message']}{colors['reset']}"
            )
            print(
                f"    {colors['grey']}Author: {commit['author']} ({commit['date']}){colors['reset']}"
            )

    # Additional metadata fields
    if data["additional_metadata"]:
        print(f"\n  {colors['info']}Additional Metadata:{colors['reset']}")
        for key, value in data["additional_metadata"].items():
            if isinstance(value, (str, int, float, bool)):
                print(f"    {colors['grey']}{key}: {value}{colors['reset']}")
            else:
                print(
                    f"    {colors['grey']}{key}: {json.dumps(value, indent=2)}{colors['reset']}"
                )

    # Package contents
    if data["contents"]:
        print(f"\n  {colors['info']}Package Contents:{colors['reset']}")
        for file_info in data["contents"]:
            print(
                f"    {colors['grey']}• {file_info['name']} ({file_info['size']}){colors['reset']}"
            )
    else:
        print(f"\n  {colors['info']}Package Contents:{colors['reset']}")
        print(f"    {colors['grey']}No standard files found{colors['reset']}")


def inspect_main(args=None):
    """Main function for the inspect command."""
    colors = get_colors()

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Inspect an installed package", prog="polly inspect"
    )
    parser.add_argument("package_name", help="Name of the package to inspect")

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return

    package_name = parsed_args.package_name

    # Print header only in normal mode
    if not is_simple_mode():
        print_header("Polly", "Package Inspection")

    # Inspect the package
    try:
        success, message, data = inspect_package(package_name)

        if success and data:
            if is_simple_mode():
                display_inspection_data_simple(data)
            else:
                display_inspection_data(data)
                print(
                    f"\n{format_message('success', 'Package inspection completed')}\n"
                )
        else:
            if is_simple_mode():
                print(f"error:{message}")
            else:
                print(format_message("error", message))
            sys.exit(1)

    except KeyboardInterrupt:
        if is_simple_mode():
            print("error:Inspection cancelled by user")
        else:
            print(format_message("error", "Inspection cancelled by user"))
        sys.exit(1)
    except Exception as e:
        if is_simple_mode():
            print(f"error:Unexpected error during inspection: {e}")
        else:
            print(format_message("error", f"Unexpected error during inspection: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    inspect_main()
