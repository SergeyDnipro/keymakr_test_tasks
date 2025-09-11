import logging
import os
import json
from pathlib import Path
from functools import wraps


def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.info(f"{result}")
        except json.JSONDecodeError as e:
            logger.error(f"[JSON Decode Error] {str(e).splitlines()[0]}")
        except Exception as e:
            logger.error(f"[ERROR] {str(e).splitlines()[0]}")
    return wrapper


BASE_DIR = Path(__file__).parent.parent
os.makedirs(f"{BASE_DIR}/data/", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False

file_handler = logging.FileHandler(f"{BASE_DIR}/data/fetch_api.log")
file_handler.setFormatter(logging.Formatter(
    "[%(asctime)s][%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
))

if not logger.handlers:
    logger.addHandler(file_handler)
