import tkinter as tk
from tkinter import ttk

class Dashboard:
    def __init__(self, root, ai_core, dispatcher):
        self.root = root
        self.ai_core = ai_core
        self.dispatcher = dispatcher
        self.root.title("Sentinel AI Dashboard")

        # Create the main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create the logs text area
        logs_frame = ttk.LabelFrame(main_frame, text="Logs")
        logs_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.logs_text = tk.Text(logs_frame, wrap=tk.WORD, width=80, height=20)
        self.logs_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create the module controls frame
        module_controls_frame = ttk.LabelFrame(main_frame, text="Module Controls")
        module_controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create the bot activation frame
        bot_activation_frame = ttk.LabelFrame(main_frame, text="Bot Activation")
        bot_activation_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create the status information frame
        status_info_frame = ttk.LabelFrame(main_frame, text="Status Information")
        status_info_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.ocr_status_label = ttk.Label(status_info_frame, text="OCR: N/A")
        self.ocr_status_label.grid(row=0, column=0, sticky=tk.W)
        self.voice_status_label = ttk.Label(status_info_frame, text="Voice: N/A")
        self.voice_status_label.grid(row=0, column=1, sticky=tk.W)

        # Create the active tasks frame
        active_tasks_frame = ttk.LabelFrame(main_frame, text="Active Tasks")
        active_tasks_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.active_tasks_listbox = tk.Listbox(active_tasks_frame, width=80, height=10)
        self.active_tasks_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create the error console frame
        error_console_frame = ttk.LabelFrame(main_frame, text="Error Console")
        error_console_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.error_text = tk.Text(error_console_frame, wrap=tk.WORD, width=80, height=10, fg="red")
        self.error_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.recover_button = ttk.Button(error_console_frame, text="Recover", command=self.recover)
        self.recover_button.grid(row=1, column=0, sticky=tk.E)

    def update_logs(self, message):
        self.logs_text.insert(tk.END, message + "\n")
        self.logs_text.see(tk.END)

    def update_status(self, ocr_status, voice_status):
        self.ocr_status_label.config(text=f"OCR: {ocr_status}")
        self.voice_status_label.config(text=f"Voice: {voice_status}")

    def update_active_tasks(self, tasks):
        self.active_tasks_listbox.delete(0, tk.END)
        for task in tasks:
            self.active_tasks_listbox.insert(tk.END, task)

    def update_errors(self, error):
        self.error_text.insert(tk.END, error + "\n")
        self.error_text.see(tk.END)

    def recover(self):
        self.ai_core.dispatcher.send_message("DebugAgent", {"type": "recover"})
