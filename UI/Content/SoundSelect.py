from UI.ContentFormat import Format
from UI.Elements.CardConstructor import BaseCustomWidget
from UI.Elements.SearchBox import SearchBox
from func.GLOBAL import SOUND_TYPES_NOLOAD


class Widget(SearchBox, BaseCustomWidget):
    TYPE = Format.NoFormat

    def __init__(self):
        super().__init__(SearchBox, SOUND_TYPES_NOLOAD)
        super().__init__(BaseCustomWidget, None)

        self.input_field.textChanged.connect(lambda val: self.signal.emit(val))

    def set_value(self, value):
        self.input_field.setText(value)

    def value(self) -> str:
        return self.input_field.text()