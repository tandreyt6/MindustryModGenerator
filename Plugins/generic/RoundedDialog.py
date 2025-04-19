from PyQt6.QtGui import QPainter, QPainterPath, QColor
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt, QRectF

class RoundedDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect())
        radius = 10.0
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius, Qt.SizeMode.AbsoluteSize)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(50, 50, 50, 240))
        painter.drawPath(path)