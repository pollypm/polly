import subprocess
from .colors import format_message
from .debug import is_debug_mode, format_error_with_debug, debug_print


def run_silent_command(command, description, cwd=None):
    """Run a command silently and return success status."""
    print(format_message("progress", f"{description}..."))

    debug_print(f"Running command: {command}")
    debug_print(f"Working directory: {cwd}")

    try:
        result = subprocess.run(
            "sudo " + command, shell=True, capture_output=True, text=True, cwd=cwd
        )

        debug_print(f"Command return code: {result.returncode}")
        debug_print(f"Command stdout: {result.stdout}")
        debug_print(f"Command stderr: {result.stderr}")

        if result.returncode == 0:
            print(format_message("success", f"{description} completed"))
            return True
        else:
            error_msg = format_error_with_debug(
                f"{description} failed",
                f"Command: {command}\nReturn code: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}",
            )
            print(format_message("error", error_msg))
            return False

    except Exception as e:
        error_msg = format_error_with_debug(
            f"{description} failed", f"Command: {command}\nWorking directory: {cwd}", e
        )
        print(format_message("error", error_msg))
        return False


def run_command_with_output(command, description, cwd=None):
    """Run a command and return the result with output."""
    debug_print(f"Running command with output: {command}")
    debug_print(f"Working directory: {cwd}")

    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, cwd=cwd
        )

        debug_print(f"Command return code: {result.returncode}")
        debug_print(f"Command stdout: {result.stdout}")
        debug_print(f"Command stderr: {result.stderr}")

        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        debug_print(f"Exception running command: {e}")
        return {"success": False, "returncode": -1, "stdout": "", "stderr": str(e)}


def check_command_available(command):
    """Check if a command is available in the system."""
    try:
        result = subprocess.run(["which", command], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False
