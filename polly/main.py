import sys
import os

# Add project root to sys.path for imports
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from polly.cli import dispatch_command
except ImportError as e:
    print(f"Error: Unable to import dispatch_command from polly.cli - {e}")
    sys.exit(1)


def main():
    args = sys.argv[1:]  # Exclude the script name
    dispatch_command(args)


if __name__ == "__main__":
    main()
