from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout,
    QPushButton, QApplication, QLabel,
    QSizeGrip, QVBoxLayout, QFrame, QToolButton, QMenu
)
from PyQt6.QtCore import Qt, QPoint, QRect, QEvent, QVariantAnimation, QEasingCurve, QTimer, QSize
from PyQt6.QtGui import QMouseEvent, QResizeEvent, QAction, QCursor

from UI.Style import window_dark_style


class CustomTitleBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('CustomTitleBar')
        self.setStyleSheet(window_dark_style)
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
            btn.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF; border: none; border-radius: 4px;")
        self.btn_close.setStyleSheet("background-color: #D32F2F; border-radius: 4px;")
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
            button = QToolButton()
            button.setDefaultAction(action)
            button.setFixedSize(100, 28)
            button.setObjectName("ActionPanelButton")
            self.actions_layout.addWidget(button)
        elif isinstance(action, QMenu):
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
        self.animation.setEasingCurve(QEasingCurve.Type.InBack)
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


class WindowAbs(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.title_bar = CustomTitleBar(self)
        self.setMenuWidget(self.title_bar)
        self.action_bar = CustomActionBar(self)
        self.title_bar.hLayout.insertWidget(0, self.action_bar)
        self.pointMode = None

        self.centralWidget = QWidget()
        super().setCentralWidget(self.centralWidget)
        self.centralLayout = QHBoxLayout(self.centralWidget)
        self.selectCentralWidget = QWidget()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkMousePos)
        self.timer.start(10)

    def setCentralWidget(self, widget):
        if self.selectCentralWidget: self.selectCentralWidget.deleteLater()
        self.selectCentralWidget = widget
        self.centralLayout.addWidget(self.selectCentralWidget)

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

    def mouseReleaseEvent(self, event):
        self.pointMode = None

    def mouseMoveEvent(self, event: QMouseEvent):
        geometry = self.geometry()
        if self.pointMode == "top_right":
            geometry.setTopRight(QCursor.pos())
            self.setGeometry(geometry)
        elif self.pointMode == "top_left":
            geometry.setTopLeft(QCursor.pos())
            self.setGeometry(geometry)
        elif self.pointMode == "bottom_right":
            geometry.setBottomRight(QCursor.pos())
            self.setGeometry(geometry)
        elif self.pointMode == "bottom_left":
            geometry.setBottomLeft(QCursor.pos())
            self.setGeometry(geometry)
        elif self.pointMode == "top":
            geometry.setTop(QCursor.pos().y())
            self.setGeometry(geometry)
        elif self.pointMode == "bottom":
            geometry.setBottom(QCursor.pos().y())
            self.setGeometry(geometry)
        elif self.pointMode == "right":
            geometry.setRight(QCursor.pos().x())
            self.setGeometry(geometry)
        elif self.pointMode == "left":
            geometry.setLeft(QCursor.pos().x())
            self.setGeometry(geometry)

    def setWindowTitle(self, title):
        self.title_bar.title.setText(title)
        return super().setWindowTitle(title)


