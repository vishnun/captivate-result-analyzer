import os
import xml.etree.ElementTree
import csv
import time
import sys

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
basepath = '/Users/vishnunarang/Sites/results/CaptivateResults/Chilab/chilab/emergence'

if len(argv == 2):
    basepath = sys.argv[1]

generateResults(basepath)
