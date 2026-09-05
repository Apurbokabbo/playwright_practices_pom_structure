import logging
from datetime import datetime
from pathlib import Path


from config.base_config import BaseConfig


def setup_logger(name: str , level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger


    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_path = Path(BaseConfig.LOGS_DIR)
    log_path.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_path / f"{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

