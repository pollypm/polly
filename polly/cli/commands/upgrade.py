import sys
import argparse
from polly.core import upgrade_packages, check_package_updates, get_upgrade_summary
from polly.utils import print_header, format_message, get_colors, format_size


def display_upgrade_summary(upgradeable_packages, error_packages, simple_mode=False):
    """Display the upgrade summary."""
    if simple_mode:
        # Simple plain text format for system integration
        if error_packages:
            for package in error_packages:
                print(f"ERROR_PACKAGE|{package}")
        
        if not upgradeable_packages:
            print("NO_UPGRADES_AVAILABLE")
            return False
        
        for package in upgradeable_packages:
            package_name = package["name"]
            update_info = package["update_info"]
            package_size = package["size"]
            
            print(f"UPGRADE_AVAILABLE|{package_name}|{update_info['current_commit']}|{update_info['remote_commit']}|{format_size(package_size)}")
            
            if update_info["commit_messages"]:
                for msg in update_info["commit_messages"][:3]:
                    print(f"COMMIT_MESSAGE|{package_name}|{msg.strip()}")
        
        return True
    
    colors = get_colors()

    if error_packages:
        print(
            f"  {colors['warning']}⚠{colors['reset']} {colors['grey']}Could not check updates for: {', '.join(error_packages)}{colors['reset']}"
        )
        print(
            f"    {colors['grey']}(These packages may not be git repositories or have network issues){colors['reset']}\n"
        )

    if not upgradeable_packages:
        print(format_message("info", "No packages need upgrading"))
        return False

    # Show upgrade summary
    print(
        f"  {colors['info']}The following packages will be upgraded:{colors['reset']}\n"
    )

    summary = get_upgrade_summary(upgradeable_packages)

    for package in upgradeable_packages:
        package_name = package["name"]
        update_info = package["update_info"]
        package_size = package["size"]

        print(
            f"    {colors['primary']}•{colors['reset']} {colors['grey']}{package_name}{colors['reset']}"
        )
        print(
            f"      {colors['grey']}Current: {update_info['current_commit']}{colors['reset']}"
        )
        print(
            f"      {colors['grey']}Latest:  {update_info['remote_commit']}{colors['reset']}"
        )
        print(
            f"      {colors['grey']}Size:    {format_size(package_size)}{colors['reset']}"
        )

        if update_info["commit_messages"]:
            print(f"      {colors['grey']}Changes:{colors['reset']}")
            for msg in update_info["commit_messages"][:3]:  # Show first 3 commits
                print(f"        {colors['grey']}• {msg}{colors['reset']}")
            if len(update_info["commit_messages"]) > 3:
                remaining = len(update_info["commit_messages"]) - 3
                print(
                    f"        {colors['grey']}• ... and {remaining} more commit(s){colors['reset']}"
                )
        print()

    # Show disk space information
    summary = get_upgrade_summary(upgradeable_packages)
    print(f"  {colors['info']}Disk Space Summary:{colors['reset']}")
    print(
        f"    {colors['grey']}Total package size: {format_size(summary['total_size'])}{colors['reset']}"
    )
    if summary["available_space"]:
        print(
            f"    {colors['grey']}Available space:    {format_size(summary['available_space'])}{colors['reset']}"
        )
        if summary["space_warning"]:
            print(f"    {colors['warning']}⚠ Low disk space warning{colors['reset']}")
    print()

    return True


def upgrade_main(args=None):
    """Main function for the upgrade command."""
    colors = get_colors()

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Upgrade installed packages", prog="polly upgrade"
    )
    parser.add_argument(
        "-y", "--yes", action="store_true", help="Skip confirmation prompt"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check for updates, don't upgrade",
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Output in simple plain text format for system integration",
    )

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return

    skip_confirmation = parsed_args.yes
    check_only = parsed_args.check_only
    simple_mode = parsed_args.simple

    # Print header (unless in simple mode)
    if not simple_mode:
        print_header("Polly", "Package Upgrade")

    # Check for updates
    if simple_mode:
        print("PROGRESS|Scanning installed packages")
    else:
        print(format_message("progress", "Scanning installed packages..."))

    try:
        upgradeable_packages, error_packages = check_package_updates()

        if simple_mode:
            print("PROGRESS|Checking for updates")
        else:
            print(format_message("progress", "Checking for updates..."))

        # Display results
        if not upgradeable_packages and not error_packages:
            print(format_message("success", "All packages are up to date!", simple_mode))
            return

        has_upgrades = display_upgrade_summary(upgradeable_packages, error_packages, simple_mode)

        if not has_upgrades:
            return

        if check_only:
            if simple_mode:
                print("INFO|Check complete. Use 'polly upgrade' to upgrade packages.")
            else:
                print(
                    format_message(
                        "info", "Check complete. Use 'polly upgrade' to upgrade packages."
                    )
                )
            return

        # Confirmation prompt (unless in simple mode or -y flag)
        if not skip_confirmation and not simple_mode:
            print(
                f"  {colors['primary']}?{colors['reset']} {colors['grey']}Do you want to continue with the upgrade? (Y/n):{colors['reset']} ",
                end="",
            )
            response = input().strip().lower()
            if response in ["n", "no"]:
                print(f"  {colors['grey']}Upgrade cancelled{colors['reset']}")
                return
            print()

        # Perform upgrades
        if simple_mode:
            print("PROGRESS|Upgrading packages")
        else:
            print(format_message("progress", "Upgrading packages..."))
            print()

        success, message, results = upgrade_packages()

        # Show results
        if results["successful"]:
            print(
                format_message(
                    "success",
                    f"Successfully upgraded: {', '.join(results['successful'])}",
                    simple_mode
                )
            )

        if results["failed"]:
            print(
                format_message(
                    "error", f"Failed to upgrade: {', '.join(results['failed'])}", simple_mode
                )
            )

        if success:
            if simple_mode:
                print("SUCCESS|All packages upgraded successfully!")
            else:
                print(
                    f"\n{format_message('success', 'All packages upgraded successfully!')}\n"
                )
        else:
            if simple_mode:
                print("WARNING|Some packages failed to upgrade. Check the errors above.")
            else:
                print(
                    f"\n{format_message('warning', 'Some packages failed to upgrade. Check the errors above.')}\n"
                )
            sys.exit(1)

    except KeyboardInterrupt:
        print(format_message("error", "Upgrade cancelled by user", simple_mode))
        sys.exit(1)
    except Exception as e:
        print(format_message("error", f"Unexpected error during upgrade: {e}", simple_mode))
        sys.exit(1)


if __name__ == "__main__":
    upgrade_main()
