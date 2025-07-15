import unittest
import os
import json
from unittest.mock import patch, MagicMock

# Set a dummy DISPLAY variable for headless environments
if "DISPLAY" not in os.environ:
    os.environ["DISPLAY"] = ":0"

import assistant

class TestAssistant(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_file.txt"
        assistant.SAFE_MODE = False

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists("error_log.txt"):
            os.remove("error_log.txt")

    def test_create_file(self):
        content = "test content"
        cmd = {"action": "create_file", "data": {"path": self.test_file, "content": content}}
        assistant.run_command(cmd)
        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, "r") as f:
            self.assertEqual(f.read(), content)

    @patch('assistant.requests.post')
    @patch('assistant.Image.open')
    def test_analyze_invalid_json(self, mock_image_open, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": [{"text": "invalid json"}]}
        mock_post.return_value = mock_response

        with patch('assistant.pytesseract.image_to_string', return_value=""):
            assistant.analyze("dummy_path")

        self.assertTrue(os.path.exists("error_log.txt"))
        with open("error_log.txt", "r") as f:
            self.assertIn("Invalid JSON from AI", f.read())

    @patch('assistant.pyautogui')
    def test_continuous_operation(self, mock_pyautogui):
        assistant.running = False
        with patch('assistant.take_screenshot'), patch('assistant.time.sleep'):
            assistant.start()
            self.assertTrue(assistant.running)
            assistant.stop()
            self.assertFalse(assistant.running)

if __name__ == '__main__':
    unittest.main()
