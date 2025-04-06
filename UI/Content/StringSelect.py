from UI.ContentFormat import Format
from UI.Elements.CardConstructor import BaseCustomWidget
from PyQt6.QtWidgets import QLineEdit
from func.GLOBAL import SOUND_TYPES_NOLOAD


class Widget(QLineEdit, BaseCustomWidget):
    TYPE = Format.String

    def __init__(self):
        super().__init__(QLineEdit, SOUND_TYPES_NOLOAD)
        super().__init__(BaseCustomWidget, None)

        self.textChanged.connect(lambda val: self.signal.emit(val))

    def set_value(self, value):
        self.setText(value)

    def value(self) -> str:
        return self.text()