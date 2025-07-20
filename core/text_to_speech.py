import pyttsx3
import logging
import tkinter as tk
from tkinter import messagebox

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)

    def speak(self, text, is_error=False):
        """
        Converts text to speech and displays a message box for errors.
        """
        logging.info(f"Speaking: {text}")
        print(f"[AI]: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        if is_error:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Sentinel AI Error", text)
            root.destroy()
