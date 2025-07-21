from agents.agent_base import AgentBase
import pyautogui

class ActionAgent(AgentBase):
    def __init__(self, agent_manager, ai_core):
        super().__init__(agent_manager)
        self.ai_core = ai_core

    def receive_message(self, message):
        for decision in message:
            action = decision["action"]
            explanation = decision["explanation"]
            self.send_message("SpeechAgent", explanation)

            action_parts = action.split(':')
            action_name = action_parts[0]
            args = action_parts[1:]

            if action_name == "close_app":
                pyautogui.hotkey('alt', 'f4')
            elif action_name == "click_ok":
                pyautogui.click()
            elif action_name == "press_enter":
                pyautogui.press("enter")
            elif action_name == "human_like_type":
                self.ai_core.human_input.human_like_type(args[0])
            else:
                print("No action triggered.")
