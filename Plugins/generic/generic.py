import os

from MmgApi.Libs import PyQt6, UI, uiMethods, Content, Main

from .Block import Block
from .Wall import Wall

QtWidgets = PyQt6.QtWidgets
QtCore = PyQt6.QtCore
QtGui = PyQt6.QtGui
CentAbsWidget = UI.Content.CentralAbstractWidget.CentAbsWidget
CanvasWidget = UI.Elements.BlockViewOnBackground.CanvasWidget


class Plugin:
    def __init__(self, app: Main):
        self.app = app
        print("generic loaded!")

    def getContent(self):
        return {
            "wall": {"displayName": "Wall", "plugin": "generic", "type": Wall, "end": ".java", "centralWidget": CanvasWidget}
        }

    def getStructuresMod(self):
        return {
            "145": self.createProject
        }

    def createProject(self, window=None):
        pass