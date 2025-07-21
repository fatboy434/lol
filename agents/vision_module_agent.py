from agents.agent_base import AgentBase
import pytesseract
from PIL import Image
import cv2
import numpy as np
import docx

class VisionModuleAgent(AgentBase):
    def __init__(self, agent_manager):
        super().__init__(agent_manager)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def run(self):
        # This agent is reactive, so it doesn't have a main loop.
        pass

    def receive_message(self, message):
        if message["type"] == "analyze_image":
            text = self.analyze_image(message["path"])
            self.send_message("DecisionAgent", {"type": "image_analysis", "text": text})
        elif message["type"] == "analyze_document":
            text = self.analyze_document(message["path"])
            self.send_message("DecisionAgent", {"type": "document_analysis", "text": text})

    def analyze_image(self, image_path):
        """
        Analyzes an image and returns the text.
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            self.send_message("DebugAgent", {"type": "error", "error": f"Error analyzing image: {e}"})
            return ""

    def analyze_document(self, doc_path):
        """
        Analyzes a document and returns the text.
        """
        try:
            doc = docx.Document(doc_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except Exception as e:
            self.send_message("DebugAgent", {"type": "error", "error": f"Error analyzing document: {e}"})
            return ""
