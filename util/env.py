import os

data_root = r"C:/"

DATA_PATH = os.path.join(
    data_root, "Users", "CarolynGorman", "OneDrive", "repos", "school-mh"
)

REPO_PATH = os.path.join(
    data_root, "Users", "CarolynGorman", "OneDrive", "repos", "school-mh", "school-mh"
)

def data_path(*args):
    return os.path.join(DATA_PATH, *args)

def repo_path(*args):
    return os.path.join(REPO_PATH, *args)

def out_data_path(*args):
    return repo_path("out", "clean_data", *args)

def out_path(*args):
    return repo_path("out", *args)