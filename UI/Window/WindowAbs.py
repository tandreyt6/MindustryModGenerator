from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout,
    QPushButton, QApplication, QLabel,
    QSizeGrip, QVBoxLayout, QFrame, QToolButton, QMenu, QDialog, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QPoint, QRect, QEvent, QVariantAnimation, QEasingCurve, QTimer, QSize, QPointF, QRectF, \
    QParallelAnimationGroup, QPropertyAnimation, QSequentialAnimationGroup
from PyQt6.QtGui import QMouseEvent, QResizeEvent, QAction, QCursor, QPainterPath, QPainter, QColor, QBrush, QPen

from UI.Window.WindowsAbstractWindow import WindowsFramelessWindow


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
    def __init__(self, parent=None, spacing=5):
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
        self.actions_layout.setSpacing(spacing)
        self.actions_container.setFixedWidth(0)

        self.hLayout.addWidget(self.toggle_button)
        self.hLayout.addWidget(self.actions_container)
        self.hLayout.addStretch()

        self.is_expanded = False
        self.animation = None
        self.action_buttons = []

    def addAction(self, action, icon=None):
        self.toggle_button.setVisible(True)

        if isinstance(action, QAction):
            button = QToolButton()
            button.setDefaultAction(action)
        elif isinstance(action, QMenu):
            button = QPushButton(action.title())
            if icon:
                button.setIcon(icon)
            button.setMenu(action)
        else:
            raise ValueError("Action must be QAction or QMenu")

        button.setFixedSize(100, 28)
        button.setObjectName("ActionPanelButton")
        button.setVisible(False)
        self.actions_layout.addWidget(button)
        self.action_buttons.append(button)

    def expand(self):
        desired_width = (100 + self.actions_layout.spacing()) * len(self.action_buttons)
        desired_width = max(desired_width, 100)

        self.actions_container.setMinimumWidth(desired_width)
        self.actions_container.setMaximumWidth(desired_width)

        self.animation = QVariantAnimation(self)
        self.animation.setStartValue(self.actions_container.width())
        self.animation.setEndValue(desired_width)
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.Type.OutExpo)
        self.animation.valueChanged.connect(lambda value: self.actions_container.setFixedWidth(int(value)))
        QTimer.singleShot(0, self.animation.start)

        for btn in self.action_buttons:
            btn.setVisible(True)
            effect = QGraphicsOpacityEffect(btn)
            btn.setGraphicsEffect(effect)
            effect.setOpacity(0)

        group = QSequentialAnimationGroup(self)
        for i, btn in enumerate(self.action_buttons):
            opacity_anim = QPropertyAnimation(btn.graphicsEffect(), b"opacity")
            opacity_anim.setDuration(100)
            opacity_anim.setStartValue(0)
            opacity_anim.setEndValue(1)
            opacity_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
            group.addAnimation(opacity_anim)

        QTimer.singleShot(200, group.start)

        self.is_expanded = True

    def collapse(self):
        current_width = self.actions_container.width()
        self.animation = QVariantAnimation(self)
        self.animation.setStartValue(current_width)
        self.animation.setEndValue(0)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.InExpo)
        self.animation.valueChanged.connect(lambda value: self.actions_container.setFixedWidth(int(value)))
        QTimer.singleShot(0, self.animation.start)

        for btn in self.action_buttons:
            btn.setVisible(False)

        self.is_expanded = False

    def toggle_actions(self):
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

class WindowAbs(WindowsFramelessWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(750)
        self.action_bar = CustomActionBar(self)
        self._titleBar.hBoxLayout.insertWidget(2, self.action_bar, 0, Qt.AlignmentFlag.AlignLeft)
        # self.titleBar.iconLabel.setVisible(False)

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
