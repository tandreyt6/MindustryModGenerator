from threading import Thread

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSplashScreen, QHBoxLayout, QPushButton, \
    QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF, QThread, QObject, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QBrush, QColor, QPixmap, QPen, QFont, QRegion, QPainterPath
import sys
import math

from UI import Language
from UI.Style import ALL_THEMES
from UI.Window.SplashWindow import SpinnerWidget


class SplashDil(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 120)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.spinner = SpinnerWidget(self)
        self.spinner.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.text = QLabel("Load...")
        self.text.setObjectName("SplashTitle")
        self.text.setFont(QFont("Arial", 12))
        self.text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.text.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.cancel = QPushButton("Cancel")
        self.cancel.setFixedSize(80, 30)
        self.cancel.setObjectName("CancelButton")

        layout.addWidget(self.spinner)
        layout.addWidget(self.text)
        layout.addWidget(self.cancel)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        radius = 10
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(50, 50, 50, 240))
        painter.drawPath(path)

        painter.end()


