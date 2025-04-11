import sys
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QPoint
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QListWidget, QListWidgetItem,
    QWidget, QVBoxLayout, QPushButton, QMenu, QMessageBox,
    QHBoxLayout, QStyle, QToolButton, QLabel
)
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor, QCursor, QPixmap

from UI import Language


class ProjectActionMenu(QMenu):
    action_triggered = pyqtSignal(str)

    def __init__(self, project_name, parent=None):
        super().__init__(parent)
        self.project_name = project_name
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        actions = {
            "open": Language.Lang.Launcher.ActionsPanel.open,
            "open_dir": Language.Lang.Launcher.ActionsPanel.open_dir,
            "delete": Language.Lang.Launcher.ActionsPanel.delete
        }

        for action_id, text in actions.items():
            action = QAction(text, self)
            action.triggered.connect(lambda _, a=action_id: self.emit_action(a))
            self.addAction(action)

    def emit_action(self, action_id):
        self.action_triggered.emit(action_id)


class ProjectItemWidget(QWidget):
    action_requested = pyqtSignal(dict, str)

    def __init__(self, name, icon=None, data=None, parent=None):
        super().__init__(parent)
        self.data = data if data is not None else {}
        self.data.setdefault('name', name)

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)

        self.icon_label = QLabel()
        self.set_icon(icon or QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon))
        layout.addWidget(self.icon_label)

        self.label = QLabel(name)
        self.menu_btn = QToolButton()
        self.menu_btn.setIcon(QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_FileDialogDetailedView))
        self.menu_btn.setFixedSize(24, 24)
        self.menu_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.menu_btn.setStyleSheet("QToolButton::menu-indicator { image: none; }")

        self.action_menu = ProjectActionMenu(self.data['name'])
        self.action_menu.action_triggered.connect(self.handle_menu_action)
        self.menu_btn.setMenu(self.action_menu)

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.menu_btn)
        self.setLayout(layout)

    def set_icon(self, icon):
        if isinstance(icon, QIcon):
            self.icon_label.setPixmap(icon.pixmap(24, 24))
        elif isinstance(icon, QPixmap):
            self.icon_label.setPixmap(icon.scaled(24, 24))

    def handle_menu_action(self, action_id):
        self.action_requested.emit(self.data, action_id)


class LauncherWindow(QMainWindow):
    settings_clicked = pyqtSignal()
    import_project_clicked = pyqtSignal()
    create_project_clicked = pyqtSignal()
    project_open_clicked = pyqtSignal(dict)
    project_open_dir_clicked = pyqtSignal(dict)
    project_delete_clicked = pyqtSignal(dict)
    close_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Launcher")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        widget = QWidget()
        self.v = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        toolbar = QHBoxLayout()
        self.v.addLayout(toolbar)
        self.setup_toolbar_buttons(toolbar)

        self.project_list = QListWidget()
        self.project_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.project_list.customContextMenuRequested.connect(self.show_context_menu)
        self.project_list.itemDoubleClicked.connect(self.handle_double_click)
        self.v.addWidget(self.project_list)

    def setup_toolbar_buttons(self, toolbar):
        self.settings_btn = QToolButton()
        self.settings_btn.setText(Language.Lang.Launcher.ActionsPanel.settings)
        self.settings_btn.clicked.connect(self.settings_clicked)

        self.import_btn = QToolButton()
        self.import_btn.setText(Language.Lang.Launcher.ActionsPanel.imp_proj)
        self.import_btn.clicked.connect(self.import_project_clicked)

        self.create_btn = QToolButton()
        self.create_btn.setText(Language.Lang.Launcher.ActionsPanel.crt_proj)
        self.create_btn.clicked.connect(self.create_project_clicked)

        toolbar.addWidget(self.settings_btn)
        toolbar.addWidget(self.import_btn)
        toolbar.addWidget(self.create_btn)

    def add_project(self, name, icon=None, data=None):
        data = data if data is not None else {}
        data['name'] = name
        item = QListWidgetItem()
        widget = ProjectItemWidget(name, icon=icon, data=data)
        widget.action_requested.connect(self.handle_project_action)
        item.setSizeHint(widget.sizeHint())
        self.project_list.addItem(item)
        self.project_list.setItemWidget(item, widget)

    def show_context_menu(self, pos):
        item = self.project_list.itemAt(pos)
        if item:
            widget = self.project_list.itemWidget(item)
            menu = ProjectActionMenu(widget.data['name'])
            menu.action_triggered.connect(
                lambda action_id: widget.handle_menu_action(action_id))
            menu.exec(QCursor.pos())

    def handle_project_action(self, data, action_id):
        if action_id == "delete":
            self.handle_delete_project(data)
        elif action_id == "open":
            self.project_open_clicked.emit(data)
        elif action_id == "open_dir":
            self.project_open_dir_clicked.emit(data)

    def handle_double_click(self, item):
        widget = self.project_list.itemWidget(item)
        if widget:
            self.project_open_clicked.emit(widget.data)

    def handle_delete_project(self, data):
        confirm = QMessageBox(
            QMessageBox.Icon.Question,
            Language.Lang.Launcher.Dialog.confirm_action,
            Language.Lang.Launcher.Dialog.delete_project_from_list.format(name=data.get('name', '')),
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.No,
            self
        )
        confirm.button(QMessageBox.StandardButton.Ok).setText(Language.Lang.Launcher.Dialog.act_del_from_project_list)
        confirm.button(QMessageBox.StandardButton.No).setText(Language.Lang.Launcher.Dialog.cancel)

        if confirm.exec() == QMessageBox.StandardButton.Yes:
            self.remove_project(data)
            self.project_delete_clicked.emit(data)

    def remove_project(self, data):
        for i in range(self.project_list.count()):
            item = self.project_list.item(i)
            widget = self.project_list.itemWidget(item)
            if widget.data == data:
                self.project_list.takeItem(i)
                break

    def closeEvent(self, event):
        self.close_signal.emit()
        event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 215, 0))
    palette.setColor(QPalette.ColorRole.Button, QColor(51, 51, 51))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 215, 0))
    app.setPalette(palette)

    window = LauncherWindow()

    window.settings_clicked.connect(lambda: print("Настройки clicked"))
    window.import_project_clicked.connect(lambda: print("Импорт проекта clicked"))
    window.create_project_clicked.connect(lambda: print("Создать проект clicked"))
    window.project_open_clicked.connect(lambda data: print(f"Открыть проект: {data}"))
    window.project_open_dir_clicked.connect(lambda data: print(f"Открыть папку: {data}"))
    window.project_delete_clicked.connect(lambda data: print(f"Удалить проект: {data}"))

    window.show()
    sys.exit(app.exec())