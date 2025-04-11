from threading import Thread

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSplashScreen
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF, QThread, QObject, pyqtSignal
from PyQt6.QtGui import QPainter, QBrush, QColor, QPixmap, QPen, QFont, QRegion, QPainterPath
import sys
import math

from UI.Style import dark_style


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.SplashScreen)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedSize(500, 300)
        self.angle = 0

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("Mindustry Mod Generator")
        self.title.setObjectName("SplashTitle")
        self.title.setFont(QFont("Arial", 24))

        self.text = QLabel("Load the application...")
        self.text.setObjectName("SplashTitle")
        self.text.setFont(QFont("Arial", 12))
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.title)
        layout.addWidget(self.text)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_spinner)
        self.timer.start(16)

    def paintEvent(self, event):
        radius = 20
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        path = QRectF(rect)

        region = QRegion(rect, QRegion.RegionType.Rectangle)
        rounded = QRegion(rect.adjusted(1, 1, -1, -1), QRegion.RegionType.Rectangle)
        self.setMask(QRegion(rect, QRegion.RegionType.Rectangle).subtracted(region.subtracted(rounded)))

        pixmap = QPixmap("SplashBG.png").scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation)

        clip_path = QPainterPath()
        clip_path.addRoundedRect(path, radius, radius)
        painter.setClipPath(clip_path)
        painter.drawPixmap(rect, pixmap)

        painter.setBrush(QColor(0, 0, 0, 100))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(path, radius, radius)

        center = QPointF(rect.center().x(), rect.height() - 50)
        r = 15
        count = 12
        for i in range(count):
            angle = (360 / count) * i + self.angle
            rad = math.radians(angle)
            x = center.x() + math.cos(rad) * 20
            y = center.y() + math.sin(rad) * 20
            alpha = int(255 * (i + 1) / count)
            painter.setBrush(QColor(255, 215, 0, alpha))
            painter.drawEllipse(QPointF(x, y), r / 5, r / 5)

    def update_spinner(self):
        self.angle = (self.angle + 5) % 360
        self.update()


