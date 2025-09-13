"""Logging utilities."""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str, log_file: Optional[Path] = None, level: int = logging.INFO
) -> logging.Logger:
    """Set up logger with console and optional file output."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(console_format)
        logger.addHandler(file_handler)

    return logger
