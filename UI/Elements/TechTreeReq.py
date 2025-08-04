from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QSpinBox, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from UI import Language
from UI.Elements.SearchBox import SearchBox
from func.GLOBAL import ITEMS

class RequirementsPanel(QWidget):
    requirement_changed = pyqtSignal(object)

    def __init__(self, tech_node=None, parent=None):
        super().__init__(parent)
        self.tech_node = tech_node
        self.rows = []
        self.init_ui()
        self.update_requirements_list()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)

        self.title_label = QLabel("Зависимости")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.title_label.setFont(font)
        self.layout.addWidget(self.title_label)

        self.add_button = QPushButton("+ Добавить зависимость")
        self.add_button.clicked.connect(lambda: self.add_row())
        self.layout.addWidget(self.add_button)

        self.layout.addStretch()
        self.setLayout(self.layout)

    def add_row(self, req_type="resource", value=None):
        print(f"Adding row with req_type={req_type}, value={value}")
        row_widget = QWidget(self)
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)

        type_combo = QComboBox()
        type_combo.addItems(["resource", "sector", "research"])
        type_combo.setCurrentText(req_type)
        type_combo.currentTextChanged.connect(self.on_type_changed)

        items = self.get_items_for_type(req_type)
        search = SearchBox(items, self)

        if value:
            if req_type == "resource" and value and isinstance(value, list) and len(value) > 0 and isinstance(value[0], (list, tuple)):
                search.input_field.setText(value[0][0])  # resource_id
            elif isinstance(value, (list, tuple)):
                cleaned_values = [str(v).strip("[]'\"") for v in value]
                search.input_field.setText(",".join(cleaned_values))
            else:
                search.input_field.setText(str(value))

        spin = QSpinBox()
        spin.setRange(1, 9999)
        if req_type == "resource" and value and isinstance(value, list) and len(value) > 0 and isinstance(value[0], (list, tuple)) and len(value[0]) > 1:
            spin.setValue(value[0][1])
        else:
            spin.setValue(1)

        remove_button = QPushButton("✕")
        remove_button.setFixedWidth(30)
        remove_button.clicked.connect(lambda: self.remove_row(row_widget))

        row_layout.addWidget(QLabel(Language.Lang.TechTreeWindow.Dialog.type_))
        row_layout.addWidget(type_combo)
        row_layout.addWidget(QLabel("ID:"))
        row_layout.addWidget(search, stretch=2)
        row_layout.addWidget(QLabel("x"))
        row_layout.addWidget(spin)
        row_layout.addWidget(remove_button)

        spin.setVisible(req_type == "resource")

        self.layout.insertWidget(self.layout.count() - 1, row_widget)
        self.rows.append((row_widget, type_combo, search, spin))

        type_combo.currentTextChanged.connect(self.emit_change)
        search.input_field.textChanged.connect(self.emit_change)
        spin.valueChanged.connect(self.emit_change)
        self.emit_change()

    def remove_row(self, widget):
        for row in self.rows:
            if row[0] == widget:
                widget.setParent(None)
                self.rows.remove(row)
                self.emit_change()
                break

    def on_type_changed(self, text):
        for row_widget, type_combo, search, spin in self.rows:
            if type_combo.currentText() == text:
                items = self.get_items_for_type(text)
                search.items = items
                search.update_list()
                spin.setVisible(text == "resource")
                self.emit_change()

    def get_items_for_type(self, req_type):
        if req_type == "resource":
            return ITEMS
        elif req_type == "sector":
            return {"sector1": {"displayName": "Sector 1"}, "sector2": {"displayName": "Sector 2"}}
        elif req_type == "research":
            return {"research1": {"displayName": "Research 1"}, "research2": {"displayName": "Research 2"}}
        return {}

    def update_requirements_list(self):
        if not self.tech_node:
            print("No tech_node set, clearing requirements list")
            for row_widget, _, _, _ in self.rows:
                row_widget.setParent(None)
            self.rows.clear()
            return
        print(f"Updating requirements list for {self.tech_node.name}: {self.tech_node.requirements}")
        for row_widget, _, _, _ in self.rows:
            row_widget.setParent(None)
        self.rows.clear()
        for req in self.tech_node.requirements:
            req_type = req[0]
            value = req[1] if req_type == "resource" else req[1:]
            self.add_row(req_type, value)

    def set_tech_node(self, tech_node):
        print(f"Setting tech_node: {tech_node.name if tech_node else None}")
        self.tech_node = tech_node
        self.update_requirements_list()

    def value(self):
        result = []
        for _, type_combo, search, spin in self.rows:
            req_type = type_combo.currentText()
            value = search.input_field.text().strip()
            print(f"Processing input for {req_type}: {value}")
            if not value:
                continue
            if req_type == "resource":
                if value in ITEMS:
                    result.append((req_type, [(value, spin.value())]))
            else:
                args = value
                if args:
                    result.append((req_type, args))
        print(f"Generated requirements value: {result}")
        return result

    def emit_change(self):
        if not self.tech_node:
            print("No tech_node, skipping emit_change")
            return
        new_requirements = self.value()
        print(f"Before update: {self.tech_node.name} requirements = {self.tech_node.requirements}")
        self.tech_node.requirements = new_requirements
        print(f"After update: {self.tech_node.name} requirements = {new_requirements}")
        self.requirement_changed.emit(new_requirements)