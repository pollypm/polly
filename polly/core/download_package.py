import subprocess

from ..utils import run_silent_command


def download_package(repo_url, dest_dir=None):
    """
    Clone a package to the specified directory.

    :param repo_url: URL of the git repository for the package
    :param dest_dir: Destination directory (optional)
    :return: None
    :raises: subprocess.CalledProcessError if git clone fails
    """
    command = f"git clone {repo_url}"
    if dest_dir:
        command += f" {dest_dir}"

    if not run_silent_command(command, "Cloning package"):
        raise subprocess.CalledProcessError(
            returncode=1, cmd=command, output="Failed to clone package"
        )
    print("Package cloned successfully.")
    return