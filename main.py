import os
import sys
import subprocess
import venv
import time
import socket

class MasterController:
    def __init__(self):
        self.venv_dir = "venv"
        self.requirements_file = "requirements.txt"
        self.main_script = "sentinel_ai_core.py"

    def run(self):
        self.setup_environment()
        self.start_system()

    def setup_environment(self):
        if not os.path.exists(self.venv_dir):
            print("Creating virtual environment...")
            venv.create(self.venv_dir, with_pip=True)
            print("Virtual environment created.")

        if not os.path.exists(self.requirements_file):
            print("Generating requirements.txt...")
            self.generate_requirements()
            print("requirements.txt generated.")

        print("Installing dependencies...")
        self.install_dependencies()
        print("Dependencies installed.")

    def generate_requirements(self):
        # This is a simplified version that just includes the known dependencies.
        # A more robust solution would scan all the files for imports.
        dependencies = [
            "requests",
            "beautifulsoup4",
            "selenium",
            "pvporcupine",
            "pyaudio",
            "nrclex",
            "whisper",
            "pyttsx3",
            "speechrecognition",
            "pytesseract",
            "opencv-python",
            "pillow",
            "keyboard",
            "mouse",
            "numpy",
            "torch",
            "torchvision",
            "tk",
            "python-docx"
        ]
        with open(self.requirements_file, "w") as f:
            for dependency in dependencies:
                f.write(f"{dependency}\n")

    def install_dependencies(self):
        pip_executable = os.path.join(self.venv_dir, "Scripts", "pip") if sys.platform == "win32" else os.path.join(self.venv_dir, "bin", "pip")
        subprocess.check_call([pip_executable, "install", "-r", self.requirements_file])

    def check_port(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    def start_system(self):
        python_executable = os.path.join(self.venv_dir, "Scripts", "python") if sys.platform == "win32" else os.path.join(self.venv_dir, "bin", "python")
        pyinstaller_executable = os.path.join(self.venv_dir, "Scripts", "pyinstaller") if sys.platform == "win32" else os.path.join(self.venv_dir, "bin", "pyinstaller")

        while True:
            try:
                if not self.check_port(1234):
                    print("Waiting for LM Studio to be available...")
                    time.sleep(5)
                    continue

                build_command = [
                    pyinstaller_executable,
                    "--noconfirm",
                    "sentinel.spec",
                ]

                subprocess.check_call(build_command)

                process = subprocess.Popen(["dist/output.exe"])
                process.wait()
            except KeyboardInterrupt:
                print("Shutting down...")
                process.kill()
                break
            except Exception as e:
                self.log_error(str(e))
                print("Restarting system in 5 seconds...")
                time.sleep(5)

    def log_error(self, error):
        with open("error.log", "a") as f:
            f.write(f"[{time.ctime()}] {error}\n")

if __name__ == "__main__":
    controller = MasterController()
    controller.run()
