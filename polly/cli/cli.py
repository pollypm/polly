from polly.cli.commands.help import display_help


def dispatch_command(args):
    """
    Receives a list of arguments. The first argument is the command.
    Dispatches the remaining arguments to the appropriate script based on the command.
    """
    if not args:
        display_help()

    command = args[0]
    command_args = args[1:]

    if command == "help":
        display_help()
    else:
        print(f"Unknown command: {command}")
