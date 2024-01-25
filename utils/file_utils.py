import os
import re
import json


def load_prompt(prompt):
    return load_text(f"prompts/{prompt}.txt")


def load_text(path, by_lines=False):
    with open(path, "r") as fp:
        if by_lines:
            return fp.readlines()
        else:
            return fp.read()


def load_json(path):
    return json.load(open(path, "r"))


def loads_json(s):
    return json.loads(s)


def dump_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def dumps_json(data, indent=4):
    return json.dumps(data, indent=indent, ensure_ascii=False)


def create_folder(path, folder_name):
    folder_path = os.path.join(path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def find_ratings(s):
    return re.findall(r'\b[1-5]\b', s)