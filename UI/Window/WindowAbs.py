from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout,
    QPushButton, QApplication, QLabel,
    QSizeGrip, QVBoxLayout, QFrame, QToolButton, QMenu, QDialog
)
from PyQt6.QtCore import Qt, QPoint, QRect, QEvent, QVariantAnimation, QEasingCurve, QTimer, QSize, QPointF, QRectF
from PyQt6.QtGui import QMouseEvent, QResizeEvent, QAction, QCursor, QPainterPath, QPainter, QColor, QBrush, QPen


class CustomTitleBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('CustomTitleBar')
        self.parent = parent
        self.setMinimumHeight(32)
        self.hLayout = QHBoxLayout(self)
        self.hLayout.setContentsMargins(10, 0, 10, 0)
        self.hLayout.setSpacing(8)
        self.title = QLabel("Custom Window")
        self.btn_min = QPushButton("—")
        self.btn_max = QPushButton("□")
        self.btn_close = QPushButton("×")
        self.btn_close.setObjectName("closeButton")
        for btn in [self.btn_min, self.btn_max, self.btn_close]:
            btn.setFixedSize(30, 30)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setObjectName("WindowTitleButtons")
        self.hLayout.addWidget(self.title)
        self.hLayout.addStretch()
        self.hLayout.addWidget(self.btn_min)
        self.hLayout.addWidget(self.btn_max)
        self.hLayout.addWidget(self.btn_close)
        self.btn_min.clicked.connect(parent.showMinimized)
        self.btn_max.clicked.connect(self.toggle_maximize)
        self.btn_close.clicked.connect(parent.close)
        self.old_pos = None
        self.normal_size = None
        self.offset = None
        self.isDrag = False

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            if self.normal_size:
                self.parent.setGeometry(self.x(), self.y(), self.normal_size.width(), self.normal_size.height())
        else:
            self.normal_size = self.parent.geometry()
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.parent.getDirectionMousePos() is None:
            self.isDrag = True
            event.accept()
        self.parent.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.parent.mouseMoveEvent(event)
        if self.parent.isMaximized():
            self.parent.showNormal()
            if self.normal_size:
                self.parent.setGeometry(self.x(), self.y(), self.normal_size.width(), self.normal_size.height())
        elif self.isDrag:
            self.isDrag = False
            self.parent.windowHandle().startSystemMove()

    def mouseReleaseEvent(self, event):
        self.parent.mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize()
            event.accept()

class CustomActionBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CustomActionBar")
        self.setStyleSheet("background-color: transparent;")
        self.setFixedHeight(36)
        self.hLayout = QHBoxLayout(self)
        self.hLayout.setContentsMargins(4, 4, 4, 4)
        self.hLayout.setSpacing(2)
        self.toggle_button = QPushButton("☰")
        self.toggle_button.setFixedSize(28, 28)
        self.toggle_button.setObjectName("ActionPanelButton")
        self.toggle_button.clicked.connect(self.toggle_actions)
        self.toggle_button.setVisible(False)
        self.actions_container = QWidget()
        self.actions_layout = QHBoxLayout(self.actions_container)
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setSpacing(4)
        self.actions_container.setFixedWidth(0)
        self.hLayout.addWidget(self.toggle_button)
        self.hLayout.addWidget(self.actions_container)
        self.hLayout.addStretch()
        self.is_expanded = False
        self.animation = None

    def addAction(self, action, icon=None):
        if isinstance(action, QAction):
            self.toggle_button.setVisible(True)
            button = QToolButton()
            button.setDefaultAction(action)
            button.setFixedSize(100, 28)
            button.setObjectName("ActionPanelButton")
            self.actions_layout.addWidget(button)
        elif isinstance(action, QMenu):
            self.toggle_button.setVisible(True)
            button = QPushButton(action.title())
            if icon:
                button.setIcon(icon)
            button.setFixedSize(100, 28)
            button.setObjectName("ActionPanelButton")
            button.setMenu(action)
            self.actions_layout.addWidget(button)
        else:
            raise ValueError("Action must be QAction or QMenu")

    def expand(self):
        desired_width = max(self.actions_layout.sizeHint().width(), 100)
        self.animation = QVariantAnimation(self)
        self.animation.setStartValue(0)
        self.animation.setEndValue(desired_width)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.OutExpo)
        self.animation.valueChanged.connect(lambda value: self.actions_container.setFixedWidth(value))
        QTimer.singleShot(0, self.animation.start)
        self.is_expanded = True

    def collapse(self):
        current_width = self.actions_container.width()
        self.animation = QVariantAnimation(self)
        self.animation.setStartValue(current_width)
        self.animation.setEndValue(0)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.InExpo)
        self.animation.valueChanged.connect(lambda value: self.actions_container.setFixedWidth(value))
        QTimer.singleShot(0, self.animation.start)
        self.is_expanded = False

    def toggle_actions(self):
        self.actions_layout.update()
        if self.animation:
            self.animation.stop()
        if not self.is_expanded:
            self.expand()
        else:
            self.collapse()

class OutlineWidget(QWidget):
    def __init__(self, parent, window_manager):
        super().__init__(parent)
        self.window_manager = window_manager
        self.parent_window = parent

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.update_position()
        self.hide()

    def update_position(self):
        if self.parent_window:
            global_pos = self.parent_window.mapToGlobal(QPoint(0, 0))

            self.setGeometry(
                global_pos.x(),
                global_pos.y(),
                self.parent_window.width(),
                self.parent_window.height()
            )
            self.update()

    def paintEvent(self, event):
        if not self.parent_window or not self.parent_window.isActiveWindow():
            return

        painter = QPainter(self)
        pen = QPen(QColor(255, 255, 255), 4)
        painter.setPen(pen)

        parent_rect_global = self.parent_window.frameGeometry()
        parent_global_top_left = parent_rect_global.topLeft()

        other_windows = [
            w for w in self.window_manager.windows
            if w is not self.parent_window and w.isVisible() and not w.isMinimized()
        ]

        for win in other_windows:
            win_rect = win.frameGeometry()
            intersection = parent_rect_global.intersected(win_rect)

            if not intersection.isNull():
                local_intersection = intersection.translated(-parent_global_top_left)

                if intersection.top() == parent_rect_global.top():
                    painter.drawLine(
                        local_intersection.left(),
                        0,
                        local_intersection.right(),
                        0
                    )

                if intersection.bottom() == parent_rect_global.bottom():
                    painter.drawLine(
                        local_intersection.left(),
                        self.height() - 1,
                        local_intersection.right(),
                        self.height() - 1
                    )

                if intersection.left() == parent_rect_global.left():
                    painter.drawLine(
                        0,
                        local_intersection.top(),
                        0,
                        local_intersection.bottom()
                    )

                if intersection.right() == parent_rect_global.right():
                    painter.drawLine(
                        self.width() - 1,
                        local_intersection.top(),
                        self.width() - 1,
                        local_intersection.bottom()
                    )

class WindowManager:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = WindowManager()
        return cls._instance

    def __init__(self):
        self.windows = []
        self.position_timer = QTimer()
        self.position_timer.timeout.connect(self.check_window_positions)
        self.position_timer.start(100)

    def add_window(self, window):
        self.windows.append(window)
        self.update_active_window_outline()

    def remove_window(self, window):
        if window in self.windows:
            self.windows.remove(window)
        self.update_active_window_outline()

    def update_active_window_outline(self):
        active_window = QApplication.activeWindow()
        for window in self.windows:
            if hasattr(window, 'outline_widget'):
                if window is active_window:
                    window.outline_widget.update_position()
                    window.outline_widget.show()
                    window.outline_widget.raise_()
                else:
                    window.outline_widget.hide()

    def check_window_positions(self):
        for window in self.windows:
            if hasattr(window, 'outline_widget') and window.isActiveWindow():
                window.outline_widget.update_position()


class WindowAbs(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(750)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.outline_widget = OutlineWidget(None, WindowManager.instance())
        self.outline_widget.parent_window = self
        self.outline_widget.update_position()
        self.outline_widget.hide()

        WindowManager.instance().add_window(self)

        self.title_bar = CustomTitleBar(self)
        self.setMenuWidget(self.title_bar)
        self.action_bar = CustomActionBar(self)
        self.title_bar.hLayout.insertWidget(0, self.action_bar)
        self.pointMode = None

        self.corner_radius = 20
        self.background_color = QColor(45, 45, 45)
        self.border_color = QColor(80, 80, 80)
        self.border_width = 2

        self.centralWidget = QWidget()
        self.centralWidget.setObjectName("contentArea")
        super().setCentralWidget(self.centralWidget)
        self.centralLayout = QHBoxLayout(self.centralWidget)
        self.selectCentralWidget = QWidget()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkMousePos)
        self.timer.start(10)

    def setCentralWidget(self, widget):
        if self.selectCentralWidget:
            self.selectCentralWidget.deleteLater()
        self.selectCentralWidget = widget
        self.centralLayout.addWidget(self.selectCentralWidget)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect())
        radius = self.corner_radius

        path = QPainterPath()
        path.moveTo(rect.left(), rect.top() + radius)
        path.quadTo(rect.left(), rect.top(), rect.left() + radius, rect.top())
        path.lineTo(rect.right() - radius, rect.top())
        path.quadTo(rect.right(), rect.top(), rect.right(), rect.top() + radius)
        path.lineTo(rect.right(), rect.bottom() - radius)
        path.quadTo(rect.right(), rect.bottom(), rect.right() - radius, rect.bottom())
        path.lineTo(rect.left() + radius, rect.bottom())
        path.quadTo(rect.left(), rect.bottom(), rect.left(), rect.bottom() - radius)
        path.lineTo(rect.left(), rect.top() + radius)

        painter.setBrush(QBrush(self.background_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)

    def checkMousePos(self):
        direct = self.getDirectionMousePos()
        if direct in ["top_right", "bottom_left"]:
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif direct in ["top_left", "bottom_right"]:
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif direct in ["right", "left"]:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif direct in ["top", "bottom"]:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        if self.action_bar.is_expanded:
            self.title_bar.title.setVisible(not self.geometry().width() < 850)
        elif not self.action_bar.is_expanded:
            self.title_bar.title.setVisible(True)

    def getDirectionMousePos(self):
        pos = self.mapFromGlobal(QCursor.pos())
        pointMode = None
        if self.isMaximized():
            return None
        if pos.x() > self.width() - 10 and pos.y() < 10:
            pointMode = "top_right"
        elif pos.x() < 10 and pos.y() < 10:
            pointMode = "top_left"
        elif pos.y() < 10:
            pointMode = "top"
        elif pos.x() > self.width() - 10 and pos.y() > self.height() - 10:
            pointMode = "bottom_right"
        elif pos.x() < 10 and pos.y() > self.height() - 10:
            pointMode = "bottom_left"
        elif pos.y() > self.height() - 10:
            pointMode = "bottom"
        elif pos.x() > self.width() - 10:
            pointMode = "right"
        elif pos.x() < 10:
            pointMode = "left"
        return pointMode

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pointMode = self.getDirectionMousePos()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.pointMode = None
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        geometry = self.geometry()
        moveMode = ['top_right', 'top_left', 'bottom_right', 'bottom_left', 'right', 'left', 'bottom', 'top']
        if self.pointMode in moveMode:
            if self.pointMode == "top_right":
                geometry.setTopRight(QCursor.pos())
            elif self.pointMode == "top_left":
                geometry.setTopLeft(QCursor.pos())
            elif self.pointMode == "bottom_right":
                geometry.setBottomRight(QCursor.pos())
            elif self.pointMode == "bottom_left":
                geometry.setBottomLeft(QCursor.pos())
            elif self.pointMode == "top":
                geometry.setTop(QCursor.pos().y())
            elif self.pointMode == "bottom":
                geometry.setBottom(QCursor.pos().y())
            elif self.pointMode == "right":
                geometry.setRight(QCursor.pos().x())
            elif self.pointMode == "left":
                geometry.setLeft(QCursor.pos().x())
            self.setGeometry(geometry)
        super().mouseMoveEvent(event)

    def setWindowTitle(self, title):
        self.title_bar.title.setText(title)
        return super().setWindowTitle(title)

    def closeEvent(self, event):
        # WindowManager.instance().remove_window(self)
        self.outline_widget.close()
        super().closeEvent(event)

    def moveEvent(self, event):
        super().moveEvent(event)
        self.outline_widget.update_position()
        WindowManager.instance().update_active_window_outline()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.outline_widget.update_position()
        WindowManager.instance().update_active_window_outline()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.Type.ActivationChange:
            WindowManager.instance().update_active_window_outline()
            self.outline_widget.update_position()


class DialogAbs(QDialog):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(750)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.action_bar = CustomTitleBar(self)
        self.main_layout.addWidget(self.action_bar)

        self.central_widget = QWidget()
        self.central_layout = QHBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.central_widget)

        self.pointMode = None
        self.dragPos = QPoint()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkMousePos)
        self.timer.start(10)

    def setCentralWidget(self, widget):
        self.central_layout.addWidget(widget)

    def checkMousePos(self):
        direct = self.getDirectionMousePos()
        cursor_map = {
            "top_right": Qt.CursorShape.SizeBDiagCursor,
            "bottom_left": Qt.CursorShape.SizeBDiagCursor,
            "top_left": Qt.CursorShape.SizeFDiagCursor,
            "bottom_right": Qt.CursorShape.SizeFDiagCursor,
            "right": Qt.CursorShape.SizeHorCursor,
            "left": Qt.CursorShape.SizeHorCursor,
            "top": Qt.CursorShape.SizeVerCursor,
            "bottom": Qt.CursorShape.SizeVerCursor
        }
        self.setCursor(cursor_map.get(direct, Qt.CursorShape.ArrowCursor))

    def getDirectionMousePos(self):
        pos = self.mapFromGlobal(QCursor.pos())
        if self.isMaximized():
            return None

        margin = 10
        width = self.width()
        height = self.height()

        if pos.x() > width - margin and pos.y() < margin:
            return "top_right"
        elif pos.x() < margin and pos.y() < margin:
            return "top_left"
        elif pos.y() < margin:
            return "top"
        elif pos.x() > width - margin and pos.y() > height - margin:
            return "bottom_right"
        elif pos.x() < margin and pos.y() > height - margin:
            return "bottom_left"
        elif pos.y() > height - margin:
            return "bottom"
        elif pos.x() > width - margin:
            return "right"
        elif pos.x() < margin:
            return "left"
        return None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pointMode = self.getDirectionMousePos()
            self.dragPos = event.position().toPoint()

            if self.action_bar.geometry().contains(event.pos()) and self.pointMode is None:
                self.pointMode = "move"

    def mouseReleaseEvent(self, event):
        self.pointMode = None

    def mouseMoveEvent(self, event: QMouseEvent):
        geometry = self.geometry()
        pos = event.globalPosition().toPoint()

        if self.pointMode == "move":
            new_pos = pos - self.dragPos
            self.move(new_pos)
        elif self.pointMode == "top_right":
            geometry.setTopRight(pos)
            self.setGeometry(geometry)
        elif self.pointMode == "top_left":
            geometry.setTopLeft(pos)
            self.setGeometry(geometry)
        elif self.pointMode == "bottom_right":
            geometry.setBottomRight(pos)
            self.setGeometry(geometry)
        elif self.pointMode == "bottom_left":
            geometry.setBottomLeft(pos)
            self.setGeometry(geometry)
        elif self.pointMode == "top":
            geometry.setTop(pos.y())
            self.setGeometry(geometry)
        elif self.pointMode == "bottom":
            geometry.setBottom(pos.y())
            self.setGeometry(geometry)
        elif self.pointMode == "right":
            geometry.setRight(pos.x())
            self.setGeometry(geometry)
        elif self.pointMode == "left":
            geometry.setLeft(pos.x())
            self.setGeometry(geometry)

    def setWindowTitle(self, title):
        if hasattr(self.action_bar, 'set_title'):
            self.action_bar.set_title(title)
        super().setWindowTitle(title)
