from PyQt6.QtWidgets import QWidget, QVBoxLayout

from UI.Elements.BaseCustomWidget import BaseCustomWidget
from UI.Elements.SearchBox import SearchBox


class SoundSelectWidget(BaseCustomWidget):
    def __init__(self, value="Sound.none"):
        super().__init__(BaseCustomWidget, None)
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        from func.GLOBAL import SOUND_TYPES
        self.search = SearchBox(SOUND_TYPES)
        self.search.input_field.textChanged.connect(self.valueChanged)
        v.addWidget(self.search)

    def valueChanged(self, val):
        self.signal.value_changed.emit(val)

    def set_value(self, value: str):
        self.search.updating = False
        self.search.input_field.setText(value)
        self.search.updating = True

    def value(self):
        return self.search.input_field.text()