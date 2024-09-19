import logging
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """Настройка логгера с ротацией файлов по дате."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=30)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

user_logger = setup_logger('user_actions', 'logs/user_actions.log')
error_logger = setup_logger('errors', 'logs/errors.log', level=logging.ERROR)