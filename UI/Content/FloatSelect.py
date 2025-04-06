from UI.ContentFormat import Format
from UI.Elements.FloatSpinBox import FloatSpinBox


class Widget(FloatSpinBox):
    TYPE = Format.Float

    def __init__(self):
        super().__init__()
