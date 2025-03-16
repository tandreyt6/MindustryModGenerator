from PyQt6.QtWidgets import (QDialog, QHBoxLayout, QScrollArea, QWidget, QVBoxLayout,
                             QListWidget, QStackedWidget, QLabel, QSpacerItem,
                             QSizePolicy, QFrame)
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty


class PluginWidget(QWidget):
    def __init__(self, name, icon_path, description):
        super().__init__()
        self.is_expanded = False
        self.description = description
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.setStyleSheet("""QWidget {
        border: 1px solid #606060;
        border-radius: 4px;
        background-color: #606060;
    }""")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.header = QWidget()
        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(0, 0, 0, 0)

        self.icon_label = QLabel()
        if icon_path:
            pixmap = QPixmap(icon_path).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio)
            self.icon_label.setPixmap(pixmap)
        self.header_layout.addWidget(self.icon_label)

        self.title_label = QLabel(name)
        self.title_label.setObjectName("title")
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.arrow_label = QLabel()
        self.arrow_label.setPixmap(QPixmap(":/icons/down-arrow.png").scaled(16, 16))
        self.header_layout.addWidget(self.arrow_label)
        self.main_layout.addWidget(self.header)

        self.description_widget = QWidget()
        self.description_layout = QVBoxLayout(self.description_widget)
        self.description_label = QLabel(description)
        self.description_label.setWordWrap(True)
        self.description_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.description_widget)

        self.animation = QPropertyAnimation(self.description_widget, b"maximumHeight")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.description_widget.setMaximumHeight(0)
        self.description_widget.hide()

    def toggle_expansion(self):
        self.is_expanded = not self.is_expanded
        start = 0 if self.is_expanded else self.description_widget.sizeHint().height()
        end = self.description_widget.sizeHint().height() if self.is_expanded else 0
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.arrow_label.setPixmap(
            QPixmap(":/icons/up-arrow.png" if self.is_expanded else ":/icons/down-arrow.png").scaled(16, 16))
        if self.is_expanded: self.description_widget.show()
        self.animation.start()

    def mousePressEvent(self, event):
        self.toggle_expansion()
        super().mousePressEvent(event)


class SettingsWindow(QDialog):
    def __init__(self, plugins_data=None):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 800, 600)
        self.plugins_data = plugins_data or {}
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.left_panel = QListWidget()
        self.left_panel.setFixedWidth(180)
        self.left_panel.addItems(["General", "Plugins", "Code Editor", "Appearance"])
        self.left_panel.currentRowChanged.connect(self.change_page)
        main_layout.addWidget(self.left_panel)

        self.right_panel = QStackedWidget()
        main_layout.addWidget(self.right_panel)

        self.right_panel.addWidget(self.create_general_page())
        self.right_panel.addWidget(self.create_plugins_page())
        self.right_panel.addWidget(self.create_code_editor_page())
        self.right_panel.addWidget(self.create_appearance_page())

    def create_plugins_page(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)

        for name, data in self.plugins_data.items():
            plugin_widget = PluginWidget(
                name=name,
                icon_path=data.get("icon", ""),
                description=data.get("description", "")
            )
            layout.addWidget(plugin_widget)

        scroll_area.setWidget(container)
        return scroll_area

    def create_general_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("General Settings"))
        return page

    def create_code_editor_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Code Editor Settings"))
        return page

    def create_appearance_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Appearance Settings"))
        return page

    def change_page(self, index):
        self.right_panel.setCurrentIndex(index)