import sys
import os
import time
import zipfile
from collections import deque

import hjson
import json

import func.MmgApi.Plugins
import func.memory as memory

import PyQt6
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import UI as UI2
from func.Types import Content as ContentAbstract
from UI.Content import CacheLayer, SoundSelect
from UI.Elements.CardConstructor import CustomNoneClass
from UI.Elements.CreateDialog import ProjectDialog
from UI.Elements.FloatSpinBox import FloatSpinBox
from UI.Elements.SettingsWindow import SettingsWindow
from UI.Elements.SoundSelectBox import SoundSelectWidget
from UI.ContentFormat import uiMethods
from UI.Style import dark_style, light_style
from UI.Window.Editor import EditorWindow
from UI.Window.Launcher import LauncherWindow
from func import settings, MmgApi
from func.GLOBAL import LIST_TYPES, LIST_MOD_TEMPLATES
from func.PluginLoader import DynamicImporter

memory.put("appIsRunning", True)


class Main:
    def __init__(self):
        settings.load()

        self.projects: list = settings.get_data("recent", [])

        self.pluginData = {}
        self.loadedPlugins = {}
        self.loadPlugins()
        func.MmgApi.Plugins.Plugins = func.MmgApi.Plugins.PluginLoader(self.loadedPlugins)
        self.initContent()
        self.initTemplates()

        self.editor = None

        self.settingsWindow = SettingsWindow(self.pluginData)
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
        def topological_sort(dependencies):
            in_degree = {plugin: 0 for plugin in dependencies}
            graph = {plugin: [] for plugin in dependencies}
            reverse_graph = {plugin: [] for plugin in dependencies}

            for plugin, deps in dependencies.items():
                for dep in deps:
                    graph[dep].append(plugin)
                    in_degree[plugin] += 1
                reverse_graph[plugin] = deps

            queue = deque([p for p in in_degree if in_degree[p] == 0])
            sorted_plugins = []

            while queue:
                node = queue.popleft()
                sorted_plugins.append(node)
                for neighbor in graph[node]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)

            if len(sorted_plugins) != len(dependencies):
                print("Error: Cyclic dependencies detected in plugins")
                return []
            return sorted_plugins

        folders = self.get_folders("./Plugins")
        plugins = []
        disabled_plugins = set()
        available_plugins = set()

        for folder in folders:
            plugin_dir = os.path.join("Plugins", folder)
            json_path = os.path.join(plugin_dir, "plugin.json")

            if not os.path.exists(json_path):
                print(f"Plugin {folder} missing plugin.json, skipping")
                continue

            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Failed to load {folder}/plugin.json: {str(e)}")
                continue

            if not data.get("enabled", True):
                print(f"Plugin {folder} is disabled")
                disabled_plugins.add(folder)
                continue

            if "main" not in data:
                print(f"Plugin {folder} has no 'main' entry, skipping")
                continue

            plugins.append((folder, data))
            available_plugins.add(folder)

        dependencies = {}
        valid_plugins = []

        for plugin_name, data in plugins:
            deps = data.get("pluginDependence", [])
            missing_deps = []

            for dep in deps:
                if dep not in available_plugins:
                    missing_deps.append(dep)
                elif dep in disabled_plugins:
                    missing_deps.append(f"{dep} (disabled)")

            if missing_deps:
                print(f"Plugin {plugin_name} skipped. Missing dependencies: {', '.join(missing_deps)}")
                continue

            dependencies[plugin_name] = deps
            valid_plugins.append((plugin_name, data))

        load_order = topological_sort(dependencies)

        if not load_order:
            print("Failed to resolve plugin load order")
            return

        reserved_names = {
            'os', 'UI2', 'Main', 'PyQt6', 'memory', 'Content',
            'settings', 'uiMethods', 'FloatSpinBox', 'DynamicImporter',
            'CustomNoneClass', 'SoundSelectWidget', 'MmgApi'
        }

        for plugin_name in load_order:
            plugin_data = next((d for name, d in valid_plugins if name == plugin_name), None)
            if not plugin_data:
                continue

            main_file = plugin_data["main"]
            plugin_dir = os.path.join("Plugins", plugin_name)
            main_path = os.path.join(plugin_dir, main_file)

            if not os.path.exists(main_path):
                print(f"Plugin {plugin_name} main file not found: {main_file}")
                continue

            gl = globals()
            plugin_env = {
                "MmgApi": MmgApi
            }

            for dep in dependencies[plugin_name]:
                if dep in reserved_names:
                    print(f"Name conflict! Plugin {plugin_name} requires reserved name: {dep}")
                    break
                if dep in plugin_env:
                    print(f"Duplicate dependency name {dep} in plugin {plugin_name}")
                    break
                plugin_env[dep] = self.loadedPlugins[dep]
            else:
                try:
                    sys.path.insert(0, plugin_dir)
                    loader = gl['DynamicImporter'](plugin_name, main_path, plugin_env)
                    module = loader.load_module()
                    self.loadedPlugins[plugin_name] = module.Plugin(self)
                    self.pluginData[plugin_name + "  (loaded)"] = {"icon": "./Plugins/" + plugin_name + "/icon.png",
                                              "description": data.get("description") + "\n\nV" + data.get("version", "Not select")}
                    print(f"Successfully loaded plugin: {plugin_name}")
                except Exception as e:
                    print(f"Failed to load plugin \"{plugin_name}\": {str(e)}")
                    if plugin_name in self.loadedPlugins:
                        del self.loadedPlugins[plugin_name]
                finally:
                    sys.path.remove(plugin_dir)
                continue

            print(f"Skipping plugin {plugin_name} due to dependency errors")

    def initContent(self):
        for plug in self.loadedPlugins:
            c = self.loadedPlugins[plug].getContent()
            for content in c:
                LIST_TYPES[plug + "_" + content] = c[content]

    def initTemplates(self):
        for plug in self.loadedPlugins:
            t = self.loadedPlugins[plug].getStructuresMod()
            for template in t:
                LIST_MOD_TEMPLATES[template + "  (" + plug + ")"] = t[template]

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


win = None

if __name__ == "__main__":
    app = QApplication([])

    app.setStyleSheet(dark_style)
    win = Main()

    while memory.get("appIsRunning", False):
        app.processEvents()

    app.exit(0)
