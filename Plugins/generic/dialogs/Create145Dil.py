from PyQt6.QtWidgets import QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QFileDialog, QLabel
from .RoundedDialog import RoundedDialog
import Language as Translate

class ProjectDialog(RoundedDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lang = Translate.Lang.Dialog
        self.setWindowTitle(self.lang.create_title)

        main_layout = QFormLayout(self)

        self.display_name_input = QLineEdit()
        self.display_name_input.setPlaceholderText(self.lang.display_name_placeholder)
        main_layout.addRow(QLabel(self.lang.display_name_label), self.display_name_input)

        self.name_input = QLineEdit()
        self.name_input.setReadOnly(True)
        main_layout.addRow(QLabel(self.lang.name_label), self.name_input)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(self.lang.path_placeholder)
        self.path_button = QPushButton(self.lang.browse_button)
        self.path_button.clicked.connect(self.browse_path)
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.path_button)
        main_layout.addRow(QLabel(self.lang.path_label), path_layout)

        self.package_input = QLineEdit()
        main_layout.addRow(QLabel(self.lang.package_label), self.package_input)

        button_layout = QHBoxLayout()
        self.create_button = QPushButton(self.lang.create_button)
        self.create_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton(self.lang.cancel_button)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.create_button)
        main_layout.addRow(button_layout)
        self.display_name_input.textChanged.connect(self.update_name)

    def update_name(self):
        display_name = self.display_name_input.text().lower()
        name = ''.join(c if c in 'abcdefghijklmnopqrstuvwxyzйцукенгшщзхъфывапролджэячсмитьбю1234567890+-_' else '-' for c in display_name)
        self.name_input.setText(name)

    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, self.lang.select_folder_title)
        if path:
            self.path_input.setText(path)

    def get_project_data(self):
        return {
            "display_name": self.display_name_input.text(),
            "name": self.name_input.text(),
            "path": self.path_input.text(),
            "package": self.package_input.text()
        }