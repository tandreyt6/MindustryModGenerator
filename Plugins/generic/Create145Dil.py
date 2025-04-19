from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog
from .RoundedDialog import RoundedDialog


class ProjectDialog(RoundedDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создание нового проекта")
        self.setFixedSize(400, 250)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.name_label = QLabel("Название проекта:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название проекта")

        self.path_label = QLabel("Путь к проекту:")
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Выберите папку")
        self.path_button = QPushButton("Обзор...")
        self.path_button.clicked.connect(self.browse_path)

        self.package_label = QLabel("Пакет:")
        self.package_combo = QComboBox()
        self.package_combo.addItems(["com.example.mod", "org.example.mod", "net.example.mod"])

        button_layout = QHBoxLayout()
        self.create_button = QPushButton("Создать")
        self.create_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addWidget(self.name_label)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(self.path_label)
        main_layout.addWidget(self.path_input)
        main_layout.addWidget(self.path_button)
        main_layout.addWidget(self.package_label)
        main_layout.addWidget(self.package_combo)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, "Выберите папку для проекта")
        if path:
            self.path_input.setText(path)

    def get_project_data(self):
        return {
            "name": self.name_input.text(),
            "path": self.path_input.text(),
            "package": self.package_combo.currentText()
        }