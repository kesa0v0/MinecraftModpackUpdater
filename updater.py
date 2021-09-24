import os
import shutil
import zipfile
import pprint


from GoogleDownload import download_file_from_google_drive


def move_files(path, files):
    print("moving files: ")
    pprint.pprint(files)

    makedirs(path)
    for file in files:
        print(file)
        shutil.move(curr_path + '/files/mods/' + file, path+file)

def download_mods():
    print("downloading  mods...")
    file_id = '12ro9Oh_hVJYeAEO6t4AJRwRFHn01DKxB'
    destination = curr_path + '/files/mods.zip'
    download_file_from_google_drive(file_id, destination)

def download_version_file():
    print("downloading  version files...")
    file_id = '1u5mgk1uuEh5jfq-KdsJIJ6ZaJ3SriN00'
    destination = curr_path + '/files/version.txt'
    download_file_from_google_drive(file_id, destination)

def read_version(minecraft_mod_path):
    print("reading version...")
    download_version_file()
    current_version = ""
    with open(minecraft_mod_path + "version.txt", "r") as f:
        current_version = f.read()
    with open(curr_path + "/files/version.txt", "r") as f:
        new_version = f.read()
    
    if current_version == new_version:
        print("same version!")
        return False
    else:
        print("new version is available")
        return True

def makedirs(path): 
   try: 
        os.makedirs(path) 
   except OSError: 
       if not os.path.isdir(path): 
           raise

def unzip():
    print("unzipping")
    with zipfile.ZipFile(curr_path+"/files/mods.zip", 'r') as zip_ref:
        zip_ref.extractall(curr_path+"/files")
    
    os.remove(curr_path+"/files/mods.zip")

def update(minecraft_mod_path):
    print("updating...")
    download_mods()
    unzip()
    move_files(minecraft_mod_path, [file for file in os.listdir(curr_path+"/files/mods/")])
    shutil.move(curr_path + '/files/version.txt', minecraft_mod_path+"/version.txt")


def loader(minecraft_mod_path):
    print("start loading")
    if os.path.isfile(minecraft_mod_path + 'version.txt'):
        if read_version(minecraft_mod_path):
            print("update start...")
            shutil.rmtree(minecraft_mod_path)
            
            update(minecraft_mod_path)
        else:
            print("no need to update")
    else: # new downloader
        print("new downloader")
        download_version_file()
        update(minecraft_mod_path)


import tkinter
from tkinter import filedialog


curr_path = os.getcwd()


class GUI(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)

        self.initialize()

    def initialize(self):
        self.minecraft_mod_path = tkinter.StringVar()

        tkinter.Label(self, text="Insert Minecraft Path(.minecraft folder): ").pack()

        self.pathlabel = tkinter.Entry(self, textvariable=self.minecraft_mod_path, width=75)
        self.pathlabel.pack()

        self.loading = tkinter.Label(self, text="")
        self.loading.pack()

        tkinter.Button(self, text = "Browse", command = self.ask_file_location, width = 10).pack()
        tkinter.Button(self, text = "DO IT!", command= self.do_download, width = 10).pack()

        self.minecraft_mod_path.set("")
        
    def ask_file_location(self):
        self.minecraft_mod_path.set(filedialog.askdirectory() + '/')
    
    def do_download(self):
        self.loading.config(text="loading...")
        self.loading.update_idletasks()
        minecraft_mod_path = self.minecraft_mod_path.get() + 'mods/'
        makedirs(curr_path + '/files')
        print(minecraft_mod_path)

        loader(minecraft_mod_path)
        self.loading.config(text="done!")


if __name__ == "__main__":
    gui = GUI()
    gui.title = "Updater"
    gui.mainloop()



