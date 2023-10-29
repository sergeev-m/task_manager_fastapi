import logging
import os

from logging import Logger, handlers

from src.core.config.settings import settings, LOG_PATH


def get_log() -> Logger:
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)

    log_file = os.path.join(LOG_PATH, settings.LOG_FILENAME)

    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s'
    )
    file_handler = handlers.RotatingFileHandler(
        log_file, maxBytes=50000000, backupCount=5
    )
    file_handler.setLevel(logging.WARN)
    file_handler.setFormatter(file_formatter)

    console_formatter = logging.Formatter(
        '%(levelname)s -- %(filename)s -- %(message)s'
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    return logger


log = get_log()
