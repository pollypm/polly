import sys
import argparse
from polly.core import list_packages
from polly.utils import print_header, format_message, get_colors


import sys
import argparse
from polly.core import list_packages
from polly.utils import print_header, format_message, get_colors, is_simple_mode


def display_packages_simple_mode(packages_data):
    """Display packages in simple format for external tools."""
    packages = packages_data["packages"]

    if not packages:
        print("No packages installed")
        return

    # Simple format: name,type,size,installed_date
    for package in packages:
        install_date = package["install_date"].split(" ")[0]  # Just the date part
        print(
            f"{package['name']},{package['size_formatted']},{install_date}"
        )


def display_packages_detailed_simple_mode(packages_data):
    """Display packages in detailed format for external tools."""
    packages = packages_data["packages"]

    if not packages:
        print("No packages installed")
        return

    for package in packages:
        print(f"name:{package['name']}")
        print(f"size:{package['size_formatted']}")
        print(f"installed:{package['install_date']}")
        print(f"location:{package['path']}")

        if package["has_metadata"]:
            if "version" in package and package["version"]:
                print(f"version:{package['version']}")

            if "description" in package and package["description"]:
                print(f"description:{package['description']}")
        else:
            print("status:invalid_metadata")

        print("---")  # Separator between packages


def display_packages_simple(packages_data):
    """Display packages in simple format."""
    colors = get_colors()
    packages = packages_data["packages"]

    if not packages:
        print(format_message("info", "No packages are currently installed"))
        print(
            f"  {colors['grey']}Use 'polly install <repo_url>' to install a package{colors['reset']}\n"
        )
        return

    # Calculate column widths
    max_name_length = max(len(pkg["name"]) for pkg in packages)

    # Header
    print(
        f"  {colors['info']}{'NAME':<{max_name_length}} {'SIZE':<10} {'INSTALLED'}{colors['reset']}"
    )
    print(
        f"  {colors['grey']}{'-' * max_name_length} {'-' * 10} {'-' * 10}{colors['reset']}"
    )

    # Package rows
    for package in packages:
        name_color = colors["primary"] if package["has_metadata"] else colors["error"]

        install_date = package["install_date"].split(" ")[0]  # Just the date part

        print(
            f"  {name_color}{package['name']:<{max_name_length}}{colors['reset']} "
            f"{colors['grey']}{package['size_formatted']:<10} {install_date}{colors['reset']}"
        )

    print(
        f"\n  {colors['info']}Total: {packages_data['total_count']} package(s), {packages_data['total_size_formatted']}{colors['reset']}"
    )


def display_packages_detailed(packages_data):
    """Display packages in detailed format."""
    colors = get_colors()
    packages = packages_data["packages"]

    if not packages:
        print(format_message("info", "No packages are currently installed"))
        print(
            f"  {colors['grey']}Use 'polly install <repo_url>' to install a package{colors['reset']}\n"
        )
        return

    for package in packages:
        print(
            f"  {colors['primary']}•{colors['reset']} {colors['info']}{package['name']}{colors['reset']}"
        )
        print(
            f"    {colors['grey']}Size:      {package['size_formatted']}{colors['reset']}"
        )
        print(
            f"    {colors['grey']}Installed: {package['install_date']}{colors['reset']}"
        )
        print(f"    {colors['grey']}Location:  {package['path']}{colors['reset']}")

        if package["has_metadata"]:
            if "version" in package and package["version"]:
                print(
                    f"    {colors['grey']}Version:   {package['version']}{colors['reset']}"
                )

            if "description" in package and package["description"]:
                print(
                    f"    {colors['grey']}Description: {package['description']}{colors['reset']}"
                )
        else:
            print(
                f"    {colors['grey']}Status:    {colors['error']}Invalid metadata{colors['reset']}"
            )

        print()

    print(f"  {colors['info']}Summary:{colors['reset']}")
    print(
        f"    {colors['grey']}Total packages: {packages_data['total_count']}{colors['reset']}"
    )
    print(
        f"    {colors['grey']}Total size:     {packages_data['total_size_formatted']}{colors['reset']}"
    )


def list_main(args=None):
    """Main function for the list command."""
    colors = get_colors()

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="List installed packages", prog="polly list"
    )
    parser.add_argument(
        "-l",
        "--detailed",
        action="store_true",
        help="Show detailed information for each package",
    )

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return

    detailed = parsed_args.detailed

    # In simple mode, skip header
    if not is_simple_mode():
        print_header("Polly", "Installed Packages")

    # List the packages
    try:
        success, message, packages_data = list_packages(detailed)

        if not success:
            print(format_message("error", message))
            sys.exit(1)

        # Display packages based on mode
        if is_simple_mode():
            if detailed:
                display_packages_detailed_simple_mode(packages_data)
            else:
                display_packages_simple_mode(packages_data)
        else:
            if detailed:
                display_packages_detailed(packages_data)
            else:
                display_packages_simple(packages_data)
            print()

    except KeyboardInterrupt:
        print(format_message("error", "Listing cancelled by user"))
        sys.exit(1)
    except Exception as e:
        print(format_message("error", f"Unexpected error during listing: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    list_main()
