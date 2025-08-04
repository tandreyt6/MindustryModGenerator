from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QPushButton, QColorDialog, QWidget, QHBoxLayout
import MmgApi

Format = MmgApi.Libs.UI.ContentFormat.Format
BaseCustomWidget = MmgApi.Libs.UI.Elements.BaseCustomWidget.BaseCustomWidget

class ColorPickerButton(QPushButton):
    colorChanged = pyqtSignal(str)

    def __init__(self, text="Select Color", parent=None):
        super().__init__(text, parent)
        self.current_color = QColor(255, 255, 255)
        self.update_button_color()
        self.clicked.connect(self.choose_color)

    def choose_color(self):
        color = QColorDialog.getColor(
            initial=self.current_color,
            title="Select Color",
            options=QColorDialog.ColorDialogOption.DontUseNativeDialog
        )
        if color.isValid():
            self.setColor(color.name(QColor.NameFormat.HexRgb))

    def update_button_color(self):
        self.colorChanged.emit(self.getColor())
        self.setStyleSheet(f"background-color: {self.getColor()};")

    def setColor(self, hex_color: str):
        color = QColor(hex_color)
        if color.isValid():
            self.current_color = QColor(color)
            self.update_button_color()

    def getColor(self) -> str:
        return self.current_color.name(QColor.NameFormat.HexRgb)

class ColorWidget(BaseCustomWidget):
    TYPE = Format.NoFormat

    def __init__(self):
        super().__init__("#ffffff")
        self.h = QHBoxLayout(self)
        self.h.setContentsMargins(0, 0, 0, 0)
        self.h.setSpacing(0)
        self.btn = ColorPickerButton()
        self.btn.colorChanged.connect(self.signal.value_changed.emit)
        self.h.addWidget(self.btn)

    def set_value(self, value):
        self.btn.setColor(value)

    def value(self):
        return self.btn.getColor()