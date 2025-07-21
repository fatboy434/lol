from agents.agent_base import AgentBase
from core.action_parser import ActionParser
import random
import requests
import json

class DecisionAgent(AgentBase):
    def __init__(self, agent_manager, ai_core):
        super().__init__(agent_manager)
        self.ai_core = ai_core
        self.action_parser = ActionParser()
        self.load_personality()

    def get_llm_decision(self, prompt):
        """
        Connects to the local LLM to get a decision.
        """
        self.ai_core.speak("Thinking...")
        endpoints = [
            "http://192.168.100.131:1234/v1/chat/completions",
            "http://192.168.100.131:1234/v1/completions",  # Fallback endpoint
        ]
        for endpoint in endpoints:
            try:
                response = requests.post(
                    endpoint,
                    json={
                        "model": "microsoft/phi-4-reasoning-plus",
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.7,
                        "max_tokens": 200,
                    },
                )
                if response.status_code == 404:
                    continue  # Try the next endpoint
                response.raise_for_status()
                # The response from the LLM is expected to be a JSON object
                # with a list of actions and explanations.
                return self.action_parser.parse(response.json()["choices"][0]["message"]["content"])
            except requests.exceptions.RequestException as e:
                self.ai_core.speak(f"Error getting LLM decision: {e}", is_error=True)
        return []

    def load_personality(self):
        """
        Loads the personality profile from the personality.json file.
        """
        with open("personality.json", "r") as f:
            self.personality = json.load(f)

    def receive_message(self, message):
        if message.get("type") == "short_term_response":
            self.handle_short_term_response(message)
        elif message.get("type") == "long_term_response":
            self.handle_long_term_response(message)
        elif "emotion" in message:
            self.emotion = message["emotion"]
        elif message.get("type") == "image_analysis" or message.get("type") == "document_analysis":
            self.handle_visual_analysis(message)
        else:
            self.send_message("MemoryAgent", {"type": "get_short_term", "key": "last_action", "sender": "DecisionAgent"})
            self.pending_message = message

    def handle_visual_analysis(self, message):
        prompt = f"Visual analysis: {message['text']}"
        decisions = self.get_llm_decision(prompt)
        self.ai_core.context.append({"observation": message, "actions": decisions})
        self.send_message("ActionAgent", decisions)

    def handle_short_term_response(self, message):
        self.last_action = message["value"]
        self.send_message("MemoryAgent", {"type": "get_long_term", "key": "user_preferences", "sender": "DecisionAgent"})

    def handle_long_term_response(self, message):
        user_preferences = message["value"]
        prompt = f"Emotion: {self.emotion}\nPersonality: {self.personality}\nShort-term memory: {self.last_action}\nLong-term memory: {user_preferences}\nContext: {self.ai_core.context}\nScreen text: {self.pending_message['text']}\nDetected objects: {self.pending_message['objects']}"
        decisions = self.get_llm_decision(prompt)
        self.ai_core.context.append({"observation": self.pending_message, "actions": decisions})
        self.send_message("MemoryAgent", {"type": "set_short_term", "key": "last_action", "value": decisions})
        self.send_message("ActionAgent", decisions)
