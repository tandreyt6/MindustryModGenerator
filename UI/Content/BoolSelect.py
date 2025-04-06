from UI.ContentFormat import Format
from UI.Elements.CardConstructor import BaseCustomWidget
from PyQt6.QtWidgets import QCheckBox


class Widget(QCheckBox, BaseCustomWidget):
    TYPE = Format.Bool

    def __init__(self):
        super().__init__(QCheckBox, None)
        super().__init__(BaseCustomWidget, None)

        self.stateChanged.connect(lambda val: self.signal.emit(bool(val)))

    def set_value(self, value: str|bool):
        if str(value).lower() == 'true':
            self.setChecked(True)
        elif str(value).lower() == 'false':
            self.setChecked(False)
        else: raise ValueError("Unknown type \""+str(value)+"\"!")

    def value(self) -> bool:
        return self.isChecked()