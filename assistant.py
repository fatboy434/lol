import os, time, threading, traceback, json
from datetime import datetime
from tkinter import Tk, Button, Label, messagebox
import pyautogui, requests, pytesseract
from PIL import Image

# 📁 Create screenshot folder
screenshot_folder = "screenshots"
os.makedirs(screenshot_folder, exist_ok=True)

# ⚙️ User preferences
USE_OCR = True            # Set to False if you prefer manual input
SAFE_MODE = True          # If True, ask before executing
AI_MODEL = "mistral:instruct-v0.3"

# 📷 Capture screenshot
def take_screenshot():
    try:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"{screenshot_folder}/screenshot_{ts}.png"
        img = pyautogui.screenshot()
        img.save(path)
        status_label.config(text=f"Saved: {path}")
        threading.Thread(target=lambda: analyze(path)).start()
    except Exception as e:
        log_error(str(e))

# 🧠 Analyze with Mistral Instruct
def analyze(image_path):
    try:
        if USE_OCR:
            text = pytesseract.image_to_string(Image.open(image_path))
        else:
            text = input("Describe the screenshot: ")

        prompt = f"""Based on this text from a screenshot:
\"\"\"{text}\"\"\"
What action should I take? Return JSON {{"action": "...", "data": "..."}}"""
        resp = requests.post("http://localhost:11434/api/generate",
                             json={"model": AI_MODEL, "prompt": prompt})
        out = resp.json()["choices"][0]["text"]
        try:
            cmd = json.loads(out.strip())
            run_command(cmd)
        except json.JSONDecodeError:
            log_error(f"Invalid JSON from AI: {out}")
    except Exception as e:
        log_error(str(e))

# 🛠️ Run the AI command
def run_command(cmd):
    try:
        if SAFE_MODE:
            if not messagebox.askyesno("AI Command", f"Execute?\n{cmd}"):
                return
        a = cmd["action"]; d = cmd["data"]
        if a == "type": pyautogui.typewrite(d)
        elif a == "click": pyautogui.click(*d)
        elif a == "move": pyautogui.moveTo(*d)
        elif a == "open_file": os.startfile(d)
        elif a == "create_file":
            path = d.get("path")
            content = d.get("content", "")
            dirname = os.path.dirname(path)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            with open(path, "w") as f: f.write(content)
        else:
            print("Unknown action:", cmd)
    except Exception as e:
        log_error(str(e))

# 📝 Error logging
def log_error(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_label.config(text=f"❌ {msg}")
    with open("error_log.txt", "a") as f:
        f.write(f"[{ts}] {msg}\n{traceback.format_exc()}\n")

# 🚫 Stop the assistant
running = False

def start():
    global running
    running = True
    status_label.config(text="Running...")
    threading.Thread(target=run_continuously).start()

def stop():
    global running
    running = False
    status_label.config(text="Stopped")

def run_continuously():
    while running:
        take_screenshot()
        time.sleep(5) # Wait 5 seconds between screenshots

# 🖼️ GUI Setup
root = Tk(); root.title("🤖 AI Screenshot Assistant")
Button(root, text="🚀 Start", command=start, height=2, width=25).pack(pady=5)
Button(root, text="🛑 Stop", command=stop, height=2, width=25).pack(pady=5)
status_label = Label(root, text="Ready"); status_label.pack(pady=5)

if __name__ == "__main__":
    root.mainloop()
