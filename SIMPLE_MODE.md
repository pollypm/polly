# Simple Mode Documentation

The `--simple` flag provides plain text output format that's optimized for system integration and GUI applications.

## Usage

Add `--simple` as a global flag before any command:

```bash
polly --simple <command> [arguments]
```

## Supported Commands

All major commands support simple mode:

- `polly --simple help`
- `polly --simple list`
- `polly --simple list --detailed`
- `polly --simple install <repo_url>`
- `polly --simple uninstall <package_name>`
- `polly --simple inspect <package_name>`
- `polly --simple upgrade`

## Output Format

### Help Command
```
POLLY_HELP
VERSION|7ae2f47
LATEST_VERSION|7ae2f47
UPDATE_REQUIRED|False
COMMAND|help|Show this help message
COMMAND|update|Update Polly to the latest version
...
WEBSITE|https://github.com/pollypm/polly
```

### List Command (Simple)
```
# When packages exist:
package1|Git|1.2MB|2024-01-15|True
package2|Direct|856KB|2024-01-14|False
TOTAL|2|2.1MB

# When no packages:
NO_PACKAGES
```

### List Command (Detailed)
```
package1|Git|1.2MB|2024-01-15 10:30:45|/opt/pollypackages/package1|True|1.0.0|A sample package|/usr/local/bin/package1|True
TOTAL|1|1.2MB
```

### Install Command
```
PACKAGE_ID|owner/repo
REPOSITORY|https://github.com/owner/repo.git
SUCCESS|Package installed successfully
LOCATION|/opt/pollypackages/repo
```

### Uninstall Command
```
PACKAGE|package_name
SUCCESS|Package uninstalled successfully
```

### Inspect Command
```
NAME|package_name
TYPE|Git
PATH|/opt/pollypackages/package_name
INSTALLED|2024-01-15 10:30:45
SIZE|1.2MB
FILES|150
EXECUTABLE_PATH|/usr/local/bin/package_name
EXECUTABLE_EXISTS|True
ENTRY_POINT|package_name
GIT_ORIGIN|https://github.com/owner/repo.git
GIT_BRANCH|main
GIT_LAST_COMMIT|abc123|Initial commit|John Doe|2024-01-15
METADATA_VERSION|1.0.0
FILE|README.md|2KB
FILE|setup.py|1KB
```

### Upgrade Command
```
PROGRESS|Scanning installed packages
PROGRESS|Checking for updates
UPGRADE_AVAILABLE|package1|abc123|def456|1.2MB
COMMIT_MESSAGE|package1|Fix critical bug
PROGRESS|Upgrading packages
SUCCESS|Successfully upgraded: package1
SUCCESS|All packages upgraded successfully!
```

### Error Messages
All error messages follow the format:
```
ERROR: <error description>
```

### Success Messages
All success messages follow the format:
```
SUCCESS: <success description>
```

### Progress Messages
All progress messages follow the format:
```
PROGRESS: <progress description>
```

## Benefits for GUI Integration

1. **Structured Output**: Pipe-delimited fields make parsing easy
2. **No ANSI Colors**: Clean text without escape sequences
3. **Consistent Format**: Predictable structure across all commands
4. **Machine Readable**: Easy to parse with any programming language
5. **Error Handling**: Clear error/success status indicators

## Example GUI Integration

```python
import subprocess

def run_polly_command(command):
    result = subprocess.run(
        ["polly", "--simple"] + command,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return None, result.stdout.strip()
    
    return result.stdout.strip().split('\n'), None

# List packages
packages, error = run_polly_command(["list"])
if packages:
    for line in packages:
        if line.startswith("TOTAL|"):
            _, count, size = line.split("|")
            print(f"Total: {count} packages ({size})")
        elif line == "NO_PACKAGES":
            print("No packages installed")
        elif "|" in line:
            name, type_, size, date, has_metadata = line.split("|")
            print(f"{name}: {size} ({type_})")
```

This simple mode makes it very easy to integrate Polly with GUI applications, system monitoring tools, or any other software that needs to interact with Polly programmatically.
