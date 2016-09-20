# participationGrade.py
# Takes a CSV file generated from the reslts of a Google Survey
# for partner participation in NXT Robotics at PTS
# 
# Created by Joseph Rivera
# Created April 2016

import sys
import csv
import tkinter as tk
from tkinter import filedialog


#create necessary objects to produce File Open Dialog
root = tk.Tk()
root.withdraw()
opts = {}
opts['filetypes'] = [('TXT Files','.txt'),('all files','.*')]


#read answer key from given file
try:
    keyFile = open(filedialog.askopenfilename(title="Scoring Rubric for Surveys",**opts), "r")
except:
    print("Failed to open scoring rubric file! Exiting...")
    sys.exit()



# AnswerKey ==> List of Tuples
#                   Each Tuple is the type of question and
#                   a dictionary with keywords found in the answers and their grade value
#
# mc ==> Multiple choice - have 1 or more answers, each with a numeric grade value.
# sc ==> Scale of 1-10 - mult key with numeric value that can be multiplied by the given scale value.

answerKey = [("mc", {"lead":20, "shared":20, "often":15, "once":10, "not":5 }),
               ("mc", {"lead":20, "shared":20, "often":15, "sometimes":10, "not":5}),
               ("sc", {"mult":2}),
               ("mc", {"always":20, "usually":15, "seem":10, "unwilling":5}),
               ("mc", {"easily":20, "most":15, "some":10, "unable":5})]

def clean(str):
    return str.lower().strip()

# DisplayGrades - displays partner grades calculated with described answer key.
#   Input - list of 3-tuples
def displayGrades(results):
    for username, partner, grading in results:
        grade = 0
        for k, v in grading.items():
            grade += v

        print(username.replace("@palmertrinity.org", ""), " - ",partner + "'s grade: ",grade)

#=========Program Start=========

print("Welcome to the PTS Participation Grader Mk.I")
print("============================================\n")


opts = {}
opts['filetypes'] = [('CSV Files','.csv'),('all files','.*')]

#attempt to open the given file
#filename = input("Enter your participation survey CSV file:")
filename = filedialog.askopenfilename(title="Survey File to Grade", **opts)

try:
    surveyFile = open(filename, "r")
except:
    print("Failed to open survey file! Exiting...")
    sys.exit()

surveys = csv.reader(surveyFile)
headings = surveys.__next__()
surveyResults = []

#don't include the timestamp, username, and partner name in calculating the grade
headings.pop(0)
headings.pop(0)
headings.pop(0)

for response in surveys:
    student = {}
    tstamp = clean(response.pop(0))
    username = clean(response.pop(0))
    partner = clean(response.pop(0))

    #calculate the grade for each response
    for i in range(len(response)):
        qst = answerKey[i]
        if qst[0] == "mc": #handle multiple choice questions
            answers = qst[1]
            for k, v in answers.items(): #find the matching answer and 
                if k in clean(response[i]):
                    student[clean(headings[i])] = v
        elif qst[0] == "sc": #handle question that uses scale (1 - 10)
            student[clean(headings[i])] = int(qst[1]["mult"]) * int(response[i]) #scale factor * selected scale value
    
    gradeSheet = (username, partner, student)
    surveyResults.append(gradeSheet)

surveyFile.close()
displayGrades(surveyResults)

