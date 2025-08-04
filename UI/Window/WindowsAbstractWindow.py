# coding:utf-8
import ctypes
import sys
from enum import Enum
from ctypes import POINTER, Structure, byref, c_bool, c_int, pointer, sizeof, WinDLL, cast
from ctypes.wintypes import BOOL, DWORD, HWND, LONG, LPCVOID, POINT, UINT, ULONG, HRGN, LPRECT, MSG
import win32api
import win32con
import win32gui
from PyQt6.QtCore import QFile, QPointF, QRectF, Qt, QEvent, QSize, QRect, pyqtProperty, QTimer
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QPen, QIcon, QCursor, QCloseEvent
from PyQt6.QtWidgets import QApplication, QWidget, QAbstractButton, QLabel, QHBoxLayout, QMainWindow, QVBoxLayout, \
    QSizePolicy
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtXml import QDomDocument

# Enumerations and Structures
class WINDOWCOMPOSITIONATTRIB(Enum):
    WCA_UNDEFINED = 0
    WCA_NCRENDERING_ENABLED = 1
    WCA_NCRENDERING_POLICY = 2
    WCA_TRANSITIONS_FORCEDISABLED = 3
    WCA_ALLOW_NCPAINT = 4
    WCA_CAPTION_BUTTON_BOUNDS = 5
    WCA_NONCLIENT_RTL_LAYOUT = 6
    WCA_FORCE_ICONIC_REPRESENTATION = 7
    WCA_EXTENDED_FRAME_BOUNDS = 8
    WCA_HAS_ICONIC_BITMAP = 9
    WCA_THEME_ATTRIBUTES = 10
    WCA_NCRENDERING_EXILED = 11
    WCA_NCADORNMENTINFO = 12
    WCA_EXCLUDED_FROM_LIVEPREVIEW = 13
    WCA_VIDEO_OVERLAY_ACTIVE = 14
    WCA_FORCE_ACTIVEWINDOW_APPEARANCE = 15
    WCA_DISALLOW_PEEK = 16
    WCA_CLOAK = 17
    WCA_CLOAKED = 18
    WCA_ACCENT_POLICY = 19
    WCA_FREEZE_REPRESENTATION = 20
    WCA_EVER_UNCLOAKED = 21
    WCA_VISUAL_OWNER = 22
    WCA_HOLOGRAPHIC = 23
    WCA_EXCLUDED_FROM_DDA = 24
    WCA_PASSIVEUPDATEMODE = 25
    WCA_USEDARKMODECOLORS = 26
    WCA_CORNER_STYLE = 27
    WCA_PART_COLOR = 28
    WCA_DISABLE_MOVESIZE_FEEDBACK = 29
    WCA_LAST = 30

class ACCENT_STATE(Enum):
    ACCENT_DISABLED = 0
    ACCENT_ENABLE_GRADIENT = 1
    ACCENT_ENABLE_TRANSPARENTGRADIENT = 2
    ACCENT_ENABLE_BLURBEHIND = 3
    ACCENT_ENABLE_ACRYLICBLURBEHIND = 4
    ACCENT_ENABLE_HOSTBACKDROP = 5
    ACCENT_INVALID_STATE = 6

class DWMNCRENDERINGPOLICY(Enum):
    DWMNCRP_USEWINDOWSTYLE = 0
    DWMNCRP_DISABLED = 1
    DWMNCRP_ENABLED = 2
    DWMNCRP_LAS = 3

class DWMWINDOWATTRIBUTE(Enum):
    DWMWA_NCRENDERING_ENABLED = 1
    DWMWA_NCRENDERING_POLICY = 2
    DWMWA_TRANSITIONS_FORCEDISABLED = 3
    DWMWA_ALLOW_NCPAINT = 4
    DWMWA_CAPTION_BUTTON_BOUNDS = 5
    DWMWA_NONCLIENT_RTL_LAYOUT = 6
    DWMWA_FORCE_ICONIC_REPRESENTATION = 7
    DWMWA_FLIP3D_POLICY = 8
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    DWMWA_HAS_ICONIC_BITMAP = 10
    DWMWA_DISALLOW_PEEK = 11
    DWMWA_EXCLUDED_FROM_PEEK = 12
    DWMWA_CLOAK = 13
    DWMWA_CLOAKED = 14
    DWMWA_FREEZE_REPRESENTATION = 15
    DWMWA_PASSIVE_UPDATE_MODE = 16
    DWMWA_USE_HOSTBACKDROPBRUSH = 17
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    DWMWA_BORDER_COLOR = 34
    DWMWA_CAPTION_COLOR = 35
    DWMWA_TEXT_COLOR = 36
    DWMWA_VISIBLE_FRAME_BORDER_THICKNESS = 37
    DWMWA_SYSTEMBACKDROP_TYPE = 38
    DWMWA_LAST = 39

class RECT(Structure):
    _fields_ = [
        ('left', LONG),
        ('top', LONG),
        ('right', LONG),
        ('bottom', LONG)
    ]


class DWM_BLURBEHIND(Structure):
    _fields_ = [
        ('dwFlags',                DWORD),
        ('fEnable',                BOOL),
        ('hRgnBlur',               HRGN),
        ('fTransitionOnMaximized', BOOL),
    ]

# Utility Functions
def isMaximized(hWnd):
    placement = win32gui.GetWindowPlacement(hWnd)
    return placement[1] == win32con.SW_SHOWMAXIMIZED

def isFullScreen(hWnd):
    rect = win32gui.GetWindowRect(hWnd)
    screen_rect = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
    return rect == screen_rect

def getResizeBorderThickness(hWnd, isHorizontal):
    if isHorizontal:
        return win32api.GetSystemMetrics(win32con.SM_CXFRAME)
    return win32api.GetSystemMetrics(win32con.SM_CYFRAME)

def toggleMaxState(window):
    hwnd = int(window.winId())
    if window.isMaximized():
        win32gui.PostMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    else:
        win32gui.PostMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)

class Taskbar:
    AUTO_HIDE_THICKNESS = 2

    @staticmethod
    def isAutoHide():
        return False

    @staticmethod
    def getPosition(hWnd):
        return "bottom"

def isSystemBorderAccentEnabled():
    return True

def getSystemAccentColor():
    return QColor(0, 120, 215)

def isGreaterEqualWin10():
    return sys.getwindowsversion().major >= 10

def isGreaterEqualWin11():
    return sys.getwindowsversion().major >= 10 and sys.getwindowsversion().build >= 22000

def IsCompositionEnabled():
    return True

class ACCENT_POLICY(Structure):
    _fields_ = [
        ("AccentState", DWORD),
        ("AccentFlags", DWORD),
        ("GradientColor", DWORD),
        ("AnimationId", DWORD),
    ]

class WINDOWCOMPOSITIONATTRIBDATA(Structure):
    _fields_ = [
        ("Attribute", DWORD),
        ("Data", POINTER(ACCENT_POLICY)),
        ("SizeOfData", ULONG),
    ]

class MARGINS(Structure):
    _fields_ = [
        ("cxLeftWidth", c_int),
        ("cxRightWidth", c_int),
        ("cyTopHeight", c_int),
        ("cyBottomHeight", c_int),
    ]

class NCCALCSIZE_PARAMS(Structure):
    _fields_ = [
        ('rgrc', RECT * 3),
        ('lppos', c_int)
    ]

LPNCCALCSIZE_PARAMS = POINTER(NCCALCSIZE_PARAMS)

def isSystemBorderAccentEnabled():
    return True

def getSystemAccentColor():
    return QColor(0, 120, 215)

class WindowsWindowEffect:
    def __init__(self, window):
        self.window = window
        self.user32 = WinDLL("user32")
        self.dwmapi = WinDLL("dwmapi")
        self.SetWindowCompositionAttribute = self.user32.SetWindowCompositionAttribute
        self.DwmExtendFrameIntoClientArea = self.dwmapi.DwmExtendFrameIntoClientArea
        self.DwmSetWindowAttribute = self.dwmapi.DwmSetWindowAttribute

        self.SetWindowCompositionAttribute.restype = c_bool
        self.DwmExtendFrameIntoClientArea.restype = LONG
        self.DwmSetWindowAttribute.restype = LONG
        self.SetWindowCompositionAttribute.argtypes = [c_int, POINTER(WINDOWCOMPOSITIONATTRIBDATA)]
        self.DwmExtendFrameIntoClientArea.argtypes = [c_int, POINTER(MARGINS)]
        self.DwmSetWindowAttribute.argtypes = [c_int, DWORD, LPCVOID, DWORD]

        self.accentPolicy = ACCENT_POLICY()
        self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        self.winCompAttrData.Attribute = 19  # WCA_ACCENT_POLICY
        self.winCompAttrData.SizeOfData = sizeof(self.accentPolicy)
        self.winCompAttrData.Data = pointer(self.accentPolicy)

    def getResizeBorderThickness(self, hWnd, isHorizontal):
        if isHorizontal:
            return win32api.GetSystemMetrics(win32con.SM_CXFRAME)
        return win32api.GetSystemMetrics(win32con.SM_CYFRAME)

    def moveWindow(self, hwnd):
        hwnd = int(hwnd)
        release_capture = ctypes.windll.user32.ReleaseCapture
        send_message = ctypes.windll.user32.SendMessageW
        release_capture()
        send_message(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MOVE + win32con.HTCAPTION, 0)

    def addWindowAnimation(self, hWnd):
        hWnd = int(hWnd)
        style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            hWnd,
            win32con.GWL_STYLE,
            style | win32con.WS_MINIMIZEBOX | win32con.WS_MAXIMIZEBOX | win32con.WS_CAPTION | win32con.CS_DBLCLKS | win32con.WS_THICKFRAME
        )

    def addShadowEffect(self, hWnd):
        hWnd = int(hWnd)
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(hWnd, byref(margins))

    def setBorderAccentColor(self, hWnd, color):
        hWnd = int(hWnd)
        colorref = DWORD(color.red() | (color.green() << 8) | (color.blue() << 16))
        self.DwmSetWindowAttribute(hWnd, 34, byref(colorref), 4)  # DWMWA_BORDER_COLOR

    def removeBorderAccentColor(self, hWnd):
        hWnd = int(hWnd)
        self.DwmSetWindowAttribute(hWnd, 34, byref(DWORD(0xFFFFFFFF)), 4)

class TitleBarButtonState(Enum):
    NORMAL = 0
    HOVER = 1
    PRESSED = 2

class TitleBarButton(QAbstractButton):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setFixedSize(46, 32)
        self._state = TitleBarButtonState.NORMAL
        self._normalColor = QColor(0, 0, 0)
        self._hoverColor = QColor(0, 0, 0)
        self._pressedColor = QColor(0, 0, 0)
        self._normalBgColor = QColor(0, 0, 0, 0)
        self._hoverBgColor = QColor(0, 0, 0, 26)
        self._pressedBgColor = QColor(0, 0, 0, 51)

    def setState(self, state):
        self._state = state
        self.update()

    def isPressed(self):
        return self._state == TitleBarButtonState.PRESSED

    def _getColors(self):
        if self._state == TitleBarButtonState.NORMAL:
            return self._normalColor, self._normalBgColor
        elif self._state == TitleBarButtonState.HOVER:
            return self._hoverColor, self._hoverBgColor
        return self._pressedColor, self._pressedBgColor

    def setHoverColor(self, color):
        self._hoverColor = QColor(color)
        self.update()

    def setPressedColor(self, color):
        self._pressedColor = QColor(color)
        self.update()

    def setHoverBackgroundColor(self, color):
        self._hoverBgColor = QColor(color)
        self.update()

    def setPressedBackgroundColor(self, color):
        self._pressedBgColor = QColor(color)
        self.update()

    def enterEvent(self, e):
        self.setState(TitleBarButtonState.HOVER)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setState(TitleBarButtonState.NORMAL)
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() != Qt.MouseButton.LeftButton:
            return
        self.setState(TitleBarButtonState.PRESSED)
        super().mousePressEvent(e)


class MinimizeButton(TitleBarButton):
    def paintEvent(self, e):
        painter = QPainter(self)
        _, bgColor = self._getColors()

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(bgColor)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(Qt.GlobalColor.white, 1.3)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)


class MaximizeButton(TitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isMax = False

    def setMaxState(self, isMax):
        if self._isMax == isMax:
            return
        self._isMax = isMax
        self.setState(TitleBarButtonState.NORMAL)

    def paintEvent(self, e):
        painter = QPainter(self)
        _, bgColor = self._getColors()

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(bgColor)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(Qt.GlobalColor.white, 1.3)
        pen.setCosmetic(True)
        painter.setPen(pen)

        r = self.devicePixelRatioF()
        painter.scale(1 / r, 1 / r)

        if not self._isMax:
            painter.drawRect(int(18 * r), int(11 * r), int(10 * r), int(10 * r))
        else:
            painter.drawRect(int(18 * r), int(13 * r), int(8 * r), int(8 * r))

            x0 = int(18 * r) + int(2 * r)
            y0 = int(13 * r) - int(2 * r)
            painter.drawRect(x0, y0, int(8 * r), int(8 * r))


class CloseButton(TitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHoverBackgroundColor(QColor(232, 17, 35))
        self.setPressedBackgroundColor(QColor(241, 112, 122))

    def paintEvent(self, e):
        painter = QPainter(self)
        _, bgColor = self._getColors()

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), bgColor)

        pen = QPen(Qt.GlobalColor.white, 1.3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        w, h = self.width(), self.height()
        center_x = w // 2
        center_y = h // 2
        size = 4
        painter.drawLine(center_x - size, center_y - size,
                         center_x + size, center_y + size)
        painter.drawLine(center_x + size, center_y - size,
                         center_x - size, center_y + size)

class TitleBarBase(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.minBtn = MinimizeButton(parent=self)
        self.closeBtn = CloseButton(parent=self)
        self.maxBtn = MaximizeButton(parent=self)
        self._isDoubleClickEnabled = True
        self.resize(200, 32)
        self.setFixedHeight(32)
        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.closeBtn.clicked.connect(self.window().close)
        self.window().installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.window() and e.type() == QEvent.Type.WindowStateChange:
            self.window().updateWindowState()
            return False
        return super().eventFilter(obj, e)

    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton or not self._isDoubleClickEnabled:
            return
        self.__toggleMaxState()

    def mouseMoveEvent(self, e):
        if sys.platform != "win32" or not self.canDrag(e.pos()):
            return
        self.window().windowEffect.moveWindow(self.window().winId())

    def mousePressEvent(self, e):
        if sys.platform == "win32" or not self.canDrag(e.pos()):
            return
        self.window().windowEffect.moveWindow(self.window().winId())

    def __toggleMaxState(self):
        toggleMaxState(self.window())
        self.window().updateWindowState()

    def _isDragRegion(self, pos):
        width = sum(btn.width() for btn in self.findChildren(TitleBarButton) if btn.isVisible())
        return 0 < pos.x() < self.width() - width

    def _hasButtonPressed(self):
        return any(btn.isPressed() for btn in self.findChildren(TitleBarButton))

    def canDrag(self, pos):
        return self._isDragRegion(pos) and not self._hasButtonPressed()

class TitleBar(TitleBarBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignmentFlag.AlignRight)

class StandardTitleBar(TitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(25, 25)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.window().windowIconChanged.connect(self.setIcon)

        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px
            }
        """)
        self.window().windowTitleChanged.connect(self.setTitle)

        self.titleLabel.installEventFilter(self)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.Resize or event.type() == event.Type.LayoutRequest:
            if obj in (self, self.titleLabel):
                self.adjustTitleVisibility()
        return super().eventFilter(obj, event)

    def adjustTitleVisibility(self):
        if self.titleLabel.pos().x() > self.width()*2//3:
            self.titleLabel.setFixedWidth(1)
        else:
            self.titleLabel.setMaximumWidth(200)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(25, 25))

class WindowsFramelessWindow(QMainWindow):
    BORDER_WIDTH = 8

    def __init__(self, parent=None):
        super().__init__(parent)
        self.windowEffect = WindowsWindowEffect(self)
        self._titleBar = StandardTitleBar(self)
        self._isResizeEnabled = True

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.windowEffect.addWindowAnimation(self.winId())
        self.windowEffect.addShadowEffect(self.winId())

        self.setMinimumSize(300, 200)
        self.resize(500, 500)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self._titleBar.setFixedHeight(32)
        main_layout.addWidget(self._titleBar, 0, Qt.AlignmentFlag.AlignTop)

        self.content_widget = QWidget(self)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(self.content_widget)

    def addContentWidget(self, widget):
        self.content_layout.addWidget(widget)

    def showMaximized(self):
        hwnd = int(self.winId())
        win32gui.PostMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
        self.updateWindowState()

    def showNormal(self):
        hwnd = int(self.winId())
        win32gui.PostMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        self.updateWindowState()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._titleBar.setFixedWidth(self.width())

    def nativeEvent(self, eventType, message):
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return False, 0

        if msg.message == win32con.WM_NCHITTEST and self._isResizeEnabled:
            xPos, yPos = win32gui.ScreenToClient(msg.hWnd, win32api.GetCursorPos())
            clientRect = win32gui.GetClientRect(msg.hWnd)
            w = clientRect[2] - clientRect[0]
            h = clientRect[3] - clientRect[1]
            bw = self.BORDER_WIDTH if not self.isMaximized() else 0
            lx = xPos < bw
            rx = xPos > w - bw
            ty = yPos < bw
            by = yPos > h - bw

            local_pos = self._titleBar.mapFromGlobal(QCursor.pos())
            child = self._titleBar.childAt(local_pos)
            title_bar_height = self._titleBar.height()

            if ty:
                if lx:
                    return True, win32con.HTTOPLEFT
                elif rx:
                    return True, win32con.HTTOPRIGHT
                else:
                    return True, win32con.HTTOP

            if yPos < title_bar_height:
                if child is not None:
                    return False, 0
                if self._titleBar.canDrag(local_pos):
                    return True, win32con.HTCAPTION
                return False, 0

            if lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
            elif by:
                return True, win32con.HTBOTTOM

        elif msg.message == win32con.WM_NCCALCSIZE:
            if self.isMaximized():
                return True, 0
            else:
                result = 0 if not msg.wParam else win32con.WVR_REDRAW
                return True, result
        elif msg.message == win32con.WM_SETFOCUS and isSystemBorderAccentEnabled():
            self.windowEffect.setBorderAccentColor(self.winId(), getSystemAccentColor())
            return True, 0
        elif msg.message == win32con.WM_KILLFOCUS:
            self.windowEffect.removeBorderAccentColor(self.winId())
            return True, 0
        return False, 0

    def updateWindowState(self):
        self.windowEffect.addShadowEffect(self.winId())
        self._titleBar.maxBtn.setMaxState(self.isMaximized())
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowsFramelessWindow()
    window.show()
    sys.exit(app.exec())