import os
import shutil

class ProjectOrganizer:
    def __init__(self, files, output_dir="dist"):
        self.files = files
        self.output_dir = output_dir

    def organize(self):
        self.create_project_structure()
        self.move_files()

    def create_project_structure(self):
        os.makedirs(os.path.join(self.output_dir, "modules"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "core"), exist_ok=True)

    def move_files(self):
        for file_path in self.files:
            if "main" in file_path.lower() or "launcher" in file_path.lower():
                shutil.copy(file_path, self.output_dir)
            else:
                shutil.copy(file_path, os.path.join(self.output_dir, "modules"))
