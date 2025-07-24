import os

class MainFileGenerator:
    def __init__(self, modules, output_dir="dist"):
        self.modules = modules
        self.output_dir = output_dir

    def generate(self):
        with open(os.path.join(self.output_dir, "main.py"), "w") as f:
            f.write("from core.central_dispatcher import CentralDispatcher\n")
            for module in self.modules:
                f.write(f"from modules.{os.path.basename(module)[:-3]} import {self.get_class_name(module)}\n")
            f.write("\n")
            f.write("def main():\n")
            f.write("    dispatcher = CentralDispatcher()\n")
            for module in self.modules:
                class_name = self.get_class_name(module)
                f.write(f"    {class_name.lower()}_agent = {class_name}(dispatcher)\n")
                f.write(f"    dispatcher.register_agent('{class_name}', {class_name.lower()}_agent)\n")
            f.write("    dispatcher.start_agents()\n")
            f.write("\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    main()\n")

    def get_class_name(self, file_path):
        # This is a simplified version that assumes the class name is the same as the file name.
        return os.path.basename(file_path)[:-3].capitalize()
