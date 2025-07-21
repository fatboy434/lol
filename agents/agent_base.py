import threading

class AgentBase(threading.Thread):
    """
    The base class for all agents.
    """
    def __init__(self, agent_manager):
        super().__init__()
        self.agent_manager = agent_manager

    def run(self):
        """
        The main loop of the agent.
        """
        while True:
            message = self.agent_manager.get_message(self.__class__.__name__)
            if message:
                self.receive_message(message)

    def send_message(self, agent_name, message):
        """
        Sends a message to another agent.
        """
        self.agent_manager.send_message(agent_name, message)

    def receive_message(self, message):
        """
        Receives a message from another agent.
        """
        raise NotImplementedError
