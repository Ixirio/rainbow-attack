import json
import os

class JsonStorer:
    def store(data = {}):
        if not os.path.exists('data'): os.makedirs('data')

        if not os.path.isfile('data/data.json'):
            with open("data/data.json", "w") as file:
                json.dump({}, file, indent=4)

        with open('data/data.json', 'r+') as file:
            existing_data = json.load(file)

            existing_data.update(data)

            file.seek(0)

            json.dump(existing_data, file, indent=4)
        
    def find(key):
        with open('data/data.json', 'r') as file:
            return json.load(file)[key] if key in json.load(file) else None
