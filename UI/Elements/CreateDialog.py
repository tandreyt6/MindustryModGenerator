import sys
import os
import re
from PyQt6.QtWidgets import (
    QApplication, QDialog, QFormLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QComboBox, QMessageBox, QHBoxLayout, QWidget
)
from PyQt6.QtCore import Qt

from func.GLOBAL import LIST_MOD_TEMPLATES


class ProjectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.create = False
        self.setWindowTitle("Выбор конструктора")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QFormLayout()
        l = [_ for _ in LIST_MOD_TEMPLATES]
        self.setFixedSize(self.sizeHint())
        if len(l) > 0:
            self.lbl = QLabel("Выберите конструктор для дальнейшей настройки!\nЗа настройку отвечает полностью плагин!")
            layout.addRow(self.lbl)
            self.combo = QComboBox()
            self.combo.addItems(l)
            layout.addRow(self.combo)
            h = QHBoxLayout()
            ok = QPushButton("Открыть")
            ok.setDefault(True)
            ok.clicked.connect(self.accept)
            h.addWidget(ok)
            cancel = QPushButton("Отмена")
            cancel.clicked.connect(self.reject)
            h.addWidget(cancel)
            layout.addRow(h)
        else:
            self.lbl = QLabel("Ни одного конструктора не было создано!\nДобавьте плагин с поддержкой конструктора!")
            layout.addRow(self.lbl)
            h = QHBoxLayout()
            ok = QWidget()
            h.addWidget(ok)
            cancel = QPushButton("Отмена")
            cancel.setDefault(True)
            cancel.clicked.connect(self.reject)
            h.addWidget(cancel)
            layout.addRow(h)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ProjectDialog()
    dialog.exec()
    sys.exit(app.exec())