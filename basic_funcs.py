import os
import shutil

def clear_folder(folderPath):
    if os.path.isdir(folderPath):
        shutil.rmtree(folderPath)
    os.makedirs(folderPath)

def sort_file_by_int_key(file_name):
    return int(os.path.splitext(file_name)[0])
