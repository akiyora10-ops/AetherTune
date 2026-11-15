import json, os
PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')

def load():
    if os.path.exists(PATH):
        return json.load(open(PATH))
    return {}

def save(d):
    json.dump(d, open(PATH,'w'), indent=2)
