import os

import generic
from Constuctors.Item import ItemConstructor
from Constuctors.Wall import WallConstructor

ID_WALLS = ["generic_wall"]
ID_ITEMS = ["generic_item"]

class JavaConstructor:
    def     __init__(self, parent):
        self.parent = parent
        self.content = self.parent.getContent()

    def saveElements(self, data: dict, package: str):
        walls = {}
        items = {}
        for el in data:
            if isinstance(el, int): continue
            if data[el].get("data", {}).get('content', "") in ID_WALLS:
                walls[data[el]['name']] = data[el]['data']
            elif data[el].get("data", {}).get('content', "") in ID_ITEMS:
                items[data[el]['name']] = data[el]['data']
        save_items = ItemConstructor.getJavaCode(package, items)
        save_walls = WallConstructor.getJavaCode(package, walls)
        print(package+".content", items, save_items)
        print(package+".content", walls, save_walls)
        elements = {**save_items, **save_walls}
        for item in elements:
            path = self.parent.app.editor.path + "/src/" + "/".join(package.split(".")) + "/content/" + elements[item]['path'] + "/"
            print(path + elements[item]['filename'])
            os.makedirs(path, exist_ok=True)
            with open(path + elements[item]['filename'],
                      'w') as f:
                f.write(elements[item]['code'])

        return [(elements[_]['init'][0], (elements[_]['init'][1], "var_"+_, _)) for _ in elements]
