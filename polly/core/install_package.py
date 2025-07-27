import json
import os
import shutil
from .download_package import download_package
from ..utils import (
    extract_package_id_from_url,
    validate_metadata_file,
    run_silent_command,
    safe_create_directory,
    safe_remove_directory,
    PACKAGES_DIR,
)


def install_package_from_metadata(package_dir, metadata):
    """Install package based on metadata configuration."""
    install_type = metadata["installType"]
    entry_points = metadata["entryPoint"]

    # Execute entry point commands
    for i, command in enumerate(entry_points):
        description = f"Running install command {i + 1}/{len(entry_points)}"
        if not run_silent_command(command, description, cwd=package_dir):
            return False

    # Handle executable installation
    if install_type == "executable" and "installExecutablePath" in metadata:
        executable_path = metadata["installExecutablePath"]
        # Create executable script or symlink if needed
        description = f"Setting up executable at {executable_path}"
        if not run_silent_command(f"sudo chmod +x {executable_path}", description):
            return False

    return True


def install_package_from_git(repo_url):
    """
    Install a package from a git repository URL.

    :param repo_url: URL of the git repository for the package
    :return: Tuple of (success: bool, message: str, package_name: str or None)
    """
    try:
        # Extract package ID from URL
        package_id = extract_package_id_from_url(repo_url)

        # Set up destination directory
        package_dest = os.path.join(PACKAGES_DIR, package_id)

        # Create packages directory if it doesn't exist
        if not safe_create_directory(PACKAGES_DIR):
            return (
                False,
                "Failed to create packages directory. Check permissions.",
                None,
            )

        # Remove existing package directory if it exists
        if os.path.exists(package_dest):
            if not safe_remove_directory(package_dest):
                return False, "Failed to remove existing package installation", None

        # Download the package
        try:
            download_package(repo_url, package_dest)
        except Exception as e:
            return False, f"Failed to download package: {e}", None

        # Check for metadata file
        metadata_file = os.path.join(package_dest, ".install.polly.json")

        # Validate metadata
        is_valid, error_msg = validate_metadata_file(metadata_file)
        if not is_valid:
            # Clean up downloaded package
            safe_remove_directory(package_dest)
            return False, f"Invalid package metadata: {error_msg}", None

        # Load metadata
        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
        except Exception as e:
            safe_remove_directory(package_dest)
            return False, f"Failed to load metadata: {e}", None

        # Install package based on metadata
        if not install_package_from_metadata(package_dest, metadata):
            # Clean up downloaded package
            safe_remove_directory(package_dest)
            return False, "Package installation failed", None

        return True, f"Package '{package_id}' installed successfully", package_id

    except Exception as e:
        return False, f"Unexpected error during installation: {e}", None
