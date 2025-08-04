import json
from collections import defaultdict

from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, QObject, Qt, QVariant, QModelIndex, QAbstractTableModel
from PyQt6.QtGui import QFont
import inspect

from UI import Language
from UI.Content import FloatSelect, IntSelect, BoolSelect, StringSelect
from UI.ContentFormat import Format, saveMode
from UI.Elements.BaseCustomWidget import BaseCustomWidget, CustomNoneClass
from UI.Elements.FloatSpinBox import FloatSpinBox


class ParamDelegate(QStyledItemDelegate):
    def __init__(self, param_configs, parent=None):
        super().__init__(parent)
        self.param_configs = param_configs

    def createEditor(self, parent, option, index):
        param_name = index.model().data(index.model().index(index.row(), 0), Qt.ItemDataRole.DisplayRole)
        config = self.param_configs.get(param_name)
        if not config:
            return super().createEditor(parent, option, index)

        ctype = config[0]

        if ctype == int:
            editor = QSpinBox(parent)
            editor.setMinimum(-999999)
            editor.setMaximum(999999)
            return editor
        elif ctype == float:
            editor = FloatSelect.Widget(parent)
            editor.setDecimals(3)
            editor.setMinimum(parent.minimum())
            editor.setMaximum(parent.maximum())
            return editor
        elif ctype == bool:
            editor = QCheckBox(parent)
            editor.setText("")
            return editor
        elif ctype == str:
            editor = QLineEdit(parent)
            return editor
        elif inspect.isclass(ctype) and issubclass(ctype, BaseCustomWidget):
            # Для кастомных виджетов можно создать адаптер или отдельный редактор
            # Но это сложнее, пока можно вернуть None или базовый редактор
            return None
        else:
            return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        if isinstance(editor, QDoubleSpinBox):
            editor.setValue(float(value))
        elif isinstance(editor, QSpinBox):
            editor.setValue(int(value))
        elif isinstance(editor, QCheckBox):
            editor.setChecked(bool(value))
        elif isinstance(editor, QLineEdit):
            editor.setText(str(value))

    def setModelData(self, editor, model, index):
        if isinstance(editor, QSpinBox) or isinstance(editor, QDoubleSpinBox):
            model.setData(index, editor.value(), Qt.ItemDataRole.EditRole)
        elif isinstance(editor, QCheckBox):
            model.setData(index, editor.isChecked(), Qt.ItemDataRole.EditRole)
        elif isinstance(editor, QLineEdit):
            model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class ParamsTableModel(QAbstractTableModel):
    def __init__(self, param_configs, changed_params, hidden_params, parent=None):
        super().__init__(parent)
        self.param_configs = param_configs
        self.changed_params = changed_params
        self.hidden_params = hidden_params
        self.filtered_params = []

    def set_filter(self, search_text):
        search_text = search_text.lower()
        self.beginResetModel()
        self.filtered_params = [
            (p, self.param_configs[p][7]) for p in self.param_configs
            if search_text in p.lower()
               and p not in self.hidden_params
               and self.param_configs[p][3]  # visible flag
        ]
        self.filtered_params.sort(key=lambda x: x[1] if x[1] is not None else float('inf'))
        self.filtered_params = [p[0] for p in self.filtered_params]
        print(f"[DEBUG] Filtered params: {self.filtered_params}")
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self.filtered_params)

    def columnCount(self, parent=QModelIndex()):
        return 2  # Параметр + Значение

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return QVariant()

        param = self.filtered_params[index.row()]
        config = self.param_configs[param]
        _, default, _, _, _, _, _, _ = config
        value = self.changed_params.get(param, default)

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            if index.column() == 0:
                return param
            elif index.column() == 1:
                return value
        return QVariant()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        if index.column() == 1:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable
        else:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if index.isValid() and index.column() == 1 and role == Qt.ItemDataRole.EditRole:
            param = self.filtered_params[index.row()]
            self.changed_params[param] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

class SyncSignals(QObject):
    global_value_changed = pyqtSignal(str, object, object)

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
        print(f"[DEBUG] Adding widget for {param_name}: widget={widget}, has_label={has_label}")
        if widget is not None:
            widget.setParent(self.content)
            widget.setVisible(True)
            if has_label:
                label = QLabel(has_label if isinstance(has_label, str) else param_name)
                label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                self.content_layout.addRow(label, widget)
                print(f"[DEBUG] Added {param_name} with label to QFormLayout")
            else:
                self.content_layout.addRow(widget)
                print(f"[DEBUG] Added {param_name} without label to QFormLayout")
            print(f"[DEBUG] Widget {param_name} visibility: {widget.isVisible()}")
            print(f"[DEBUG] Content visibility: {self.content.isVisible()}")
            print(f"[DEBUG] Collapsible visibility: {self.isVisible()}")
        else:
            print(f"[ERROR] Attempted to add None widget for parameter {param_name}")


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
            print(f"[DEBUG] Processing param {param}: content_type={content_type}, type={type(content_type)}")

            if not visible:
                self.hidden_params.add(param)
                print(f"[DEBUG] Param {param} is hidden")
                continue

            if not inspect.isclass(content_type):
                print(f"[DEBUG] Registering {param} as widget instance")
                self.custom_widgets[param] = (content_type, show_title)
            elif inspect.isclass(content_type) and issubclass(content_type, BaseCustomWidget):
                print(f"[DEBUG] Registering {param} as BaseCustomWidget class")
                self.custom_widgets[param] = (content_type, show_title)
            elif content_type in [int, float, bool, str]:
                print(f"[DEBUG] Mapping {param} as standard type {content_type}")
                self._map_standard_types(content_type, param, show_title)
            elif content_type is None:
                print(f"[DEBUG] Registering {param} as CustomNoneClass")
                self.custom_widgets[param] = (CustomNoneClass, False)
            else:
                print(f"[WARNING] Unhandled content_type for {param}: {content_type}")

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
            print(f"[DEBUG] Mapped {param} to widget class {widget_class}")
        else:
            print(f"[WARNING] No widget mapping for type {ctype} in param {param}")

    def _get_widget_class(self, param):
        widget_info = self.custom_widgets.get(param, (None, True))
        print(f"[DEBUG] Getting widget class for {param}: {widget_info[0]}")
        return widget_info[0]

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

        previewBtn = QPushButton(Language.Lang.Editor.Dialog.preview)
        previewBtn.clicked.connect(self.previewChange)
        layout.addWidget(previewBtn)

        save_btn = QPushButton(Language.Lang.Editor.Dialog.save)
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
                print(f"[DEBUG] Skipping hidden param {param}")
                continue
            _, _, group, visible, _, _, show_title, filter_idx = self.param_configs[param]
            if not visible:
                print(f"[DEBUG] Skipping invisible param {param}")
                continue
            categories[group].append((param, show_title, filter_idx))
            print(f"[DEBUG] Added {param} to category {group} with filter_idx={filter_idx}")

        for group, params in categories.items():
            print(f"[DEBUG] Creating category {group}")
            collapsible = CollapsibleCategory(group)
            params.sort(key=lambda x: x[2] if x[2] is not None else float('inf'))
            for param, show_title, filter_idx in params:
                print(f"[DEBUG] Adding widget for {param} with filter_idx={filter_idx}")
                widget = self.create_param_widget(param)
                if widget:
                    widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    collapsible.add_widget(widget, show_title, param)
                else:
                    print(f"[WARNING] No widget created for parameter {param}")
            layout.addWidget(collapsible)
            print(f"[DEBUG] Category {group} visibility: {collapsible.isVisible()}")
        layout.addStretch()

        scroll.setWidget(content)
        tab_layout = QVBoxLayout(tab)
        tab_layout.addWidget(scroll)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs.addTab(tab, Language.Lang.Editor.Dialog.variables)

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

        self.customTabs = self.classe.get_custom_tabs()
        for tab in self.customTabs:
            self.tabs.addTab(tab[1], tab[0])

    def create_param_widget(self, param):
        config = self.param_configs[param]
        content_type, default, _, _, _, _, show_title, _ = config
        current_value = self.changed_params.get(param, default)
        print(
            f"[DEBUG] Creating widget for {param}: content_type={content_type}, type={type(content_type)}, current_value={current_value}")

        widget = None

        if not inspect.isclass(content_type):
            print(f"[DEBUG] Using existing widget instance for {param}")
            widget = content_type
        elif inspect.isclass(content_type) and issubclass(content_type, BaseCustomWidget):
            print(f"[DEBUG] Creating BaseCustomWidget instance for {param}")
            widget = content_type()
        elif content_type in [int, float, bool, str]:
            widget_class = self._get_widget_class(param)
            print(f"[DEBUG] Widget class for {param}: {widget_class}")
            if widget_class:
                widget = widget_class()
            else:
                print(f"[WARNING] No widget class found for {param}")

        if widget:
            print(f"[DEBUG] Setting up widget for {param}: {type(widget)}")
            if hasattr(widget, 'set_value'):
                widget.set_value(current_value)
                print(f"[DEBUG] Set value {current_value} for {param}")
            else:
                print(f"[WARNING] Widget for {param} has no set_value method")

            if hasattr(widget, 'signal') and hasattr(widget.signal, 'value_changed'):
                widget.signal.value_changed.connect(
                    lambda v, p=param, w=widget: self.on_param_changed(p, v, w)
                )
                print(f"[DEBUG] Connected signal for {param}")
            else:
                print(f"[WARNING] Widget for {param} has no signal.value_changed")

            self.register_widget(
                param=param,
                widget=widget,
                meta={'default': default, 'save_mode': config[5]}
            )
            print(f"[DEBUG] Registered widget for {param}")
        else:
            print(f"[ERROR] Failed to create widget for {param}")

        return widget

    def on_param_changed(self, param, value, source_widget):
        print(param, "change to", value)
        self.sync_signals.global_value_changed.emit(param, value, source_widget)
        self.changed_params[param] = value

    def update_all_widgets(self, param, value, source_widget):
        if param in self.param_widgets:
            for widget in list(self.param_widgets[param]['widgets']):
                if widget is source_widget:
                    continue
                try:
                    widget.blockSignals(True)
                    widget.set_value(value)
                    widget.blockSignals(False)
                except RuntimeError:
                    self.param_widgets[param]['widgets'].remove(widget)

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
            idx = self.tabs.indexOf(self.search_tab)
            if idx != -1:
                self.tabs.removeTab(idx)
            self.search_tab = None

        if search_text:
            self.search_tab = QWidget()
            layout = QVBoxLayout(self.search_tab)
            layout.setContentsMargins(2, 2, 2, 2)

            self.search_table = QTableView()
            self.search_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
            self.search_table.setEditTriggers(
                QTableView.EditTrigger.DoubleClicked | QTableView.EditTrigger.SelectedClicked)
            layout.addWidget(self.search_table)

            self.search_model = ParamsTableModel(self.param_configs, self.changed_params, self.hidden_params, self)
            self.search_model.set_filter(search_text)
            self.search_table.setModel(self.search_model)

            self.search_delegate = ParamDelegate(self.param_configs, self.search_table)
            self.search_table.setItemDelegateForColumn(1, self.search_delegate)

            self.search_model.dataChanged.connect(self.on_search_model_changed)

            self.tabs.addTab(self.search_tab, Language.Lang.Editor.Dialog.search)
            self.tabs.setCurrentWidget(self.search_tab)

    def on_search_model_changed(self, topLeft, bottomRight, roles):
        if Qt.ItemDataRole.EditRole in roles:
            row = topLeft.row()
            param = self.search_model.filtered_params[row]
            value = self.changed_params.get(param)
            self.sync_signals.global_value_changed.emit(param, value)

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
        if isinstance(widget, BaseCustomWidget):
            widget.set_value(value)
        elif isinstance(widget, QCheckBox):
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

    def _collect_changes_from_widgets(self):
        changes = {}

        def dict_converter(x):
            if isinstance(x, dict):
                return x
            return json.loads(x)

        format_map = {
            Format.Int: (int, "int"),
            Format.Float: (float, "float"),
            Format.String: (str, "str"),
            Format.Bool: (lambda x: bool(x) if not isinstance(x, str)
            else x.lower() in ("true", "1"), "bool"),
            Format.Dict: (dict_converter, "dict"),
            Format.NoFormat: (None, "object"),
        }

        for param, meta in self.param_widgets.items():
            default = meta['default']
            save_mode = meta['save_mode']
            widget = meta['widgets'][0]

            if save_mode == saveMode.noSave: continue

            raw = self.get_widget_value(widget)
            print(raw, type(raw))

            widget_fmt = getattr(widget, "TYPE", Format.NoFormat)
            converter, type_name = format_map.get(widget_fmt, (None, "object"))

            if converter:
                try:
                    current = converter(raw)
                except Exception as e:
                    raise TypeError(
                        f"Parameter '{param}': widget TYPE={widget_fmt} returned {raw!r}, "
                        f"failed to result in {type_name}"
                    ) from e
            else:
                current = raw

            try:
                if converter:
                    default_converted = converter(default)
                else:
                    default_converted = default
            except Exception:
                default_converted = default

            if save_mode == saveMode.Force \
                    or ((save_mode == saveMode.ifChanged or save_mode is True) and current != default_converted):
                changes[param] = current

        return changes

    def save(self):
        changes = self._collect_changes_from_widgets()
        self.saved.emit(changes)
        self.saveFromSelf.emit(self, changes)

    def previewChange(self):
        changes = self._collect_changes_from_widgets()

        def do_save():
            dialog.accept()
            self.saved.emit(changes)
            self.saveFromSelf.emit(self, changes)

        dialog = QDialog(self)
        dialog.setWindowIcon(QApplication.windowIcon())
        dialog.setWindowTitle(Language.Lang.Editor.Dialog.preview)
        layout = QVBoxLayout(dialog)

        listWidget = QListWidget()
        for param, val in changes.items():
            listWidget.addItem(f"{param} = {val!r}")
        layout.addWidget(listWidget)

        save_btn = QPushButton(Language.Lang.Editor.Dialog.save)
        save_btn.clicked.connect(do_save)
        layout.addWidget(save_btn)

        dialog.exec()

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