import os
from pathlib import Path

from functions.read_json_file import read_json_file

ROOT = Path(__file__).resolve().parents[1]


def load_config():
    path = Path(os.environ.get("CPA_CONFIG", ROOT / "config.json"))
    config = read_json_file(path)
    for key in ("sheet_credentials", "cookies", "local_storage",
                "website_credentials", "xpath_config", "landing_pages"):
        if config.get(key):
            config[key] = str((path.resolve().parent / config[key]).resolve())
    return config
