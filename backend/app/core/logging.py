"""Structured logging configuration."""
import logging
import sys
from typing import Optional


def setup_logging(level: int = logging.INFO) -> None:
    """Configure application-wide logging."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name or __name__)

