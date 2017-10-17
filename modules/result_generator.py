import xml.etree.ElementTree
import csv
import time
import os

def writeToCSV(destpath, results, keys):
    """ Creates a csv file and writes the data from the <results> dictionary. """
    filename = "%s/study-result-%s.csv" % (destpath, int(time.time()))
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)


def parseXMLFile(filepath, index):
    """ Parse individual XML files and create the dictionary for a row in the CSV file. The keys need to be in a
    certain order hence need special attention. """
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

    parse_questions(keys, root, row)

    return keys, row


def parse_questions(keys, root, row):
    questions = root.findall(".//Interactions")
    total_correct = 0
    total_wrong = 0
    keys.append('correct-count')
    keys.append('wrong-count')
    for i, question in enumerate(questions):
        qn = "Answer to Question %d" % (i)
        row[qn] = question.find('StudentResponse').get('value')
        keys.append(qn)
        # row['time-taken'] = question.find('Latency').get('value')
        result = question.find('Result').get('value')
        if result == 'W':
            total_wrong += 1
        elif result == 'C':
            total_correct += 1
    row['correct-count'] = total_correct
    row['wrong-count'] = total_wrong

def generateResults(dirpath, destination_path):
    student_results = []
    keys = []
    for i, filename in enumerate(os.listdir(dirpath)):
        if filename.endswith(".xml"):
            keys, result = parseXMLFile("%s/%s" % (dirpath, filename), i)
            student_results.append(result)

    writeToCSV(destination_path, student_results, keys)