import cv2
import numpy as np
import pyautogui
import os
import logging
import tkinter as tk
from tkinter import filedialog
from PIL import Image

class PCCommander:
    def __init__(self):
        self.templates_dir = "templates"
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger("PCCommander")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("pc_commander.log")
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def log(self, message):
        self.logger.info(message)
        print(message)

if __name__ == "__main__":
    commander = PCCommander()
