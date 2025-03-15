from collections import defaultdict

from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, QObject, Qt
from PyQt6.QtGui import QColor, QFont
import inspect


class CustomWidgetSignal(QObject):
    value_changed = pyqtSignal(object)


class BaseCustomWidget(QWidget):
    def __init__(self, initial_value, parent=None):
        super().__init__(parent)
        self.signal = CustomWidgetSignal()
        self._value = initial_value

    def set_value(self, value):
        raise NotImplementedError("Subclasses must implement set_value")

    def value(self):
        return self._value


class CustomNoneClass(BaseCustomWidget):

    def __init__(self, initial_value, parent=None):
        super().__init__(initial_value, parent)

    def set_value(self, value):
        pass


class SyncSignals(QObject):
    global_value_changed = pyqtSignal(str, object)

class clickedWidget(QWidget):
    clicked = pyqtSignal()
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, a0):
        self.clicked.emit()
        super().mousePressEvent(a0)

class CollapsibleCategory(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.is_collapsed = False
        self.setup_ui(title)

    def setup_ui(self, title):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        self.header = clickedWidget()
        self.header.clicked.connect(self.toggle_collapse)
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))

        self.collapse_button = QToolButton()
        self.collapse_button.setText("▲")
        self.collapse_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.collapse_button.clicked.connect(self.toggle_collapse)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.collapse_button)

        self.layout.addWidget(self.header)

        self.content = QWidget()
        self.content_layout = QFormLayout(self.content)
        self.content_layout.setContentsMargins(10, 0, 10, 10)
        self.layout.addWidget(self.content)

    def toggle_collapse(self):
        self.is_collapsed = not self.is_collapsed
        self.content.setVisible(not self.is_collapsed)
        self.collapse_button.setText("▼" if self.is_collapsed else "▲")

    def add_widget(self, widget, has_label, param_name):
        if widget is not None:
            if has_label:
                label = QLabel(param_name)
                self.content_layout.addRow(label, widget)
            else:
                self.content_layout.addRow(widget)


class TabbedCustomEditor(QWidget):
    saved = pyqtSignal(dict)
    saveFromSelf = pyqtSignal(object, dict)

    def __init__(self, classes, changed_params=None, categories=None, parent=None):
        super().__init__(parent)
        self.classes = classes
        self.changed_params = changed_params or {}
        self.categories = categories or {}
        self.param_widgets = {}
        self.search_tab = None
        self.custom_widgets = {}
        self.sync_signals = SyncSignals()
        self.param_to_category = {}
        self.hidden_params = set()

        for category, params in self.categories.items():
            for param in params:
                self.param_to_category[param] = category

    def pack(self):
        self.init_ui()
        self.apply_initial_params()
        self.setup_connections()

    def setup_connections(self):
        self.sync_signals.global_value_changed.connect(self.update_all_widgets)

    def init_ui(self):
        layout = QVBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(self.update_search_tab)
        layout.addWidget(self.search_box)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        self.create_main_tabs()

        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def register_custom_widget(self, param_name, widget_class):
        if inspect.isclass(widget_class) and widget_class.__name__ == 'CustomNoneClass':
            self.hidden_params.add(param_name)
        else:
            self.custom_widgets[param_name] = widget_class

    def create_main_tabs(self):
        param_mapping = self.calculate_parameter_mapping()
        for class_idx, cls in enumerate(self.classes):
            tab = QWidget()
            scroll = QScrollArea()
            content = QWidget()
            main_layout = QVBoxLayout(content)
            main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            category_groups = {}
            uncategorized_params = []
            for param in param_mapping[class_idx]:
                if param in self.param_to_category:
                    category = self.param_to_category[param]
                    category_groups.setdefault(category, []).append(param)
                else:
                    uncategorized_params.append(param)

            for category in self.categories:
                if category in category_groups:
                    print(1)
                    params_in_category = [p for p in self.categories[category] if not p in self.hidden_params]
                    print(params_in_category)
                    collapsible_category = CollapsibleCategory(category)
                    for param in params_in_category:
                        default_value = getattr(cls(), param)
                        widget, has_label = self.create_widget(param, default_value)
                        if widget is not None:
                            collapsible_category.add_widget(widget, has_label, param)
                            collapsible_category.is_collapsed = False
                            collapsible_category.toggle_collapse()
                            self.register_widget(param, widget, default_value)
                    main_layout.addWidget(collapsible_category)

            if uncategorized_params:
                form_layout = QFormLayout()
                form_layout.setContentsMargins(10, 0, 10, 10)
                for param in uncategorized_params:
                    default_value = getattr(cls(), param)
                    widget, has_label = self.create_widget(param, default_value)
                    if widget is None:
                        continue
                    if has_label:
                        param_label = QLabel(param)
                        form_layout.addRow(param_label, widget)
                    else:
                        form_layout.addRow(widget)
                    self.register_widget(param, widget, default_value)
                main_layout.addLayout(form_layout)

            scroll.setWidget(content)
            scroll.setWidgetResizable(True)
            tab_layout = QVBoxLayout(tab)
            tab_layout.setContentsMargins(0, 0, 0, 0)
            tab_layout.addWidget(scroll)
            self.tabs.addTab(tab, cls.__name__)

    def create_widget(self, param_name, default_value):
        if param_name in self.custom_widgets:
            widget_class = self.custom_widgets[param_name][0]
            if widget_class is None:
                return None, False
            initial_value = self.changed_params.get(param_name, default_value)
            widget = widget_class(initial_value)
            widget.signal.value_changed.connect(
                lambda val: self.on_custom_widget_changed(param_name, val)
            )
            return widget, self.custom_widgets[param_name][1]

        if isinstance(default_value, bool):
            widget = QCheckBox()
            widget.setChecked(self.changed_params.get(param_name, default_value))
            widget.stateChanged.connect(
                lambda: self.on_widget_changed(param_name, widget.isChecked())
            )
        elif isinstance(default_value, int):
            widget = QSpinBox()
            widget.setValue(self.changed_params.get(param_name, default_value))
            widget.valueChanged.connect(
                lambda: self.on_widget_changed(param_name, widget.value())
            )
        elif isinstance(default_value, float):
            widget = QDoubleSpinBox()
            widget.setValue(self.changed_params.get(param_name, default_value))
            widget.valueChanged.connect(
                lambda: self.on_widget_changed(param_name, widget.value())
            )
        else:
            widget = QLineEdit(str(self.changed_params.get(param_name, default_value)))
            widget.textChanged.connect(
                lambda: self.on_widget_changed(param_name, widget.text())
            )

        return widget, True

    def on_widget_changed(self, param_name, value):
        self.sync_signals.global_value_changed.emit(param_name, value)

    def on_custom_widget_changed(self, param_name, value):
        self.sync_signals.global_value_changed.emit(param_name, value)

    def update_all_widgets(self, param_name, value):
        for widget in self.param_widgets.get(param_name, {}).get('widgets', []):
            if widget != self.sender():
                if isinstance(widget, BaseCustomWidget):
                    widget.set_value(value)
                else:
                    self.set_standard_widget_value(widget, value)

    def register_widget(self, param, widget, default_value):
        if param not in self.param_widgets:
            self.param_widgets[param] = {
                'widgets': [],
                'default': default_value
            }
        self.param_widgets[param]['widgets'].append(widget)

    def update_search_tab(self, text):
        search_text = text.strip().lower()
        if self.search_tab:
            self.tabs.removeTab(self.tabs.indexOf(self.search_tab))
            self.search_tab = None

        if search_text:
            self.search_tab = QWidget()
            scroll = QScrollArea()
            content = QWidget()
            form_layout = QFormLayout()
            content.setLayout(form_layout)
            scroll.setWidget(content)
            scroll.setWidgetResizable(True)

            found_params = [p for p in self.param_widgets
                            if search_text in p.lower() and p not in self.hidden_params]

            for param in found_params:
                default = self.param_widgets[param]['default']
                widget, _ = self.create_widget(param, default)
                if _:
                    label = QLabel(param)
                    form_layout.addRow(label, widget)
                else:
                    form_layout.addRow(widget)
                self.register_widget(param, widget, default)

            self.search_tab.setLayout(QVBoxLayout())
            self.search_tab.layout().addWidget(scroll)
            self.tabs.addTab(self.search_tab, "Поиск")
            self.tabs.setCurrentWidget(self.search_tab)

    def calculate_parameter_mapping(self):
        param_owners = {}
        for class_idx, cls in enumerate(self.classes):
            instance = cls()
            for name in vars(instance):
                if not name.startswith('_') and name not in self.hidden_params:
                    param_owners[name] = class_idx
        return {i: [p for p, c in param_owners.items() if c == i]
                for i in range(len(self.classes))}

    def set_standard_widget_value(self, widget, value):
        if isinstance(widget, QCheckBox):
            widget.setChecked(bool(value))
        elif isinstance(widget, QDoubleSpinBox):
            widget.setValue(float(value))
        elif isinstance(widget, QSpinBox):
            widget.setValue(int(value))
        elif isinstance(widget, QLineEdit):
            widget.setText(str(value))

    def apply_initial_params(self):
        for param, info in self.param_widgets.items():
            if param in self.changed_params:
                value = self.changed_params[param]
                for widget in info['widgets']:
                    if isinstance(widget, BaseCustomWidget):
                        widget.set_value(value)
                    else:
                        self.set_standard_widget_value(widget, value)

    def save(self):
        changes = {}
        for param, info in self.param_widgets.items():
            current_value = self.get_widget_value(info['widgets'][0])
            if current_value != info['default']:
                changes[param] = current_value
        self.saved.emit(changes)
        self.saveFromSelf.emit(self, changes)

    def get_widget_value(self, widget):
        if widget is None:
            return None
        elif isinstance(widget, BaseCustomWidget):
            return widget.value()
        elif isinstance(widget, QCheckBox):
            return widget.isChecked()
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            return widget.value()
        elif isinstance(widget, QLineEdit):
            return widget.text()
        return None