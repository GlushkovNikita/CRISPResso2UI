import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfile
import os
import functools


class CRISPRparams():
    """
    Parameters
    """
    def __init__(self):
        self.sections = [[tk.StringVar(), tk.StringVar(), "", ""]]
    def generateCommand(self):
        return ""

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

def openFastqFile(postfix, sequenceId, sectionId):
    file = askopenfile(mode="r", title='Please select Fastq ' + postfix,
                            filetypes=[('Fastq Files', ['.fq', '.fq.gz', '.fastq', '.fastq.gz'])])
    if not file:
        return None
    # dir_ = os.path.dirname(file.name)
    # filetype = os.path.splitext(file.name)
    # print (dir_, filetype)
    # fastq2.set(os.path.basename(file.name))


def addDelimeter(root, row, text, hintText):
    labelTop = tk.Label(root, width=41, text = "-------  " + text + "  -------", height = 2)
    labelTop.grid(column=0, row=row, columnspan=2)
    if hintText:
        rna_ttp = CreateToolTip(labelTop, hintText)
    row += 1
    return row

def addLabel(root, row, label, longLabel):
    if not longLabel:
        labelTop = tk.Label(root, anchor = tk.W, width=20, text = label)
        labelTop.grid(column=0, row=row)
    else:
        labelTop = tk.Label(root, anchor = tk.W, width=52, text = label)
        labelTop.grid(column=0, row=row, columnspan=3)
        row += 1
    return (row, labelTop)

def addTextEdit(root, row, label, longLabel, hintText):
    row, labelTop = addLabel(root, row, label, longLabel)
    text = tk.Entry(root, width=36)
    text.grid(column=1, row=row, columnspan=2)
    if hintText:
        rna_ttp = CreateToolTip(labelTop, hintText)
        rna_ttp = CreateToolTip(text, hintText)
    row += 1
    return row

def addComboBox(root, row, label, longLabel, comboValues, values, hintText):
    row, labelTop = addLabel(root, row, label, longLabel)

    combo = ttk.Combobox(root, values = comboValues, state="readonly")
    combo.current(values)
    combo.grid(column=1, row=row)
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

def createSequenceDesignSection(root, row, sectionId, sectionsNumber):

    btn = ttk.Button(root, text = '+', command = functools.partial(openFastqFile, "R1", 0, sectionId), width = 2)  
    btn.grid(column=3, row=row, rowspan=4)

    # Fastq files 1
    labelTop = tk.Label(root, anchor = tk.W, width=20, text = "Fastq file R1:")
    labelTop.grid(column=0, row=row)
    labelTop = tk.Label(root, text = "Please, select file", bd = 1, relief=tk.GROOVE, width=20, anchor = tk.W)
    labelTop.grid(column=1, row=row)
    btn = ttk.Button(root, text = 'Browse', command = functools.partial(openFastqFile, "R1", 0, sectionId))  
    btn.grid(column=2, row=row)
    row += 1

    # Fastq files 2
    labelTop = tk.Label(root, anchor = tk.W, width=20, text = "Fastq file R2:")
    labelTop.grid(column=0, row=row)
    fastq2 = tk.StringVar()
    fastq2.set("Please, select file")
    labelTop = tk.Label(root, textvariable = fastq2, bd = 1, relief=tk.GROOVE, width=20, anchor = tk.W)
    labelTop.grid(column=1, row=row)
    btn = ttk.Button(root, text = 'Browse', command = functools.partial(openFastqFile, "R2", 1, sectionId))  
    btn.grid(column=2, row=row)
    row += 1

    # Amplicon
    hintText = """Enter the amplicon sequence. If submitting more than one amplicon, please separate amplicons using commas."""
    row = addTextEdit(root, row, "Amplicon*:", False, hintText)

    # sgRNA
    hintText = """The sgRNA sequence should be provided without the PAM sequence. If the sgRNA is not provided, quantification may include modifications far from the predicted editing site and may result in overestimation of editing rates. Multiple sgRNA sequences may be given separated by commas."""
    row = addTextEdit(root, row, "sgRNA*:", False, hintText)

    return row


def createMainWindow(root):
    row = 0

    # editing tool
    comboValues = [ "Cas9", "Cpfl", "Base editors", "Prime editors", "Custom"]
    row = addComboBox(root, row, "Editing tool:", False, comboValues, 0, None)

    # Sequencing design:
    comboValues = [ "Paired end reads", "Single end reads", "Interleaved reads"]
    row = addComboBox(root, row, "Sequencing design:", False, comboValues, 0, None)

    row = createSequenceDesignSection(root, row, 0, 2)
    # row = createSequenceDesignSection(row, 1, 2)

    # Optional parameters
    row = addDelimeter(root, row, "Optional parameters", None)

    # Sequence Name
    hintText = """Optional suffix to append to the report name. Only alphanumeric characters are allowed."""
    row = addTextEdit(root, row, "Sample Name *:", False, hintText)

    # Amplicon Name
    hintText = """If submitting more than one amplicon, please separate amplicon names using commas."""
    row = addTextEdit(root, row, "Amplicon Name/s:", False, hintText)

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
    row = addDelimeter(root, row, "Base editing *", hintText)

    # pegRNA spacer sequence
    hintText = """The spacer should not include the PAM sequence. The sequence should be given in the RNA 5'->3' order, so for Cas9, the PAM would be on the right side of the given sequence."""
    row = addTextEdit(root, row, "pegRNA spacer sequence*:", False, hintText)

    # pegRNA extension sequence
    hintText = """The sequence should be given in the RNA 5'->3' order, such that the sequence starts with the RT template including the edit, followed by the Primer-binding site (PBS)."""
    row = addTextEdit(root, row, "pegRNA extension sequence*:", True, hintText)

    # pegRNA quantification
    comboValues = [ "1", "5", "10" ]
    hintText = """Quantification window size (in bp) at flap site for measuring modifications anchored at the right side of the extension sequence. Similar to the 'quantification window size' parameter, the total length of the quantification window will be 2x this parameter. Default is 5bp (10bp total window size)."""
    row = addComboBox(root, row, "pegRNA extension quantification window size:", True, comboValues, 2, hintText)

    hintText = """Nicking sgRNA sequence used in prime editing. The sgRNA should not include the PAM sequence. The sequence should be given in the RNA 5'->3' order, so for Cas9, the PAM would be on the right side of the sequence."""
    row = addTextEdit(root, row, "Nicking sgRNA*:", False, hintText)

    hintText = """If given, reads containing any of this scaffold sequence before extension sequence will be classified as 'Scaffold-incorporated'. The sequence should be given in the 5'->3' order such that the RT template directly follows this sequence. A common value is 'GGCACCGAGUCGGUGC'."""
    row = addTextEdit(root, row, "Scaffold sequence*:", False, hintText)
    
    # Quantification window
    row = addDelimeter(root, row, "Quantification window", None)

    comboValues = [ "-15", "-10", "-3", "0", "+1" ]
    hintText = """Only mutations in the quantification window will be used to determine whether a read is modified or unmodified. At least one sgRNA must be provided to use the quantification window."""
    row = addComboBox(root, row, "Center of the quantification window (relative to 3' end of the provided sgRNA):*:", True, comboValues, 2, hintText)
    
    comboValues = [ "No window", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "15", "20", "25", "30" ]
    hintText = """This setting controls the center of the quantification window. Remember that the sgRNA sequence must be entered without the PAM. For cleaving nucleases, this is the predicted cleavage position. The default is -3 and is suitable for the Cas9 system."""
    row = addComboBox(root, row, "Quantification window size (bp)*:", False, comboValues, 1, hintText)

    row = addDelimeter(root, row, "HDR", None)
    row = addTextEdit(root, row, "Expected HDR amplicon sequence:", True, hintText)
    row = addDelimeter(root, row, "Exon specification", None)
    row = addTextEdit(root, row, "Coding Sequence/s:", False, hintText)
    row = addDelimeter(root, row, "Quality filtering and trimming", None)

    comboValues = [ "No Filter", ">10", ">20", ">30", ">35" ]
    row = addComboBox(root, row, "Minimum average read quality (phred33 scale):", True, comboValues, 0, None)
    comboValues = [ "No Filter", ">10", ">20", ">30", ">35" ]
    row = addComboBox(root, row, "Minimum single bp quality (phred33 scale):", True, comboValues, 0, None)
    comboValues = [ "No Filter", "<10", "<20", "<30", "<35" ]
    row = addComboBox(root, row, "Replace bases with N that have a quality lower than (phred33 scale):", True, comboValues, 0, None)
    comboValues = [ "Disabled", "5", "10", "15", "20", "40", "50" ]
    row = addComboBox(root, row, "Exclude bp from the left side of the amplicon sequence for the quantification of the mutations:", True, comboValues, 0, None)
    comboValues = [ "Disabled", "5", "10", "15", "20", "40", "50" ]
    row = addComboBox(root, row, "Exclude bp from the right side of the amplicon sequence for the quantification of the mutations:", True, comboValues, 0, None)
    comboValues = [ "No Trimming", "Nextera PE", "TruSeq3 PE", "TruSeq3 SE", "TruSeq2 PE", "TruSeq2 SE" ]
    row = addComboBox(root, row, "Trimming adapter: ", False, comboValues, 0, None)


    # Process
    btn = ttk.Button(root, text = 'Process', command = openFastqFile)  
    btn.grid(column=0, row=row, columnspan = 3)
    row += 1

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.pack(side=tk.LEFT, fill="y", expand = 1)
        # self.grid_rowconfigure(0, weight=1) # this needed to be added
        # self.grid_columnconfigure(0, weight=1) # as did this

        canvas = tk.Canvas(self)
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


app = tk.Tk()

params = CRISPRparams()

s = ttk.Style()
s.theme_use("xpnative")
# s = ttk.Style()
# sequencingDesignValues = s.theme_names()

app.geometry('600x800')
app.title("CRISPResso2")
frame = ScrollableFrame(app)

createMainWindow(frame.scrollable_frame)

frame.pack()
app.mainloop()
