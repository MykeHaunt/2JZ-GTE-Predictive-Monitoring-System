import logging
from logging.handlers import RotatingFileHandler
import config
import os

def setup_logger():
    log_dir = os.path.dirname(config.Config.LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("2JZ-GTE-Monitor")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(config.Config.LOG_FILE, maxBytes=1000000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger