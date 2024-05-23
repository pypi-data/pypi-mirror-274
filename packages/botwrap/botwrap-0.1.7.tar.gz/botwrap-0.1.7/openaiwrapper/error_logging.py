# Path: C:\Users\jamig\OneDrive\Desktop\botwrap\openaiwrapper\error_logging.py

import logging
import functools
from typing import Optional

def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """Setup logger configuration."""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

def log_error_decorator(logger: Optional[logging.Logger] = None):
    """Decorator to automatically log errors when they are raised."""
    if not logger:
        logger = logging.getLogger(__name__)
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as error:
                logger.error(f"Error in {func.__name__}: {error}", exc_info=True)
                raise
        return wrapper
    return decorator
