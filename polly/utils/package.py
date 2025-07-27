import os
import json
from datetime import datetime
from .filesystem import get_directory_size, file_exists


PACKAGES_DIR = "/opt/pollypackages"


def get_installed_packages():
    """Get list of installed packages with their metadata."""
    if not os.path.exists(PACKAGES_DIR):
        return []

    packages = []
    for item in os.listdir(PACKAGES_DIR):
        package_path = os.path.join(PACKAGES_DIR, item)
        if os.path.isdir(package_path):
            metadata_file = os.path.join(package_path, ".install.polly.json")
            if os.path.exists(metadata_file):
                try:
                    with open(metadata_file, "r") as f:
                        metadata = json.load(f)

                    # Get package information
                    size = get_directory_size(package_path)
                    install_time = os.path.getctime(package_path)
                    install_date = datetime.fromtimestamp(install_time).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    packages.append(
                        {
                            "name": item,
                            "path": package_path,
                            "metadata": metadata,
                            "size": size,
                            "install_date": install_date,
                            "install_type": metadata.get("installType", "Unknown"),
                        }
                    )
                except:
                    # If metadata is invalid, still include package but with limited info
                    size = get_directory_size(package_path)
                    install_time = os.path.getctime(package_path)
                    install_date = datetime.fromtimestamp(install_time).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    packages.append(
                        {
                            "name": item,
                            "path": package_path,
                            "metadata": None,
                            "size": size,
                            "install_date": install_date,
                            "install_type": "Invalid",
                        }
                    )

    return sorted(packages, key=lambda x: x["name"].lower())


def get_package_by_name(package_name):
    """Get a specific package by name."""
    packages = get_installed_packages()
    for package in packages:
        if package["name"] == package_name:
            return package
    return None


def package_exists(package_name):
    """Check if a package is installed."""
    package_path = os.path.join(PACKAGES_DIR, package_name)
    metadata_file = os.path.join(package_path, ".install.polly.json")
    return os.path.exists(package_path) and os.path.exists(metadata_file)


def get_package_names():
    """Get list of installed package names."""
    packages = get_installed_packages()
    return [package["name"] for package in packages]


def validate_metadata_file(metadata_file):
    """Validate the .install.polly.json metadata file."""
    if not file_exists(metadata_file):
        return False, "Metadata file not found"

    try:
        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        # Required fields
        required_fields = ["installType", "entryPoint"]
        for field in required_fields:
            if field not in metadata:
                return False, f"Missing required field: {field}"

        # Validate installType
        valid_install_types = ["executable", "library", "script"]
        if metadata["installType"] not in valid_install_types:
            return (
                False,
                f"Invalid installType. Must be one of: {', '.join(valid_install_types)}",
            )

        # Validate entryPoint is a list
        if not isinstance(metadata["entryPoint"], list):
            return False, "entryPoint must be a list of commands"

        # If installType is executable, check for installExecutablePath
        if (
            metadata["installType"] == "executable"
            and "installExecutablePath" not in metadata
        ):
            return False, "installExecutablePath is required for executable packages"

        return True, "Valid metadata"

    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in metadata file: {e}"
    except Exception as e:
        return False, f"Error validating metadata: {e}"


def load_package_metadata(package_path):
    """Load metadata for a package."""
    metadata_file = os.path.join(package_path, ".install.polly.json")
    try:
        with open(metadata_file, "r") as f:
            return json.load(f)
    except Exception:
        return None
