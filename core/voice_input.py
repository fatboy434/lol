import speech_recognition as sr
import logging

class VoiceInput:
    def __init__(self, ai_core):
        self.ai_core = ai_core
        self.recognizer = sr.Recognizer()

    def voice_command_loop(self):
        """
        Listens for voice commands and processes them.
        """
        try:
            with sr.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic)
                self.ai_core.speak("Voice activated. Listening for commands.")
                while True:
                    try:
                        audio = self.recognizer.listen(mic)
                        command = self.recognizer.recognize_google(audio)
                        self.ai_core.speak(f"You said: {command}")
                        self.ai_core.process_command(command.lower())
                    except sr.UnknownValueError:
                        self.ai_core.speak("I didn't catch that.")
                    except sr.RequestError as e:
                        self.ai_core.speak(f"Could not request results from Google Speech Recognition service; {e}", is_error=True)
        except OSError:
            self.ai_core.speak("No microphone found. Switching to text mode.", is_error=True)
            self.fallback_text_command()

    def fallback_text_command(self):
        """
        Provides a text-based command prompt as a fallback.
        """
        while True:
            command = input(">> ").lower()
            self.ai_core.process_command(command)
