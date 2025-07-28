import os
import subprocess
from urllib.parse import urlparse
from ..utils import run_silent_command
from .debug import debug_print, format_error_with_debug


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


def check_for_updates(package_path, debug=False):
    """Check if a package has updates available by comparing with remote."""

    debug_print(f"Checking for updates in package: {package_path}")

    if not is_git_repository(package_path):
        debug_print(f"{package_path} is not a git repository")
        return None

    try:
        # Fetch latest changes from remote
        debug_print(f"Fetching latest changes from remote for {package_path}")
        result = subprocess.run(
            ["sudo", "git", "fetch", "origin"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            debug_print(f"Failed to fetch from remote: {result.stderr}")
            return None

        # Get current commit hash
        debug_print("Getting current commit hash")
        result = subprocess.run(
            ["sudo", "git", "rev-parse", "HEAD"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            debug_print(f"Failed to get current commit: {result.stderr}")
            return None
        current_commit = result.stdout.strip()
        debug_print(f"Current commit: {current_commit}")

        # Get current branch name
        debug_print("Getting current branch name")
        result = subprocess.run(
            ["sudo", "git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )
        current_branch = result.stdout.strip() if result.returncode == 0 else "main"
        debug_print(f"Current branch: {current_branch}")

        # Get remote commit hash for current branch
        debug_print(f"Getting remote commit hash for branch {current_branch}")
        result = subprocess.run(
            ["sudo", "git", "rev-parse", f"origin/{current_branch}"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )

        # Fallback to common branch names if current branch doesn't exist on remote
        if result.returncode != 0:
            debug_print(
                f"Branch {current_branch} not found on remote, trying fallback branches"
            )
            for branch in ["main", "master"]:
                result = subprocess.run(
                    ["sudo", "git", "rev-parse", f"origin/{branch}"],
                    cwd=package_path,
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    debug_print(f"Using fallback branch {branch}")
                    break
            else:
                debug_print("No valid remote branch found")
                return None

        remote_commit = result.stdout.strip()
        debug_print(f"Remote commit: {remote_commit}")

        # Check if updates are available
        if current_commit == remote_commit:
            debug_print("Package is up to date")
            return False  # Up to date

        # Get commit count and messages for updates
        debug_print("Getting commit count and messages for updates")
        result = subprocess.run(
            [
                "sudo",
                "git",
                "rev-list",
                "--count",
                f"{current_commit}..{remote_commit}",
            ],
            cwd=package_path,
            capture_output=True,
            text=True,
        )
        commit_count = int(result.stdout.strip()) if result.returncode == 0 else 0

        result = subprocess.run(
            ["sudo", "git", "log", "--oneline", f"{current_commit}..{remote_commit}"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )

        commit_messages = []
        if result.returncode == 0 and result.stdout.strip():
            commit_messages = [
                line.strip()
                for line in result.stdout.strip().split("\n")
                if line.strip()
            ]

        update_info = {
            "current_commit": current_commit[:8],
            "remote_commit": remote_commit[:8],
            "commit_count": commit_count,
            "commit_messages": commit_messages[:10],  # Limit to 10 most recent
        }

        debug_print(f"Found {commit_count} updates available")

        return update_info

    except Exception as e:
        debug_print(f"Exception occurred while checking for updates: {e}")
        return None


def upgrade_git_package(package_path):
    """Upgrade a git package by pulling latest changes."""
    debug_print(f"Attempting to upgrade git package at: {package_path}")

    if not is_git_repository(package_path):
        debug_print(f"Directory is not a git repository: {package_path}")
        return False

    try:
        debug_print("Running 'git pull origin'")
        # Pull latest changes
        result = subprocess.run(
            ["sudo", "git", "pull", "origin"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )

        debug_print(f"Git pull return code: {result.returncode}")
        debug_print(f"Git pull stdout: {result.stdout}")
        debug_print(f"Git pull stderr: {result.stderr}")

        if result.returncode == 0:
            debug_print("Git package upgrade successful")
        else:
            debug_print(
                f"Git package upgrade failed with return code: {result.returncode}"
            )

        return result.returncode == 0

    except Exception as e:
        debug_print(f"Exception during git package upgrade: {e}")
        return False
