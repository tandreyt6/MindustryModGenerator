import sys
import os
import time
import zipfile
import hjson
import json
import func.memory as memory

import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import UI as UI2
from UI.Content import CacheLayer, SoundSelect
from UI.Elements.CardConstructor import CustomNoneClass
from UI.Elements.CreateDialog import ProjectDialog
from UI.Elements.FloatSpinBox import FloatSpinBox
from UI.Elements.SettingsWindow import SettingsWindow
from UI.Elements.SoundSelectBox import SoundSelectWidget
from UI.Style import dark_style, light_style
from UI.Window.Editor import EditorWindow
from UI.Window.Launcher import LauncherWindow
from func import settings
from func.GLOBAL import LIST_TYPES, LIST_MOD_TEMPLATES
from func.PluginLoader import DynamicImporter

memory.put("appIsRunning", True)


class Main:
    def __init__(self):
        settings.load()

        self.projects: list = settings.get_data("recent", [])

        self.loadedPlugins = {}
        self.disabledPlugins = settings.get_data("disabledPlugins", [])
        self.loadPlugins()
        self.initContent()
        self.initTemplates()

        self.editor = None
        data = {}
        for _ in self.loadedPlugins:
            data[_ + "  (loaded)"] = {"icon": "./Plugins/" + _ + "/icon.png",
                                      "description": self.loadedPlugins[_].getDescription()}
        self.settingsWindow = SettingsWindow(data)
        self.launcher_window = LauncherWindow()
        self.launcher_window.create_project_clicked.connect(self.create_project)
        self.launcher_window.project_open_clicked.connect(self.select_project)
        self.launcher_window.settings_clicked.connect(self.openSettings)
        self.launcher_window.close_signal.connect(self.close)
        self.launcher_window.project_open_dir_clicked.connect(self.showExplorerFolder)

        if settings.get_data("openedProject", None) and os.path.exists(settings.get_data("openedProject")):
            self.openProject(settings.get_data("openedProject", None))
        else:
            self.launcher_window.show()

        self.load_recent()

        self.timer = QTimer(self.launcher_window)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def get_folders(self, directory):
        if not os.path.exists(directory): return []
        return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

    def loadPlugins(self):
        folders = self.get_folders("./Plugins")
        for folder in folders:
            if os.path.exists(os.getcwd() + "/Plugins/" + folder + "/Plugin.py"):
                if folders in self.disabledPlugins:
                    print("skip", folder, "because disabled!")
                    continue
                gl = globals()
                pluginDict = {
                    "UI2": gl["UI2"],
                    "Main": gl["Main"],
                    "PyQt6": gl["PyQt6"],
                    "memory": gl["memory"],
                    "settings": gl["settings"],
                    "FloatSpinBox": gl["FloatSpinBox"],
                    "DynamicImporter": gl["DynamicImporter"],
                    "CustomNoneClass": gl["CustomNoneClass"],
                    "SoundSelectWidget": gl["SoundSelectWidget"],
                }
                loader = DynamicImporter(folder, os.getcwd() + "/Plugins/" + folder + "/Plugin.py", pluginDict)
                module = loader.load_module()
                self.loadedPlugins[folder] = module.Plugin(self)

    def initContent(self):
        for plug in self.loadedPlugins:
            c = self.loadedPlugins[plug].getContent()
            for content in c:
                LIST_TYPES[plug + "_" + content] = c[content]

    def initTemplates(self):
        for plug in self.loadedPlugins:
            t = self.loadedPlugins[plug].getStructuresMod()
            for template in t:
                LIST_MOD_TEMPLATES[template+"  ("+plug+")"] = t[template]

    def load_recent(self):
        for i in self.projects:
            print(i)
            self.launcher_window.add_project(
                name=i.get("name", "Unknown"),
                icon=QIcon(i.get("path", "") + "/icon.png") if os.path.exists(
                    i.get("path", "") + "/icon.png") else None,
                data=i
            )

    def update(self):
        if not memory.get("appIsRunning", False): return

    def select_project(self, data):
        if os.path.exists(str(data.get("path", ""))):
            self.launcher_window.hide()
            self.openProject(data.get("path", ""))

    def openProject(self, path: str):
        settings.save_data("openedProject", path)
        self.editor = EditorWindow(path)
        self.editor.apply_settings(settings.get_data("editorGeometry", {}))
        self.editor.saveRequested.connect(self.editorGeometrySave)
        self.editor.closeSignal.connect(self.closeEditor)
        self.editor.settingsWindowRequest.connect(self.openSettings)
        self.editor.setFocus()
        self.editor.show()

    def openSettings(self):
        if not self.settingsWindow.isVisible():
            self.settingsWindow.exec()

    def closeEditor(self, event, b):
        event.accept()
        if not b:
            settings.save_data("openedProject", None)
        self.close(b)

    def create_project(self):
        dil = ProjectDialog()
        r = dil.exec()
        if r == 1:
            constructor = LIST_MOD_TEMPLATES[dil.combo.currentText()]
            constructor(self.launcher_window)

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

app.setStyleSheet(dark_style)

win = Main()

while memory.get("appIsRunning", False):
    app.processEvents()

app.exit(0)
