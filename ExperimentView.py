import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfile
import os
import functools
import tkinter.font
import json
from json import JSONEncoder

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 280   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#fafafa", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

def openFastqFile(postfix, sectionId):
    file = askopenfile(mode="r", title='Please select Fastq ' + postfix,
                            filetypes=[('Fastq Files', ['.fq', '.fq.gz', '.fastq', '.fastq.gz'])])
    if not file:
        return None
    global params
    if postfix == "R1":
        params.sequences[sectionId].fastq1.set(os.path.basename(file.name))
        params.sequences[sectionId].fastq1.path = file.name
    else:
        params.sequences[sectionId].fastq2.set(os.path.basename(file.name))
        params.sequences[sectionId].fastq2.path = file.name
    # dir_ = os.path.dirname(file.name)
    # filetype = os.path.splitext(file.name)
    # print (dir_, filetype)
    # fastq2.set(os.path.basename(file.name))
    return file.name

def addDelimeter(root, row, text, hintText):
    labelTop = tk.Label(root, anchor = tk.W, text = text + ":", height = 1, bg='lavender')
    labelTop.grid(column=0, row=row, columnspan=2, sticky=tk.NSEW)
    if hintText:
        rna_ttp = CreateToolTip(labelTop, hintText)
    row += 1
    return row

# def addDelimeter(root, row, text, hintText):
#     labelTop = tk.Label(root, width=41, text = "-------  " + text + "  -------", height = 2)
#     labelTop.grid(column=0, row=row, columnspan=2)
#     if hintText:
#         rna_ttp = CreateToolTip(labelTop, hintText)
#     row += 1
#     return row

def addLabel(root, row, label, longLabel, narrow = False):
    if not longLabel:
        labelTop = tk.Label(root, anchor = tk.W, text = label)
        labelTop.grid(column=0, row=row, sticky=tk.EW)
    else:
        labelTop = tk.Label(root, anchor = tk.W, justify = tk.LEFT, text = label, wraplength=280)
        labelTop.grid(column=0, row=row, sticky=tk.EW)
    return (row, labelTop)

def addTextEdit(root, row, label, longLabel, value, hintText, narrow = False):
    row, labelTop = addLabel(root, row, label, longLabel, narrow)
    text = tk.Entry(root, textvariable = value)
    text.grid(column=1, row=row, columnspan=2, sticky=tk.EW)
    if hintText:
        rna_ttp = CreateToolTip(labelTop, hintText)
        rna_ttp = CreateToolTip(text, hintText)
    row += 1
    return row

def addComboBox(root, row, label, longLabel, comboValues, values, hintText, narrow = False):
    row, labelTop = addLabel(root, row, label, longLabel, narrow)

    combo = ttk.Combobox(root, values = comboValues, state="readonly")
    combo.current(values)
    combo.grid(column=1, row=row, sticky=tk.W)
    if hintText:
        rna_ttp = CreateToolTip(labelTop, hintText)
        rna_ttp = CreateToolTip(combo, hintText)
    row += 1
    return row

def addCheckBox(root, row, label, longLabel, value, hintText):
    row, labelTop = addLabel(root, row, label, longLabel)

    checkbutton = tk.Checkbutton(root, text="", variable=value, width = 1)
    checkbutton.grid(column=1, row=row, sticky=tk.W)

    if hintText:
        rna_ttp = CreateToolTip(labelTop, hintText)
        rna_ttp = CreateToolTip(checkbutton, hintText)
    row += 1
    return row

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.pack(side=tk.LEFT, fill="y", expand = 1)
        # self.grid_rowconfigure(0, weight=1) # this needed to be added
        # self.grid_columnconfigure(0, weight=1) # as did this

        canvas = tk.Canvas(self)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # self.scrollable_frame.grid(column=0, row=0, sticky = "nsew")
        # self.scrollable_frame.grid_rowconfigure(0, weight = 1)
        # self.scrollable_frame.grid_columnconfigure(0, weight = 1)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def createSequenceDesignSection(root, row, sequence, sectionId, sectionsNumber):
    global params

    btn = tk.Button(root, text = '+', command = lambda: print("test"), height = 6, width = 1)  
    btn.grid(column=3, row=row, rowspan=4, padx = 4, sticky=tk.W)

    # Fastq files 1
    row, labelTop = addLabel(root, row, "Fastq file R1:", False, True)
    labelTop = tk.Label(root, textvariable = sequence.fastq1, bd = 1, relief=tk.GROOVE, anchor = tk.W)
    labelTop.grid(column=1, row=row, sticky="EW")
    btn = ttk.Button(root, text = 'Browse', command = functools.partial(openFastqFile, "R1", sectionId), width=8)  
    btn.grid(column=2, row=row, sticky=tk.EW)
    row += 1

    # Fastq files 2
    row, labelTop = addLabel(root, row, "Fastq file R2:", False, True)
    labelTop = tk.Label(root, textvariable = sequence.fastq2, bd = 1, relief=tk.GROOVE, anchor = tk.W)
    labelTop.grid(column=1, row=row, sticky="EW")
    btn = ttk.Button(root, text = 'Browse', command = functools.partial(openFastqFile, "R2", sectionId), width=8)  
    btn.grid(column=2, row=row, sticky=tk.EW)
    row += 1

    # Amplicon
    hintText = """Enter the amplicon sequence. If submitting more than one amplicon, please separate amplicons using commas."""
    row = addTextEdit(root, row, "Amplicon*:", False, sequence.amplicon, hintText, True)

    # sgRNA
    hintText = """The sgRNA sequence should be provided without the PAM sequence. If the sgRNA is not provided, quantification may include modifications far from the predicted editing site and may result in overestimation of editing rates. Multiple sgRNA sequences may be given separated by commas."""
    row = addTextEdit(root, row, "sgRNA*:", False, sequence.sgRNA, hintText, True)

    return row

def createLeftPanel(root):
    global params
    row = 0
    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=100)
    root.columnconfigure(2, weight=0)
    root.columnconfigure(3, weight=0)
    # Sequence Name
    hintText = """Optional suffix to append to the report name. Only alphanumeric characters are allowed."""
    row = addTextEdit(root, row, "Sample Name *:", False, params.sequenceName, hintText, True)

    # Amplicon Name
    hintText = """If submitting more than one amplicon, please separate amplicon names using commas."""
    row = addTextEdit(root, row, "Amplicon Name/s*:", False, params.ampliconNames, hintText, True)

    # editing tool
    comboValues = [ "Cas9", "Cpfl", "Base editors", "Prime editors", "Custom"]
    row = addComboBox(root, row, "Editing tool:", False, comboValues, 0, None, True)

    # Sequencing design:
    comboValues = [ "Paired end reads", "Single end reads", "Interleaved reads"]
    row = addComboBox(root, row, "Sequencing design:", False, comboValues, 0, None, True)

    for i in range(0, len(params.sequences)):
        row = createSequenceDesignSection(root, row, params.sequences[i], i, len(params.sequences))
    # row = createSequenceDesignSection(row, 1, 2)

    # Process
    def onProcess():
        print(params.toJSON())
        params.fromJSON(params.toJSON())
    btn = ttk.Button(root, text = 'Process', command = onProcess)  
    btn.grid(column=0, row=row, columnspan = 3)
    row += 1

def createMiddlePanel(root, row = 0):
    global params
    # Optional parameters
    # row = addDelimeter(root, row, "Optional parameters", None)

    # Minimum homology
    comboValues = [ "50%", "60%", "70%", "80%", "90%", "100%" ]
    hintText = """When reads are aligned to each reference amplicon, they must share this percentage of bases in common."""
    row = addComboBox(root, row, "Minimum homology for alignment to an amplicon *:", True, comboValues, 1, hintText)

    # Base editing
    row = addDelimeter(root, row, "Base editing", None)

    # Base editor output
    hintText = """Check this box to produce plots and tables detailing substitution rates for each base."""
    row = addCheckBox(root, row, "Base editor output *:", False, False, hintText)

    # Base editor target base 
    comboValues = [ "A", "C", "T", "G" ]
    hintText = """The is the pre-edited base. E.g. for C->T editors, this should be set to "C"."""
    row = addComboBox(root, row, "Base editor target base *:", False, comboValues, 1, hintText)

    # Base editor result base
    comboValues = [ "A", "C", "T", "G" ]
    hintText = """The is the post-edited base. E.g. for C->T editors, this should be set to "T"."""
    row = addComboBox(root, row, "Base editor result base *:", False, comboValues, 2, hintText)

    # Prime editing
    hintText = """For prime editing experiments, provide the unmodified reference sequence in the 'Amplicon' input above. pegRNA and other prime editing components are input below."""
    row = addDelimeter(root, row, "Prime editing *", hintText)

    # pegRNA spacer sequence
    hintText = """The spacer should not include the PAM sequence. The sequence should be given in the RNA 5'->3' order, so for Cas9, the PAM would be on the right side of the given sequence."""
    row = addTextEdit(root, row, "pegRNA spacer sequence*:", False, params.pegRNAspacer, hintText)

    # pegRNA extension sequence
    hintText = """The sequence should be given in the RNA 5'->3' order, such that the sequence starts with the RT template including the edit, followed by the Primer-binding site (PBS)."""
    row = addTextEdit(root, row, "pegRNA extension sequence*:", True, params.pegRNAextension, hintText)

    # pegRNA quantification
    comboValues = [ "1", "5", "10" ]
    hintText = """Quantification window size (in bp) at flap site for measuring modifications anchored at the right side of the extension sequence. Similar to the 'quantification window size' parameter, the total length of the quantification window will be 2x this parameter. Default is 5bp (10bp total window size)."""
    row = addComboBox(root, row, "pegRNA extension quantification window size:", True, comboValues, 2, hintText)

    hintText = """Nicking sgRNA sequence used in prime editing. The sgRNA should not include the PAM sequence. The sequence should be given in the RNA 5'->3' order, so for Cas9, the PAM would be on the right side of the sequence."""
    row = addTextEdit(root, row, "Nicking sgRNA*:", False, params.nickingSgRNA, hintText)

    hintText = """If given, reads containing any of this scaffold sequence before extension sequence will be classified as 'Scaffold-incorporated'. The sequence should be given in the 5'->3' order such that the RT template directly follows this sequence. A common value is 'GGCACCGAGUCGGUGC'."""
    row = addTextEdit(root, row, "Scaffold sequence*:", False, params.scaffoldSequence, hintText)
    
    # Quantification window
    row = addDelimeter(root, row, "Quantification window", None)
    return row

def createRightPanel(root, row = 0):
    global params
    comboValues = [ "-15", "-10", "-3", "0", "+1" ]
    hintText = """Only mutations in the quantification window will be used to determine whether a read is modified or unmodified. At least one sgRNA must be provided to use the quantification window."""
    row = addComboBox(root, row, "Center of the quantification window (relative to 3' end of the provided sgRNA):*:", True, comboValues, 2, hintText)
    
    comboValues = [ "No window", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "15", "20", "25", "30" ]
    hintText = """This setting controls the center of the quantification window. Remember that the sgRNA sequence must be entered without the PAM. For cleaving nucleases, this is the predicted cleavage position. The default is -3 and is suitable for the Cas9 system."""
    row = addComboBox(root, row, "Quantification window size (bp)*:", False, comboValues, 1, hintText)

    row = addDelimeter(root, row, "HDR", None)
    row = addTextEdit(root, row, "Expected HDR amplicon sequence:", True, params.expectedHDRamplicon, hintText)
    row = addDelimeter(root, row, "Exon specification", None)
    row = addTextEdit(root, row, "Coding Sequence/s:", False, params.codingSequence, hintText)
    row = addDelimeter(root, row, "Quality filtering and trimming", None)

    comboValues = [ "No Filter", ">10", ">20", ">30", ">35" ]
    row = addComboBox(root, row, "Minimum average read quality (phred33 scale):", True, comboValues, 0, None)
    comboValues = [ "No Filter", ">10", ">20", ">30", ">35" ]
    row = addComboBox(root, row, "Minimum single bp quality (phred33 scale):", True, comboValues, 0, None)
    comboValues = [ "No Filter", "<10", "<20", "<30", "<35" ]
    row = addComboBox(root, row, "Replace bases with N that have a quality lower than (phred33 scale):", True, comboValues, 0, None)
    comboValues = [ "Disabled", "5", "10", "15", "20", "40", "50" ]
    row = addComboBox(root, row, "Exclude bp from the left side of the amplicon sequence for the quantification of the mutations:", True, comboValues, 3, None)
    comboValues = [ "Disabled", "5", "10", "15", "20", "40", "50" ]
    row = addComboBox(root, row, "Exclude bp from the right side of the amplicon sequence for the quantification of the mutations:", True, comboValues, 3, None)
    comboValues = [ "No Trimming", "Nextera PE", "TruSeq3 PE", "TruSeq3 SE", "TruSeq2 PE", "TruSeq2 SE" ]
    row = addComboBox(root, row, "Trimming adapter: ", False, comboValues, 0, None)
    return row

def createExperiment():
    global params
    params = Experiment()

