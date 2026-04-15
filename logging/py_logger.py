import logging
import sys
from copy import copy
from logging.handlers import RotatingFileHandler
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "data"

# ANSI escape codes for colors
BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RESET = '\033[0m'

LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(name)s - %(funcName)s(%(lineno)d) - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# example costume color
# logger.info("check_list: Done!", extra={'custom_color': True})

class ColorFormatter(logging.Formatter):
    """Formatter that colors level and message in console."""

    def format(self, record):
        record_copy = copy(record)

        color = ''
        if getattr(record_copy, 'custom_color', False):
            if record_copy.levelno == logging.INFO:
                color = GREEN
            elif record_copy.levelno == logging.DEBUG:
                color = BLUE
        else:
            if record_copy.levelno == logging.WARNING:
                color = YELLOW
            elif record_copy.levelno in (logging.ERROR, logging.CRITICAL):
                color = RED

        if color:
            record_copy.msg = f'{color}{record_copy.getMessage()}{RESET}'
            record_copy.levelname = f'{color}{record_copy.levelname}{RESET}'
            record_copy.args = ()

        return super().format(record_copy)


def get_logger(name: str,logs_dir: str | Path = LOGS_DIR,
               log_file: str = "logs.log",) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # Якщо логер вже мав хендлери — прибираємо їх коректно
    if logger.handlers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()

    logs_dir = Path(logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)
    final_log_path = logs_dir / Path(log_file).name

    file_handler = RotatingFileHandler(
        final_log_path,
        maxBytes=1_000_000,   # ~1 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(ColorFormatter(LOG_FORMAT, datefmt=DATE_FORMAT))

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger