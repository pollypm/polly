import os
import subprocess
from urllib.parse import urlparse


def extract_package_id_from_url(repo_url):
    """Extract package ID from git repository URL."""
    parsed = urlparse(repo_url)
    path = parsed.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    # Use the repository name as package ID
    return path.split("/")[-1]


def is_git_repository(directory):
    """Check if a directory is a git repository."""
    git_dir = os.path.join(directory, ".git")
    return os.path.exists(git_dir) and os.path.isdir(git_dir)


def get_git_info(package_path):
    """Get git repository information if available."""
    if not is_git_repository(package_path):
        return None

    git_info = {}

    try:
        # Get remote origin URL
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            git_info["origin"] = result.stdout.strip()
    except:
        pass

    try:
        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            git_info["branch"] = result.stdout.strip()
    except:
        pass

    try:
        # Get last commit info
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H|%s|%an|%ad", "--date=short"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            commit_data = result.stdout.strip().split("|")
            if len(commit_data) == 4:
                git_info["last_commit"] = {
                    "hash": commit_data[0][:8],
                    "message": commit_data[1],
                    "author": commit_data[2],
                    "date": commit_data[3],
                }
    except:
        pass

    return git_info if git_info else None


def check_for_updates(package_path):
    """Check if a package has updates available by comparing with remote."""
    if not is_git_repository(package_path):
        return None  # Not a git repository

    try:
        # Fetch latest changes from remote
        subprocess.run(
            ["git", "fetch", "origin"],
            cwd=package_path,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Get current commit hash
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return None
        current_commit = result.stdout.strip()

        # Get remote commit hash
        result = subprocess.run(
            ["git", "rev-parse", "origin/HEAD"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # Try with main/master branch
            result = subprocess.run(
                ["git", "rev-parse", "origin/main"],
                cwd=package_path,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                result = subprocess.run(
                    ["git", "rev-parse", "origin/master"],
                    cwd=package_path,
                    capture_output=True,
                    text=True,
                )

        if result.returncode != 0:
            return None

        remote_commit = result.stdout.strip()

        if current_commit != remote_commit:
            # Get commit messages for the updates
            result = subprocess.run(
                ["git", "log", "--oneline", f"{current_commit}..{remote_commit}"],
                cwd=package_path,
                capture_output=True,
                text=True,
            )

            commit_messages = []
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                commit_messages = [line for line in lines if line.strip()]

            return {
                "current_commit": current_commit[:8],
                "remote_commit": remote_commit[:8],
                "commit_messages": commit_messages,
            }

        return False  # Up to date

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, Exception):
        return None  # Error checking updates


def upgrade_git_package(package_path):
    """Upgrade a git package by pulling latest changes."""
    if not is_git_repository(package_path):
        return False

    try:
        # Pull latest changes
        result = subprocess.run(
            ["git", "pull", "origin"], cwd=package_path, capture_output=True, text=True
        )

        return result.returncode == 0

    except Exception:
        return False
