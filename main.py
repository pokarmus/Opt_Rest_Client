import time

from apiRequests import *
from fileReader import *
from fileList import *


if __name__ == '__main__':

    path = read_con_params()["inputDir"]

    while (True):
        files_list = list_files()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Lista plików w katalogu wejściowym: " + str(files_list))
        if len(files_list)>0:
            print("Pobieram plik " + files_list[0])
            try:
                session = login_from_file()
                response = send_vrp_json(session, path +"/" + files_list[0])
                dir = create_dir(path +"/" + files_list[0])
                move_file_to_output(path +"/" + files_list[0])
                save_resoult_to_output(response, dir, path +"/" + files_list[0])
            except ValueError:
                print("!!! Błędny plik, sprawdź zawartość i spróbuj ponownie !!!")
                dir = create_dir(path + "/" + files_list[0])
                move_file_to_output_err(path + "/" + files_list[0])
            except requests.exceptions.RequestException:
                print("!!! Nie udało się połączyć z serwerem. Nastąpi ponowna próba połączenia !!!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        time.sleep(10)