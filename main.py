import time
from requests.exceptions import RequestException

from apiRequests import login_from_file, send_vrp_json
from fileReader import read_single_json, list_files, move_file_to_output, save_resoult_to_output, PARAMS_PATH, \
    create_dir

if __name__ == '__main__':

    path = read_single_json(PARAMS_PATH)["inputDir"]

    while True:
        files_list = list_files()
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(f'Lista plików w katalogu wejściowym: {str(files_list)}')
        if len(files_list) > 0:
            print(f'Pobieram plik {files_list[0]}')
            try:
                session = login_from_file()
                response = send_vrp_json(session, path + "/" + files_list[0])
                dir_f = create_dir(path + "/" + files_list[0])
                move_file_to_output(path + "/" + files_list[0])
                save_resoult_to_output(response, dir_f, path + "/" + files_list[0])
            except ValueError:
                print('!!! Błędny plik, sprawdź zawartość i spróbuj ponownie !!!')
                dir_f = create_dir(path + "/" + files_list[0])
                move_file_to_output(path + "/" + files_list[0], True)
            except RequestException:
                print('!!! Nie udało się połączyć z serwerem. Nastąpi ponowna próba połączenia !!!')
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        time.sleep(10)
