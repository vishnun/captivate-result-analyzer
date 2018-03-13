import xml.etree.ElementTree
import csv
import time
import os
import re


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split('(\d+)', text)]


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
    interactions = root.findall(".//Interactions")
    variables = root.find(".//Variables")
    ans_els = [elem.tag for elem in variables.iter() if elem is not variables]
    ans_els.sort(key=natural_keys)

    total_correct = 0
    total_wrong = 0
    total_skipped = 0

    keys.append('correct-count')
    keys.append('wrong-count')
    keys.append('skipped')

    interaction_counter = 0

    for i, ans_el in enumerate(ans_els):
        qn = "Answer to Question %d" % (i)
        keys.append(qn)

        answer = variables.find(ans_el).get('value')
        if answer != "":
            if interaction_counter < len(interactions):
                interaction = interactions[interaction_counter]
                interaction_counter += 1
                result = interaction.find("Result").get('value')
                if result == 'W':
                    total_wrong += 1
                elif result == 'C':
                    total_correct += 1
            row[qn] = answer
        else:
            total_skipped += 1

    row['correct-count'] = total_correct
    row['wrong-count'] = total_wrong
    row['skipped'] = total_skipped


def generateResults(dirpath, destination_path):
    student_results = []
    keys = []
    for i, filename in enumerate(os.listdir(dirpath)):
        if filename.endswith(".xml"):
            keys, result = parseXMLFile("%s/%s" % (dirpath, filename), i)
            student_results.append(result)

    writeToCSV(destination_path, student_results, keys)
