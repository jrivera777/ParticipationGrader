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
from GraderWindow import GraderWindow


   

# AnswerKey ==> List of Tuples
#                   Each Tuple is the type of question and
#                   a dictionary with keywords found in the answers and their grade value
#
# mc ==> Multiple choice - have 1 or more answers, each with a numeric grade value.
# sc ==> Scale of 1-10 - mult key with numeric value that can be multiplied by the given scale value.
# fr ==> Free response - optional text

# answerKey = [("mc", {"lead":20, "shared":20, "often":15, "once":10, "not":5 }),
#                ("mc", {"lead":20, "shared":20, "often":15, "sometimes":10, "not":5}),
#                ("sc", {"mult":2}),
#                ("mc", {"always":20, "usually":15, "seem":10, "unwilling":5}),
#                ("mc", {"easily":20, "most":15, "some":10, "unable":5})]



#=========Program Start=========

if __name__ == "__main__":
    app = GraderWindow()
    app.mainloop()

    #setup main GUI window
    mainWindow = tk.Tk()

