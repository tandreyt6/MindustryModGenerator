from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem,
    QHBoxLayout, QHeaderView, QSpinBox, QLabel
)
from PyQt6.QtCore import Qt
import MmgApi

Format = MmgApi.Libs.UI.ContentFormat.Format
SearchBox = MmgApi.Libs.UI.Elements.SearchBox.SearchBox
CustomWidgetSignal = MmgApi.Libs.UI.Elements.BaseCustomWidget.CustomWidgetSignal
BaseCustomWidget = MmgApi.Libs.UI.Elements.BaseCustomWidget.BaseCustomWidget



class RequirementsWidget(BaseCustomWidget):
    def __init__(self, initial_value=None, parent=None):
        super().__init__(initial_value or [], parent)

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.rows = []

        self._block_emit = False

        self.add_button = QPushButton("+ Добавить ресурс")
        self.add_button.clicked.connect(lambda: self.add_row())
        self.layout.addWidget(self.add_button)
        print(self._value)
        if isinstance(self._value, list):
            for resource_id, amount in self._value:
                if isinstance(resource_id, str) and resource_id in MmgApi.Libs.Main.editor._GLOBALS.ITEMS and isinstance(amount, int):
                    self.add_row(resource_id, amount)

    def add_row(self, resource_id="", amount=1):
        row_widget = QWidget(self)
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)

        search = SearchBox(MmgApi.Libs.Main.editor._GLOBALS.ITEMS)
        search.input_field.setText(resource_id)

        spin = QSpinBox()
        spin.setRange(1, 9999)
        spin.setValue(amount)

        remove_button = QPushButton("✕")
        remove_button.setFixedWidth(30)
        remove_button.clicked.connect(lambda: self.remove_row(row_widget))

        row_layout.addWidget(QLabel("ID:"))
        row_layout.addWidget(search, stretch=2)
        row_layout.addWidget(QLabel("x"))
        row_layout.addWidget(spin)
        row_layout.addWidget(remove_button)

        self.layout.insertWidget(self.layout.count() - 1, row_widget)
        self.rows.append((row_widget, search, spin))

        spin.valueChanged.connect(self.emit_change)
        search.input_field.textChanged.connect(self.emit_change)
        if not self._block_emit:
            self.signal.value_changed.emit(self.value())

    def remove_row(self, widget):
        for row in self.rows:
            if row[0] == widget:
                widget.setParent(None)
                self.rows.remove(row)
                self.emit_change()
                break

    def set_value(self, value, emit_signal=True):
        self._block_emit = not emit_signal
        self._value = []
        for row_widget, _, _ in self.rows:
            row_widget.setParent(None)
        self.rows.clear()
        if isinstance(value, list):
            for entry in value:
                if (
                        isinstance(entry, list) and len(entry) == 2
                        and isinstance(entry[0], str)
                        and entry[0] in MmgApi.Libs.Main.editor._GLOBALS.ITEMS
                        and isinstance(entry[1], int)
                ):
                    self._value.append(entry)
                    print(entry[0], entry[1])
                    self.add_row(entry[0], entry[1])

        self._block_emit = False

    def value(self):
        result = []
        for _, search, spin in self.rows:
            resource_id = search.input_field.text()
            amount = spin.value()
            if resource_id in MmgApi.Libs.Main.editor._GLOBALS.ITEMS:
                result.append([resource_id, amount])
        return result

    def emit_change(self):
        if self._block_emit:
            return
        self.signal.value_changed.emit(self.value())

