"""Logging configuration for the application."""

import logging
import sys
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Logger name (typically __name__). Defaults to root logger.
        
    Returns:
        Logger instance.
    """
    return logging.getLogger(name or __name__)

