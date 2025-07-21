from agents.agent_base import AgentBase
from core.memory import Memory

class MemoryAgent(AgentBase):
    def __init__(self, agent_manager):
        super().__init__(agent_manager)
        self.memory = Memory()

    def receive_message(self, message):
        if message["type"] == "set_short_term":
            self.memory.set_short_term(message["key"], message["value"])
        elif message["type"] == "get_short_term":
            value = self.memory.get_short_term(message["key"])
            self.send_message(message["sender"], {"type": "short_term_response", "value": value})
        elif message["type"] == "set_long_term":
            self.memory.set_long_term(message["key"], message["value"])
        elif message["type"] == "get_long_term":
            value = self.memory.get_long_term(message["key"])
            self.send_message(message["sender"], {"type": "long_term_response", "value": value})
