from agents.agent_base import AgentBase
import logging

class TrainingAgent(AgentBase):
    def __init__(self, agent_manager):
        super().__init__(agent_manager)
        self.feedback_log = "feedback.log"
        logging.basicConfig(filename=self.feedback_log, level=logging.INFO, format='%(asctime)s - %(message)s')

    def run(self):
        # This agent is reactive, so it doesn't have a main loop.
        pass

    def receive_message(self, message):
        if message["type"] == "feedback":
            self.log_feedback(message["feedback"])

    def log_feedback(self, feedback):
        """
        Logs the user's feedback.
        """
        logging.info(feedback)
