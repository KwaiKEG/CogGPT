import os
import csv
import json
import pandas as pd


def load_prompt(prompt):
    return load_text(f"prompts/{prompt}.txt")


def load_operations(operarion):
    return load_json(f"operations/{operarion}.json")


def load_text(path, by_lines=False):
    with open(path, "r") as fp:
        if by_lines:
            return fp.readlines()
        else:
            return fp.read()
        
        
def load_json(path):
    return json.load(open(path, "r"))
        
        
def load_csv(path):
    return csv.reader(open(path, 'r'))


def load_xlsx(path):
    return pd.read_excel(path)


def loads_json(s):
    return json.loads(s)
        
        
def json_dump(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    
def json_dumps(data, indent=4):
    return json.dumps(data, indent=indent, ensure_ascii=False)


def create_folder(path, folder_name):
    folder_path = os.path.join(path, folder_name)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)