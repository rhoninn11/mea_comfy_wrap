import os
import shutil

def ensure_path_exist(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def proj_asset(name):
    prompt_src = f"assets/{name}"
    prompt_dst = f"fs/{name}"
    ensure_path_exist("fs")
    if not os.path.exists(prompt_dst):
        if not os.path.exists(prompt_src):
            raise FileExistsError()
        shutil.copy(prompt_src, prompt_dst)

    return prompt_dst

import json

def file2json2obj(json_file):
    data = None
    with open(json_file, 'r', encoding='utf-8') as j_file:
        json_content = j_file.read()
        data = json.loads(json_content)
    return data
