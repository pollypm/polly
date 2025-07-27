from polly.cli.commands.help import help_main
from polly.cli.commands.update import update_main
from polly.cli.commands.install import install_main
from polly.cli.commands.uninstall import uninstall_main
from polly.cli.commands.inspect import inspect_main
from polly.cli.commands.upgrade import upgrade_main
from polly.cli.commands.list import list_main


def dispatch_command(args):
    """
    Receives a list of arguments. The first argument is the command.
    Dispatches the remaining arguments to the appropriate script based on the command.
    """
    if not args:
        help_main()
        return

    # Check for global --simple flag
    simple_mode = False
    filtered_args = []
    for arg in args:
        if arg == "--simple":
            simple_mode = True
        else:
            filtered_args.append(arg)
    
    # Update args to filtered list
    args = filtered_args
    
    if not args:
        help_main()
        return

    command = args[0]
    command_args = args[1:]

    # Add simple mode to command args if enabled
    if simple_mode:
        command_args.append("--simple")

    if command == "help":
        help_main(command_args if simple_mode else [])
    elif command == "update":
        update_main()
    elif command == "install":
        install_main(command_args)
    elif command == "uninstall":
        uninstall_main(command_args)
    elif command == "inspect":
        inspect_main(command_args)
    elif command == "upgrade":
        upgrade_main(command_args)
    elif command == "list":
        list_main(command_args)
    else:
        if simple_mode:
            print(f"ERROR: Unknown command: {command}")
        else:
            print(f"Unknown command: {command}")
