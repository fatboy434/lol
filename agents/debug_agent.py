from agents.agent_base import AgentBase
import logging
import datetime

class DebugAgent(AgentBase):
    def __init__(self, agent_manager):
        super().__init__(agent_manager)
        self.error_log = "error.log"
        logging.basicConfig(filename=self.error_log, level=logging.ERROR, format='%(asctime)s - %(message)s')

    def run(self):
        # This agent is reactive, so it doesn't have a main loop.
        pass

    def receive_message(self, message):
        if message["type"] == "error":
            self.log_error(message["error"])
            self.report_issue(message["error"])
            self.attempt_fix(message["error"])

    def log_error(self, error):
        """
        Logs an error with a timestamp.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"[{timestamp}] {error}")

    def report_issue(self, error):
        """
        Reports an issue to a log file and verbally.
        """
        self.send_message("SpeechAgent", f"An error occurred: {error}")
        self.send_message("DashboardAgent", {"type": "error", "error": str(error)})

    def attempt_fix(self, error):
        """
        Attempts to fix or bypass an error using backup logic.
        """
        # In a real implementation, this would contain more sophisticated logic.
        # For now, we'll just try to restart the failed agent.
        if "agent" in error:
            self.restart_agent(error["agent"])
        else:
            self.reboot_assistant()

    def restart_agent(self, agent_name):
        """
        Restarts a failed agent.
        """
        self.send_message("SpeechAgent", f"Restarting the {agent_name}.")
        self.agent_manager.restart_agent(agent_name)

    def reboot_assistant(self):
        """
        Reboots the assistant.
        """
        self.send_message("SpeechAgent", "Rebooting the assistant.")
        # In a real implementation, this would restart the application.
        # For now, we'll just exit the application.
        exit()
