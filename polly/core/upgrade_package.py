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


def check_package_updates():
    """
    Check all installed packages for available updates.

    :return: Tuple of (upgradeable_packages: list, error_packages: list)
    """
    packages = get_installed_packages()
    upgradeable_packages = []
    error_packages = []

    for package in packages:
        package_name = package["name"]
        package_path = package["path"]

        update_info = check_for_updates(package_path)
        if update_info is None:
            error_packages.append(package_name)
        elif update_info is not False:  # Has updates
            package["update_info"] = update_info
            upgradeable_packages.append(package)

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

    # Pull latest changes
    if not upgrade_git_package(package_path):
        return False

    # Run any update commands if specified in metadata
    if metadata and "updateCommands" in metadata:
        update_commands = metadata["updateCommands"]
        if isinstance(update_commands, list):
            for i, command in enumerate(update_commands):
                description = f"Running update command {i+1}/{len(update_commands)} for {package_name}"
                if not run_silent_command(command, description, cwd=package_path):
                    return False

    return True


def upgrade_packages(package_names=None):
    """
    Upgrade specified packages or all upgradeable packages.

    :param package_names: List of specific package names to upgrade, or None for all
    :return: Tuple of (success: bool, message: str, results: dict)
    """
    try:
        # Get packages that need upgrading
        upgradeable_packages, error_packages = check_package_updates()

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
            upgradeable_packages = [
                pkg for pkg in upgradeable_packages if pkg["name"] in package_names
            ]

        # Perform upgrades
        successful_upgrades = []
        failed_upgrades = []

        for package in upgradeable_packages:
            if upgrade_single_package(package, package["update_info"]):
                successful_upgrades.append(package["name"])
            else:
                failed_upgrades.append(package["name"])

        # Determine overall success
        success = len(failed_upgrades) == 0

        if success and successful_upgrades:
            message = f"Successfully upgraded {len(successful_upgrades)} package(s)"
        elif failed_upgrades:
            message = f"Failed to upgrade {len(failed_upgrades)} package(s)"
        else:
            message = "No packages were upgraded"

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
        return (
            False,
            f"Unexpected error during upgrade: {e}",
            {"upgradeable": [], "errors": [], "successful": [], "failed": []},
        )
