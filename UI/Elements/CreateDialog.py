import sys
import os
import re
from PyQt6.QtWidgets import (
    QApplication, QDialog, QFormLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QComboBox, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt


class ProjectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.create = False
        self.setWindowTitle("Создание проекта")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.folder_line_edit = QLineEdit()
        self.browse_button = QPushButton("Выбрать папку")
        self.browse_button.clicked.connect(self.browse_folder)
        h0 = QHBoxLayout()
        h0.addWidget(self.folder_line_edit, 1)
        h0.addWidget(self.browse_button)
        layout.addRow("Локация:", h0)

        self.display_name_line_edit = QLineEdit()
        self.display_name_line_edit.textChanged.connect(self.update_project_name)
        layout.addRow("Отображаемое название:", self.display_name_line_edit)

        self.name_line_edit = QLineEdit()
        layout.addRow("Название проекта:", self.name_line_edit)

        self.package_line_edit = QLineEdit()
        layout.addRow("Пакет (например, example):", self.package_line_edit)

        self.author_line_edit = QLineEdit()
        layout.addRow("Автор:", self.author_line_edit)

        self.version_combo_box = QComboBox()
        self.version_combo_box.addItem("145")
        layout.addRow("Версия игры:", self.version_combo_box)

        self.create_button = QPushButton("Создать проект")
        self.create_button.clicked.connect(self.create_project)
        layout.addRow(self.create_button)

        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            self.folder_line_edit.setText(folder)

    def update_project_name(self):
        allowed_chars = r"[^a-zA-Z0-9_\.-]"
        display_text = self.display_name_line_edit.text()
        sanitized = re.sub(allowed_chars, '-', display_text)
        sanitized = re.sub(r'-+', '-', sanitized)
        self.name_line_edit.setText(sanitized)

    def create_project(self):
        folder = self.folder_line_edit.text()
        name = self.name_line_edit.text()
        display_name = self.display_name_line_edit.text()
        package = self.package_line_edit.text()
        author = self.author_line_edit.text()
        version = self.version_combo_box.currentText()

        if not all([folder, name, display_name, package, author]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        self.create = True
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ProjectDialog()
    dialog.exec()
    sys.exit(app.exec())