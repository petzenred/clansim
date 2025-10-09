
import json
import os
import shutil
from pprint import pprint
from typing import Union

import yaml

FILES = "files"
CODES = "codes" # "%{color}" -> <CAT/main/pelt_colour>
json_files = {
    "resources": {
        "lang": {
            "en": {
                "cat": {
                    FILES: ["accessories", "backstories", "eyes", "history", "eyes"]
                }
            }
        }
    }
}

def _write_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        # success = f.write(json.dump(data, f))
        json.dump(data, f)
        f.flush()
        os.fsync(f.fileno())
        return True

def _read_json(filepath) -> dict:
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    else:
        print(f"Can't read from file because it doesn't exist")

def _write_yaml(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        success = f.write(yaml.dump(data))
        f.flush()
        os.fsync(f.fileno())
        return success

def _read_yaml(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f.read())

def build_filepaths(contents: dict, path: str ) -> list:
    print("Running build_filepaths()")
    for c in contents.keys():
        if c != FILES:
            return build_filepaths(contents = contents[c], path=str(path + c + '/'))
        else:
            result = []
            for f in contents[FILES]:
                result.append(path + f)
            return result

def alphabetize_complex_dictionary(contents):
    print("Running alphabetize_complex_dictionary()")
    if isinstance(contents, dict):
        for c in contents.keys():
            contents[c] = alphabetize_complex_dictionary(contents=contents[c])
    elif isinstance(contents, list):
        contents.sort()
    return contents

def convert_all_json_files():
    print("Running convert_all_json_files()")
    filepaths: list = build_filepaths(contents=json_files, path="")
    for base_path in filepaths:
        json_file_path = base_path + ".en.json"
        yaml_file_path = base_path + ".en.yaml"
    # TODO conversion stuff here
    # TODO don't need to specify "en" in path as well as file name, so take it out of path before writing the YAML file

def make_flavour_text():
    print("Running make_flavour_text()")
    # flavour.en.yaml - Flavour text strings for cats.
    en_personalities = _read_json("resources/lang/en/cat/personality.en.json")
    personalities = en_personalities["en"]
    for key in personalities.keys():
        personalities[key] = None
    return _write_yaml(filepath="resources/lang/en/_Red/flavour.en.yaml", data=personalities)

def alphabetize_names():
    print("Running alphabetize_names()")
    readpath = "resources/dicts/names/names.json"
    writepath = "resources/lang/en/cat/cat_names.en.yaml"
    names: dict = _read_json(readpath)
    sorted_names: dict = alphabetize_complex_dictionary(contents = names)
    _write_yaml(writepath, sorted_names)

def move_pelts():
    print("Running move_pelts()")
    readpath = "resources/lang/en/cat/pelts.en.json"
    writepath = "resources/lang/en/cat/pelt.en.yaml"
    pelts = _read_json(readpath)
    sorted_pelts = alphabetize_complex_dictionary(pelts)
    _write_yaml(writepath, sorted_pelts)

def move_moon_events():
    print("Running move_moon_events()")
    readpath = "saves/Test/events.json"
    writepath = "saves/Test/last_moon_events.yaml"
    events = _read_json(readpath)
    _write_yaml(filepath=writepath, data=events)

def conditions():
    print("Running conditions()")
    yaml_filepaths = ("resources/_red/dicts/conditions.yaml", "resources/_red/dicts/condition_risks.yaml")
    json_filepaths = ("resources/_red/dicts/conditions.json", "resources/_red/dicts/condition_risks.json")

    for n in range(len(yaml_filepaths)):
        _write_json(filepath=json_filepaths[n], data=_read_yaml(yaml_filepaths[n]))

# Run this method
print(f"But nothing happened!")