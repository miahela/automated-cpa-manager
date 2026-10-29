import json


def read_json_file(file_name):
    with open(file_name, encoding="utf-8-sig") as f:
        data = json.load(f)
    return data
