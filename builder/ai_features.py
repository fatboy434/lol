class MemoryManager:
    def __init__(self):
        self.memory = {}

    def set(self, key, value):
        self.memory[key] = value

    def get(self, key):
        return self.memory.get(key)

class BrainConnector:
    def __init__(self, modules):
        self.modules = modules
        self.memory_manager = MemoryManager()

    def connect(self):
        for module in self.modules:
            module.memory = self.memory_manager
            module.send_message = self.send_message

    def send_message(self, message):
        for module in self.modules:
            if hasattr(module, "receive_message"):
                module.receive_message(message)
