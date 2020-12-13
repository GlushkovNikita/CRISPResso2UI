import tkinter as tk
from tkinter import ttk
import os
import tkinter.font
from ExperimentsView import LoadExperiments, StartExperimentsView
from ExperimentView import StartExperimentView

def createMenu(root):
    menu = tk.Menu(root)
    app.config(menu=menu)

    fileMenu = tk.Menu(menu, tearoff=0)
    fileMenu.delete(0)
    fileMenu.add_command(label="Item")
    menu.add_cascade(label="File", menu=fileMenu)

    editMenu = tk.Menu(menu, tearoff=0)
    editMenu.delete(0)
    editMenu.add_command(label="Undo")
    editMenu.add_command(label="Redo")
    menu.add_cascade(label="Edit", menu=editMenu)

def createWindow():
    global app
    app = tk.Tk()

    # Set Style
    s = ttk.Style()
    s.theme_use("xpnative")

    def_font = tk.font.nametofont("TkDefaultFont")
    def_font.configure(size=11)
    app.option_add("*Font", def_font)
    # s = ttk.Style()
    # sequencingDesignValues = s.theme_names()
    app.geometry("934x603+273+53")
    app.minsize(120, 1)
    app.maxsize(1540, 845)
    app.resizable(1,  1)
    app.title("CRISPResso2UI")
    app.configure(highlightbackground="#d9d9d9")
    app.configure(highlightcolor="black")
    createMenu(app)
    app.experimentsView = LoadExperiments(os.path.join("Experiments"))
    #StartExperimentsView(app)
    StartExperimentView(app, "Test", "Experiments\Experiment0025", lambda:StartExperimentsView(app))
    app.mainloop()

createWindow()