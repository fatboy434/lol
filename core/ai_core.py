import requests
import time
import pyautogui
import logging
from core.text_to_speech import TextToSpeech
from core.human_input import HumanInput
from core.computer_vision import ComputerVision
from core.voice_input import VoiceInput

class AICore:
    def __init__(self):
        self.tts = TextToSpeech()
        self.human_input = HumanInput()
        self.cv = ComputerVision()
        self.voice_input = VoiceInput(self)

    def speak(self, text, is_error=False):
        self.tts.speak(text, is_error)

    def human_like_move(self, x, y):
        self.human_input.human_like_move(x, y)

    def human_like_type(self, text):
        self.human_input.human_like_type(text)

    def capture_screen_text(self):
        return self.cv.capture_screen_text()

    def detect_objects(self):
        return self.cv.detect_objects()

    def voice_command_loop(self):
        self.voice_input.voice_command_loop()

    def fallback_text_command(self):
        self.voice_input.fallback_text_command()

    def process_command(self, command):
        # This will be handled by the plugin manager
        pass

    def connect_to_lm_studios(self, url="http://localhost:1234"):
        """
        Connects to a localhost server with retry logic.
        """
        self.speak("Connecting to LM Studios...")
        while True:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    self.speak("Connected to LM Studios.")
                    break
            except requests.exceptions.ConnectionError:
                self.speak("Connection failed. Retrying in 5 seconds...", is_error=True)
                time.sleep(5)

    def main_loop(self):
        """
        The main loop of the AI assistant.
        """
        pyautogui.FAILSAFE = True
        while True:
            try:
                # This will be handled by a plugin
                time.sleep(1)
            except pyautogui.FailSafeException:
                self.speak("Failsafe triggered. Pausing for 10 seconds.")
                logging.warning("Failsafe triggered.")
                time.sleep(10)
            except Exception as e:
                logging.error(f"An error occurred in the main loop: {e}", exc_info=True)
                self.speak("An error occurred. See the log for details.", is_error=True)
                time.sleep(10)
