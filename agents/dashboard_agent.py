from agents.agent_base import AgentBase
import tkinter as tk
from core.dashboard import Dashboard

class DashboardAgent(AgentBase):
    def __init__(self, agent_manager, ai_core):
        super().__init__(agent_manager)
        self.ai_core = ai_core
        self.root = tk.Tk()
        self.dashboard = Dashboard(self.root, self.ai_core)
        self.ai_core.dashboard = self.dashboard

    def run(self):
        self.root.mainloop()

    def receive_message(self, message):
        if isinstance(message, dict) and message.get("type") == "error":
            self.dashboard.update_errors(message["error"])
        elif message == "hide":
            self.root.withdraw()
        elif message == "show":
            self.root.deiconify()
