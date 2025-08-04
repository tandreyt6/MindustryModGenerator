from PyQt6.QtWidgets import QDoubleSpinBox

from UI.Elements.BaseCustomWidget import BaseCustomWidget


class FloatSpinBox(QDoubleSpinBox, BaseCustomWidget):
    def __init__(self, value=0):
        super().__init__(QDoubleSpinBox, None)
        super().__init__(BaseCustomWidget, None)
        self.setValue(value)
        self.valueChanged.connect(lambda val: self.signal.value_changed.emit(val))

    def setValue(self, val):
        super().setValue(float(val.lower().split("f")[0]) if isinstance(val, str) else float(val))

    def set_value(self, value):
        self.setValue(value)

    def value(self) -> str:
        return super().value()
