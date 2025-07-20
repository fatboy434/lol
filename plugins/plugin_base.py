class PluginBase:
    """
    The base class for all plugins.
    """
    def __init__(self, ai_core):
        self.ai_core = ai_core

    def process(self, data):
        """
        Processes the data and returns the result.
        """
        raise NotImplementedError
