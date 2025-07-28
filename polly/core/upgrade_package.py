import os
from ..utils import (
    get_installed_packages,
    check_for_updates,
    upgrade_git_package,
    run_silent_command,
    get_directory_size,
    get_available_space,
    PACKAGES_DIR,
)
from ..utils.debug import (
    format_error_with_debug,
    handle_exception_with_debug,
    debug_print,
)


def check_package_updates():
    """
    Check all installed packages for available updates.

    :return: Tuple of (upgradeable_packages: list, error_packages: list)
    """
    packages = get_installed_packages()
    upgradeable_packages = []
    error_packages = []

    debug_print(f"Checking updates for {len(packages)} packages")

    for package in packages:
        package_name = package["name"]
        package_path = package["path"]

        debug_print(f"Checking updates for package: {package_name} at {package_path}")

        try:
            update_info = check_for_updates(package_path)
            if update_info is None:
                debug_print(
                    f"Failed to check updates for {package_name} - check_for_updates returned None"
                )
                error_packages.append(package_name)
            elif update_info is not False:  # Has updates
                debug_print(f"Updates available for {package_name}: {update_info}")
                package["update_info"] = update_info
                upgradeable_packages.append(package)
            else:
                debug_print(f"No updates available for {package_name}")
        except Exception as e:
            debug_print(f"Exception while checking updates for {package_name}: {e}")
            error_packages.append(package_name)

    return upgradeable_packages, error_packages


def get_upgrade_summary(upgradeable_packages):
    """
    Get summary information about the upgrade.

    :param upgradeable_packages: List of packages that can be upgraded
    :return: Dictionary with summary information
    """
    total_size = sum(
        get_directory_size(package["path"]) for package in upgradeable_packages
    )
    available_space = get_available_space(PACKAGES_DIR)

    return {
        "total_packages": len(upgradeable_packages),
        "total_size": total_size,
        "available_space": available_space,
        "space_warning": available_space and available_space < total_size * 2,
    }


def upgrade_single_package(package, update_info):
    """
    Upgrade a single package.

    :param package: Package information dictionary
    :param update_info: Update information from check_for_updates
    :return: bool indicating success
    """
    package_name = package["name"]
    package_path = package["path"]
    metadata = package["metadata"]

    debug_print(f"Starting upgrade for package: {package_name}")
    debug_print(f"Package path: {package_path}")
    debug_print(f"Update info: {update_info}")

    try:
        # Pull latest changes
        debug_print(f"Pulling latest changes for {package_name}")
        if not upgrade_git_package(package_path):
            debug_print(f"Git upgrade failed for {package_name}")
            return False

        # Run uninstall commands if specified
        if "uninstall" in metadata:
            debug_print(
                f"Running uninstall commands for {package_name}: {metadata['uninstall']}"
            )
            for command in metadata["uninstall"]:
                if not run_silent_command(
                    command,
                    f"Running uninstall command for {package_name}",
                    cwd=package_path,
                ):
                    debug_print(
                        f"Uninstall command failed for {package_name}: {command}"
                    )
                    return False

        # Run install commands
        if "install" in metadata:
            debug_print(
                f"Running install commands for {package_name}: {metadata['install']}"
            )
            for command in metadata["install"]:
                if not run_silent_command(
                    command,
                    f"Running install command for {package_name}",
                    cwd=package_path,
                ):
                    debug_print(f"Install command failed for {package_name}: {command}")
                    return False

        debug_print(f"Successfully upgraded {package_name}")
        return True

    except Exception as e:
        debug_print(f"Exception during upgrade of {package_name}: {e}")
        return False


def upgrade_packages(package_names=None):
    """
    Upgrade specified packages or all upgradeable packages.

    :param package_names: List of specific package names to upgrade, or None for all
    :return: Tuple of (success: bool, message: str, results: dict)
    """
    try:
        debug_print(f"Starting package upgrade process. Package names: {package_names}")

        # Get packages that need upgrading
        upgradeable_packages, error_packages = check_package_updates()

        debug_print(
            f"Found {len(upgradeable_packages)} upgradeable packages, {len(error_packages)} errors"
        )

        if not upgradeable_packages:
            return (
                True,
                "No packages need upgrading",
                {
                    "upgradeable": [],
                    "errors": error_packages,
                    "successful": [],
                    "failed": [],
                },
            )

        # Filter by specific package names if provided
        if package_names:
            debug_print(f"Filtering packages by names: {package_names}")
            original_count = len(upgradeable_packages)
            upgradeable_packages = [
                pkg for pkg in upgradeable_packages if pkg["name"] in package_names
            ]
            debug_print(
                f"Filtered from {original_count} to {len(upgradeable_packages)} packages"
            )

        # Perform upgrades
        successful_upgrades = []
        failed_upgrades = []

        debug_print(f"Starting upgrade of {len(upgradeable_packages)} packages")

        for package in upgradeable_packages:
            package_name = package["name"]
            debug_print(f"Upgrading package: {package_name}")

            try:
                if upgrade_single_package(package, package["update_info"]):
                    successful_upgrades.append(package_name)
                    debug_print(f"Successfully upgraded: {package_name}")
                else:
                    failed_upgrades.append(package_name)
                    debug_print(f"Failed to upgrade: {package_name}")
            except Exception as e:
                failed_upgrades.append(package_name)
                debug_print(f"Exception while upgrading {package_name}: {e}")

        # Determine overall success
        success = len(failed_upgrades) == 0

        if success and successful_upgrades:
            message = f"Successfully upgraded {len(successful_upgrades)} package(s)"
        elif failed_upgrades:
            message = format_error_with_debug(
                f"Failed to upgrade {len(failed_upgrades)} package(s)",
                f"Failed packages: {', '.join(failed_upgrades)}",
            )
        else:
            message = "No packages were upgraded"

        debug_print(
            f"Upgrade process completed. Success: {success}, Message: {message}"
        )

        return (
            success,
            message,
            {
                "upgradeable": [pkg["name"] for pkg in upgradeable_packages],
                "errors": error_packages,
                "successful": successful_upgrades,
                "failed": failed_upgrades,
            },
        )

    except Exception as e:
        error_message = handle_exception_with_debug(
            f"Unexpected error during upgrade: {e}", e
        )
        debug_print(f"Exception in upgrade_packages: {e}")
        return (
            False,
            error_message,
            {"upgradeable": [], "errors": [], "successful": [], "failed": []},
        )
