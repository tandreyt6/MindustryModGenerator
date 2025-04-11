
from MmgApi.Libs import UI, Main, PyQt6
import MmgApi
from .Wall import Wall

CentAbsWidget = UI.Content.CentralAbstractWidget.CentAbsWidget
CanvasWidget = UI.Elements.BlockViewOnBackground.CanvasWidget


class Plugin:
    def __init__(self, app: Main):
        self.app = app

    def getContent(self):
        return {
            "wall": {"displayName": "Wall", "plugin": "generic", "type": Wall, "end": ".java", "centralWidget": CanvasWidget}
        }

    def initComplite(self):
        print("generic loaded!")

    def getStructuresMod(self):
        return {
            "145": self.createProject
        }

    def getDialogSettings(self, data: dict):
        dil = PyQt6.QtWidgets.QDialog()
        dil.setWindowTitle("Project settings")
        dil.exec()

    def createProject(self, window=None):
        wid = PyQt6.QtWidgets.QDialog()
        wid.exec()