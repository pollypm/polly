import os
import shutil


def get_directory_size(directory):
    """Calculate the total size of a directory in bytes."""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    pass
    except (OSError, FileNotFoundError):
        pass
    return total_size


def format_size(size_bytes):
    """Format size in bytes to human readable format."""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    size_index = 0
    size = float(size_bytes)

    while size >= 1024.0 and size_index < len(size_names) - 1:
        size /= 1024.0
        size_index += 1

    return f"{size:.1f} {size_names[size_index]}"


def get_file_count(directory):
    """Count the number of files in a directory."""
    count = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            count += len(filenames)
    except (OSError, FileNotFoundError):
        pass
    return count


def get_available_space(path):
    """Get available disk space for a given path."""
    try:
        stat = os.statvfs(path)
        available_bytes = stat.f_bavail * stat.f_frsize
        return available_bytes
    except (OSError, AttributeError):
        return None


def safe_remove_directory(directory_path):
    """Safely remove a directory and all its contents."""
    try:
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)
            return True
    except Exception:
        pass
    return False


def safe_create_directory(directory_path):
    """Safely create a directory, including parent directories."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception:
        return False


def file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path) and os.path.isfile(file_path)


def directory_exists(directory_path):
    """Check if a directory exists."""
    return os.path.exists(directory_path) and os.path.isdir(directory_path)
