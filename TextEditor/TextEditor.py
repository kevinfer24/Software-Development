from functools import partial
from tkinter import *
from tkinter import filedialog
import tkinter
from tkinter.scrolledtext import ScrolledText
from tkinter import font
import pyperclip
from tkinter import messagebox

# App variables
saved = True
currentFilePath = None
currentFileName = "Untitled"

# Utility Variables
fileTypes = [('Text Document', '*.txt'), ('Python Files', '*.py')]

# After something is typed, saved = false
def typed(key):
    global saved
    saved = False

def updateFileName(path):
    global currentFileName
    currentFileName = path.split("/")[-1].split(".")[0]

# Makes new file
def resetFile():
    textfield.delete(1.0, END)
    global saved, currentFilePath, currentFileName
    saved = True
    currentFilePath = None
    currentFileName = "Untitled"

# Menu Item functions
# FILE
def newFile ():
    if saved:
        resetFile()
    else:
        save = messagebox.askyesnocancel(title="Save changes?", message=f"Would you like to save changes to {currentFileName}?")
        # Cancel returns none, no False, yes True
        if save is None: return
        if save:
           saveFile()

        resetFile()

# Assumming the path is known of current file
def saveFile():
    # If the current path is not None
    global currentFilePath
    if currentFilePath is not None:
        with open(currentFilePath, "w") as wFile:
            wFile.truncate(0)
            wFile.write(textfield.get("1.0",END))
            saved = True
    else:
        saveAs()

def saveAs():
    file = filedialog.asksaveasfile(filetypes = fileTypes, defaultextension = fileTypes)
    with open(file.name, "w") as wFile:
        wFile.write(textfield.get("1.0",END))
    global saved, currentFilePath
    saved = True
    updateFileName(file.name)
    currentFilePath = file.name

# Opens file explorer
def browseFiles():
    return filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = fileTypes)
    
def openFile ():
    path = browseFiles()
    if not path == "":
        newFile() # Do this for the whole save if haven't saved sequence
        with open(path, "r") as rFile:
            textfield.insert(1.0, rFile.read())
        global currentFilePath, saved
        updateFileName(path)
        currentFilePath = path
        saved = True

# EDIT
def cutcopypaste(cmd):
    if cmd == "cut": textfield.event_generate("<<Cut>>")
    elif cmd == "copy": pyperclip.copy(textfield.selection_get())
    elif cmd == "paste": textfield.event_generate("<<Paste>>")

    global saved
    if cmd != "copy": saved = False

# CREDITS

def showCredits():
    messagebox.showinfo(title="Credits", message="Developed by: Kevin Fernandez\nContact: kevinjfernandez24@gmail.com")

# Make window
root = Tk()
root.title('Text Editor App')
root.geometry("500x500")
root.resizable(True, True) # Two bools for width and height
root.configure(background='white')

# Menu Items
menubar = Menu(root)

# FILE
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As", command=saveAs)
#filemenu.add_separator()
menubar.add_cascade(label="File", menu=filemenu)

# EDIT
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=partial(cutcopypaste, "cut"))
editmenu.add_command(label="Copy", command=partial(cutcopypaste, "copy"))
editmenu.add_command(label="Paste", command=partial(cutcopypaste, "paste"))
menubar.add_cascade(label="Edit", menu=editmenu)

# CREDITS
credits = Menu(menubar, tearoff=0)
credits.add_command(label="Show Credits", command=showCredits)
menubar.add_cascade(label="Credits", menu=credits)

# Text field
textfield = ScrolledText(root, wrap=tkinter.WORD)
textfield.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)


root.configure(menu=menubar)
root.bind("<KeyPress>", typed)
root.mainloop()
