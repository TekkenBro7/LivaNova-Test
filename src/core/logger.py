import logging
from pathlib import Path

from src.core.config import base_config


def setup_logger(name: str) -> logging.Logger:
    """
    Set up and return a logger instance.

    Args:
        name: The name of the logger (typically __name__)

    Returns:
        Configured logger instance with console and file handlers
    """
    logger = logging.getLogger(name)
    logger.setLevel(base_config.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(base_config.LOG_LEVEL)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    log_file = Path(base_config.LOGS_DIR) / f"{name}.log"
    log_file.parent.mkdir(exist_ok=True)
    fh = logging.FileHandler(log_file)
    fh.setLevel(base_config.LOG_LEVEL)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


logger = setup_logger("logger")
