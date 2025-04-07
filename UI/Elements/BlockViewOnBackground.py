import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import os


class Sprite:
    def __init__(self, pixmap, x, y, movable=True):
        self.pixmap = pixmap
        self.pos = QPointF(x, y)
        self.rotation = 0.0
        self.scale = 1.0
        self.movable = movable
        self.selected = False
        self.dragging = False
        self.canDelete = True


class CanvasWidget(QWidget):
    GRID_SIZE = 32

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.scene_rect = QRectF(0, 0, 2000, 2000)
        self.sprites = []
        self.view_offset = QPointF(0, 0)
        self.view_scale = 1.0
        self.zoom_range = (0.3, 5.0)
        self.dragging_view = False
        self.grid = True
        self.mouse_scene_pos = QPointF()
        self.selected_sprite = None
        self.grab_offset = QPointF()
        self.snap_to_grid = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.timeUpdate)
        self.timer.start(10)

        self.coord_label = QLabel(self)
        self.coord_label.setStyleSheet("background:black; color:white; padding:2px;")
        self.coord_label.hide()

    def add_sprite(self, pixmap, x, y, movable=True):
        self.sprites.append(Sprite(pixmap, x, y, movable))
        return len(self.sprites)-1

    def paintEvent(self, event):
        p = QPainter(self)
        p.translate(self.view_offset)
        p.scale(self.view_scale, self.view_scale)

        for sprite in self.sprites:
            p.save()
            p.translate(sprite.pos)
            p.rotate(sprite.rotation)
            p.scale(sprite.scale, sprite.scale)
            p.drawPixmap(-sprite.pixmap.width() // 2, -sprite.pixmap.height() // 2, sprite.pixmap)

            if sprite.selected:
                p.setPen(QPen(Qt.GlobalColor.green, 2))
                p.drawRect(-sprite.pixmap.width() // 2, -sprite.pixmap.height() // 2,
                           sprite.pixmap.width(), sprite.pixmap.height())

            p.restore()

        if self.grid:
            cell_size = self.GRID_SIZE
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
        scene_pos = self.mapToScene(e.pos())

        if e.button() == Qt.MouseButton.LeftButton and e.modifiers() & Qt.KeyboardModifier.ControlModifier and self.selected_sprite or self.selected_sprite and self.selected_sprite.movable == False:
            self.selected_sprite.selected = False
            self.selected_sprite = None

            for sprite in reversed(self.sprites):
                sprite_rect = QRectF(
                    sprite.pos.x() - sprite.pixmap.width() // 2,
                    sprite.pos.y() - sprite.pixmap.height() // 2,
                    sprite.pixmap.width(), sprite.pixmap.height()
                )
                if sprite_rect.contains(scene_pos):
                    sprite.selected = True
                    self.repaint()
                    if e.modifiers() & Qt.KeyboardModifier.ControlModifier and sprite.movable:
                        self.selected_sprite = sprite
                        self.selected_sprite.dragging = True
                        self.grab_offset = scene_pos - sprite.pos
                        self.snap_to_grid = bool(e.modifiers() & Qt.KeyboardModifier.ShiftModifier)
                    else:
                        self.selected_sprite = sprite
                    break

        else:
            self.dragging_view = True
            self.last_pos = e.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

        self.update()

    def mouseMoveEvent(self, e):
        self.mouse_scene_pos = self.mapToScene(e.pos())
        self.coord_label.setText(f"X:{self.mouse_scene_pos.x():.1f}, Y:{self.mouse_scene_pos.y():.1f}")
        self.coord_label.move(e.pos().x() + 40, e.pos().y() + 10)
        self.coord_label.resize(150, 20)
        self.coord_label.show()

        if self.selected_sprite and self.selected_sprite.dragging and self.selected_sprite.movable:
            new_pos = self.mouse_scene_pos - self.grab_offset

            if self.snap_to_grid:
                new_pos.setX(round(new_pos.x() / self.GRID_SIZE) * self.GRID_SIZE)
                new_pos.setY(round(new_pos.y() / self.GRID_SIZE) * self.GRID_SIZE)

            self.selected_sprite.pos = new_pos
            self.update()
            return

        if self.dragging_view:
            delta = e.pos() - self.last_pos
            self.last_pos = e.pos()
            self.view_offset += QPointF(delta)
            self.view_offset.setX(
                min(0, max(-(self.scene_rect.width() * self.view_scale - self.width()), self.view_offset.x())))
            self.view_offset.setY(
                min(0, max(-(self.scene_rect.height() * self.view_scale - self.height()), self.view_offset.y())))
            self.update()

    def mouseReleaseEvent(self, e):
        if self.selected_sprite:
            self.selected_sprite.dragging = False

        self.dragging_view = False
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def leaveEvent(self, e):
        self.coord_label.hide()

    def timeUpdate(self):
        if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier and self.selected_sprite and QApplication.mouseButtons() & Qt.MouseButton.LeftButton:
            self.selected_sprite.dragging = True
        else:
            if self.selected_sprite:
                self.selected_sprite.dragging = False
        if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.snap_to_grid = True
        else:
            self.snap_to_grid = False

    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        if e.key() == Qt.Key.Key_Delete:
            if self.selected_sprite and self.selected_sprite.canDelete:
                idx = self.sprites.index(self.selected_sprite)
                self.sprites.pop(idx)
                self.selected_sprite = None
                self.repaint()

    def keyReleaseEvent(self, e):
        super().keyPressEvent(e)

    def mapToScene(self, pos):
        return QPointF(
            (pos.x() - self.view_offset.x()) / self.view_scale,
            (pos.y() - self.view_offset.y()) / self.view_scale
        )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    idx = self.add_sprite(pixmap, 0, 0)
                    if self.selected_sprite:
                        self.selected_sprite.selected = False
                    self.selected_sprite = self.sprites[idx]
                    self.selected_sprite.selected = True
                    new_pos = self.mouse_scene_pos = self.mapToScene(self.mapFromGlobal(QCursor.pos()))
                    new_pos.setX(round(new_pos.x() / self.GRID_SIZE) * self.GRID_SIZE)
                    new_pos.setY(round(new_pos.y() / self.GRID_SIZE) * self.GRID_SIZE)
                    self.selected_sprite.pos = new_pos
                    print(new_pos)
                    self.repaint()

        self.update()


