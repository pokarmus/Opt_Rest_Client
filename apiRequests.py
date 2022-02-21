import requests
from requests.structures import CaseInsensitiveDict
from fileReader import *
from readConParams import read_con_params


def login(user, password, api_url):
    todo = {"User": user, "Password": password}
    response = requests.post(api_url + 'Authenticate', json=todo)
    print(response.json())


def login_from_file():
    params = read_con_params()
    data = {"username": params["user"], "password": params["password"]}
    print("Logowanie użytkownika za pomocą parametrów: " + str(data))
    response = requests.post(params["address"] + params["loginUrl"], json=data)
    print("Session jwt: " + response.json()["jwt"])
    return response.json()


def send_vrp_json(login_params, vrp_json_path):
    params = read_con_params()
    vrp_json = read_single_json(vrp_json_path)

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + login_params["jwt"]

    print("Wysyłam plik " + get_full_file_name(vrp_json_path) + " do serwera optymalizacji VRP...")

    response = requests.post(params["address"] + params["solveUrl"], headers=headers, json=vrp_json)

    print("Otrzymano odpowiedź, zapisuję pliki...")
    return response.json()
