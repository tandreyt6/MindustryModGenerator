import os

import generic
from Constuctors.Wall import WallConstructor


class JavaConstructor:
    def __init__(self, parent):
        self.parent = parent
        self.content = self.parent.getContent()

    def saveElements(self, data: dict, package: str):
        walls = {}
        for el in data:
            if isinstance(el, int): continue
            if data[el].get("data", {}).get('content', "") == "generic_wall":
                walls[data[el]['name']] = data[el]['data']

        save_walls = WallConstructor.getJavaCode(package+".content", walls)
        for wall in save_walls:
            path = self.parent.app.editor.path + "/src/" + "/".join(package.split(".")) + "/content/" + save_walls[wall]['path'] + "/"
            print(path + save_walls[wall]['filename'])
            os.makedirs(path, exist_ok=True)
            with open(path + save_walls[wall]['filename'],
                      'w') as f:
                f.write(save_walls[wall]['code'])

        return [(save_walls[_]['init'][0], (save_walls[_]['init'][1], "var_"+_, _)) for _ in save_walls]
