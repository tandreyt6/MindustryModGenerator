from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QTabWidget, QApplication


class DraggableTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMovable(True)
        self._drag_start_pos = QPoint()
        self._dragging = False

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = event.pos()
            self._dragging = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._dragging:
            if (event.pos() - self._drag_start_pos).manhattanLength() > QApplication.startDragDistance():
                index = self.tabBar().tabAt(self._drag_start_pos)
                if index != -1:
                    self.tabBar().moveTab(index, self.tabBar().tabAt(event.pos()))
                    self._drag_start_pos = event.pos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
        super().mouseReleaseEvent(event)