import json
import os

class JsonStorer:
    def store(data = {}, folder = 'data', file_name = 'data.json'):
        if not os.path.exists(folder): os.makedirs(folder)

        if not os.path.isfile(f'{folder}/{file_name}'):
            with open(f'{folder}/{file_name}', "w") as file:
                json.dump({}, file, indent=4)

        with open(f'{folder}/{file_name}', 'r+') as file:
            existing_data = json.load(file)

            existing_data.update(data)

            file.seek(0)

            json.dump(existing_data, file, indent=4)
        
    def find(key):
        with open('data/data.json', 'r') as file:
            return json.load(file)[key] if key in json.load(file) else None
