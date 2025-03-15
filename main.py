import sys
import os
import time
import zipfile
import hjson
import json
import func.memory as memory

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from UI.Elements.CreateDialog import ProjectDialog
from UI.Window.Editor import EditorWindow
from UI.Window.Launcher import LauncherWindow
from func import settings

memory.put("appIsRunning", True)

def unzip_file(zip_path, extract_to):
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"ZIP-файл не найден: {zip_path}")
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Архив успешно распакован в: {extract_to}")

class Main:
    def __init__(self):
        settings.load()

        self.projects: list = settings.get_data("recent", [])

        self.editor = None
        self.launcher_window = LauncherWindow()
        self.launcher_window.show()
        self.launcher_window.create_project_clicked.connect(self.create_project)
        self.launcher_window.project_open_clicked.connect(self.select_project)
        self.launcher_window.close_signal.connect(self.close)
        self.launcher_window.project_open_dir_clicked.connect(self.showExplorerFolder)

        self.load_recent()

        self.timer = QTimer(self.launcher_window)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def load_recent(self):
        for i in self.projects:
            print(i)
            self.launcher_window.add_project(
                name=i.get("name", "Unknown"),
                icon=QIcon(i.get("path","")+"/icon.png") if os.path.exists(i.get("path","")+"/icon.png") else None,
                data=i
            )

    def update(self):
        if not memory.get("appIsRunning", False): return

    def select_project(self, data):
        if os.path.exists(str(data.get("path", ""))):
            self.launcher_window.hide()
            self.editor = EditorWindow(data.get("path", ""))
            self.editor.apply_settings(settings.get_data("editorGeometry", {}))
            self.editor.saveRequested.connect(self.editorGeometrySave)
            self.editor.closeSignal.connect(self.closeEditor)
            self.editor.setFocus()
            self.editor.show()

    def closeEditor(self, event, b):
        event.accept()
        self.close(b)

    def create_project(self):
        dil = ProjectDialog()
        dil.exec()
        if not dil.create: return
        path = dil.folder_line_edit.text()+"/"+dil.name_line_edit.text()
        unzip_file("./ModTemplate.zip", path)
        with open(path+"/mod.hjson", "r", encoding="utf-8") as e:
            data = hjson.load(e)
            data["displayName"] = dil.display_name_line_edit.text()
            data["name"] = dil.name_line_edit.text()
            data["author"] = dil.author_line_edit.text()
            data["main"] = dil.package_line_edit.text()+".javaMod"
            data["minGameVersion"] = dil.version_combo_box.currentText()
        with open(path+"/mod.hjson", "w", encoding="utf-8") as e:
            hjson.dump(data, e)
        self.projects.append({"name": dil.display_name_line_edit.text(), "path": path})
        settings.save_data("recent", self.projects)
        self.launcher_window.hide()
        self.editor = EditorWindow(path)
        self.editor.apply_settings(settings.get_data("editorGeometry", {}))
        self.editor.saveRequested.connect(self.editorGeometrySave)
        self.editor.closeSignal.connect(self.closeEditor)
        self.editor.setFocus()
        self.editor.show()

    def showExplorerFolder(self, data):
        os.startfile(data["path"])

    def editorGeometrySave(self, data):
        settings.save_data("editorGeometry", data)

    def close(self, b=True):
        if b:
            memory.put("appIsRunning", False)
            app.exit(0)
        else:
            QTimer.singleShot(200, self.launcher_window.show)




app = QApplication([])

palette = QPalette()
palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 215, 0))
palette.setColor(QPalette.ColorRole.Button, QColor(51, 51, 51))
palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 215, 0))
app.setPalette(palette)

win = Main()

while memory.get("appIsRunning", False):
    app.processEvents()

app.exit(0)