import os

data_root = r"C:/"

DATA_PATH = os.path.join(
    data_root, "Users", "CarolynGorman", "OneDrive", "repos", "school-mh", "school-mh"
)

REPO_PATH = os.path.join(
    data_root, "Users", "CarolynGorman", "OneDrive", "repos", "school-mh", "school-mh"
)

def data_path(*args):
    return os.path.join(REPO_PATH, "src", *args)

def out_path(*args):
    return os.path.join(REPO_PATH, "out", *args)

def out_data_path(*args):
    return out_path("clean_data", *args)