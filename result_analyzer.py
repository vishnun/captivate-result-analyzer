import os
import xml.etree.ElementTree
import csv
import time
import sys

import Tkinter as tk # for python 2.7
import tkFileDialog


def writeToCSV(results, keys):
    filename = "study-result-%s.csv" % int(time.time())
    with open(filename, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)


def parseXMLFile(filepath, index):
    root = xml.etree.ElementTree.parse(filepath).getroot()
    row = {}
    keys = []
    row['Sr. No.'] = index + 1
    keys.append('Sr. No.')
    row['student-name'] = root.find('LearnerName').get('value')
    keys.append('student-name')
    row['status'] = root.find(".//Status").get('value')
    keys.append('status')
    row['score'] = root.find(".//Score").get('value')
    keys.append('score')
    row['session-time'] = root.find(".//SessionTime").get('value')
    keys.append('session-time')
    
    questions = root.findall(".//Interactions")
    
    totalCorrect = 0
    totalWrong = 0
    keys.append('correct-count')
    keys.append('wrong-count')

    
    for i, question in enumerate(questions):
        qn = "Answer to Question %d" % (i)
        row[qn] = question.find('StudentResponse').get('value')
        keys.append(qn)
        # row['time-taken'] = question.find('Latency').get('value')
        result = question.find('Result').get('value')
        if result == 'W':
            totalWrong += 1
        elif result == 'C':
            totalCorrect += 1

    row['correct-count'] = totalCorrect
    row['wrong-count'] = totalWrong

    return keys, row


def generateResults(basepath):
    student_results = []
    keys = []
    for i, filename in enumerate(os.listdir(basepath)):
        if filename.endswith(".xml"):
            keys, result = parseXMLFile("%s/%s"%(basepath, filename), i)
            student_results.append(result)

    writeToCSV(student_results, keys)

# Future api: generateResults('source_directory', target_csv_file_name)
basepath = None

if (len(sys.argv) == 2):
    basepath = sys.argv[1]

# generateResults(basepath)

# basepath = None

def ask_directory(label):
    global basepath
    dir_opt = {}
    dir_opt['initialdir'] = os.environ["HOME"] + '\\'
    dir_opt['mustexist'] = False
    dir_opt['title'] = 'Please select directory'
    result = tkFileDialog.askdirectory(**dir_opt)
    basepath = result
    label.config(text="Directory selected: %s" % (basepath))


def analyze_results():
    global basepath
    if not basepath:
        basepath = '/Users/vishnunarang/Sites/results/CaptivateResults/Chilab/chilab/emergence'
    generateResults(basepath)

def center_window(root, width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def createGUI():
    global basepath

    root = tk.Tk()
    root.title("Custom Captivatte Result Analyzer")
    label = tk.Label(root)
    label.config(text="Select the directory: ")
    label.pack(padx=10, pady=10, side='top')
    
    dir_button = tk.Button(root, text='select directory', width=25, command=lambda: ask_directory(label), bg="blue")
    dir_button.pack(padx=5, pady=10, side='top')

    button_frame = tk.Frame(root, relief='raised', bd=1, pady=20)
    button_frame.pack(pady=5)
    
    close_button = tk.Button(button_frame, text='Close', width=25, command=root.destroy, bg="red")
    submit_button = tk.Button(button_frame, text='Submit', width=25, command=analyze_results, bg="green")

    close_button.pack(padx=1, pady=10, fill='y', expand=1, side='left')
    submit_button.pack(padx=10, pady=10, fill='y', side='left')    

    center_window(root, 1000, 400)
    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)
    root.configure(pady=100)
    root.mainloop() 

createGUI()


