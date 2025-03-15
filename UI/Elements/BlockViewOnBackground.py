import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.scene_rect = QRectF(0, 0, 2000, 2000)
        self.layers = [{'pixmap': QPixmap(), 'pos': QPointF(), 'rot': 0.0, 'scale': 1.0} for _ in range(4)]
        self.view_offset = QPointF(0, 0)
        self.view_scale = 1.0
        self.zoom_range = (0.5, 5.0)
        self.dragging = False
        self.grid = True
        self.mouse_scene_pos = QPointF()

        self.coord_label = QLabel(self)
        self.coord_label.setStyleSheet("background:black; color:white; padding:2px;")
        self.coord_label.hide()

    def set_scene_size(self, w, h):
        self.scene_rect = QRectF(0, 0, w, h)
        self.update()

    def set_layer(self, idx, pixmap, x, y, rotation=0.0, scale=1.0):
        if 0 <= idx < 4:
            self.layers[idx]['pixmap'] = pixmap
            self.layers[idx]['pos'] = QPointF(x, y)
            self.layers[idx]['rot'] = rotation
            self.layers[idx]['scale'] = scale
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.translate(self.view_offset)
        p.scale(self.view_scale, self.view_scale)

        for layer in self.layers:
            if not layer['pixmap'].isNull():
                p.save()
                p.translate(layer['pos'])
                p.rotate(layer['rot'])
                p.scale(layer['scale'], layer['scale'])
                p.drawPixmap(-layer['pixmap'].width() // 2, -layer['pixmap'].height() // 2, layer['pixmap'])
                p.restore()

        if self.grid:
            cell_size = 32
            vis_rect = self.visible_rect()

            left = vis_rect.left() - (vis_rect.left() % cell_size)
            top = vis_rect.top() - (vis_rect.top() % cell_size)

            p.setPen(QPen(QColor(200, 200, 200, 100), 1))

            x = left
            while x <= vis_rect.right():
                p.drawLine(QPointF(x, vis_rect.top()), QPointF(x, vis_rect.bottom()))
                x += cell_size

            y = top
            while y <= vis_rect.bottom():
                p.drawLine(QPointF(vis_rect.left(), y), QPointF(vis_rect.right(), y))
                y += cell_size

    def visible_rect(self):
        return QRectF(
            (-self.view_offset.x()) / self.view_scale,
            (-self.view_offset.y()) / self.view_scale,
            self.width() / self.view_scale,
            self.height() / self.view_scale
        )

    def wheelEvent(self, e):
        zoom = 1.25 if e.angleDelta().y() > 0 else 0.8
        self.view_scale = max(self.zoom_range[0], min(self.zoom_range[1], self.view_scale * zoom))
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_pos = e.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseMoveEvent(self, e):
        self.mouse_scene_pos = self.mapToScene(e.pos())
        self.coord_label.setText(f"X:{self.mouse_scene_pos.x():.1f}, Y:{self.mouse_scene_pos.y():.1f}")
        self.coord_label.move(e.pos().x() + 10, e.pos().y() + 10)
        self.coord_label.show()

        if self.dragging:
            delta = e.pos() - self.last_pos
            self.last_pos = e.pos()
            self.view_offset += QPointF(delta)
            self.view_offset.setX(
                min(0, max(-(self.scene_rect.width() * self.view_scale - self.width()), self.view_offset.x())))
            self.view_offset.setY(
                min(0, max(-(self.scene_rect.height() * self.view_scale - self.height()), self.view_offset.y())))
            self.update()

    def mouseReleaseEvent(self, e):
        self.dragging = False
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def leaveEvent(self, e):
        self.coord_label.hide()

    def mapToScene(self, pos):
        return QPointF(
            (pos.x() - self.view_offset.x()) / self.view_scale,
            (pos.y() - self.view_offset.y()) / self.view_scale
        )
