import os

def make_dir(path_file) -> str:
    if not os.path.exists(path_file):
        os.makedirs(path_file)
    return path_file
