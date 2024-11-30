"""Module providing various methods that do io operations"""

import json
import sys


def load_json_from_file(json_path: str) -> dict:
    """Build the filesystem tree from a json file.

    Parameters
    ----------
    json_path: str
        the path of the json file
    """
    json_data = {}
    try:
        with open(json_path, encoding="UTF-8") as json_file:
            json_data = json.load(json_file)
        if "size" not in json_data or "time_modified" not in json_data \
                or "name" not in json_data or "permissions" not in json_data:
            json_data = {}
            raise ValueError
    except ValueError:
        print("The provided json filesystem is invalid", file=sys.stderr)
    except FileNotFoundError:
        print(f"There is no {json_path} file in the current folder",
              file=sys.stderr)
    return json_data
