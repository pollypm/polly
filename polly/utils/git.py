import os
import subprocess
from urllib.parse import urlparse
from ..utils import run_silent_command


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

    if not is_git_repository(package_path):
        if debug:
            print(f"Debug: {package_path} is not a git repository")
        return None

    try:
        # Fetch latest changes from remote
        if debug:
            print(f"Debug: Fetching latest changes from remote for {package_path}")
        result = subprocess.run(
            ["sudo", "git", "fetch", "origin"], cwd=package_path, capture_output=True, text=True
        )
        if result.returncode != 0:
            if debug:
                print(f"Debug: Failed to fetch from remote: {result.stderr}")
            return None

        # Get current commit hash
        if debug:
            print("Debug: Getting current commit hash")
        result = subprocess.run(
            ["sudo", "git", "rev-parse", "HEAD"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            if debug:
                print(f"Debug: Failed to get current commit: {result.stderr}")
            return None
        current_commit = result.stdout.strip()

        # Get current branch name
        if debug:
            print("Debug: Getting current branch name")
        result = subprocess.run(
            ["sudo", "git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )
        current_branch = result.stdout.strip() if result.returncode == 0 else "main"

        # Get remote commit hash for current branch
        if debug:
            print(f"Debug: Getting remote commit hash for branch {current_branch}")
        result = subprocess.run(
            ["sudo", "git", "rev-parse", f"origin/{current_branch}"],
            cwd=package_path,
            capture_output=True,
            text=True,
        )

        # Fallback to common branch names if current branch doesn't exist on remote
        if result.returncode != 0:
            if debug:
                print(
                    f"Debug: Branch {current_branch} not found on remote, trying fallback branches"
                )
            for branch in ["main", "master"]:
                result = subprocess.run(
                    ["sudo", "git", "rev-parse", f"origin/{branch}"],
                    cwd=package_path,
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    if debug:
                        print(f"Debug: Using fallback branch {branch}")
                    break
            else:
                if debug:
                    print("Debug: No valid remote branch found")
                return None

        remote_commit = result.stdout.strip()

        # Check if updates are available
        if current_commit == remote_commit:
            if debug:
                print("Debug: Package is up to date")
            return False  # Up to date

        # Get commit count and messages for updates
        if debug:
            print("Debug: Getting commit count and messages for updates")
        result = subprocess.run(
            ["sudo", "git", "rev-list", "--count", f"{current_commit}..{remote_commit}"],
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

        if debug:
            print(f"Debug: Found {commit_count} updates available")

        return update_info

    except Exception as e:
        if debug:
            print(f"Debug: Exception occurred: {e}")
        return None


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
