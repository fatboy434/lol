from core.central_dispatcher import CentralDispatcher
from agents.screen_analysis_agent import ScreenAnalysisAgent
from agents.decision_agent import DecisionAgent
from agents.action_agent import ActionAgent
from agents.speech_agent import SpeechAgent
from agents.memory_agent import MemoryAgent
from agents.profit_seeker_agent import ProfitSeekerAgent
from agents.dashboard_agent import DashboardAgent
from agents.dashboard_agent import DashboardAgent
from agents.debug_agent import DebugAgent
from agents.emotion_agent import EmotionAgent
from agents.routine_agent import RoutineAgent
from agents.web_agent import WebAgent
from agents.training_agent import TrainingAgent
from agents.vision_module_agent import VisionModuleAgent
from core.ai_core import AICore
from logging_config import setup_logging
import logging
import tkinter as tk
from core.dashboard import Dashboard
import threading
import requests
import time

def main():
    """
    The main function of the AI assistant.
    """
    setup_logging()
    logging.info("Sentinel AI Online.")

    ai_core = AICore()
    dispatcher = CentralDispatcher()

    screen_analysis_agent = ScreenAnalysisAgent(dispatcher, ai_core)
    decision_agent = DecisionAgent(dispatcher, ai_core)
    action_agent = ActionAgent(dispatcher, ai_core)
    speech_agent = SpeechAgent(dispatcher)
    memory_agent = MemoryAgent(dispatcher)
    profit_seeker_agent = ProfitSeekerAgent(dispatcher, ai_core)
    dashboard_agent = DashboardAgent(dispatcher, ai_core)
    debug_agent = DebugAgent(dispatcher)
    emotion_agent = EmotionAgent(dispatcher)
    routine_agent = RoutineAgent(dispatcher)
    web_agent = WebAgent(dispatcher)
    training_agent = TrainingAgent(dispatcher)
    vision_module_agent = VisionModuleAgent(dispatcher)

    dispatcher.register_agent("ScreenAnalysisAgent", screen_analysis_agent)
    logging.info("ScreenAnalysisAgent registered.")
    dispatcher.register_agent("DecisionAgent", decision_agent)
    logging.info("DecisionAgent registered.")
    dispatcher.register_agent("ActionAgent", action_agent)
    logging.info("ActionAgent registered.")
    dispatcher.register_agent("SpeechAgent", speech_agent)
    logging.info("SpeechAgent registered.")
    dispatcher.register_agent("MemoryAgent", memory_agent)
    logging.info("MemoryAgent registered.")
    dispatcher.register_agent("ProfitSeekerAgent", profit_seeker_agent)
    logging.info("ProfitSeekerAgent registered.")
    dispatcher.register_agent("DashboardAgent", dashboard_agent)
    logging.info("DashboardAgent registered.")
    dispatcher.register_agent("DebugAgent", debug_agent)
    logging.info("DebugAgent registered.")
    dispatcher.register_agent("EmotionAgent", emotion_agent)
    logging.info("EmotionAgent registered.")
    dispatcher.register_agent("RoutineAgent", routine_agent)
    logging.info("RoutineAgent registered.")
    dispatcher.register_agent("WebAgent", web_agent)
    logging.info("WebAgent registered.")
    dispatcher.register_agent("TrainingAgent", training_agent)
    logging.info("TrainingAgent registered.")
    dispatcher.register_agent("VisionModuleAgent", vision_module_agent)
    logging.info("VisionModuleAgent registered.")

    dispatcher.start_agents()
    logging.info("All agents started.")

    # Create the dashboard
    root = tk.Tk()
    dashboard = Dashboard(root, ai_core, dispatcher)
    ai_core.dashboard = dashboard

    # Start the dashboard in a new thread
    dashboard_thread = threading.Thread(target=root.mainloop)
    dashboard_thread.start()

    # Connect to the local LLM
    speech_agent.speak("Connecting to LM Studios...")
    while True:
        try:
            response = requests.get("http://192.168.100.131:1234")
            if response.status_code == 200:
                speech_agent.speak("Connected to LM Studios.")
                break
        except requests.exceptions.ConnectionError as e:
            dispatcher.send_message("DebugAgent", {"type": "error", "error": e})
            time.sleep(5)

    # Keep the main thread alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
