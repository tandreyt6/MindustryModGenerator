import os
import subprocess

from PyQt6.QtWidgets import (QDialog, QHBoxLayout, QScrollArea, QWidget, QVBoxLayout,
                             QListWidget, QStackedWidget, QLabel, QSpacerItem,
                             QSizePolicy, QFrame, QFormLayout, QComboBox, QPushButton, QLineEdit, QMessageBox,
                             QFileDialog)
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, pyqtSignal

from GradlewManager import GradleWrapper
from UI import Language
from UI.Language import Langs
from UI.Style import ALL_THEMES
from UI.Window.WindowAbs import DialogAbs
from func import settings, memory


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


class SettingsWindow(DialogAbs):
    themeChanged = pyqtSignal(str)

    def __init__(self, plugins_data=None):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 800, 600)
        self.plugins_data = plugins_data or {}
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.main_layout.addLayout(main_layout)

        self.left_panel = QListWidget()
        self.left_panel.setFixedWidth(180)
        self.left_panel.addItems(["General", "Appearance", "Plugins", "Code Editor", "Java"])
        self.left_panel.currentRowChanged.connect(self.change_page)
        main_layout.addWidget(self.left_panel)

        self.right_panel = QStackedWidget()
        main_layout.addWidget(self.right_panel)

        self.right_panel.addWidget(self.create_general_page())
        self.right_panel.addWidget(self.create_appearance_page())
        self.right_panel.addWidget(self.create_plugins_page())
        self.right_panel.addWidget(self.create_code_editor_page())
        self.right_panel.addWidget(self.create_gradle_page())

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

    def selectLangEvent(self):
        lang = list(Langs.keys())[self.langSelect.currentIndex()]
        settings.save_data("lang", lang)
        self.changeWarn(Langs[lang][1])

    def changeWarn(self, lang):
        self.needRestartTitle.setText(lang.Settings.General.needRestart)
        self.needRestartTitle.setVisible(True)

    def create_general_page(self):
        page = QScrollArea()
        widget = QWidget()
        page.setWidget(widget)
        page.setWidgetResizable(True)
        layout = QFormLayout(widget)

        self.needRestartTitle = QLabel()
        self.needRestartTitle.setVisible(False)
        layout.addRow(self.needRestartTitle)

        self.langSelect = QComboBox()
        self.langSelect.addItems([_[1][0] for _ in Langs.items()])
        self.langSelect.currentIndexChanged.connect(self.selectLangEvent)
        layout.addRow("Select language:", self.langSelect)

        return page

    def create_code_editor_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Code Editor Settings"))
        return page

    def create_gradle_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Java Configuration")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        self.java_path_label = QLabel("Path: Not selected")
        self.java_path_label.setWordWrap(True)
        self.java_type_label = QLabel("Type: Unknown")
        self.java_version_label = QLabel("Version: Unknown")

        self.btn_choose_java = QPushButton("Select JDK Directory")
        self.btn_choose_java.clicked.connect(self._select_jdk)

        info_layout = QVBoxLayout()
        info_layout.addWidget(self.java_path_label)
        info_layout.addWidget(self.java_type_label)
        info_layout.addWidget(self.java_version_label)

        layout.addLayout(info_layout)
        layout.addWidget(self.btn_choose_java)

        self._load_java_settings()

        return page

    def _select_jdk(self):
        path = QFileDialog.getExistingDirectory(
            self,
            "Select Java Installation Directory",
            os.path.expanduser("~"),
            QFileDialog.Option.ShowDirsOnly
        )

        if path:
            valid, java_type, version = GradleWrapper.analyze_java_directory(path)

            if valid:
                self._update_java_ui(path, java_type, version)
                settings.save_data("java_home", path)
                os.environ['JAVA_HOME'] = path
            else:
                QMessageBox.warning(
                    self,
                    "Invalid Java",
                    "Selected directory does not contain valid JDK installation!"
                )

    def _update_java_ui(self, path, java_type, version):
        self.java_path_label.setText(f"Path: {path}")
        self.java_type_label.setText(f"Type: {java_type}")
        self.java_version_label.setText(f"Version: {version if version else 'Unknown'}")

    def _load_java_settings(self):
        saved_path = settings.get_data("java_home", "")
        if saved_path and os.path.exists(saved_path):
            valid, java_type, version = GradleWrapper.analyze_java_directory(saved_path)
            if valid:
                self._update_java_ui(saved_path, java_type, version)

    def create_appearance_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        label = QLabel("Select Theme:")
        layout.addWidget(label)

        self.theme_combo = QComboBox()
        for name in ALL_THEMES:
            self.theme_combo.addItem(name)
        layout.addWidget(self.theme_combo)

        self.theme_combo.currentTextChanged.connect(self.on_theme_selected)

        layout.addStretch()

        return page

    def on_theme_selected(self, index: str):
        self.themeChanged.emit(index)

    def change_page(self, index):
        self.right_panel.setCurrentIndex(index)
