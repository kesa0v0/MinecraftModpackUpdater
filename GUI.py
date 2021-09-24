
import tkinter
from tkinter import filedialog
import getpass


class GUI(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)

        self.initialize()

    def initialize(self):
        self.minecraft_mod_path = tkinter.StringVar()

        tkinter.Label(self, text="Insert Minecraft Path(.minecraft folder): ").pack()
        self.pathlabel = tkinter.Entry(self, textvariable=self.minecraft_mod_path, width=75)
        self.pathlabel.pack()
        tkinter.Button(self, text = "Browse", command = self.ask_file_location, width = 10).pack()
        tkinter.Button(self, text = "DO IT!", command= self.do_download, width = 10).pack()

        self.minecraft_mod_path.set("")
        
    def ask_file_location(self):
        self.minecraft_mod_path.set(filedialog.askdirectory())
    
    def do_download(self):
        import updater


if __name__ == "__main__":
    gui = GUI()
    gui.title = "Updater"
    gui.mainloop()
