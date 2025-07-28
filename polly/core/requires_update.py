import requests
import subprocess
from functools import lru_cache


@lru_cache(maxsize=1)
def get_latest_commit():
    # Try git command first (faster, no rate limits)
    try:
        result = subprocess.run(
            ["git", "ls-remote", "https://github.com/pollypm/polly.git", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.split()[0]
    except Exception:
        pass

    # Fallback to API
    try:
        response = requests.get("https://api.github.com/repos/pollypm/polly/commits")
        response.raise_for_status()
        commits = response.json()
        if commits:
            return commits[0]["sha"]
        return None
    except Exception:
        return None


def get_current_version():
    version_file = "/opt/polly/latest"
    try:
        with open(version_file, "r") as f:
            return f.read().strip()
    except Exception:
        return "Unknown"


def update_required() -> bool:
    latest_commit = get_latest_commit()
    current_version = get_current_version()

    return latest_commit is not None and current_version != latest_commit


def latest_version() -> str:
    latest_commit = get_latest_commit()
    return latest_commit if latest_commit else "Unknown"


def get_recent_commit_messages():
    """Get recent commit messages between current version and latest version."""
    try:
        current_version = get_current_version()
        latest_commit = get_latest_commit()

        if not current_version or current_version == "Unknown" or not latest_commit:
            return []

        # If current version and latest are the same, no updates available
        if current_version == latest_commit:
            return []

        # Try to get commit messages using GitHub API
        try:
            # Get commits from the repository
            response = requests.get(
                "https://api.github.com/repos/pollypm/polly/commits",
                params={"per_page": 20},  # Get up to 20 recent commits
                timeout=10,
            )
            response.raise_for_status()
            commits = response.json()

            commit_messages = []
            found_current = False

            # Iterate through commits from newest to oldest
            for commit in commits:
                commit_sha = commit["sha"]
                commit_message = commit["commit"]["message"].split("\n")[
                    0
                ]  # Get first line only

                # If we find the current version, stop collecting
                if commit_sha.startswith(current_version) or current_version.startswith(
                    commit_sha
                ):
                    found_current = True
                    break

                # Add commit message to list
                commit_messages.append(commit_message)

            # If we didn't find the current version in recent commits,
            # it means there are many commits between current and latest
            if not found_current and commit_messages:
                # Return the messages we found
                return commit_messages

            return commit_messages

        except Exception:
            # Fallback: try using git command if available
            try:
                result = subprocess.run(
                    [
                        "git",
                        "log",
                        "--oneline",
                        f"{current_version[:8]}..{latest_commit[:8]}",
                        "--max-count=10",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd="/",  # Run from root to avoid issues
                )

                if result.returncode == 0 and result.stdout.strip():
                    commit_lines = result.stdout.strip().split("\n")
                    # Extract commit messages (remove hash prefix)
                    messages = []
                    for line in commit_lines:
                        if line.strip():
                            # Split on first space to remove hash
                            parts = line.strip().split(" ", 1)
                            if len(parts) > 1:
                                messages.append(parts[1])
                    return messages

            except Exception:
                pass

    except Exception:
        pass

    return []
