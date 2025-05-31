from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

from UI.Elements.SearchBox import SearchBox
from func.GLOBAL import LIST_TYPES


class CreateElementDialog(QDialog):
    def __init__(self, path=[]):
        super().__init__()
        self.setWindowTitle("Создание объекта")
        self.setMinimumWidth(300)

        main_layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.valid_symbol = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л',
            'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш',
            'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '_', '-'
        ]

        self.valid_path = self.valid_symbol.copy()
        self.valid_path.append("/")
        self.type_edit = SearchBox(LIST_TYPES, self)
        self.name_edit = QLineEdit()
        self.name_edit.textChanged.connect(self.validSymbols)
        self.category_edit = QLineEdit()
        self.category_edit.setText("/".join(path))
        self.category_edit.textChanged.connect(self.validPath)

        form_layout.addRow("Тип объекта:", self.type_edit)
        form_layout.addRow("Название:", self.name_edit)
        form_layout.addRow("Категория:", self.category_edit)

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Отмена")
        self.save_button = QPushButton("Сохранить")
        self.save_button.setDefault(True)

        button_layout.addWidget(cancel_button, stretch=1)
        button_layout.addWidget(self.save_button, stretch=1)

        main_layout.addLayout(button_layout)

        cancel_button.clicked.connect(self.reject)

    def validSymbols(self, text):
        if any(False if _.lower() in self.valid_symbol else True for _ in text):
            self.name_edit.blockSignals(True)
            self.name_edit.setText("".join([_ if _.lower() in self.valid_symbol else "_" for _ in text]))
            self.name_edit.blockSignals(False)

    def validPath(self, text):
        if any(False if _.lower() in self.valid_path else True for _ in text):
            self.category_edit.blockSignals(True)
            self.category_edit.setText("".join([_ if _.lower() in self.valid_path else "_" for _ in text]))
            self.category_edit.blockSignals(False)
