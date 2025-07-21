from agents.agent_base import AgentBase
import time

class VisionAgent(AgentBase):
    def __init__(self, agent_manager, ai_core):
        super().__init__(agent_manager)
        self.ai_core = ai_core

    def run(self):
        while True:
            screen_text = self.ai_core.capture_screen_text()
            objects = self.ai_core.detect_objects()
            self.send_message("DecisionAgent", {"text": screen_text, "objects": objects})
            time.sleep(5)
