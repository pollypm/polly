import os
import json
from ..utils import (
    get_package_by_name,
    run_silent_command,
    safe_remove_directory,
    load_package_metadata,
)


def run_uninstall_commands(package_dir, metadata):
    """Run any uninstall commands specified in the metadata."""
    if "uninstall" not in metadata:
        return True

    commands = metadata["uninstall"]
    if not isinstance(commands, list):
        return True

    for i, command in enumerate(commands):
        description = f"Running uninstall command {i + 1}/{len(commands)}"
        if not run_silent_command(command, description, cwd=package_dir):
            return False

    return True


def uninstall_package(package_name):
    """
    Uninstall a package by name.

    :param package_name: Name of the package to uninstall
    :return: Tuple of (success: bool, message: str)
    """
    try:
        # Get package information
        package = get_package_by_name(package_name)
        if not package:
            return False, f"Package '{package_name}' is not installed"

        package_path = package["path"]
        metadata = package["metadata"]

        if not metadata:
            return False, f"Package metadata not found for '{package_name}'"

        # Run uninstall commands if specified
        if not run_uninstall_commands(package_path, metadata):
            # Continue with removal anyway, but note the failure
            pass

        # Remove package directory
        if not safe_remove_directory(package_path):
            return False, "Failed to remove package files. Check permissions."

        return True, f"Package '{package_name}' uninstalled successfully"

    except Exception as e:
        return False, f"Unexpected error during uninstallation: {e}"
