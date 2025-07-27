import os
import json
from datetime import datetime
from ..utils import (
    get_package_by_name,
    get_directory_size,
    format_size,
    get_file_count,
    get_git_info,
    file_exists,
)


def get_package_statistics(package_path):
    """Get statistics for a package."""
    package_size = get_directory_size(package_path)
    file_count = get_file_count(package_path)
    install_time = os.path.getctime(package_path)
    install_date = datetime.fromtimestamp(install_time).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "size": package_size,
        "file_count": file_count,
        "install_date": install_date,
    }


def get_package_contents(package_path):
    """Get information about important package files."""
    important_files = [
        ".install.polly.json",
        "README.md",
        "main.py",
        "setup.py",
        "requirements.txt",
    ]
    found_files = []

    for file in important_files:
        file_path = os.path.join(package_path, file)
        if file_exists(file_path):
            size = format_size(os.path.getsize(file_path))
            found_files.append({"name": file, "size": size})

    return found_files


def inspect_package(package_name):
    """
    Inspect a package and return detailed information.

    :param package_name: Name of the package to inspect
    :return: Tuple of (success: bool, message: str, data: dict or None)
    """
    try:
        # Get package information
        package = get_package_by_name(package_name)
        if not package:
            return False, f"Package '{package_name}' is not installed", None

        package_path = package["path"]
        metadata = package["metadata"]

        if not metadata:
            return False, f"Package metadata not found for '{package_name}'", None

        # Get package statistics
        stats = get_package_statistics(package_path)

        # Get Git information if available
        git_info = get_git_info(package_path)

        # Get package contents
        contents = get_package_contents(package_path)

        # Check executable status
        executable_status = None
        if (
            metadata.get("installType") == "executable"
            and "installExecutablePath" in metadata
        ):
            executable_path = metadata["installExecutablePath"]
            executable_status = {
                "path": executable_path,
                "exists": os.path.exists(executable_path),
            }

        # Prepare additional metadata (excluding standard fields)
        standard_fields = {
            "installType",
            "entryPoint",
            "installExecutablePath",
            "uninstallCommands",
        }
        additional_metadata = {
            k: v for k, v in metadata.items() if k not in standard_fields
        }

        # Compile all information
        inspection_data = {
            "name": package_name,
            "path": package_path,
            "install_type": metadata.get("installType", "Unknown"),
            "stats": stats,
            "metadata": metadata,
            "git_info": git_info,
            "contents": contents,
            "executable_status": executable_status,
            "additional_metadata": additional_metadata,
        }

        return True, "Package inspection completed", inspection_data

    except Exception as e:
        return False, f"Unexpected error during inspection: {e}", None
