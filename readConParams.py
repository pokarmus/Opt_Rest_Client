import json

params_path = "params.json"


def read_con_params():
    with open(params_path, 'r', encoding='UTF8') as f:
        text = f.read().replace('\n', '')
        data = json.loads(text)
        f.close()
        return data
