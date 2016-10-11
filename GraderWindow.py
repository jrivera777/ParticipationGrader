import sys
import csv
from tkinter import filedialog
import tkinter as tk

class GraderWindow(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.resizable(0,0)
        self.answerKey = None
        self.surveyResults = None
        self.setupFrame()
        self.pack()

    #ask for rubric file and generate an answer key
    def loadAnswerKey(self):
        self.answerKey = []
        #read answer key file
        try:
            fileToRead = filedialog.askopenfilename(title="Scoring Rubric for Surveys",**self.opts)
            keyFile = open(fileToRead, "r")
        except: 
            print("Failed to open scoring rubric file! Exiting...")
            print("Unexpected error:", sys.exc_info()[0])
            #sys.exit()
            return False
            
            #generate answer key list

        for line in keyFile:
            quest = line.strip().split("-")
            if(quest[0] == "fr"):
                pair = (quest[0], {})
                self.answerKey.append(pair)
                continue
            ansDict = {};
            keys = quest[1].split(",")
            for ans in keys:
                key = ans.split(":")
                ansDict[key[0]] = int(key[1])
            pair = (quest[0], ansDict)
            self.answerKey.append(pair)

        return True

    def clean(self, str):
        return str.lower().strip()

    def generateGrades(self, surveyFile):
        self.surveyResults = []
        surveys = csv.reader(surveyFile)
        headings = surveys.__next__()

        #don't include the timestamp, username, and partner name in calculating the grade
        headings.pop(0)
        headings.pop(0)
        headings.pop(0)
        
        for response in surveys:
            student = {}
            tstamp = self.clean(response.pop(0))
            username = self.clean(response.pop(0))
            partner = self.clean(response.pop(0))
            
            #calculate the grade for each response
            for i in range(len(response)):
                qst = self.answerKey[i]
                if qst[0] == "mc": #handle multiple choice questions
                    answers = qst[1]
                    for k, v in answers.items(): #find the matching answer and 
                        if k in self.clean(response[i]):
                            student[self.clean(headings[i])] = v
                        elif qst[0] == "sc": #handle question that uses scale (1 - 10)
                            student[self.clean(headings[i])] = int(qst[1]["mult"]) * int(response[i]) #scale factor * selected scale value
                        elif qst[0] == "fr": #ignore free response questions for now...
                            pass
            
            gradeSheet = (username, partner, student)
            self.surveyResults.append(gradeSheet)

        return True


    def loadAKCallback(self):
        self.opts = {}
        self.opts['filetypes'] = [('TXT Files','.txt'),('all files','.*')]
        loaded = self.loadAnswerKey()
        
        if loaded:
            self.rubricFileLabel.configure(text="Loaded Rubric File!\n", fg="green")
            self.loadSurveyBtn.configure(state="normal")
        else:
            self.rubricFileLabel.configure(text="Failed to Load Rubric File!\n", fg="red")
            self.loadSurveyBtn.configure(state="disabled")

    def loadSurveysCallback(self):
        opts = {}
        opts['filetypes'] = [('CSV Files','.csv'),('all files','.*')]

        #attempt to open the given file
        filename = filedialog.askopenfilename(title="Survey File to Grade", **opts)
        surveyFile = None
        try:
            surveyFile = open(filename, "r")
        except:
            print("Failed to open survey file! Exiting...")
            return False
        
        self.generateGrades(surveyFile)
        surveyFile.close()

        self.displayGrades(self.surveyResults)
    
    # DisplayGrades - displays partner grades calculated with described answer key.
    #   Input - list of 3-tuples
    def displayGrades(self, results):
        self.outputText.delete("1.0", "end")
        for username, partner, grading in results:
            grade = 0
            for k, v in grading.items():
                grade += v
            out = username.replace("@palmertrinity.org", "") + " - " + partner + "'s grade: " + str(grade) + "\n"
            self.outputText.insert("end", out)
        
        

    def setupFrame(self):
        self.master.title("PTS Robotics Partner Participation Survey Grader")
        self.master.geometry("600x400")

        self.scrollbar = tk.Scrollbar(self)
        self.titleLabel = tk.Label(self, text="Welcome to the PTS Participation Grader Mk.I\n============================================\n")
        self.loadRubricBtn = tk.Button(self, text="Load Grading Rubric", command=self.loadAKCallback)
        self.rubricFileLabel = tk.Label(self)
        self.loadSurveyBtn = tk.Button(self, text="Load Survey Results", state="disabled", command=self.loadSurveysCallback)
        self.outputText = tk.Text(self)

        self.titleLabel.pack()
        self.loadRubricBtn.pack()
        self.rubricFileLabel.pack()
        self.loadSurveyBtn.pack()
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.outputText.configure(yscrollcommand=self.scrollbar.set)
        self.outputText.pack()
        self.scrollbar.configure(command=self.outputText.yview)    

