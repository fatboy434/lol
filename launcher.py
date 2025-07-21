import tkinter as tk
from tkinter import ttk
import os
import sys
import subprocess
import json
import threading
import winreg

class LauncherController:
    def __init__(self, launcher):
        self.launcher = launcher
        self.processes = {}
        self.config = self.load_config()
        self.launcher.create_status_lights(self.config.keys())

    def load_config(self):
        with open("launcher_config.json", "r") as f:
            return json.load(f)

    def start_all(self):
        for module_name, module_config in self.config.items():
            self.start_module(module_name, module_config)

    def start_module(self, module_name, module_config):
        if module_name not in self.processes:
            python_executable = os.path.join("venv", "Scripts", "python") if sys.platform == "win32" else os.path.join("venv", "bin", "python")
            log_file = os.path.join("logs", f"{module_name}.log")
            with open(log_file, "w") as f:
                process = subprocess.Popen([python_executable, module_config["path"]], stdout=f, stderr=f)
            self.processes[module_name] = process
            self.launcher.update_status_light(module_name, "running")

    def stop_all(self):
        for module_name in self.processes:
            self.stop_module(module_name)

    def stop_module(self, module_name):
        if module_name in self.processes:
            self.processes[module_name].kill()
            del self.processes[module_name]
            self.launcher.update_status_light(module_name, "stopped")

    def restart_system(self):
        self.stop_all()
        self.start_all()

    def view_logs(self):
        # This is a placeholder. In a real implementation, this would open a log viewer.
        print("Viewing logs...")

    def sync_modules(self):
        # This is a placeholder. In a real implementation, this would sync the modules.
        print("Syncing modules...")

    def add_to_startup(self):
        key = winreg.HKEY_CURRENT_USER
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, sub_key, 0, winreg.KEY_SET_VALUE) as registry_key:
            winreg.SetValueEx(registry_key, "SentinelAI", 0, winreg.REG_SZ, sys.executable)
        print("Added to startup.")

    def remove_from_startup(self):
        key = winreg.HKEY_CURRENT_USER
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, sub_key, 0, winreg.KEY_SET_VALUE) as registry_key:
            winreg.DeleteValue(registry_key, "SentinelAI")
        print("Removed from startup.")

class Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Sentinel AI Launcher")
        self.controller = LauncherController(self)

        # Create the main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create the module status frame
        module_status_frame = ttk.LabelFrame(main_frame, text="Module Status")
        module_status_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.module_status_lights = {}

        # Create the control buttons frame
        control_buttons_frame = ttk.LabelFrame(main_frame, text="Controls")
        control_buttons_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.start_all_button = ttk.Button(control_buttons_frame, text="Start All", command=self.controller.start_all)
        self.start_all_button.grid(row=0, column=0)
        self.stop_all_button = ttk.Button(control_buttons_frame, text="Stop All", command=self.controller.stop_all)
        self.stop_all_button.grid(row=0, column=1)
        self.restart_system_button = ttk.Button(control_buttons_frame, text="Restart System", command=self.controller.restart_system)
        self.restart_system_button.grid(row=0, column=2)
        self.view_logs_button = ttk.Button(control_buttons_frame, text="View Logs", command=self.controller.view_logs)
        self.view_logs_button.grid(row=0, column=3)
        self.sync_modules_button = ttk.Button(control_buttons_frame, text="Sync Modules", command=self.controller.sync_modules)
        self.sync_modules_button.grid(row=0, column=4)
        self.add_to_startup_button = ttk.Button(control_buttons_frame, text="Add to Startup", command=self.controller.add_to_startup)
        self.add_to_startup_button.grid(row=1, column=0)
        self.remove_from_startup_button = ttk.Button(control_buttons_frame, text="Remove from Startup", command=self.controller.remove_from_startup)
        self.remove_from_startup_button.grid(row=1, column=1)

    def create_status_lights(self, modules):
        for i, module_name in enumerate(modules):
            label = ttk.Label(self.module_status_frame, text=module_name)
            label.grid(row=i, column=0, sticky=tk.W)
            canvas = tk.Canvas(self.module_status_frame, width=20, height=20)
            canvas.grid(row=i, column=1, sticky=tk.W)
            status_light = canvas.create_oval(5, 5, 15, 15, fill="red")
            self.module_status_lights[module_name] = status_light

    def update_status_light(self, module_name, status):
        color = "green" if status == "running" else "red"
        self.module_status_frame.itemconfig(self.module_status_lights[module_name], fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = Launcher(root)
    root.mainloop()
