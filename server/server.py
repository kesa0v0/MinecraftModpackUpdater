from flask import Flask

import os
import json

#####################################################

path_to_folder = os.path.abspath(".\\test\\")
path_to_mods = path_to_folder + "\\mods"
path_to_modslist = path_to_folder + "\\modslist.txt"

#####################################################

def travel_path(path: str) -> dict:
    result = {}
    for root, dirs, files in os.walk(path):
        relative_path = os.path.relpath(root, path)
        result[relative_path] = {
            "dirs": dirs,
            "files": files
        }
    return result

def dict_to_string(data):
  return json.dumps(data, indent=4)

def string_to_dict(data_string):
  return json.loads(data_string)

def generate_modlist(path: str):
    tree = travel_path(path_to_mods)

    with open(path_to_modslist, "w") as f:
        f.write(dict_to_string(tree))




app = Flask(__name__)

@app.route("/") 
def index():
    return "Download Client"

@app.route("/api/modlist") 
def modlist():


    return ""

@app.route("/api/download/<path:modpath>")
def download(modpath: str):

    return ""

if __name__ == "__main__":
    # app.run()
    generate_modlist(path_to_folder)
