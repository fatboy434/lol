import os
import importlib

class PluginManager:
    def __init__(self, ai_core):
        self.ai_core = ai_core
        self.plugins = []

    def load_plugins(self):
        """
        Loads all plugins from the plugins directory.
        """
        plugins_dir = "plugins"
        for filename in os.listdir(plugins_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"{plugins_dir}.{filename[:-3]}"
                module = importlib.import_module(module_name)
                for name in dir(module):
                    obj = getattr(module, name)
                    if isinstance(obj, type) and issubclass(obj, object) and obj is not object:
                        self.plugins.append(obj(self.ai_core))

    def process_command(self, command):
        """
        Passes the command to all loaded plugins.
        """
        for plugin in self.plugins:
            plugin.process(command)
