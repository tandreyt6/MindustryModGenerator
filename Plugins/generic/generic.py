import os
import threading
import zipfile
import hjson
import json

from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QDialog, QApplication

import MmgApi
from JavaConstructor import JavaConstructor
from MmgApi.Libs import UI, Main, PyQt6, Language
from .dialogs.Create145Dil import ProjectDialog
from .content.Wall import Wall
from .content.easy_planet import PlanetDialog
import Language as Translate

CentAbsWidget = UI.Content.CentralAbstractWidget.CentAbsWidget
CanvasWidget = UI.Elements.BlockViewOnBackground.CanvasWidget


class Plugin:
    def __init__(self, app: Main):
        self.app = app
        Translate.Lang = Translate.RU if Language.Lang.type == "ru" else Translate.EN
        MmgApi.Libs.Events.on("editorStarted", lambda x: self.onEditor(x['editor']))

    def onEditor(self, editor = None):
        self.open_tree_action = QAction("New planet")
        self.open_tree_action.triggered.connect(self.newPlanet)
        editor.treeMenu.addAction(self.open_tree_action)

    def newPlanet(self):
        print("newPlanet")

    def getContent(self):
        return {
            "wall": {
                "displayName": "Wall",
                "type": Wall,
                "end": ".java",
                "centralWidget": CanvasWidget
            }
        }

    def getPlanets(self):
        return {
            "easy_planet": {
                "displayName": "Easy Planet",
                "type": PlanetDialog,
                "end": ".java"
            }
        }

    def getConstructor(self):
        return JavaConstructor(self)

    def hasConstructor(self):
        return True

    def initComplite(self):
        print("generic loaded!")
        return True

    def getStructuresMod(self):
        return {
            "149": self.createProject
        }

    def getDialogSettings(self, data: dict):
        dialog = QDialog()
        dialog.setWindowTitle("Project settings")
        dialog.exec()

    def Unzip149(self, dialog: ProjectDialog):
        data = dialog.get_project_data()
        base_path = os.path.join(data["path"], data["name"])
        src_path = os.path.join(base_path, "src", *data["package"].split("."))

        print("Current working directory:", os.getcwd())

        with zipfile.ZipFile("./Plugins/generic/mod.zip", "r") as zf:
            zf.extractall(base_path)

        os.makedirs(src_path, exist_ok=True)

        with open(os.path.join(src_path, "MindustryMod.java"), "w", encoding="utf-8") as f:
            f.write(f"""package {data['package']};
import mindustry.mod.*;

public class MindustryMod extends Mod {{

    @Override
    public void init() {{
    }}

    @Override
    public void loadContent() {{
        var contentLoader = new initScript();
        contentLoader.loadContent();
    }}
}}""")

        with open(os.path.join(src_path, "initScript.java"), "w", encoding="utf-8") as f:
            f.write(f"""package {data['package']};

public class initScript {{

    void initScript(){{
    }}

    public void loadContent(){{
    }}
}}""")

        with open(os.path.join(base_path, "mod.hjson"), "w", encoding="utf-8") as f:
            hjson.dump({
                "displayName": data["display_name"],
                "name": data["name"],
                "author": "Me",
                "main": f"{data['package']}.MindustryMod",
                "description": "A Mindustry Java mod template.",
                "version": "1.0",
                "minGameVersion": "149",
                "java": "true"
            }, f)

        with open(os.path.join(base_path, "Elements.mmg_j"), "w", encoding="utf-8") as f:
            json.dump({}, f)

    def createProject(self, window=None):
        dialog = ProjectDialog()
        if dialog.exec():
            splash = UI.Elements.SplashDil.SplashDil()
            splash.text.setText("Generate...")
            splash.show()

            thread = threading.Thread(target=self.Unzip149, args=(dialog,))
            thread.start()

            while thread.is_alive():
                QApplication.processEvents()

            splash.close()
            if window:
                window.hide()

            data = dialog.get_project_data()
            path = os.path.join(data["path"], data["name"])
            icon_path = os.path.join(path, "icon.png")

            project_data = {
                "name": data["name"],
                "path": path,
                "plugin": ["generic", "145"]
            }

            self.app.launcher_window.add_project(
                name=project_data["name"],
                icon=QIcon(icon_path) if os.path.exists(icon_path) else None,
                data=project_data
            )

            self.app.select_project(data=project_data)
