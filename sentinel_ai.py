from core.ai_core import AICore
from core.plugin_manager import PluginManager
from logging_config import setup_logging
import logging
import threading

def main():
    """
    The main function of the AI assistant.
    """
    setup_logging()
    logging.info("Sentinel AI Online.")
    ai_core = AICore()
    plugin_manager = PluginManager(ai_core)
    plugin_manager.load_plugins()
    ai_core.process_command = plugin_manager.process_command

    ai_core.connect_to_lm_studios()
    main_thread = threading.Thread(target=ai_core.main_loop, daemon=True)
    main_thread.start()
    ai_core.voice_command_loop()

if __name__ == "__main__":
    main()
