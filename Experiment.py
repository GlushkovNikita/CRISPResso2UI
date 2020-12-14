import tkinter as tk
from tkinter import ttk
import os
import json
from json import JSONEncoder

class Sequence():
    """
    Sequence
    """
    def __init__(self):
        self.defaultFastqText = "Please, select file"
        self.sampleName = tk.StringVar()
        self.fastq1 = tk.StringVar(value = self.defaultFastqText)
        self.fastq2 = tk.StringVar(value = self.defaultFastqText)
        self.fastq1.path = ""
        self.fastq2.path = ""
        self.amplicon = tk.StringVar()
        self.sgRNA = tk.StringVar()
    def pack(self):
        obj = {}
        for item in self.__dict__:
            val = getattr(self, item)
            if isinstance(val, tk.StringVar):
                obj[item] = val.get()
        obj["fastq1"] = self.fastq1.path
        obj["fastq2"] = self.fastq2.path
        return obj
    def unpack(self, obj):
        for item in self.__dict__:
            val = getattr(self, item)
            if isinstance(val, tk.StringVar):
                val.set(obj[item])
        self.fastq1.path = self.fastq1.get()
        self.fastq2.path = self.fastq2.get()
        self.fastq1.set(os.path.splitext(self.fastq1.path))
        self.fastq2.set(os.path.splitext(self.fastq2.path))
        return obj

class Experiment():
    """
    Experiment
    """
    def __init__(self):
        self.sequenceName = tk.StringVar()
        self.ampliconNames = tk.StringVar()
        self.editingTool = tk.IntVar(value = 0)
        self.sequencingDesign = tk.IntVar(value = 0)
        self.sequences = [Sequence()]
        self.minimumHomology = tk.IntVar(value = 1)
        self.baseEditorOutput = tk.IntVar(value = 0)
        self.targetBase = tk.IntVar(value = 1)
        self.resultBase = tk.IntVar(value = 2)
        self.pegRNAspacer = tk.StringVar()
        self.pegRNAextension = tk.StringVar()
        self.pegRNAQuantificationWindowSize = tk.IntVar(value = 1)
        self.nickingSgRNA = tk.StringVar()
        self.scaffoldSequence = tk.StringVar()
        self.centerQuantificationWindow = tk.IntVar(value = 2)
        self.quantificationWindowSize = tk.IntVar(value = 1)
        self.expectedHDRamplicon = tk.StringVar()
        self.codingSequence = tk.StringVar()
        self.minimumAverageReadQuality = tk.IntVar(value = 0)
        self.minimumSingleQuality = tk.IntVar(value = 0)
        self.replaceBasesN = tk.IntVar(value = 0)
        self.excludeBpFromLeft  = tk.IntVar(value = 3)
        self.excludeBpFromRight = tk.IntVar(value = 3)
        self.trimmingAdapter = tk.IntVar(value = 0)
    def generateCommand(self):
        return ""
    def toJSON(self):
        obj = {}
        for item in self.__dict__:
            val = getattr(self, item)
            if isinstance(val, tk.StringVar) or isinstance(val, tk.IntVar):
                obj[item] = val.get()
            elif item == "sequences":
                obj[item] = [x.pack() for x in self.sequences]

        return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    def fromJSON(self, j):
        obj = json.loads(j)
        for item in self.__dict__:
            val = getattr(self, item)
            if isinstance(val, tk.StringVar) or isinstance(val, tk.IntVar):
                val.set(obj[item])
            elif item == "sequences":
                for s in obj[item]:
                    se = Sequence()
                    se.unpack(s)
                    self.sequences.append(se)
    def saveExperiment(self, path):
        obj = {}
        for item in self.__dict__:
            val = getattr(self, item)
            if isinstance(val, tk.StringVar) or isinstance(val, tk.IntVar):
                obj[item] = val.get()
            elif item == "sequences":
                obj[item] = [x.pack() for x in self.sequences]
        with open(path, 'w') as outfile:
            json.dump(obj, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    def loadExperiment(self):
        return 0
    def setDefault(self):
        self.sequences[0].fastq1.path = "E:\Freelance\Bochkov\9i_508__adapters_trimmed__paired_R1.fastq"
        self.sequences[0].fastq2.path = "E:\Freelance\Bochkov\9i_508__adapters_trimmed__paired_R2.fastq"
        self.sequences[0].fastq1.set("9i_508__adapters_trimmed__paired_R1.fastq")
        self.sequences[0].fastq2.set("9i_508__adapters_trimmed__paired_R2.fastq")
        self.sequences[0].amplicon.set("TGGAGCCTTCAGAGGGTAAAATTAAGCACAGTGGAAGAATTTCATTCTGTTCTCAGTTTTCCTGGATTATGCCTGGCACCATTAAAGAAAATATCATTGGTGTTTCCTATGATGAATATAGATACAGAAGCGTCATCAAAGCATG")
        self.sequences[0].sgRNA.set("ACCATTAAAGAAAATATCAT")
        self.expectedHDRamplicon.set("TGGAGCCTTCAGAGGGTAAAATTAAGCACAGTGGAAGAATTTCATTCTGTTCTCAGTTTTCCTGGATTATGCCTGGCACCATTAAAGAAAATATCATCTTTGGTGTTTCCTATGATGAATATAGATACAGAAGCGTCATCAAAGCATG")
        self.trimmingAdapter.set(2)

class ExperimentContext():
    def __init__(self, experiments, experimentName, experimentId, workingDirectory, backFunc):
        self.experiments = experiments
        self.experimentName = experimentName
        self.experimentId = experimentId
        self.workingDirectory = workingDirectory
        self.backFunc = backFunc
