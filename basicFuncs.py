import os

def clear_folder(folderPath):
    if os.path.isdir(folderPath):
        shutil.rmtree(folderPath)
    os.makedirs(folderPath)
