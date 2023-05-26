import logging


def setup_logger():
    # Set up logger
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)  # Set level to INFO

    # Create formatters
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # Create handlers
    info_file_handler = logging.FileHandler("info.log")
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)

    error_file_handler = logging.FileHandler("error.log")
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(info_file_handler)
    logger.addHandler(error_file_handler)

    return logger
