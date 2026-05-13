import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(name: str) -> logging.Logger:
    """
    Setup a logger that writes detailed logs to a file in the 'logs' folder,
    and shorter, meaningful logs to the terminal.
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times if logger is already set up
    if logger.handlers:
        return logger

    # Set base level to DEBUG to catch everything
    logger.setLevel(logging.DEBUG)

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    # 1. File Handler (detailed, rotating)
    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # 2. Console Handler (short, meaningful)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    # Shorter format for terminal
    console_formatter = logging.Formatter(
        "[%(levelname)s] %(name)s: %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Do not propagate to root logger to avoid duplicate prints in Streamlit
    logger.propagate = False
    
    return logger
