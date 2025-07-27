from polly.cli.commands.help import help_main
from polly.cli.commands.update import update_main


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
    else:
        print(f"Unknown command: {command}")
