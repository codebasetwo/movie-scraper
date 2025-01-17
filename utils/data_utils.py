import json
import pickle

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def save_pickle(name, data):
    with open(name, 'wb') as f:
        pickle.dump(data, f)

def load_pickle(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


