import tkinter as tk
from tkinter import ttk
import os
import tkinter.font
import json
from json import JSONEncoder
from pathlib import Path
import sys
from datetime import datetime
import shutil
from ExperimentView import StartExperiment, RestartExperiment, OpenExperimentResults
from Experiment import *

class Experiments():
    """
    Data of experiments
    """
    def __init__(self):
        self.val = 1

class ExperimentsView():
    """
    List of experiments and controls
    """
    def __init__(self, root):
        self.root = root
        self.createExperimentsList(root)
        self.createButtons(root)

    def itemSelected(self, cmd):
        if len(self.expmList.selection()) == 0:
            self.ButtonBasedOn["state"] = "disabled"
            self.ButtonView["state"] = "disabled"
            self.ButtonDel["state"] = "disabled"
        elif len(self.expmList.selection()) == 1:
            self.ButtonBasedOn["state"] = "normal"
            self.ButtonView["state"] = "normal"
            self.ButtonDel["state"] = "normal"
        else:
            self.ButtonBasedOn["state"] = "disabled"
            self.ButtonView["state"] = "disabled"
            self.ButtonDel["state"] = "normal"
    def getExperimentId(self):
        id = 0
        p = os.path.join(curWorkingFolder, "counter.json")
        if os.path.isfile(p):
            with open(p) as j:
                data = json.load(j)
                id = int(data["id"])
        id = id + 1
        obj = {}
        obj["id"] = id
        with open(p, 'w') as outfile:
            json.dump(obj, outfile)
        return id
    def newExperiment(self):
        experimentName = "(not inited)"
        try:
            id = self.getExperimentId()
            experimentName = "Experiment" + str(id).zfill(4)
            StartExperiment(self.root, ExperimentContext(experiments, experimentName, id, os.path.join(curWorkingFolder, experimentName), lambda:StartExperimentsView(self.root)))
        except Exception as err:
            print("Error: {0}".format(err))
            pass
        return 0
    def newBasedOn(self):
        return 0
    def openExperiment(self):
        return 0
    def deleteExperiments(self):
        selected = self.expmList.selection()
        for s in selected:
            shutil.rmtree(experiments[int(s)]["folder"])
            self.expmList.delete(s)
        self.itemSelected(None)
        return 0

    def createExperimentsList(self, root):
        style = ttk.Style()
        self.expmList = ttk.Treeview(root, columns = ("Name", "Data")) #Scrolled
        self.expmList.tag_configure('odd', background="#CCFFFF")
        self.expmList.tag_configure('odd2', background='red')
        self.expmList.column('#0', width=50,  stretch=True)
        self.expmList.column('#1', width=240, stretch=True)
        self.expmList.column('#2', width=150, stretch=True)
        self.expmList.heading('#0', text='Id')
        self.expmList.heading('#1', text='Name')
        self.expmList.heading('#2', text='Data')
        self.expmList.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=0.5)

        i = 0
        for e in experiments:
            if i % 2 == 0:
                self.expmList.insert('', index = 'end', iid = i, text = str(i), values = (e["name"], e["dateText"]), tags = ('odd',))
            else:
                self.expmList.insert('', index = 'end', iid = i, text = str(i), values = (e["name"], e["dateText"]), tags = ('odd2',))
            i = i + 1

        self.expmList.bind("<<TreeviewSelect>>", self.itemSelected)

    def createButtons(self, root):
        self.ButtonNew = tk.Button(root, command = self.newExperiment)
        self.ButtonNew.place(relx=0.51, rely=0.022, height=36, width=150)
        self.ButtonNew.configure(activebackground="#ececec")
        self.ButtonNew.configure(activeforeground="#000000")
        self.ButtonNew.configure(background="#d9d9d9")
        self.ButtonNew.configure(disabledforeground="#a3a3a3")
        self.ButtonNew.configure(foreground="#000000")
        self.ButtonNew.configure(highlightbackground="#d9d9d9")
        self.ButtonNew.configure(highlightcolor="black")
        self.ButtonNew.configure(pady="0")
        self.ButtonNew.configure(text='''New Experiment''')
        
        self.ButtonBasedOn = tk.Button(root, command = self.newBasedOn)
        self.ButtonBasedOn.place(relx=0.51, rely=0.089, height=36, width=150)
        self.ButtonBasedOn.configure(activebackground="#ececec")
        self.ButtonBasedOn.configure(activeforeground="#000000")
        self.ButtonBasedOn.configure(background="#d9d9d9")
        self.ButtonBasedOn.configure(disabledforeground="#a3a3a3")
        self.ButtonBasedOn.configure(foreground="#000000")
        self.ButtonBasedOn.configure(highlightbackground="#d9d9d9")
        self.ButtonBasedOn.configure(highlightcolor="black")
        self.ButtonBasedOn.configure(pady="0")
        self.ButtonBasedOn.configure(text='''Experiment based on''')
        self.ButtonBasedOn["state"] = "disabled"

        self.ButtonView = tk.Button(root, command = self.openExperiment)
        self.ButtonView.place(relx=0.51, rely=0.156, height=36, width=150)
        self.ButtonView.configure(activebackground="#ececec")
        self.ButtonView.configure(activeforeground="#000000")
        self.ButtonView.configure(background="#d9d9d9")
        self.ButtonView.configure(disabledforeground="#a3a3a3")
        self.ButtonView.configure(foreground="#000000")
        self.ButtonView.configure(highlightbackground="#d9d9d9")
        self.ButtonView.configure(highlightcolor="black")
        self.ButtonView.configure(pady="0")
        self.ButtonView.configure(text='''View''')
        self.ButtonView["state"] = "disabled"
        #b1["state"] = "disabled"
        #b2["text"] = "enable"
        #b1["state"] = "normal"
        #b2["text"] = "disable"

        self.ButtonDel = tk.Button(root, command = self.deleteExperiments)
        self.ButtonDel.place(relx=0.51, rely=0.223, height=36, width=150)
        self.ButtonDel.configure(activebackground="#ececec")
        self.ButtonDel.configure(activeforeground="#000000")
        self.ButtonDel.configure(background="#d9d9d9")
        self.ButtonDel.configure(disabledforeground="#a3a3a3")
        self.ButtonDel.configure(foreground="#000000")
        self.ButtonDel.configure(highlightbackground="#d9d9d9")
        self.ButtonDel.configure(highlightcolor="black")
        self.ButtonDel.configure(pady="0")
        self.ButtonDel.configure(text='''Delete''')
        self.ButtonDel["state"] = "disabled"

experiments = []
curWorkingFolder = ""

def LoadExperiments(workingDirectory):
    Path(workingDirectory).mkdir(parents=True, exist_ok=True)
    directories = os.listdir(workingDirectory)
    global curWorkingFolder
    curWorkingFolder = workingDirectory
    print("Working directory: " + workingDirectory)
    for entry in directories:
        try:
            p = os.path.join(workingDirectory, entry)
            if not os.path.isdir(p):
                continue
            print(os.path.join(p, 'id.json'))
            with open(os.path.join(p, 'id.json')) as j:
                data = json.load(j)
                print("Experiment '{}' loaded".format(data["name"]))
                # executeUtility(ctx) contains the same code!
                data["dateText"] = str(datetime.fromtimestamp(data["date"]))
                data["folder"] = p
                experiments.append(data)
        except Exception as err:
            print("Error: {0}".format(err))
            pass
    return experiments

def getClearFrame(root):
    for widget in root.winfo_children():
        widget.destroy()
    return root

def StartExperimentsView(root):
    getClearFrame(root)
    return ExperimentsView(root)

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')
