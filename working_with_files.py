from tkinter import filedialog


def ask_file_path():
    file_path = filedialog.askopenfilename()
    return file_path