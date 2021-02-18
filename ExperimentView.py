import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfile
from tkinter import messagebox
import os
import functools
import tkinter.font
import json
from json import JSONEncoder
from Experiment import *
import datetime
import subprocess as sb
import webbrowser
import logging
import sys
import copy

#from test._mock_backport import inplace
logging.basicConfig(level=logging.INFO,
                     format='%(message)s \n',
                     stream=sys.stderr,
                     filemode="w"
                     )
error   = logging.critical
warn    = logging.warning
debug   = logging.debug
info    = logging.info

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
    # warn (dir_, filetype)
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

def addComboBox(root, row, label, longLabel, comboValues, value, hintText, narrow = False):
    row, labelTop = addLabel(root, row, label, longLabel, narrow)

    combo = ttk.Combobox(root, values = comboValues, state="readonly")
    combo.current(value.get())
    def onSelected(obj):
        index = 0
        for v in comboValues:
            if v == obj.widget.get():
                value.set(index)
                break
            index = index + 1
    combo.bind("<<ComboboxSelected>>", onSelected)
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

def createSequenceDesignSection(root, row, sequence, sectionId, sectionsNumber):
    global params

    btn = tk.Button(root, text = '+', command = lambda: warn("test"), height = 6, width = 1)  
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

def generateCmd(ctx, params):
    info("Current directory is: " + os.getcwd())
    cmd = ctx.CRISPRessoPath
    #CRISPResso -r1 r1.gz -r2 r2.gz -a <amp> -g <sgRNA> -e <Expected HDR amplicon sequence>
    #[-r1 FASTQ_R1] [-r2 FASTQ_R2]
    if len(params.sequences) == 1:
        seq = params.sequences[0]
        fastq_found = False;
        if os.path.isfile(seq.fastq1.path):
            cmd = cmd + " -r1 " + seq.fastq1.path
            fastq_found = True
        if os.path.isfile(seq.fastq2.path):
            cmd = cmd + " -r2 " + seq.fastq2.path
            fastq_found = True
        if not fastq_found:
            return None, "Fastq1 or Fastq2 not found"
           
        #[-a AMPLICON_SEQ] [-an AMPLICON_NAME]
        if len(seq.amplicon.get()) == 0:
            return None, "Amplicon is empty"
        cmd = cmd + " -a " + seq.amplicon.get()
        #[-g GUIDE_SEQ]
        if len(seq.sgRNA.get()) == 0:
            return None, "sgRNA is empty"
        cmd = cmd + " -g " + seq.sgRNA.get()
    else:
        return None, "Only one sequence has been supported"
    if params.ampliconNames.get() != "":
        cmd = cmd + " -an " + params.ampliconNames.get()
    #[-amas AMPLICON_MIN_ALIGNMENT_SCORE]
    cmd = cmd + " -amas " + params.minimumHomologyValues[params.minimumHomology.get()]
    #-gn -fg -fgn ignored
    #-fh: flexiguides will yield guides in amplicons with at least this homology to the flexiguide sequence???
    #--discard_guide_positions_overhanging_amplicon_edge ignored
    #[-e EXPECTED_HDR_AMPLICON_SEQ]
    if params.expectedHDRamplicon.get() != "":
        cmd = cmd + " -e " + params.expectedHDRamplicon.get()
    #[-c CODING_SEQ]
    if params.codingSequence.get() != "":
        cmd = cmd + " -c " + params.codingSequence.get()
    #[-q MIN_AVERAGE_READ_QUALITY]
    cmd = cmd + " -q " + params.minimumAverageReadQualityValues[params.minimumAverageReadQuality.get()]
    #[-s MIN_SINGLE_BP_QUALITY]
    cmd = cmd + " -s " + params.minimumSingleQualityValues[params.minimumSingleQuality.get()]
    #[--min_bp_quality_or_N MIN_BP_QUALITY_OR_N]
    cmd = cmd + " --min_bp_quality_or_N " + params.replaceBasesNValues[params.replaceBasesN.get()]
    #[-n NAME]
    cmd = cmd + " -n " + params.sequenceName.get()
    #[-o OUTPUT_FOLDER]
    cmd = cmd + " -o " + ctx.workingDirectory
    #--flash_command FLASH_COMMAND
    #--min_paired_end_reads_overlap MIN_PAIRED_END_READS_OVERLAP
    #                      Parameter for the FLASH read merging step. Minimum
    #                      required overlap length between two reads to provide a
    #                      confident overlap. (default: 10)
    #--max_paired_end_reads_overlap MAX_PAIRED_END_READS_OVERLAP
    #                      Parameter for the FLASH merging step. Maximum overlap
    #                      length expected in approximately 90% of read pairs.
    #                      Please see the FLASH manual for more information.
    #                      (default: 100)
    #--stringent_flash_merging
    #                      Use stringent parameters for flash merging. In the
    #                      case where flash could merge R1 and R2 reads
    #                      ambiguously, the expected overlap is calculated as
    #                      2*average_read_length - amplicon_length. The flash
    #                      parameters for --min-overlap and --max-overlap will be
    #                      set to prefer merged reads with length within 10bp of
    #                      the expected overlap. These values override the
    #                      --min_paired_end_reads_overlap or
    #                      --max_paired_end_reads_overlap CRISPResso parameters.
    #                      (default: False)

    #[-w QUANTIFICATION_WINDOW_SIZE]
    cmd = cmd + " -w " + params.quantificationWindowSizeValues[params.quantificationWindowSize.get()]
    #[-wc QUANTIFICATION_WINDOW_CENTER]
    cmd = cmd + " -wc " + params.centerQuantificationWindowValues[params.centerQuantificationWindow.get()]
    #[--exclude_bp_from_left EXCLUDE_BP_FROM_LEFT]
    cmd = cmd + " --exclude_bp_from_left " + params.excludeBpFromLeftValues[params.excludeBpFromLeft.get()]
    #[--exclude_bp_from_right EXCLUDE_BP_FROM_RIGHT]
    cmd = cmd + " --exclude_bp_from_right " + params.excludeBpFromRightValues[params.excludeBpFromRight.get()]
    #--ignore_substitutions
    #                      Ignore substitutions events for the quantification and
    #                      visualization (default: False)
    #--ignore_insertions   Ignore insertions events for the quantification and
    #                      visualization (default: False)
    #--ignore_deletions    Ignore deletions events for the quantification and
    #                      visualization (default: False)
    #--discard_indel_reads
    #                      Discard reads with indels in the quantification window
    #                      from analysis (default: False)
    info(cmd)
    return cmd, None


def OpenExperimentResults(workingDirectory, experiment):
    path = os.path.join(workingDirectory, "CRISPResso_on_" + experiment.sequenceName.get() + ".html")
    if os.path.isfile(path):
        webbrowser.open_new_tab(path)
    else:
        messagebox.showwarning(title = "Warning", message = "CRISPResso execution has been failed")

def executeUtility(ctx, cmd, root):
    getClearFrame(root)
    #popup = tk.Toplevel()
    label = tk.Label(root, text="Report preparing, please wait several minutes...")
    label.place(relx=0.5, rely = 0.5, anchor=tk.CENTER)
    root.pack_slaves()
    root.update()
    res = sb.call(cmd)
    print(res)
    global params
    OpenExperimentResults(ctx.workingDirectory, params)

def runExperiment(ctx, root):
    global params
    try:
        cmd, message = generateCmd(ctx, params)
        if message:
            messagebox.showwarning(title = "Warning", message = message)
            return
        try:
            os.mkdir(ctx.workingDirectory)
        except OSError:
            messagebox.showwarning(title = "Warning", message = "Creation of the directory %s failed" % ctx.workingDirectory)
            return
        else:
            info ("Successfully created the directory %s " % ctx.workingDirectory)
        fileHandler = logging.FileHandler(os.path.join(ctx.workingDirectory, "log.txt"))
        logging.getLogger().addHandler(fileHandler)

        obj = {}
        obj["name"] = params.sequenceName.get()
        obj["id"] = ctx.experimentId
        obj["date"] = int(datetime.datetime.now().timestamp())
        obj["succ"] = False
        id_obj = copy.deepcopy(obj)

        with open(os.path.join(ctx.workingDirectory, "id.json"), 'w') as outfile:
            json.dump(id_obj, outfile)
        params.saveExperiment(os.path.join(ctx.workingDirectory, "experiment.json"))
        
        # LoadExperiments contains the same code!
        obj["dateText"] = str(datetime.datetime.fromtimestamp(obj["date"]))
        obj["folder"] = ctx.workingDirectory
        print("ctx.experiments", len(ctx.experiments))
        ctx.experiments.append(obj)
        executeUtility(ctx, cmd, root)
        id_obj["succ"] = True
        obj["succ"] = True
        with open(os.path.join(ctx.workingDirectory, "id.json"), 'w') as outfile:
            json.dump(id_obj, outfile)

        ctx.backFunc()
    except Exception as err:
        warn("Error: {0}".format(err))
        messagebox.showwarning(title = "Warning", message = "Error: {0}".format(err))
        ctx.backFunc()
    finally:
        logging.getLogger().removeHandler(fileHandler)
        fileHandler.close()

def createLeftPanel(root, ctx, topRoot):
    global params
    row = 0
    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=100)
    root.columnconfigure(2, weight=0)
    root.columnconfigure(3, weight=0)
    # Sequence Name
    hintText = """Optional suffix to append to the report name. Only alphanumeric characters are allowed."""
    row = addTextEdit(root, row, "Experiment Name *:", False, params.sequenceName, hintText, True)
    params.sequenceName.set(ctx.experimentName)

    # Amplicon Name
    hintText = """If submitting more than one amplicon, please separate amplicon names using commas."""
    row = addTextEdit(root, row, "Amplicon Name/s*:", False, params.ampliconNames, hintText, True)

    # editing tool
    comboValues = [ "Cas9", "Cpfl", "Base editors", "Prime editors", "Custom"]
    row = addComboBox(root, row, "Editing tool:", False, comboValues, params.editingTool, None, True)

    # Sequencing design:
    comboValues = [ "Paired end reads", "Single end reads", "Interleaved reads"]
    row = addComboBox(root, row, "Sequencing design:", False, comboValues, params.sequencingDesign, None, True)

    for i in range(0, len(params.sequences)):
        row = createSequenceDesignSection(root, row, params.sequences[i], i, len(params.sequences))
    # row = createSequenceDesignSection(row, 1, 2)

    # Process
    frame = tk.Frame(root, height = 52)
    frame.grid(column=0, row=row, columnspan = 4, sticky=tk.NSEW)
    btn = ttk.Button(frame, text = 'Process', command = lambda:runExperiment(ctx, topRoot))  
    btn.place(relx=0.11, rely=0.22, height=36, width=150)

    btn = ttk.Button(frame, text = 'Cancel', command = ctx.backFunc)
    btn.place(relx=0.56, rely=0.22, height=36, width=150)
    row += 1

def createMiddlePanel(root, row = 0):
    global params
    # Optional parameters
    # row = addDelimeter(root, row, "Optional parameters", None)

    # Minimum homology
    params.minimumHomologyValues = ["50", "60", "70", "80", "90", "100"]
    comboValues = [ x + "%" for x in params.minimumHomologyValues ]
    hintText = """When reads are aligned to each reference amplicon, they must share this percentage of bases in common."""
    row = addComboBox(root, row, "Minimum homology for alignment to an amplicon *:", True, comboValues, params.minimumHomology, hintText)

    # Base editing
    row = addDelimeter(root, row, "Base editing", None)

    # Base editor output
    hintText = """Check this box to produce plots and tables detailing substitution rates for each base."""
    row = addCheckBox(root, row, "Base editor output *:", False, params.baseEditorOutput, hintText)

    # Base editor target base 
    comboValues = [ "A", "C", "T", "G" ]
    hintText = """The is the pre-edited base. E.g. for C->T editors, this should be set to "C"."""
    row = addComboBox(root, row, "Base editor target base *:", False, comboValues, params.targetBase, hintText)

    # Base editor result base
    comboValues = [ "A", "C", "T", "G" ]
    hintText = """The is the post-edited base. E.g. for C->T editors, this should be set to "T"."""
    row = addComboBox(root, row, "Base editor result base *:", False, comboValues, params.resultBase, hintText)

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
    row = addComboBox(root, row, "pegRNA extension quantification window size:", True, comboValues, params.pegRNAQuantificationWindowSize, hintText)

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
    params.centerQuantificationWindowValues = [ "-15", "-10", "-3", "0", "1" ]
    hintText = """Only mutations in the quantification window will be used to determine whether a read is modified or unmodified. At least one sgRNA must be provided to use the quantification window."""
    row = addComboBox(root, row, "Center of the quantification window (relative to 3' end of the provided sgRNA):*:", True, comboValues, params.centerQuantificationWindow, hintText)
    
    comboValues = [ "No window", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "15", "20", "25", "30" ]
    params.quantificationWindowSizeValues = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "15", "20", "25", "30" ]
    hintText = """This setting controls the center of the quantification window. Remember that the sgRNA sequence must be entered without the PAM. For cleaving nucleases, this is the predicted cleavage position. The default is -3 and is suitable for the Cas9 system."""
    row = addComboBox(root, row, "Quantification window size (bp)*:", False, comboValues, params.quantificationWindowSize, hintText)

    row = addDelimeter(root, row, "HDR", None)
    row = addTextEdit(root, row, "Expected HDR amplicon sequence:", True, params.expectedHDRamplicon, hintText)
    row = addDelimeter(root, row, "Exon specification", None)
    row = addTextEdit(root, row, "Coding Sequence/s:", False, params.codingSequence, hintText)
    row = addDelimeter(root, row, "Quality filtering and trimming", None)

    params.minimumAverageReadQualityValues = ["0", "10", "20", "30", "35"]
    comboValues = [ "No Filter", ">10", ">20", ">30", ">35" ]
    row = addComboBox(root, row, "Minimum average read quality (phred33 scale):", True, comboValues, params.minimumAverageReadQuality, None)
    comboValues = [ "No Filter", ">10", ">20", ">30", ">35" ]

    params.minimumSingleQualityValues = ["0", "10", "20", "30", "35"]
    comboValues = [ "No Filter", "<10", "<20", "<30", "<35" ]
    row = addComboBox(root, row, "Minimum single bp quality (phred33 scale):", True, comboValues, params.minimumSingleQuality, None)

    params.replaceBasesNValues = ["0", "10", "20", "30", "35"]
    comboValues = [ "No Filter", "<10", "<20", "<30", "<35" ]
    row = addComboBox(root, row, "Replace bases with N that have a quality lower than (phred33 scale):", True, comboValues, params.replaceBasesN, None)

    params.excludeBpFromLeftValues = ["0", "5", "10", "15", "20", "40", "50"]
    comboValues = [ "Disabled", "5", "10", "15", "20", "40", "50" ]
    row = addComboBox(root, row, "Exclude bp from the left side of the amplicon sequence for the quantification of the mutations:", True, comboValues, params.excludeBpFromLeft, None)

    params.excludeBpFromRightValues = ["0", "5", "10", "15", "20", "40", "50"]
    comboValues = [ "Disabled", "5", "10", "15", "20", "40", "50" ]
    row = addComboBox(root, row, "Exclude bp from the right side of the amplicon sequence for the quantification of the mutations:", True, comboValues, params.excludeBpFromRight, None)

    comboValues = [ "No Trimming", "Nextera PE", "TruSeq3 PE", "TruSeq3 SE", "TruSeq2 PE", "TruSeq2 SE" ]
    row = addComboBox(root, row, "Trimming adapter: ", False, comboValues, params.trimmingAdapter, None)
    return row

def getClearFrame(root):
    for widget in root.winfo_children():
        widget.destroy()
    return root

def executeExperiment(root, ctx, experiment):
    getClearFrame(root)
    global params
    params = experiment

    frame1 = tk.Frame(root)
    frame1.place(relx=0.0, rely=0.0, relheight=1.002, relwidth=0.466)
    frame1.configure(relief='groove')
    frame1.configure(borderwidth="2")
    frame1.configure(relief="groove")
    frame1.configure(highlightbackground="#d9d9d9")
    frame1.configure(highlightcolor="black")

    frame2 = ScrollableFrame(root)
    frame2.place(relx=0.471, rely=0.0, relheight=1.003, relwidth=0.531)
    frame2.configure(relief='groove')
    frame2.configure(borderwidth="2")
    frame2.configure(relief="groove")
    #frame2.configure(highlightbackground="#d9d9d9")
    #frame2.configure(highlightcolor="black")

    createLeftPanel(frame1, ctx, root)
    row = createMiddlePanel(frame2.scrollable_frame)
    row = createRightPanel(frame2.scrollable_frame, row)

def RestartExperiment(root, ctx, experiment):
    info("RestartExperiment: {} in {}".format(ctx.experimentName, ctx.workingDirectory))
    executeExperiment(root, ctx, experiment)

def StartExperiment(root, ctx):
    info("StartExperiment: {} in {}".format(ctx.experimentName, ctx.workingDirectory))
    experiment = Experiment()
    experiment.setDefault()
    executeExperiment(root, ctx, experiment)
