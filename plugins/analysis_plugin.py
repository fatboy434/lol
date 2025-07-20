from plugins.plugin_base import PluginBase
import random
import pyautogui

class AnalysisPlugin(PluginBase):
    def __init__(self, ai_core):
        super().__init__(ai_core)

    def get_llm_decision(self, prompt):
        """
        This function will connect to a Large Language Model to get a decision.
        For now, it returns a mock response.
        """
        self.ai_core.speak("Thinking...")
        # In a real implementation, this would be a call to an LLM API.
        # This is a placeholder for the LLM call.
        actions = random.choice([
            ["click_ok"],
            ["close_app"],
            ["press_enter"],
            ["human_like_type:Hello World", "press_enter"]
        ])
        return actions

    def process(self, data):
        """
        Analyzes the screen and acts on the decision from the LLM.
        """
        screen_text = self.ai_core.capture_screen_text()
        objects = self.ai_core.detect_objects()
        prompt = f"Context: {self.ai_core.context}\nScreen text: {screen_text}\nDetected objects: {objects}"
        decisions = self.get_llm_decision(prompt)
        self.ai_core.context.append({"observation": {"text": screen_text, "objects": objects}, "actions": decisions})
        for decision in decisions:
            action, *args = decision.split(':')
            if action == "close_app":
                self.ai_core.speak("I see an error. Closing app.")
                pyautogui.hotkey('alt', 'f4')
            elif action == "click_ok":
                self.ai_core.speak("Clicking OK.")
                pyautogui.click()
            elif action == "press_enter":
                self.ai_core.speak("Installation detected. Pressing enter.")
                pyautogui.press("enter")
            elif action == "human_like_type":
                self.ai_core.human_like_type(args[0])
            else:
                print("No action triggered.")
