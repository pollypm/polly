import subprocess
from .colors import format_message


def run_silent_command(command, description, cwd=None):
    """Run a command silently and return success status."""
    print(format_message("progress", f"{description}..."))

    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, cwd=cwd
        )

        if result.returncode == 0:
            print(format_message("success", f"{description} completed"))
            return True
        else:
            print(format_message("error", f"{description} failed"))
            if result.stderr:
                print(f"    Error: {result.stderr.strip()}")
            return False

    except Exception as e:
        print(format_message("error", f"{description} failed"))
        print(f"    Exception: {e}")
        return False


def run_command_with_output(command, description, cwd=None):
    """Run a command and return the result with output."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, cwd=cwd
        )
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        return {"success": False, "returncode": -1, "stdout": "", "stderr": str(e)}


def check_command_available(command):
    """Check if a command is available in the system."""
    try:
        result = subprocess.run(["which", command], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False
