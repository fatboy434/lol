from agents.agent_base import AgentBase
import time

class RoutineAgent(AgentBase):
    def __init__(self, agent_manager):
        super().__init__(agent_manager)

    def run(self):
        while True:
            self.send_message("SpeechAgent", "Performing routine check.")
            time.sleep(10)
