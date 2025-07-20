import pyautogui
import keyboard
import time
import random
import numpy as np

class HumanInput:
    def human_like_move(self, x, y):
        """
        Moves the mouse to a destination with human-like motion.
        """
        start_x, start_y = pyautogui.position()
        distance = np.sqrt((x - start_x)**2 + (y - start_y)**2)
        duration = max(0.1, distance / 1000)
        pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeOutQuad)

    def human_like_type(self, text):
        """
        Types text with human-like delays.
        """
        for char in text:
            keyboard.write(char)
            time.sleep(random.uniform(0.05, 0.15))
