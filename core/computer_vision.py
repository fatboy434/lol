import pytesseract
import cv2
import numpy as np
from PIL import ImageGrab
import torch
import logging

class ComputerVision:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def capture_screen_text(self):
        """
        Captures the screen and returns the text using OCR.
        """
        try:
            img = ImageGrab.grab()
            img_np = np.array(img)
            gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            return text
        except Exception as e:
            logging.error(f"Error capturing screen text: {e}")
            return ""

    def detect_objects(self):
        """
        Detects objects on the screen using a pre-trained model.
        """
        try:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
            img = ImageGrab.grab()
            results = model(img)
            return results.pandas().xyxy[0]
        except Exception as e:
            logging.error(f"Error detecting objects: {e}")
            return None
