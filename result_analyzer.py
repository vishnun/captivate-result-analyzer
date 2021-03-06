import subprocess
import os
import Tkinter as tk  # for python 2.7
import tkFileDialog
import tkFont

import modules.result_generator as result_generator

# Used as a global variable.
basepath = None
destination_path = None

def ask_directory(label, path, updated_text, directory_type):
    global basepath
    global destination_path
    dir_options = {'initialdir': os.environ["HOME"] + '\\', 'mustexist': False, 'title': 'Please select directory'}
    result = tkFileDialog.askdirectory(**dir_options)

    if directory_type == 'basepath':
        basepath = result
    elif directory_type == 'destination':
        destination_path = result

    label.config(text=updated_text)
    path.config(text="%s" % (result))


def analyze_results():
    global basepath, destination_path
    if not basepath:
        basepath = '/Users/vishnunarang/Sites/results/CaptivateResults/Chilab/chilab/emergence'
    result_generator.generateResults(basepath, destination_path)


def center_window(root, width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


def setup_destination_selection(helv16, root):
    label_frame = tk.Frame(root, padx=20, pady=30)
    label_frame.pack()
    label = tk.Label(label_frame)
    label.config(text="Select the destination: ", font=helv16)
    update_text = "Destination selected: "
    dir_button = tk.Button(root, text='Select destination', padx=5, pady=20, width=25,
                           command=lambda: ask_directory(label, path, update_text, 'destination'), bg="blue")
    dir_button.pack(side='top')

    label.pack(padx=10, side='left')
    path = tk.Label(label_frame)
    path.config(text="...")
    path.pack(side='left')


def create_app_GUI():
    global basepath
    root = tk.Tk()

    helv16 = tkFont.Font(root, family='Helvetica', size=14, weight=tkFont.BOLD)
    h1 = tkFont.Font(root, family='Helvetica', size=24, weight=tkFont.BOLD)

    root.title("Custom Captivatte Result Analyzer - developed by Vishnu")

    title = tk.Label(root, padx=20, pady=20, text="Captivate Result Analyzer.", font=h1)
    title.pack()

    setup_directory_selection(helv16, root)

    setup_destination_selection(helv16, root)

    setup_action_buttons(helv16, root)

    center_window(root, 1000, 600)

    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)
    root.configure(pady=10)
    root.mainloop()


def setup_directory_selection(helv16, root):
    update_text = "Directory selected: "
    label_frame = tk.Frame(root, padx=20, pady=30)
    label_frame.pack()
    label = tk.Label(label_frame)
    label.config(text="Select the directory: ", font=helv16)
    dir_button = tk.Button(root, text='Select directory', padx=5, pady=20, width=25,
                           command=lambda: ask_directory(label, path, update_text, 'basepath'), bg="blue")
    dir_button.pack(side='top')
    label.pack(padx=10, side='left')
    path = tk.Label(label_frame)
    path.config(text="...")
    path.pack(side='left')

def open_in_finder(destination_path):
    subprocess.call(["open", destination_path])

def setup_action_buttons(helv16, root):
    global destination_path
    button_frame = tk.Frame(root, relief='raised', bd=1, pady=10, padx=20)
    button_frame.pack()
    close_button = tk.Button(button_frame, text='Close', width=15, command=root.destroy, bg="red")
    submit_button = tk.Button(button_frame, text='Submit', width=15, font=helv16, command=analyze_results, bg="green")
    close_button.pack(padx=1, pady=10, fill='y', side='left')
    submit_button.pack(padx=10, pady=10, fill='both', side='left')

    tk.Button(root, text='Open destination', width=15, command=lambda: open_in_finder(destination_path)).pack(pady=10)

create_app_GUI()
