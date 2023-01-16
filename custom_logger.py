import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def create_logger(name, log_file="archiver.log", max_bytes=1024 * 1024, backup_count=5):
    # Create a logger with the given name
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a rotating file handler for the log file
    file_handler = RotatingFileHandler(
        filename=str(Path("logs", log_file)),
        maxBytes=max_bytes,
        backupCount=backup_count,
    )
    file_handler.setLevel(logging.DEBUG)

    # Create a stream handler for stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    # Create a formatter for the file handler
    # Timestamp - Logger name - Logging level - Message
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
