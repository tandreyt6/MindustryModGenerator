from UI.ContentFormat import Format
from UI.Elements.BaseCustomWidget import BaseCustomWidget
from UI.Elements.SearchBox import SearchBox
from func.GLOBAL import SOUND_TYPES_NOLOAD


class Widget(SearchBox, BaseCustomWidget):
    TYPE = Format.NoFormat

    def __init__(self):
        SearchBox.__init__(self, items=SOUND_TYPES_NOLOAD)
        BaseCustomWidget.__init__(self, None)

        self.input_field.textChanged.connect(lambda val: self.signal.value_changed.emit(val))

    def set_value(self, value):
        self.input_field.setText(value)

    def value(self) -> str:
        return self.input_field.text()