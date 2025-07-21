import queue
import threading

class CentralDispatcher:
    def __init__(self):
        self.agents = {}
        self.message_queues = {}
        self.lock = threading.Lock()

    def register_agent(self, agent_name, agent_instance):
        """
        Registers an agent with the central dispatcher.
        """
        with self.lock:
            self.agents[agent_name] = agent_instance
            self.message_queues[agent_name] = queue.Queue()

    def start_agents(self):
        """
        Starts all registered agents.
        """
        for agent in self.agents.values():
            agent.start()

    def send_message(self, agent_name, message):
        """
        Sends a message to a specific agent.
        """
        if agent_name in self.message_queues:
            self.message_queues[agent_name].put(message)
        else:
            print(f"Agent '{agent_name}' not found.")

    def get_message(self, agent_name):
        """
        Gets a message from an agent's message queue.
        """
        if agent_name in self.message_queues:
            return self.message_queues[agent_name].get()
        else:
            print(f"Agent '{agent_name}' not found.")
            return None

    def restart_agent(self, agent_name):
        """
        Restarts a failed agent.
        """
        if agent_name in self.agents:
            self.agents[agent_name].join()
            self.agents[agent_name].start()
        else:
            print(f"Agent '{agent_name}' not found.")
