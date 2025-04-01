import logging
import os

logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(logs_dir, "game.log")),
    ],
)


def get_logger(name):
    """Get a logger with the specified name."""
    return logging.getLogger(name)
