from agents.agent_base import AgentBase
import speech_recognition as sr
import pyttsx3
import logging
import tkinter as tk
from tkinter import messagebox
import threading

class SpeechAgent(AgentBase):
    def __init__(self, agent_manager):
        super().__init__(agent_manager)
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.voice_only = False

    def run(self):
        """
        The main loop of the agent.
        """
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.daemon = True
        listen_thread.start()
        super().run()

    def listen(self):
        """
        Listens for voice commands and sends them to the DecisionAgent.
        """
        try:
            with sr.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic)
                self.speak("Voice activated. Listening for commands.")
                while True:
                    try:
                        audio = self.recognizer.listen(mic)
                        try:
                            # Try online recognition first
                            command = self.recognizer.recognize_google(audio)
                        except sr.RequestError:
                            # Fallback to offline recognition
                            command = self.recognizer.recognize_whisper(audio)
                        self.speak(f"You said: {command}")
                        self.send_message("EmotionAgent", command)
                        self.send_message("DecisionAgent", {"text": command, "objects": None})
                    except sr.UnknownValueError:
                        self.speak("I didn't catch that.")
        except OSError:
            self.speak("No microphone found. Switching to text mode.", is_error=True)
            while True:
                command = input(">> ").lower()
                self.send_message("EmotionAgent", command)
                self.send_message("DecisionAgent", {"text": command, "objects": None})

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

    def receive_message(self, message):
        if "toggle voice only" in message:
            self.voice_only = not self.voice_only
            if self.voice_only:
                self.speak("Voice-only mode enabled.")
                self.send_message("DashboardAgent", "hide")
            else:
                self.speak("Voice-only mode disabled.")
                self.send_message("DashboardAgent", "show")
        else:
            self.speak(message)
