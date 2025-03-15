import json
import os.path

data = {}

def save_data(key, value):
    data[key] = value
    with open("AppSettings.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def get_data(key, d=None):
    return data.get(key, d)

def load():
    global data
    if not os.path.exists("AppSettings.json"): return
    with open("AppSettings.json", "r", encoding="utf-8") as file:
        data = json.load(file)