import subprocess


def download_package(repo_url, dest_dir=None):
    """
    Clone a package to the specified directory.

    :param repo_url: URL of the git repository for the package
    :param dest_dir: Destination directory (optional)
    :return: None
    :raises: subprocess.CalledProcessError if git clone fails
    """
    cmd = ["git", "clone", repo_url]
    if dest_dir:
        cmd.append(dest_dir)
    try:
        # Run git clone with suppressed output for cleaner install process
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode, e.cmd, f"Failed to clone {repo_url}"
        )
