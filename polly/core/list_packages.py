from ..utils import get_installed_packages, format_size


def list_packages(detailed=False):
    """
    List all installed packages.

    :param detailed: Whether to return detailed information
    :return: Tuple of (success: bool, message: str, data: dict)
    """
    try:
        packages = get_installed_packages()

        if not packages:
            return (
                True,
                "No packages are currently installed",
                {
                    "packages": [],
                    "total_count": 0,
                    "total_size": 0,
                    "detailed": detailed,
                },
            )

        # Calculate totals
        total_size = sum(package["size"] for package in packages)

        # Format packages for display
        formatted_packages = []
        for package in packages:
            formatted_package = {
                "name": package["name"],
                "install_type": package["install_type"],
                "size": package["size"],
                "size_formatted": format_size(package["size"]),
                "install_date": package["install_date"],
                "path": package["path"],
                "has_metadata": package["metadata"] is not None,
            }

            if detailed:
                # Add detailed information
                if package["metadata"]:
                    metadata = package["metadata"]

                    # Check executable status
                    executable_info = None
                    if (
                        metadata.get("installType") == "executable"
                        and "installExecutablePath" in metadata
                    ):
                        import os

                        executable_path = metadata["installExecutablePath"]
                        executable_info = {
                            "path": executable_path,
                            "exists": os.path.exists(executable_path),
                        }

                    formatted_package.update(
                        {
                            "executable_info": executable_info,
                            "entry_points": metadata.get("entryPoint", []),
                            "version": metadata.get("version"),
                            "description": metadata.get("description"),
                            "author": metadata.get("author"),
                        }
                    )

            formatted_packages.append(formatted_package)

        return (
            True,
            f"Found {len(packages)} installed package(s)",
            {
                "packages": formatted_packages,
                "total_count": len(packages),
                "total_size": total_size,
                "total_size_formatted": format_size(total_size),
                "detailed": detailed,
            },
        )

    except Exception as e:
        return (
            False,
            f"Error listing packages: {e}",
            {"packages": [], "total_count": 0, "total_size": 0, "detailed": detailed},
        )
