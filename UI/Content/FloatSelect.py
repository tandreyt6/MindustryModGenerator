from UI.ContentFormat import Format
from UI.Elements.FloatSpinBox import FloatSpinBox


class Widget(FloatSpinBox):
    TYPE = Format.Float

    def __init__(self):
        super().__init__()
        self.setMinimum(0)
        self.setMaximum(2147483647)
