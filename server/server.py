from flask import Flask, send_from_directory

import os
import json

#####################################################

path_to_folder = os.path.abspath(".\\test\\")
path_to_mods = path_to_folder + "\\mods"
path_to_configs = path_to_folder + "\\config"
path_to_modslist = path_to_folder + "\\modslist.txt"
path_to_configslist = path_to_folder + "\\configslist.txt"

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

def string_to_dict(data_string) -> dict:
  return json.loads(data_string)

def generate_modlist():
    tree = travel_path(path_to_mods)

    with open(path_to_modslist, "w") as f:
        f.write(dict_to_string(tree))

def generate_configlist():
    tree =travel_path(path_to_configs)

    with open(path_to_configslist, "w") as f:
        f.write(dict_to_string(tree))



app = Flask(__name__)
modslist: str
configlist: str

@app.route("/") 
def index():
    return "Download Client"

@app.route("/api/modslist") 
def modlist():
    return modslist

@app.route("/api/configslist")
def configlist():
    return configlist

@app.route("/api/download/<path:modpath>")
def download(modpath: str):
    return send_from_directory(path_to_folder, modpath)


if __name__ == "__main__":
    generate_modlist()
    generate_configlist()
    with open(path_to_modslist, "r") as f:
        modslist = f.read()
    with open(path_to_configslist, "r") as f:
        configlist = f.read()

    app.run()
