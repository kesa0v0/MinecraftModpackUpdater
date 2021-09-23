import os
import tkinter
import requests


curr_path = os.getcwd()

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


def loader(path):
    os.mv

def download_mods():
    print(curr_path)
    file_id = '12ro9Oh_hVJYeAEO6t4AJRwRFHn01DKxB'
    destination = curr_path + '\\mods.zip'
    download_file_from_google_drive(file_id, destination)

def read_version():
    pass

minecraft_path = "C:\\Users\\{username}\\AppData\\Roaming\\.minecraft"




# root = tkinter.Tk()
# root.mainloop()