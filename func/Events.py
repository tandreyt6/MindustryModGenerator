eventsFilter = {}

def on(name: str, executable: object):
    eventsFilter.setdefault(name, []).append(executable)

def fire(name: str, args: dict|list):
    return list(map(lambda func: func(args), eventsFilter.get(name, [])))