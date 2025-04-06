import importlib
import os

from .Block import Block
from .Wall import Wall

class Plugin:
    def __init__(self, app: Main):
        self.app = app
        print("generic loaded!")

    def getName(self):
        return "generic"

    def getDescription(self):
        return "This is template plugin."

    def getContent(self):
        return {
            "wall": {"displayName": "Wall", "plugin": "generic", "type": [Wall, Block], "end": ".java", "centralWidget": UI2.Content.CentralPreviewWidget.PreviewWidget}
        }

    def getStructuresMod(self):
        return {
            "145": self.generateCode
        }

    def generateCode(self, window=None):
        print("plugin close window!")
        window.close()