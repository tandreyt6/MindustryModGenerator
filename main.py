from UI.Elements.SplashDil import SplashDil
from UI import Language
import UI
import sys
import os
import time
import traceback
from collections import deque

import json

import func
import func.memory as memory

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from threading import Thread

from UI.Window.SplashWindow import SplashScreen

from UI.Elements.CreateDialog import ProjectDialog
from UI.Window.SettingsWindow import SettingsWindow
from UI.Style import ALL_THEMES
from UI.Window.Editor import EditorWindow
from UI.Window.Launcher import LauncherWindow
from UI.Content import CacheLayer, SoundSelect
from func import settings
from func.GLOBAL import LIST_TYPES, LIST_MOD_TEMPLATES, LIST_PLANETS_TYPES
from func.PluginLoader import DynamicImporter, ModulePrint
import func.MmgApi
import func.Events as Events
func.MmgApi.Libs.UI = UI

memory.put("appIsRunning", True)

SELECTED_THEME = ("", "")

class Main:
    def __init__(self):
        settings.load()

        env = os.environ.copy()
        memory.put("env", env)

        if settings.get_data("java_home"):
            env['JAVA_HOME'] = settings.get_data("java_home")
            env['java'] = settings.get_data("java_home")+"/bin/java.exe"

        Language.Lang = Language.Langs.get(settings.get_data("lang"), Language.Langs['ru'])[1]
        print(Language.Lang)

        self.projects: list = settings.get_data("recent", [])

        self._original_stdout = sys.stdout
        sys.stdout = ModulePrint()

        self.splashWindow = SplashScreen()
        self.splashWindow.show()

        self.pluginData = {}
        self.loadedPlugins = {}

        memory.put("canOpenEditor", None)
        worker = Thread(target=self.loadPlugThread, daemon=True)
        lastCheck = Thread(target=self.checkLastAndOpen, daemon=True)
        worker.start()
        lastCheck.start()
        while worker.is_alive():
            app.processEvents()
        self.splashWindow.close()

        self.editor = None

        self.settingsWindow = SettingsWindow(self.pluginData)
        self.settingsWindow.themeChanged.connect(self.setTheme)
        self.launcher_window = LauncherWindow()
        self.launcher_window.setStyleSheet(SELECTED_THEME[1])
        self.launcher_window.create_project_clicked.connect(self.create_project)
        self.launcher_window.project_open_clicked.connect(self.select_project)
        self.launcher_window.settings_clicked.connect(self.openSettings)
        self.launcher_window.close_signal.connect(self.close)
        self.launcher_window.project_open_dir_clicked.connect(self.showExplorerFolder)

        if (data:=memory.get("canOpenEditor")) is not None:
            self.select_project(data)
        else:
            self.launcher_window.show()

        self.load_recent()

        self.timer = QTimer(self.launcher_window)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def setTheme(self, theme: str):
        global SELECTED_THEME
        SELECTED_THEME = ALL_THEMES.get(theme, ALL_THEMES['dark_classic'])
        app.setStyleSheet(SELECTED_THEME[0])
        self.launcher_window.setStyleSheet(SELECTED_THEME[1])
        self.settingsWindow.setStyleSheet(SELECTED_THEME[1])
        if self.editor is not None:
            self.editor.setTheme(SELECTED_THEME)
        settings.save_data("appStyle", theme)

    def checkLastAndOpen(self):
        if settings.get_data("openedProject", None) and os.path.exists(settings.get_data("openedProject")):
            for data in self.projects:
                if data.get("path") == settings.get_data("openedProject"):
                    memory.put("canOpenEditor", data)
                    return

    def loadPlugThread(self):
        self.splashWindow.text.setText("Wait 0.1 second...")
        time.sleep(0.1)
        self.loadPlugins()
        func.MmgApi.Plugins.Plugins = func.MmgApi.Plugins.PluginLoader(self.loadedPlugins)
        func.MmgApi.Libs.Main = self
        print(func.MmgApi.Libs.Main)
        self.initContent()
        self.initTemplates()
        self.splashWindow.text.setText("We are completing it...")
        time.sleep(0.5)
        self.initEvent()

    def get_folders(self, directory):
        if not os.path.exists(directory): return []
        return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

    def loadPlugins(self):
        self.splashWindow.text.setText("Load plugins...")
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
            'CustomNoneClass', 'SoundSelectWidget', 'MmgApi', 'functools'
        }

        for plugin_name in load_order:
            self.splashWindow.text.setText("Check plugin \""+plugin_name+"\"...")
            plugin_data = next((d for name, d in valid_plugins if name == plugin_name), None)
            if not plugin_data:
                continue

            main_file = plugin_data["main"]
            plugin_dir = os.path.join("Plugins", plugin_name)
            main_path = os.path.join(plugin_dir, main_file)

            if not os.path.exists(main_path):
                print(f"Plugin {plugin_name} main file not found: {main_file}")
                continue

            plugin_env = {
                "MmgApi": func.MmgApi
            }
            print(func.MmgApi.Libs.Main, "test ---------------")

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
                    allowedList = ["_io", "MmgApi", "os", "UI", "main", "sys", "time", "traceback", "zipfile",
                                     "collections", "hjson", "json", "PyQt6", "func.memory", "func.Types.Content",
                                     "func.settings", "UI.Language", "Language", "threading"]
                    allowedList.append(plugin_name)
                    loader = DynamicImporter(plugin_name, main_path, plugin_env,
                    allowed_modules=allowedList, checkAllowed=False)

                    module = loader.load_module()
                    self.loadedPlugins[plugin_name] = module.Plugin(self)
                    self.pluginData[plugin_name + "  (loaded)"] = {"icon": "./Plugins/" + plugin_name + "/icon.png",
                                              "description": data.get("description") + "\n\nV" + data.get("version", "Not select")}
                    self.splashWindow.text.setText("load plugin \"" + plugin_name + "\" is done.")
                except Exception as e:
                    traceback.print_exc()
                    print(f"Failed to load plugin \"{plugin_name}\": {str(e)}")
                    self.splashWindow.text.setText("Failed to load plugin \"" + plugin_name + "\".")
                    if plugin_name in self.loadedPlugins:
                        del self.loadedPlugins[plugin_name]
                finally:
                    sys.path.remove(plugin_dir)
                continue

            print(f"Skipping plugin {plugin_name} due to dependency errors")

    def initContent(self):
        removed = []
        for plug in self.loadedPlugins:
            try:
                c = self.loadedPlugins[plug].getContent()
                p = self.loadedPlugins[plug].getPlanets()
                for content in c:
                    LIST_TYPES[plug + "_" + content] = c[content]
                for content in p:
                    LIST_PLANETS_TYPES[plug + "_" + content] = p[content]
            except Exception as e:
                removed.append(plug)
                traceback.print_exc()
        for plug in removed:
            del self.loadedPlugins[plug]


    def initTemplates(self):
        removed = []
        for plug in self.loadedPlugins:
            try:
                t = self.loadedPlugins[plug].getStructuresMod()
                for template in t:
                    LIST_MOD_TEMPLATES[template + "  (" + plug + ")"] = t[template]
            except Exception as e:
                removed.append(plug)
                traceback.print_exc()
        for plug in removed:
            del self.loadedPlugins[plug]


    def initEvent(self):
        removed = []
        for plug in self.loadedPlugins:
            try:
                r = self.loadedPlugins[plug].initComplite()
            except Exception as e:
                r = False
                traceback.print_exc()
            if not r: removed.append(plug)
        for plug in removed:
            del self.loadedPlugins[plug]
        Events.fire("pluginsLoaded", self.loadedPlugins)

    def load_recent(self):
        for i in self.projects:
            if not os.path.exists(i.get("path", "")): continue
            self.launcher_window.add_project(
                name=i.get("name", "Unknown"),
                icon=QIcon(i.get("path", "") + "/icon.png") if os.path.exists(
                    i.get("path", "") + "/icon.png") else None,
                data=i
            )

    def update(self):
        if not memory.get("appIsRunning", False): return

    def select_project(self, data):
        self.launcher_window.hide()
        memory.put("canOpenEditor", False)
        dil = SplashDil()
        data['dil'] = dil
        dil.setWindowTitle("Splash")
        dil.show()
        dil.cancel.clicked.connect(dil.close)
        dil.text.setText(f"Load \"{data.get('name', 'Unknown')}\"...")
        x = Thread(target=self.checkAndOpenProject, args=(data,), daemon=True)
        x.start()
        while x.is_alive():
            app.processEvents()
        dil.close()
        del data['dil']
        if memory.get("canOpenEditor") == True:
            self.openProject(data)
            return
        else:
            print(memory.get("canOpenEditor"))
        self.launcher_window.show()

    def checkAndOpenProject(self, data):
        time.sleep(1)
        if not os.path.exists(str(data.get("path", ""))):
            memory.put("canOpenEditor", "Directory does not exist")
            return False
        if not os.path.exists(str(data.get("path", ""))+"/Elements.mmg_j"):
            memory.put("canOpenEditor", "File Elements.mmg_j does not exist")
            return False
        if not data['dil'].isVisible():
            memory.put("canOpenEditor", "Canceled")
            return False
        memory.put("canOpenEditor", True)
        return True

    def openProject(self, data: dict):
        settings.save_data("openedProject", data.get("path"))
        recent = settings.get_data('recent')
        if not data in recent:
            recent.append(data)
            settings.save_data("recent", recent)
        memory.put("selectProject", data)
        self.editor = EditorWindow(self, data)
        self.editor.setStyleSheet(SELECTED_THEME[1])
        self.editor.apply_settings(settings.get_data("editorGeometry", {}))
        self.editor.saveRequested.connect(self.editorGeometrySave)
        self.editor.closeSignal.connect(self.closeEditor)
        self.editor.settingsWindowRequest.connect(self.openSettings)
        Events.fire("editorStarted", {"editor": self.editor})
        self.editor.show()
        self.editor.setFocus()

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
        if os.path.exists(data["path"]):
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

    app.setWindowIcon(QIcon("appIcon.ico"))

    win = Main()
    win.setTheme(settings.get_data("appStyle", "Dark Original"))

    while memory.get("appIsRunning", False):
        app.processEvents()

    app.exit(0)
