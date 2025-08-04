from PyQt6.QtWidgets import QSpinBox

from UI.ContentFormat import Format
from UI.Elements.BaseCustomWidget import BaseCustomWidget


class Widget(QSpinBox, BaseCustomWidget):
    TYPE = Format.Int

    def __init__(self):
        super().__init__(QSpinBox, None)
        super().__init__(BaseCustomWidget, None)
        self.setMinimum(0)
        self.setMaximum(2147483647)

    def set_value(self, value):
        self.setValue(value)

    def value(self):
        return super().value()