import errno
import json
import os
import glob
from datetime import datetime


DATE_TIME_S = None
PARAMS_PATH = "params.json"


def read_single_json(path):
    with open(path, 'r', encoding='UTF8') as f:
        text = f.read().replace('\n', '')
        data = json.loads(text)
        f.close()
        return data


def get_file_name(file_path):
    name = os.path.basename(file_path)
    name_pos = name.find(".")
    return name[0:name_pos]


def get_full_file_name(file_path):
    name = os.path.basename(file_path)
    return name


def create_dir(file_path):
    directs = read_single_json(PARAMS_PATH)
    dir_f = directs["outputDir"] + "/" + get_file_name(file_path)
    try:
        os.makedirs(dir_f)
        print(f'Tworzę katalog wyjściowy: {dir_f}')
    except OSError as e:
        print(f'Katalog {dir_f} już istnieje')
        if e.errno != errno.EEXIST:
            raise
    return dir_f


def move_file_to_output(file_path: str, with_error=False):
    directs = read_single_json(PARAMS_PATH)
    global DATE_TIME_S
    DATE_TIME_S = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    print('Przenoszę plik wejściowy do katalogu wyjściowego...')
    if not with_error:
        os.rename(directs["inputDir"] + "/" + get_full_file_name(file_path), directs["outputDir"] + "/"
                + (get_file_name(file_path) + "/" + DATE_TIME_S + "_" + get_full_file_name(file_path)))
    else:
        os.rename(directs["inputDir"] + "/" + get_full_file_name(file_path), directs["outputDir"] + "/"
                  + (get_file_name(file_path) + "/" + DATE_TIME_S + "_ERROR_" + get_full_file_name(file_path)))


def save_resoult_to_output(json_data, dir_f, path):
    out_path = os.path.normpath(os.path.join(dir_f, DATE_TIME_S + "_RESULT_" + get_full_file_name(path)))
    print('Zapisuję plik wynikowy do katalogu wyjściowego...')

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
        f.close()
    print(f'Plik {get_full_file_name(path)} przetworzony poprawnie.')


def list_files():
    dir = read_single_json(PARAMS_PATH)["inputDir"]
    list_of_files = filter(os.path.isfile, glob.glob(dir + '/*'))
    list_of_files = sorted(list_of_files, key=os.path.getmtime)
    files = []
    for l in list_of_files:
        files.append(l.replace(dir + "\\", ""))
    return files