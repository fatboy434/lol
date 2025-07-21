from agents.agent_base import AgentBase
from nrclex import NRCLex

class EmotionAgent(AgentBase):
    def __init__(self, agent_manager):
        super().__init__(agent_manager)

    def receive_message(self, message):
        emotion = self.detect_emotion(message)
        self.send_message("DecisionAgent", {"emotion": emotion})

    def detect_emotion(self, text):
        """
        Detects the emotion from the given text.
        """
        emotion = NRCLex(text)
        return emotion.top_emotions[0][0]
