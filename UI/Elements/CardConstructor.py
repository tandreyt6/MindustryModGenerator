from collections import defaultdict

from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, QObject, Qt
from PyQt6.QtGui import QFont
import inspect

from UI.Content import FloatSelect, IntSelect, BoolSelect, StringSelect
from UI.ContentFormat import Format, saveMode
from UI.Elements.BaseCustomWidget import BaseCustomWidget, CustomNoneClass


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

        self.collapse_button = QLabel()
        self.collapse_button.setText("▲")
        self.collapse_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

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

    def __init__(self, classe, changed_params=None, id=0, name="Block", parent=None):
        super().__init__()
        self.classe = classe(id, name)
        self.changed_params = changed_params or {}
        self.param_configs = defaultdict(lambda: (None, None, "unknown", True, None, saveMode.ifChanged, True, None))
        self.param_widgets = {}
        self.sync_signals = SyncSignals()
        self.custom_widgets = {}
        self.hidden_params = set()
        self.loadedFromClass = False

        for attr_name in dir(self.classe):
            if not attr_name.startswith('_'):
                attr = getattr(self.classe, attr_name)
                if isinstance(attr, tuple):
                    self.param_configs[attr_name] = self._complete_tuple(attr)
        self._process_param_configs()

    def _complete_tuple(self, t):
        default = (None, None, "unknown", True, None, saveMode.ifChanged, True, None)
        return tuple(t + default[len(t):])

    def _process_param_configs(self):
        for param, config in self.param_configs.items():
            content_type, default, group, visible, event_filter, save_mode, show_title, filter_idx = config

            if not visible:
                self.hidden_params.add(param)
                continue

            if inspect.isclass(content_type) and issubclass(content_type, BaseCustomWidget):
                self.custom_widgets[param] = (content_type, show_title)
            elif content_type in [int, float, bool, str]:
                self._map_standard_types(content_type, param, show_title)
            elif content_type is None:
                self.custom_widgets[param] = (CustomNoneClass, False)

    def _map_standard_types(self, ctype, param, show_title):
        widget_map = {
            int: (IntSelect.Widget, Format.Int),
            float: (FloatSelect.Widget, Format.Float),
            bool: (BoolSelect.Widget, Format.Bool),
            str: (StringSelect.Widget, Format.String)
        }
        if ctype in widget_map:
            widget_class, fmt = widget_map[ctype]
            widget_class.TYPE = fmt
            self.custom_widgets[param] = (widget_class, show_title)

    def _get_widget_class(self, param):
        return self.custom_widgets.get(param, (None, True))[0]

    def _get_show_title(self, param):
        return self.custom_widgets.get(param, (None, True))[1]

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

        previewBtn = QPushButton("Preview")
        previewBtn.clicked.connect(self.previewChange)
        layout.addWidget(previewBtn)

        save_btn = QPushButton("Save")
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
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        content = QWidget()
        content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout = QVBoxLayout(content)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(2, 2, 2, 2)

        categories = defaultdict(list)
        for param in self.param_configs:
            if param in self.hidden_params:
                continue
            _, _, group, _, _, _, show_title, _ = self.param_configs[param]
            categories[group].append((param, show_title))

        for group, params in categories.items():
            collapsible = CollapsibleCategory(group)
            collapsible.toggle_collapse()
            for param, show_title in params:
                widget = self.create_param_widget(param)
                if widget:
                    widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    collapsible.add_widget(widget, show_title, param)
            layout.addWidget(collapsible)
        layout.addStretch()

        scroll.setWidget(content)
        tab_layout = QVBoxLayout(tab)
        tab_layout.addWidget(scroll)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs.addTab(tab, "Variables")

        tabFunc = QWidget()
        scrollF = QScrollArea()
        scrollF.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollF.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scrollF.setWidgetResizable(True)
        contentF = QWidget()
        contentF.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout = QVBoxLayout(contentF)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(2, 2, 2, 2)

        scrollF.setWidget(contentF)
        tab_layoutF = QVBoxLayout(tabFunc)
        tab_layoutF.addWidget(scrollF)
        tab_layoutF.setContentsMargins(0, 0, 0, 0)
        self.tabs.addTab(tabFunc, "Methods")

        self.customTabs = self.classe.get_custom_tabs()
        for tab in self.customTabs:
            self.tabs.addTab(tab[1], tab[0])

    def create_param_widget(self, param):
        config = self.param_configs[param]
        content_type, default, _, _, _, _, show_title, _ = config
        current_value = self.changed_params.get(param, default)

        widget = None

        if content_type in [int, float, bool, str]:
            widget_class = self._get_widget_class(param)
            if widget_class:
                widget = widget_class()
                widget.set_value(current_value)
        elif inspect.isclass(content_type) and issubclass(content_type, BaseCustomWidget):
            widget = content_type()
            widget.set_value(current_value)

        if widget:
            self.register_widget(
                param=param,
                widget=widget,
                meta={
                    'default': default,
                    'save_mode': config[5]
                }
            )
            widget.signal.value_changed.connect(lambda v: self.on_param_changed(param, v))

        return widget

    def on_param_changed(self, param, value):
        print(param, "change to", value)
        self.sync_signals.global_value_changed.emit(param, value)
        self.changed_params[param] = value

    def update_all_widgets(self, param, value):
        if param in self.param_widgets:
            for widget in self.param_widgets[param]['widgets']:
                try:
                    if widget != self.sender():
                        widget.blockSignals(True)
                        widget.set_value(value)
                        widget.blockSignals(False)
                except RuntimeError:
                    self.param_widgets[param]['widgets'].pop(self.param_widgets[param]['widgets'].index(widget))

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

        return None, True

    def on_widget_changed(self, param_name, value):
        self.sync_signals.global_value_changed.emit(param_name, value)

    def on_custom_widget_changed(self, param_name, value):
        self.sync_signals.global_value_changed.emit(param_name, value)

    def register_widget(self, param, widget, meta):
        if param not in self.param_widgets:
            self.param_widgets[param] = {
                'widgets': [],
                'default': meta['default'],
                'save_mode': meta['save_mode']
            }
        self.param_widgets[param]['widgets'].append(widget)

    def update_search_tab(self, text):
        search_text = text.strip().lower()

        if hasattr(self, 'search_tab') and self.search_tab:
            self.tabs.removeTab(self.tabs.indexOf(self.search_tab))
            self.search_tab = None

        if search_text:
            self.search_tab = QWidget()
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)

            content = QWidget()
            form_layout = QFormLayout(content)
            form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

            found_params = [
                p for p in self.param_configs
                if search_text in p.lower()
                   and p not in self.hidden_params
                   and self.param_configs[p][3]
            ]

            for param in found_params:
                widget = self.create_param_widget(param)
                if widget:
                    widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    label = QLabel(param)
                    form_layout.addRow(label, widget)

            scroll.setWidget(content)

            tab_layout = QVBoxLayout(self.search_tab)
            tab_layout.addWidget(scroll)
            tab_layout.setContentsMargins(2, 2, 2, 2)

            self.tabs.addTab(self.search_tab, "Search")
            self.tabs.setCurrentWidget(self.search_tab)

    def calculate_parameter_mapping(self, objs:object=None):
        param_owners = {}
        if objs is None: objs = self.classe

        p = self.calculate_parameter_mapping_class(objs, 0)
        param_owners.update(p)
        return {i: [p for p, c in param_owners.items() if c == i]
                for i in range(len(objs))}

    def calculate_parameter_mapping_class(self, cls):
        param_owners = {}
        instance = cls()
        for attr_name in dir(instance):
            if attr_name.startswith('_'): continue
            attr = getattr(instance, attr_name)
            if isinstance(attr, tuple):
                params = self.parse_parameter_tuple(attr)
                if params['visible'] and attr_name not in self.hidden_params:
                    param_owners[attr_name] = cls.__name__
        return param_owners

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
        for param in self.param_configs:
            if param in self.changed_params:
                value = self.changed_params[param]
                for widget in self.param_widgets.get(param, {}).get("widgets", []):
                    widget.set_value(value)

    def save(self):
        changes = {}
        for param, config in self.param_configs.items():
            _, default, _, _, _, save_mode, _, _ = config
            current = self.changed_params.get(param, default)

            if save_mode == saveMode.Force:
                changes[param] = current
            elif (save_mode == saveMode.ifChanged or save_mode == True) and current != default:
                changes[param] = current

        self.saved.emit(changes)
        self.saveFromSelf.emit(self, changes)

    def previewChange(self):
        changes = {}
        for param, config in self.param_configs.items():
            _, default, _, _, _, save_mode, _, _ = config
            current = self.changed_params.get(param, default)

            if save_mode == saveMode.Force:
                changes[param] = current
            elif (save_mode == saveMode.ifChanged or save_mode == True) and current != default:
                changes[param] = current

        def save():
            dil.accept()
            self.saved.emit(changes)
            self.saveFromSelf.emit(self, changes)

        print(changes)
        dil = QDialog()
        dil.setWindowIcon(QApplication.windowIcon())
        dil.setWindowTitle("Preview")
        v = QVBoxLayout()
        dil.setLayout(v)
        listWidget = QListWidget()
        v.addWidget(listWidget)
        for param in changes:
            listWidget.addItem(f"{param} = {str(changes[param])}")
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(save)
        v.addWidget(save_btn)
        dil.exec()


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