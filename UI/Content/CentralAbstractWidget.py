from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import *


class CentAbsWidget(QWidget):
    paramChange = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
