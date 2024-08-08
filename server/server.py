from flask import Flask

import os

#####################################################

path_to_folder = "./test/"

#####################################################

app = Flask(__name__)

@app.route('/') 
def index():
    return "Download Client"

@app.route('/api/modlist') 
def modlist():

    os.path(path_to_folder)

    return ""

@app.route('/api/download')
def download():

    return ""

if __name__ == '__main__':
    app.run()