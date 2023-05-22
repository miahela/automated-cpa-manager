import json
import logging


def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
    )


def read_json_file(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data
