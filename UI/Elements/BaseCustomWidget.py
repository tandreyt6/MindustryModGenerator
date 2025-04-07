from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget

from UI.ContentFormat import Format


class CustomWidgetSignal(QObject):
    value_changed = pyqtSignal(object)


class BaseCustomWidget(QWidget):
    TYPE = Format.NoFormat

    def __init__(self, initial_value, parent=None):
        super().__init__(parent)
        self.signal = CustomWidgetSignal()
        self._value = initial_value

    def set_value(self, value):
        raise NotImplementedError("Subclasses must implement set_value")

    def value(self):
        return self._value


class CustomNoneClass(BaseCustomWidget):

    def __init__(self, initial_value, parent=None):
        super().__init__(initial_value, parent)

    def set_value(self, value):
        pass
