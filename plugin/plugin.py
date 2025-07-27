from polly.api import Plugin

class ExamplePlugin(Plugin):
    """
    Example plugin for Polly package manager.
    This plugin demonstrates basic functionality and can be extended as needed.
    """

    def __init__(self):
        super().__init__()
        
    def activate(self):
        """
        Activate the plugin.
        This method is called when the plugin is loaded.
        NOTE: This will run on every Polly command, so keep it lightweight.
        """
        print("ExamplePlugin activated!")
        
    def deactivate(self):
        """
        Deactivate the plugin.
        This method is called when the plugin is unloaded.
        NOTE: This will run on every Polly command, so keep it lightweight.
        """
        print("ExamplePlugin deactivated!")
        
    def on_event(self, event, *args, **kwargs):
        """
        Handle events from Polly.
        This method can be overridden to respond to specific events.
        
        :param event: The event type (e.g., 'install', 'upgrade', etc.)
        :param args: Positional arguments for the event
        :param kwargs: Keyword arguments for the event
        """
        print(f"Event received: {event}, args: {args}, kwargs: {kwargs}")