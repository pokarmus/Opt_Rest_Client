import errno
import json
import os
from datetime import datetime

from readConParams import read_con_params

DATE_TIME_S = None


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
    directs = read_con_params()
    dir_f = directs["outputDir"] + "/" + get_file_name(file_path)
    try:
        os.makedirs(dir_f)
        print("Tworzę katalog wyjściowy: " + dir_f)
    except OSError as e:
        print("Katalog " + dir_f + " już istnieje")
        if e.errno != errno.EEXIST:
            raise
    return dir_f


def move_file_to_output(file_path):
    directs = read_con_params()
    global DATE_TIME_S
    DATE_TIME_S = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    os.rename(directs["inputDir"] + "/" + get_full_file_name(file_path), directs["outputDir"] + "/"
              + (get_file_name(file_path) + "/" + DATE_TIME_S + "_" + get_full_file_name(file_path)))
    print("Przenoszę plik wejściowy do katalogu wyjściowego...")


def move_file_to_output_err(file_path):
    directs = read_con_params()
    global DATE_TIME_S
    DATE_TIME_S = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    os.rename(directs["inputDir"] + "/" + get_full_file_name(file_path), directs["outputDir"] + "/"
              + (get_file_name(file_path) + "/" + DATE_TIME_S + "_ERROR_" + get_full_file_name(file_path)))
    print("Przenoszę błędny plik wejściowy do katalogu wyjściowego...")


def save_resoult_to_output(json_data, dir_f, path):
    out_path = os.path.normpath(os.path.join(dir_f, DATE_TIME_S + "_RESULT_" + get_full_file_name(path)))
    print("Zapisuję plik wynikowy do katalogu wyjściowego...")

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
        f.close()
    print("Plik " + get_full_file_name(path) + " przetworzony poprawnie.")
