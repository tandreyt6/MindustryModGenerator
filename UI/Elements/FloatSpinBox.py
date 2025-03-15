from PyQt6.QtWidgets import QDoubleSpinBox

from UI.Elements.CardConstructor import BaseCustomWidget


class FloatSpinBox(QDoubleSpinBox, BaseCustomWidget):
    def __init__(self, value=0):
        super().__init__(QDoubleSpinBox, None)
        super().__init__(BaseCustomWidget, None)
        self.setValue(value)

        self.valueChanged.connect(lambda val: self.signal.emit(val))

    def setValue(self, val):
        if isinstance(val, str):
            value = float(val.lower().split("f")[0])
        else:
            value = float(val)
        super().setValue(value)

    def set_value(self, value):
        self.setValue(value)

    def value(self) -> str:
        return str(super().value()) + "f"
