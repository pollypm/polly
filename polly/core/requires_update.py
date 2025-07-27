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
