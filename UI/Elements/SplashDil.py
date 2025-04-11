from threading import Thread

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSplashScreen, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF, QThread, QObject, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QBrush, QColor, QPixmap, QPen, QFont, QRegion, QPainterPath
import sys
import math

from UI import Language
from UI.Style import dark_style


class SplashDil(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(350, 150)
        self.angle = 0

        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text = QLabel("Load...")
        self.text.setObjectName("SplashTitle")
        self.text.setFont(QFont("Arial", 12))
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cancel = QPushButton(Language.Lang.Editor.Dialog.cancel)
        self.cancel.setParent(self)

        layout.addWidget(QLabel(), 2, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.text, 2, alignment=Qt.AlignmentFlag.AlignRight)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_spinner)
        self.timer.start(16)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        if self.cancel.isVisible():
            self.btnPos = QRect()
            self.btnPos.setX(rect.x() + rect.width() - 100)
            self.btnPos.setY(rect.height() - 40)
            self.btnPos.setWidth(50)
            self.btnPos.setHeight(30)
            self.cancel.setGeometry(self.btnPos)

        pos = QPointF(rect.x()+50, rect.height()//2)
        r = 15
        count = 12
        for i in range(count):
            angle = (360 / count) * i + self.angle
            rad = math.radians(angle)
            x = pos.x() + math.cos(rad) * 20
            y = pos.y() + math.sin(rad) * 20
            alpha = int(255 * (i + 1) / count)
            painter.setBrush(QColor(255, 215, 0, alpha))
            painter.drawEllipse(QPointF(x, y), r / 5, r / 5)

    def update_spinner(self):
        self.angle = (self.angle + 5) % 360
        self.update()


