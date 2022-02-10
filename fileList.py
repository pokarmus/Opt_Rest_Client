import glob
import os

from readConParams import read_con_params


def list_files():
    dir = read_con_params()["inputDir"]
    list_of_files = filter(os.path.isfile, glob.glob(dir + '/*'))
    list_of_files = sorted(list_of_files, key=os.path.getmtime)
    files = []
    for l in list_of_files:
        files.append(l.replace(dir + "\\", ""))
    return files
