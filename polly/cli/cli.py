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

    command = args[0]
    command_args = args[1:]

    if command == "help":
        help_main()
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
        print(f"Unknown command: {command}")
