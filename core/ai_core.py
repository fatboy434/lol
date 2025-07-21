from core.human_input import HumanInput
from core.computer_vision import ComputerVision

class AICore:
    def __init__(self):
        self.human_input = HumanInput()
        self.cv = ComputerVision()
        self.context = []
        self.dashboard = None

    def human_like_move(self, x, y):
        self.human_input.human_like_move(x, y)

    def human_like_type(self, text):
        self.human_input.human_like_type(text)

    def capture_screen_text(self):
        return self.cv.capture_screen_text()

    def detect_objects(self):
        return self.cv.detect_objects()
