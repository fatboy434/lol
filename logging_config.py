import logging
import sys

def setup_logging():
    """Set up the logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("sentinel_ai.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )
