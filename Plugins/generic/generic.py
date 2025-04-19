import threading
import time

from MmgApi.Libs import UI, Main, PyQt6, Language
import MmgApi
from .Create145Dil import ProjectDialog
from .Wall import Wall

CentAbsWidget = UI.Content.CentralAbstractWidget.CentAbsWidget
CanvasWidget = UI.Elements.BlockViewOnBackground.CanvasWidget


class Plugin:
    def __init__(self, app: Main):
        self.app = app
        print(Language.Lang.type)

    def getContent(self):
        return {
            "wall": {"displayName": "Wall", "plugin": "generic", "type": Wall, "end": ".java", "centralWidget": CanvasWidget}
        }

    def initComplite(self):
        print("generic loaded!")
        return True

    def getStructuresMod(self):
        return {
            "145": self.createProject
        }

    def getDialogSettings(self, data: dict):
        dil = PyQt6.QtWidgets.QDialog()
        dil.setWindowTitle("Project settings")
        dil.exec()

    def Unzip145(self):
        time.sleep(10)

    def createProject(self, window=None):
        dil = ProjectDialog()
        r = dil.exec()
        if r:
            SplashDil = UI.Elements.SplashDil.SplashDil()
            SplashDil.text.setText("Generate...")
            SplashDil.show()
            x = threading.Thread(target=self.Unzip145)
            x.start()
            while x.is_alive():
                PyQt6.QtWidgets.QApplication.processEvents()
