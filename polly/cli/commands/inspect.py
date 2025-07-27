import sys
import json
import argparse
from polly.core import inspect_package
from polly.utils import print_header, format_message, get_colors, format_size


def display_inspection_data(data, simple_mode=False):
    """Display the package inspection data in a formatted way."""
    if simple_mode:
        # Simple plain text format for system integration
        name = data['name']
        install_type = data['install_type']
        path = data['path']
        install_date = data['stats']['install_date']
        size = format_size(data['stats']['size'])
        file_count = data['stats']['file_count']
        
        # Basic info
        print(f"NAME|{name}")
        print(f"TYPE|{install_type}")
        print(f"PATH|{path}")
        print(f"INSTALLED|{install_date}")
        print(f"SIZE|{size}")
        print(f"FILES|{file_count}")
        
        # Executable status
        if data['executable_status']:
            executable_path = data['executable_status']['path']
            executable_exists = data['executable_status']['exists']
            print(f"EXECUTABLE_PATH|{executable_path}")
            print(f"EXECUTABLE_EXISTS|{executable_exists}")
        else:
            print("EXECUTABLE_PATH|N/A")
            print("EXECUTABLE_EXISTS|N/A")
        
        # Entry points
        metadata = data['metadata']
        if 'entryPoint' in metadata and isinstance(metadata['entryPoint'], list):
            for entry_point in metadata['entryPoint']:
                print(f"ENTRY_POINT|{entry_point}")
        
        # Uninstall commands
        if 'uninstallCommands' in metadata and isinstance(metadata['uninstallCommands'], list):
            for command in metadata['uninstallCommands']:
                print(f"UNINSTALL_COMMAND|{command}")
        
        # Git info
        if data['git_info']:
            git_info = data['git_info']
            print(f"GIT_ORIGIN|{git_info.get('origin', 'N/A')}")
            print(f"GIT_BRANCH|{git_info.get('branch', 'N/A')}")
            if 'last_commit' in git_info:
                commit = git_info['last_commit']
                print(f"GIT_LAST_COMMIT|{commit['hash']}|{commit['message']}|{commit['author']}|{commit['date']}")
        
        # Additional metadata
        if data['additional_metadata']:
            for key, value in data['additional_metadata'].items():
                if isinstance(value, (str, int, float, bool)):
                    print(f"METADATA_{key.upper()}|{value}")
        
        # Package contents
        if data['contents']:
            for file_info in data['contents']:
                print(f"FILE|{file_info['name']}|{file_info['size']}")
        
        return
    
    colors = get_colors()
    
    # Basic information
    print(f"  {colors['info']}Package Name:{colors['reset']} {colors['primary']}{data['name']}{colors['reset']}")
    print(f"  {colors['info']}Install Type:{colors['reset']} {colors['grey']}{data['install_type']}{colors['reset']}")
    print(f"  {colors['info']}Location:{colors['reset']} {colors['grey']}{data['path']}{colors['reset']}")
    print(f"  {colors['info']}Installed:{colors['reset']} {colors['grey']}{data['stats']['install_date']}{colors['reset']}")
    print(f"  {colors['info']}Size:{colors['reset']} {colors['grey']}{format_size(data['stats']['size'])}{colors['reset']}")
    print(f"  {colors['info']}Files:{colors['reset']} {colors['grey']}{data['stats']['file_count']:,}{colors['reset']}")
    
    # Executable information
    if data['executable_status']:
        executable_path = data['executable_status']['path']
        executable_exists = data['executable_status']['exists']
        status = f"{colors['success']}✔ Available{colors['reset']}" if executable_exists else f"{colors['error']}✖ Missing{colors['reset']}"
        print(f"  {colors['info']}Executable:{colors['reset']} {colors['grey']}{executable_path}{colors['reset']} {status}")
    
    # Entry points
    metadata = data['metadata']
    if 'entryPoint' in metadata:
        entry_points = metadata['entryPoint']
        if isinstance(entry_points, list) and entry_points:
            print(f"\n  {colors['info']}Entry Points:{colors['reset']}")
            for i, entry_point in enumerate(entry_points, 1):
                print(f"    {colors['grey']}{i}. {entry_point}{colors['reset']}")
    
    # Uninstall commands if available
    if 'uninstallCommands' in metadata:
        uninstall_commands = metadata['uninstallCommands']
        if isinstance(uninstall_commands, list) and uninstall_commands:
            print(f"\n  {colors['info']}Uninstall Commands:{colors['reset']}")
            for i, command in enumerate(uninstall_commands, 1):
                print(f"    {colors['grey']}{i}. {command}{colors['reset']}")
    
    # Git information if available
    if data['git_info']:
        git_info = data['git_info']
        print(f"\n  {colors['info']}Git Information:{colors['reset']}")
        if 'origin' in git_info:
            print(f"    {colors['grey']}Origin: {git_info['origin']}{colors['reset']}")
        if 'branch' in git_info:
            print(f"    {colors['grey']}Branch: {git_info['branch']}{colors['reset']}")
        if 'last_commit' in git_info:
            commit = git_info['last_commit']
            print(f"    {colors['grey']}Last Commit: {commit['hash']} - {commit['message']}{colors['reset']}")
            print(f"    {colors['grey']}Author: {commit['author']} ({commit['date']}){colors['reset']}")
    
    # Additional metadata fields
    if data['additional_metadata']:
        print(f"\n  {colors['info']}Additional Metadata:{colors['reset']}")
        for key, value in data['additional_metadata'].items():
            if isinstance(value, (str, int, float, bool)):
                print(f"    {colors['grey']}{key}: {value}{colors['reset']}")
            else:
                print(f"    {colors['grey']}{key}: {json.dumps(value, indent=2)}{colors['reset']}")
    
    # Package contents
    if data['contents']:
        print(f"\n  {colors['info']}Package Contents:{colors['reset']}")
        for file_info in data['contents']:
            print(f"    {colors['grey']}• {file_info['name']} ({file_info['size']}){colors['reset']}")
    else:
        print(f"\n  {colors['info']}Package Contents:{colors['reset']}")
        print(f"    {colors['grey']}No standard files found{colors['reset']}")


def inspect_main(args=None):
    """Main function for the inspect command."""
    colors = get_colors()
    
    if args is None:
        args = sys.argv[1:]
    
    parser = argparse.ArgumentParser(
        description="Inspect an installed package",
        prog="polly inspect"
    )
    parser.add_argument(
        "package_name",
        help="Name of the package to inspect"
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Output in simple plain text format for system integration",
    )
    
    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return
    
    package_name = parsed_args.package_name
    simple_mode = parsed_args.simple
    
    # Print header (unless in simple mode)
    if not simple_mode:
        print_header("Polly", "Package Inspection")
    
    # Inspect the package
    try:
        success, message, data = inspect_package(package_name)
        
        if success and data:
            display_inspection_data(data, simple_mode)
            if not simple_mode:
                print(f"\n{format_message('success', 'Package inspection completed')}\n")
        else:
            print(format_message('error', message, simple_mode))
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(format_message('error', "Inspection cancelled by user", simple_mode))
        sys.exit(1)
    except Exception as e:
        print(format_message('error', f"Unexpected error during inspection: {e}", simple_mode))
        sys.exit(1)


if __name__ == "__main__":
    inspect_main()
