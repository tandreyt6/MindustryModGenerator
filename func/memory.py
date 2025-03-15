data = {}

def put(key, value):
    data[key] = value

def get(key, d=None):
    return data.get(key, d)