import json
import os.path
import shutil
import threading
import time
import uuid
from threading import Thread
from typing import List

import hjson
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GradlewManager import GradleWrapper
from UI import Language
from UI.Content.CentralPreviewWidget import PreviewWidget
from UI.ContentFormat import ALL_TABS, PanelsPos
from UI.Elements.CardConstructor import TabbedCustomEditor
from UI.Elements.ConsoleWidget import ConsoleWidget
from UI.Elements.CreateElementDialog import CreateElementDialog
from UI.Elements.DragTab import DraggableTabWidget
from UI.Elements.SplashDil import SplashDil
from UI.Window.WindowAbs import WindowAbs
from func import settings
from func.GLOBAL import CONTENT_FOLDER, LIST_TYPES
from func.Types.Content import Content
from UI.Window.TechTreeWindow import TechTreeWindow


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, text, data=None, parent=None):
        super().__init__(parent)
        self.setText(0, text)
        self.wParent = parent
        self.data = data if data else {}

        flags = self.flags()
        if 'NoChange' in self.data.get('flag', []):
            flags &= ~Qt.ItemFlag.ItemIsEditable
        else:
            flags |= Qt.ItemFlag.ItemIsEditable

        if self.data.get('type') == 'category':
            flags &= ~Qt.ItemFlag.ItemIsDragEnabled
            flags |= Qt.ItemFlag.ItemIsDropEnabled
            folder_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
            self.setIcon(0, folder_icon)
        else:
            flags |= Qt.ItemFlag.ItemIsDragEnabled
            flags &= ~Qt.ItemFlag.ItemIsDropEnabled

        self.setSizeHint(0, QSize(100, 20))
        self.setFlags(flags)

    def get_path(self) -> list:
        path = [self.text(0)]
        parent = self.wParent
        current = self
        while isinstance(parent, TreeWidgetItem):
            path.insert(0, parent.text(0))
            current = parent
            parent = current.wParent
        return path

    def get_item_path(self):
        path = [self]
        parent = self.wParent
        while isinstance(parent, TreeWidgetItem):
            path.insert(0, parent)
            parent = parent.wParent
        return path


class EditDelegate(QStyledItemDelegate):
    editCompleted = pyqtSignal(str, str, QTreeWidgetItem)

    def __init__(self, validation_callback, parent=None):
        super().__init__(parent)
        self.indexEditor = None
        self.optionEditor = None
        self.parentEditor = None
        self.validation_callback = validation_callback
        self.current_item = None
        self.old_text = ""
        self.valid_symbol = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л',
            'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш',
            'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '_', '-'
        ]
        self.editor = None

    def createEditor(self, parent, option, index):
        self.editor = super().createEditor(parent, option, index)
        if isinstance(self.editor, QLineEdit):
            self.current_item = self.parent().itemFromIndex(index)
            self.old_text = self.current_item.text(0)
            self.parentEditor = parent
            self.optionEditor = option
            self.indexEditor = index
            self.editor.setText(self.old_text)
            self.editor.selectAll()
            self.editor.textChanged.connect(self.validSymbols)
            self.editor.installEventFilter(self)
        return self.editor

    def validSymbols(self, text):
        if any(False if _.lower() in self.valid_symbol else True for _ in text):
            self.editor.blockSignals(True)
            self.editor.setText("".join([_ if _.lower() in self.valid_symbol else "_" for _ in text]))
            self.editor.blockSignals(False)

    def eventFilter(self, editor, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
                new_text = editor.text()
                if self.validation_callback:
                    result = self.validation_callback(self.old_text, new_text, self.current_item)
                    if not result:
                        self.editCompleted.emit(self.old_text, self.old_text, self.current_item)
                        return True
                    self.editCompleted.emit(self.old_text, new_text, self.current_item)
                    self.commitData.emit(editor)
                    self.closeEditor.emit(editor, QStyledItemDelegate.EndEditHint.SubmitModelCache)
                    return True
            elif event.key() == Qt.Key.Key_Escape:
                self.closeEditor.emit(editor, QStyledItemDelegate.EndEditHint.RevertModelCache)
                return True
        return super().eventFilter(editor, event)


class TreeWidget(QTreeWidget):
    itemSelected = pyqtSignal(object)
    openRequested = pyqtSignal(object)
    renameRequested = pyqtSignal(object)
    deleteRequested = pyqtSignal(object)
    createItemRequested = pyqtSignal(object)
    createCategoryRequested = pyqtSignal(object)
    createCategoryPath = pyqtSignal(object)
    itemRenamed = pyqtSignal(str, str, object)
    itemMoved = pyqtSignal(object, object)

    def __init__(self):
        super().__init__()
        self.setHeaderHidden(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.delegate = EditDelegate(
            validation_callback=self.validate_rename,
            parent=self
        )
        self.delegate.editCompleted.connect(self.handle_rename_complete)
        self.setItemDelegate(self.delegate)

        self.itemClicked.connect(self.emit_item_selected)
        self.itemDoubleClicked.connect(self.handle_double_click)

    def get_path(self) -> list:
        return []

    def dropEvent(self, event: QDropEvent):
        selected_items = self.selectedItems()
        if not selected_items:
            return
        item = selected_items[0]
        old_parent = item.parent()
        old_row = self.indexFromItem(item).row()
        super().dropEvent(event)
        self.itemMoved.emit(item, old_parent)

    def find_child_by_text(self, parent: TreeWidgetItem, text: str, item_type: str = None):
        items = []
        if parent is None:
            for i in range(self.topLevelItemCount()):
                item = self.topLevelItem(i)
                if item.text(0) == text and (item_type is None or item.data.get("type") == item_type):
                    items.append(item)
        else:
            for i in range(parent.childCount()):
                item = parent.child(i)
                if item.text(0) == text and (item_type is None or item.data.get("type") == item_type):
                    items.append(item)
        return items

    def add_item(self, path_text: list, data=None, parent: TreeWidgetItem = None):
        current_parent = parent
        for i, txt in enumerate(path_text):
            is_last = i == len(path_text) - 1
            new_data = data if is_last and data else {"type": "category"}
            item_type = new_data.get("type")
            existing_children = self.find_child_by_text(current_parent, txt, item_type)
            if existing_children:
                child = existing_children[0]
            else:
                child = TreeWidgetItem(txt, new_data, current_parent)
                if new_data.get("type") == "category":
                    self.createCategoryPath.emit(child)
                if current_parent:
                    current_parent.addChild(child)
                else:
                    self.addTopLevelItem(child)
            current_parent = child
        return current_parent

    def find_path_by_text(self, path_text: list) -> list | None:
        current_parent = None
        result = []
        for txt in path_text:
            children = self.find_child_by_text(current_parent, txt)
            if len(children) != 1:
                return None
            child = children[0]
            result.append(child)
            current_parent = child
        return result

    def find_item_path(self, target: TreeWidgetItem) -> list:
        return target.get_path()

    def validate_text(self, text: str) -> bool:
        return len(text.strip()) > 0

    def validate_rename(self, old_text, new_text, item):
        return self.parent().parent().parent().parent().parent().handle_rename_validation(old_text, new_text, item)

    def handle_rename_complete(self, old_text, new_text, item):
        self.itemRenamed.emit(old_text, new_text, item)

    def emit_item_selected(self, item):
        self.itemSelected.emit(item)

    def handle_double_click(self, item: TreeWidgetItem, column):
        if item.data.get('type') == 'category':
            item.setExpanded(not item.isExpanded())
        elif item.data.get('type') == 'item':
            self.openRequested.emit(item)

    def contextMenuEvent(self, event):
        item: TreeWidgetItem = self.itemAt(event.pos())
        menu = QMenu(self)
        open_action = None
        if item:
            open_action = menu.addAction(Language.Lang.Editor.ActionPanel.open)
        rename_action = None
        if item and 'NoChange' not in item.data.get('flag', []):
            rename_action = menu.addAction(Language.Lang.Editor.ActionPanel.rename)
        delete_action = None
        if item and 'NoDelete' not in item.data.get('flag', []):
            delete_action = menu.addAction(Language.Lang.Editor.ActionPanel.delete)
        create_category = None
        if not item or (item and item.data.get("type", "") == "category"):
            create_category = menu.addAction(Language.Lang.Editor.ActionPanel.create_category)
        create_element = None
        if not item or (item and item.data.get("type", "") == "category"):
            create_element = menu.addAction(Language.Lang.Editor.ActionPanel.create_item)
        action = menu.exec(event.globalPos())
        if item and action == open_action:
            self.openRequested.emit(item)
        elif create_category and action == create_category:
            self.createCategoryRequested.emit(item)
        elif create_element and action == create_element:
            self.createItemRequested.emit(item if item else self)
        elif item and 'NoChange' not in item.data.get('flag', []) and action == rename_action:
            self.renameRequested.emit(item)
        elif item and 'NoDelete' not in item.data.get('flag', []) and action == delete_action:
            self.deleteRequested.emit(item)


class ElementsDict:
    def __init__(self):
        self.data = {}
        self.key_map = {}
        self.identifiers = {}

    def add(self, key1, key2, key3, value):
        identifier = uuid.uuid4()
        self.data[identifier] = value
        self.identifiers[identifier] = (key1, key2, key3)
        for key in (key1, key2, key3):
            self.key_map[key] = identifier

    def _remove_element(self, identifier):
        if identifier not in self.identifiers:
            return
        for key in self.identifiers[identifier]:
            if key in self.key_map:
                del self.key_map[key]
        del self.data[identifier]
        del self.identifiers[identifier]

    def rename_key(self, old, new):
        identifier = self.key_map[old]
        del self.key_map[old]
        self.key_map[new] = identifier

    def __getitem__(self, key):
        return self.data[self.key_map[key]]

    def __delitem__(self, key):
        identifier = self.key_map[key]
        self._remove_element(identifier)

    def __contains__(self, key):
        return key in self.key_map

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.key_map)

    def keys(self):
        return self.key_map.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return [(key, self.data[identifier]) for key, identifier in self.key_map.items()]


class EditorWindow(WindowAbs):
    splitterPosChanged = pyqtSignal(list)
    saveRequested = pyqtSignal(dict)
    closeSignal = pyqtSignal(object, bool)
    settingsWindowRequest = pyqtSignal()

    def __init__(self, main, data):
        super().__init__()
        self.elementsData = ElementsDict()
        self.planetsData = {}
        self.path = data.get("path")
        self.main = main
        self.launcherData = data
        try:
            self.gradlewManager = GradleWrapper(self.path)
        except:
            self.gradlewManager = None
        self.data = {}
        self.notExitOnLauncher = True
        if data.get("path"):
            with open(os.path.join(data.get("path"), "mod.hjson"), "r", encoding="utf-8") as e:
                self.data = hjson.load(e)
        x = self.data.get("main", "example.javaMod").split(".")
        x.pop(-1)
        self.package = ".".join(x)
        self.init_ui()

    def handle_rename_validation(self, old_name, new_name, item):
        if not new_name.strip():
            QMessageBox.warning(self, Language.Lang.Editor.Dialog.error,
                                Language.Lang.Editor.Dialog.name_empty_warn)
            return False
        if len(new_name) < 3:
            QMessageBox.warning(self, Language.Lang.Editor.Dialog.error,
                                Language.Lang.Editor.Dialog.name_is_long_warn)
            return False
        if new_name[0].isdigit():
            QMessageBox.warning(self, Language.Lang.Editor.Dialog.error,
                                Language.Lang.Editor.Dialog.name_first_word_isDigit_warn)
            return False
        items = [_ for _ in self.tree.find_child_by_text(item.parent(), new_name) if _.data.get("type") != "category"]
        folders = [_ for _ in self.tree.find_child_by_text(item.parent(), new_name) if _.data.get("type") == "category"]
        path = item.get_path()
        path[-1] = new_name
        if ((len(items) > 1 or len(items) > 0 and items[0] != item) and item.data.get("type") != "category") \
                or (item.data.get("type") == "category" and any(_.get_path() == path for _ in folders)):
            QMessageBox.warning(self, Language.Lang.Editor.Dialog.error,
                                Language.Lang.Editor.Dialog.name_exist_item)
            return False
        if new_name in self.elementsData and item.data.get("type") != "category":
            QMessageBox.warning(self, Language.Lang.Editor.Dialog.error,
                                Language.Lang.Editor.Dialog.name_exist_item)
            return False
        if item.data.get("type") != "category" and self.elementsData[old_name]['item'] != id(
                item) and new_name in self.elementsData.key_map:
            QMessageBox.warning(self, Language.Lang.Editor.Dialog.error,
                                Language.Lang.Editor.Dialog.name_exist_item)
            return False
        return True

    def init_ui(self):
        self.setWindowTitle(self.data.get("displayName", "") + " - Editor")
        if self.path:
            if os.path.exists(os.path.join(self.path, "icon.png")):
                QApplication.setWindowIcon(QIcon(os.path.join(self.path, "icon.png")))
        self.setGeometry(100, 100, 1200, 800)

        FileMenu = QMenu(Language.Lang.Editor.ActionPanel.file)
        self.projectSettingsAct = QAction(Language.Lang.Editor.ActionPanel.project_settings)
        self.projectSettingsAct.triggered.connect(self.openProjectSettings)
        self.settingsAct = QAction(Language.Lang.Editor.ActionPanel.settings)
        self.settingsAct.triggered.connect(self.settingsWindowRequest.emit)
        self.openModFolder = QAction(Language.Lang.Editor.ActionPanel.show_project_folder)
        self.openModFolder.triggered.connect(self.ShowModFolder)
        self.exitOnLauncherAct = QAction(Language.Lang.Editor.ActionPanel.exit_project)
        self.exitOnLauncherAct.triggered.connect(self.exitOnLauncher)
        self.exitOnProgram = QAction(Language.Lang.Editor.ActionPanel.exit)
        self.exitOnProgram.triggered.connect(self.close)

        FileMenu.addAction(self.projectSettingsAct)
        FileMenu.addAction(self.openModFolder)
        FileMenu.addSeparator()
        FileMenu.addAction(self.settingsAct)
        FileMenu.addSeparator()
        FileMenu.addAction(self.exitOnLauncherAct)
        FileMenu.addAction(self.exitOnProgram)

        ViewMenu = QMenu(Language.Lang.Editor.ActionPanel.view)
        self.setPosPanelsSelect = QMenu(Language.Lang.Editor.ActionPanel.menu_pos_panels)
        self.setPosPanelsAct1 = QAction(Language.Lang.Editor.ActionPanel.menu_pos1_panels)
        self.setPosPanelsAct1.triggered.connect(lambda: self.setPosForPanels(PanelsPos.Left_Right))
        self.setPosPanelsAct2 = QAction(Language.Lang.Editor.ActionPanel.menu_pos2_panels)
        self.setPosPanelsAct2.triggered.connect(lambda: self.setPosForPanels(PanelsPos.Right_Left))
        self.setPosPanelsAct3 = QAction(Language.Lang.Editor.ActionPanel.menu_pos3_panels)
        self.setPosPanelsAct3.triggered.connect(lambda: self.setPosForPanels(PanelsPos.Left_left))
        self.setPosPanelsAct4 = QAction(Language.Lang.Editor.ActionPanel.menu_pos4_panels)
        self.setPosPanelsAct4.triggered.connect(lambda: self.setPosForPanels(PanelsPos.left_Left))
        self.setPosPanelsAct5 = QAction(Language.Lang.Editor.ActionPanel.menu_pos5_panels)
        self.setPosPanelsAct5.triggered.connect(lambda: self.setPosForPanels(PanelsPos.Right_right))
        self.setPosPanelsAct6 = QAction(Language.Lang.Editor.ActionPanel.menu_pos6_panels)
        self.setPosPanelsAct6.triggered.connect(lambda: self.setPosForPanels(PanelsPos.right_Right))

        ViewMenu.addMenu(self.setPosPanelsSelect)
        self.setPosPanelsSelect.addAction(self.setPosPanelsAct1)
        self.setPosPanelsSelect.addAction(self.setPosPanelsAct2)
        self.setPosPanelsSelect.addAction(self.setPosPanelsAct3)
        self.setPosPanelsSelect.addAction(self.setPosPanelsAct4)
        self.setPosPanelsSelect.addAction(self.setPosPanelsAct5)
        self.setPosPanelsSelect.addAction(self.setPosPanelsAct6)

        buildMenu = QMenu(Language.Lang.Editor.ActionPanel.gradle)
        testMenu = QMenu(Language.Lang.Editor.ActionPanel.test)
        testMenu.addAction("Coming soon...")

        self.lastActionLabel = QLabel()

        if self.gradlewManager is None:
            buildMenu.setEnabled(False)
            self.setActionLabel(Language.Lang.Editor.ToolTip.gradleMenu_noloaded)
        else:
            d = []

            def load(d):
                suc, ver = self.gradlewManager.get_version()
                d.append(suc)
                d.append(ver)

            splashDil = SplashDil()
            splashDil.setFixedWidth(350)
            splashDil.text.setText(Language.Lang.Editor.ActionPanel.load_gradle)
            splashDil.cancel.clicked.connect(splashDil.close)
            splashDil.show()
            x = threading.Thread(target=load, args=(d,), daemon=True)
            x.start()
            while x.is_alive():
                QApplication.processEvents()
            suc, ver = d
            if not suc:
                buildMenu.setEnabled(False)
                buildMenu.setToolTip(Language.Lang.Editor.ToolTip.gradleMenu_noloaded)
                self.setActionLabel(Language.Lang.Editor.ToolTip.gradleMenu_noloaded + ver)
            else:
                buildMenu.setToolTip(Language.Lang.Editor.ToolTip.gradleMenu_loaded)
                self.setActionLabel(Language.Lang.Editor.ToolTip.gradleMenu_loaded)

            self.BuildAct = QAction(Language.Lang.Editor.ActionPanel.build_project)
            self.BuildAct.triggered.connect(self.buildTask)
            buildMenu.addAction(self.BuildAct)

            self.RunTaskAct = QAction(Language.Lang.Editor.ActionPanel.run_task)
            self.RunTaskAct.triggered.connect(self.runTask)
            buildMenu.addAction(self.RunTaskAct)

        gitMenu = QMenu(Language.Lang.Editor.ActionPanel.git_menu)
        gitMenu.addAction("Coming soon...")

        self.treeMenu = QMenu(Language.Lang.Editor.ActionPanel.treeMenu)
        self.open_tree_action = QAction(Language.Lang.Editor.ActionPanel.openTreeMenu)
        self.open_tree_action.triggered.connect(self.showTechTree)
        self.treeMenu.addAction(self.open_tree_action)

        self.techTree = TechTreeWindow()
        self.techTree.project_path = self.path

        self.action_bar.addAction(FileMenu)
        self.action_bar.addAction(ViewMenu)
        self.action_bar.addAction(buildMenu)
        self.action_bar.addAction(testMenu)
        self.action_bar.addAction(gitMenu)
        self.action_bar.addAction(self.treeMenu)

        self.central_widget = QWidget()
        self.central_widget.setObjectName("contentArea")
        self.v = QVBoxLayout(self.central_widget)
        self.v.setContentsMargins(0, 0, 0, 0)
        self.v.setSpacing(2)
        self.setCentralWidget(self.central_widget)

        self.splitter = QSplitter()
        self.actionPanel = QWidget()
        self.actionPanel.setObjectName("ActionPanel")
        self.actionPanel.setFixedHeight(25)
        self.actionLayout = QHBoxLayout(self.actionPanel)
        self.actionLayout.setContentsMargins(5, 1, 5, 1)
        self.lastActionLabel.setObjectName("ActionPanelContent")
        self.actionLayout.addWidget(self.lastActionLabel)
        self.actionLayout.addStretch()
        self.v.addWidget(self.actionPanel)

        self.tree = TreeWidget()
        self.tree.itemRenamed.connect(self.handle_rename_item)
        self.central_tab = DraggableTabWidget()
        self.central_tab.setTabsClosable(True)
        self.central_tab.tabCloseRequested.connect(self.close_tab)
        self.central_tab.currentChanged.connect(self.change_tab)

        self.settings_panel = QScrollArea()
        self.settings_panel.setWidgetResizable(True)
        self.right_content = QStackedWidget()
        self.right_content.setObjectName("rightPanelStack")
        self.settings_panel.setWidget(self.right_content)

        self.setPosForPanels(settings.get_data("panPos", 0))

        self.tree.openRequested.connect(self.handle_open)
        self.tree.renameRequested.connect(self.handle_rename)
        self.tree.deleteRequested.connect(self.handle_delete)
        self.tree.itemSelected.connect(self.handle_item_selected)
        self.tree.createItemRequested.connect(self.createItem)
        self.tree.createCategoryRequested.connect(self.createDirectory)
        self.tree.createCategoryPath.connect(self.createPath)
        self.tree.itemMoved.connect(self.movedItem)
        self.splitter.splitterMoved.connect(self._emit_splitter_changes)

        self.main_splitter = QSplitter(Qt.Orientation.Vertical)
        self.console = ConsoleWidget()
        self.console.start_process(self.path)

        self.main_splitter.addWidget(self.splitter)
        self.main_splitter.addWidget(self.console)
        self.main_splitter.setSizes([600, 200])

        self.v.insertWidget(0, self.main_splitter)

        self.init_test_data()
        self.loadDirsForContent(
            CONTENT_FOLDER.replace("~", self.path).format(package="/".join(self.package.split('.'))))
        self.loadElementsFromFile()
        QApplication.processEvents()
        self.show()

    def get_researchable_elements(self):
        return [el for el in self.elementsData.data.values() if el['data']['data'].get('_canResearch', False)]

    def showTechTree(self):
        elements = self.get_researchable_elements()
        self.techTree.update_elements(elements)
        self.techTree.planetsData = self.planetsData
        self.techTree.show()
        self.techTree.raise_()

    def setTheme(self, theme):
        self.setStyleSheet(theme[1])
        self.techTree.setStyleSheet(theme[1])

    def runTask(self):
        def execute_custom_task():
            dialog.close()
            task_name = dialog.task_input.text().strip()
            if not task_name:
                return

            def task_executor(splash_dialog):
                splash_dialog.text.setText(Language.Lang.Editor.Dialog.start_task.format(name=task_name))
                return self.gradlewManager.run_task(task_name)

            self._execute_task(
                task_name=task_name,
                task_executor=task_executor,
                success_message=Language.Lang.Editor.Dialog.successful,
                error_message=Language.Lang.Editor.Dialog.error
            )

        dialog = self._create_input_dialog(
            title="Gradle Task",
            label="gradle:",
            placeholder="task name",
            execute_callback=execute_custom_task
        )
        dialog.exec()

    def buildTask(self):
        self.generateAllElements()
        def build_executor(splash_dialog):
            splash_dialog.text.setText(Language.Lang.Editor.Dialog.start_task.format(name="Clean"))
            success, message = self.gradlewManager.clean()
            if not success:
                return False, message
            splash_dialog.text.setText(Language.Lang.Editor.Dialog.start_task.format(name="Build"))
            return self.gradlewManager.build(["--warning-mode=all", "--debug"])

        self._execute_task(
            task_name="Build",
            task_executor=build_executor,
            success_message=Language.Lang.Editor.Dialog.build_successful,
            error_message=Language.Lang.Editor.Dialog.error
        )

    def _execute_task(self, task_name, task_executor, success_message, error_message):
        self.setActionLabel(Language.Lang.Editor.Dialog.start_task.format(name=task_name))
        splash_dialog = SplashDil()
        splash_dialog.setFixedSize(300, 120)
        splash_dialog.show()

        result = [None, None]

        def worker():
            try:
                result[0], result[1] = task_executor(splash_dialog)
            except Exception as e:
                result[0], result[1] = False, str(e)

        thread = Thread(target=worker, daemon=True)
        thread.start()
        while thread.is_alive():
            QApplication.processEvents()

        splash_dialog.hide()
        if result[0]:
            QMessageBox.information(self, Language.Lang.Editor.Dialog.successful, success_message)
        else:
            QMessageBox.critical(self, Language.Lang.Editor.Dialog.error, result[1] or error_message)

    def _create_input_dialog(self, title, label, placeholder, execute_callback):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFixedHeight(75)
        layout = QFormLayout(dialog)
        dialog.task_input = QLineEdit()
        dialog.task_input.setPlaceholderText(placeholder)
        layout.addRow(label, dialog.task_input)
        button_layout = QHBoxLayout()
        cancel_button = QPushButton(Language.Lang.Editor.Dialog.cancel)
        cancel_button.clicked.connect(dialog.close)
        execute_button = QPushButton(Language.Lang.Editor.Dialog.run_task)
        execute_button.setDefault(True)
        execute_button.clicked.connect(execute_callback)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(execute_button)
        layout.addRow(button_layout)
        return dialog

    def openProjectSettings(self):
        plugin = self.launcherData.get("plugin", None)
        if plugin and len(plugin) > 0 and plugin[0] in self.main.loadedPlugins:
            self.main.loadedPlugins[plugin[0]].getDialogSettings(self.launcherData)
        else:
            msg = Language.Lang.Editor.Dialog.plugin_created_mod_not_found
            if len(plugin) == 0:
                msg = msg.format(name="unknown")
            else:
                msg = msg.format(name=plugin[0])
            QMessageBox.warning(self, Language.Lang.Editor.Dialog.error, msg)
            return

    def setPosForPanels(self, pos: PanelsPos):
        widgets_order = [self.splitter.widget(i) for i in range(self.splitter.count())]
        sizes_dict = {widget: size for widget, size in zip(widgets_order, self.splitter.sizes())}
        if pos == PanelsPos.Right_Left:
            self.splitter.insertWidget(0, self.settings_panel)
            self.splitter.insertWidget(1, self.central_tab)
            self.splitter.insertWidget(2, self.tree)
        elif pos == PanelsPos.Left_left:
            self.splitter.insertWidget(0, self.tree)
            self.splitter.insertWidget(1, self.settings_panel)
            self.splitter.insertWidget(2, self.central_tab)
        elif pos == PanelsPos.left_Left:
            self.splitter.insertWidget(0, self.settings_panel)
            self.splitter.insertWidget(1, self.tree)
            self.splitter.insertWidget(2, self.central_tab)
        elif pos == PanelsPos.Right_right:
            self.splitter.insertWidget(0, self.central_tab)
            self.splitter.insertWidget(1, self.tree)
            self.splitter.insertWidget(2, self.settings_panel)
        elif pos == PanelsPos.right_Right:
            self.splitter.insertWidget(0, self.central_tab)
            self.splitter.insertWidget(1, self.settings_panel)
            self.splitter.insertWidget(2, self.tree)
        else:
            self.splitter.insertWidget(0, self.tree)
            self.splitter.insertWidget(1, self.central_tab)
            self.splitter.insertWidget(2, self.settings_panel)
        settings.save_data("panPos", pos)
        new_widgets_order = [self.splitter.widget(i) for i in range(self.splitter.count())]
        new_sizes = [sizes_dict.get(widget, 100) for widget in new_widgets_order]
        self.splitter.setSizes(new_sizes)

    def setActionLabel(self, text: str):
        self.lastActionLabel.setText(time.strftime("[%H:%M:%S] ") + text)

    def ShowModFolder(self):
        os.startfile(self.path)

    def exitOnLauncher(self):
        self.notExitOnLauncher = False
        self.close()

    def handle_rename_item(self, old_text, new_text, item: TreeWidgetItem):
        if old_text == new_text:
            item.setText(0, old_text)
        if self.elementsData.__contains__(id(item)) and self.elementsData[id(item)]['tab'] is not None:
            index = self.elementsData[id(item)]['tab']
            self.central_tab.setTabText(index, new_text)
        path = item.get_path()
        path[-1] = old_text
        print(item.data['type'], "renamed")
        if self.elementsData.__contains__(id(item)) and item.data['type'] == "item":
            path1 = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(path)).format(
                package="/".join(self.package.split('.'))) + self.elementsData[id(item)]['data']['end']
            path[-1] = new_text
            path2 = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(path)).format(
                package="/".join(self.package.split('.'))) + self.elementsData[id(item)]['data']['end']
            print(path1, "->", path2)
            if os.path.exists(path1) and not os.path.exists(path2):
                os.rename(path1, path2)
        elif item.data['type'] != "item":
            path1 = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(path)).format(
                package="/".join(self.package.split('.')))
            path[-1] = new_text
            path2 = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(path)).format(
                package="/".join(self.package.split('.')))
            print(path1, "->", path2)
            if os.path.exists(path1) and not os.path.exists(path2):
                os.rename(path1, path2)
        if self.elementsData.__contains__(old_text):
            print("renamed in data")
            self.elementsData.rename_key(old_text, new_text)
            self.elementsData[new_text]['name'] = new_text
        self.saveElementsData()

    def movedItem(self, item: TreeWidgetItem, oldParent: TreeWidgetItem | None):
        oldPath = CONTENT_FOLDER.format(package="/".join(self.package.split('.'))).replace("~/",
                                                                                           self.path + "/") + "/" + "/".join(
            item.get_path()) + self.elementsData[id(item)]["data"]['end']
        item.wParent = item.parent()
        path = item.get_path()
        path.pop(-1)
        self.elementsData[id(item)]["data"]["path"] = "/".join(path)
        self.saveElementsData()
        full = CONTENT_FOLDER.format(package="/".join(self.package.split('.'))).replace("~/",
                                                                                        self.path + "/") + "/" + "/".join(
            item.get_path()) + self.elementsData[id(item)]["data"]['end']
        print(oldPath, "->", full)
        if os.path.exists(oldPath):
            os.rename(oldPath, full)

    def handle_open(self, item):
        if item.data.get('type') == 'category':
            item.setExpanded(not item.isExpanded())
        elif item.data.get('type') == 'item':
            self.show_item_content(item)

    def handle_rename(self, item):
        self.tree.editItem(item, 0)

    def handle_delete(self, item: TreeWidgetItem, force=False):
        if item.data['type'] == "item":
            if not force:
                reply = QMessageBox.question(self, Language.Lang.Editor.Dialog.confirm_action,
                                             Language.Lang.Editor.Dialog.confirm_delete_item,
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply != QMessageBox.StandardButton.Yes:
                    return
            file = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(item.get_path())).format(
                package="/".join(self.package.split('.')))
            if os.path.exists(file + self.elementsData[id(item)]['data']['end']):
                os.remove(file + self.elementsData[id(item)]['data']['end'])
            if self.elementsData[id(item)]['tab'] is not None:
                self.close_tab(self.elementsData[id(item)]['tab'])
            del self.elementsData[id(item)]
            self.saveElementsData()
        else:
            if item.childCount() > 0:
                if not force:
                    reply = QMessageBox.question(self, Language.Lang.Editor.Dialog.confirm_action,
                                                 Language.Lang.Editor.Dialog.confirm_delete_item,
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if reply != QMessageBox.StandardButton.Yes:
                        return
                for i in range(item.childCount()):
                    it: TreeWidgetItem = item.child(0)
                    self.handle_delete(it, True)
            folder = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(item.get_path())).format(
                package="/".join(self.package.split('.')))
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(folder, "removed")
            else:
                print(folder, "not exist!")
        parent = item.parent()
        if parent:
            parent.removeChild(item)
        else:
            index = self.tree.indexOfTopLevelItem(item)
            self.tree.takeTopLevelItem(index)

    def init_test_data(self):
        pass

    def generateImportJavaCode(self, imports, inits) -> str:
        im = "\n".join(imports)
        vr = '\n'.join([f'  {_[2]} {_[1]};' for _ in inits])
        ex = '\n'.join([f'      this.{_[1]} = {_[0]}' for _ in inits])
        template = \
            f"""package {self.package};

{im}

public class initScript {{

{vr}

    void initScript(){{

    }}

    public void loadContent() 
    {{
{ex}
    }}
}}
        """
        return template

    def saveInitScript(self, text):
        path = self.path + f"/src/{'/'.join(self.package.split('.'))}/initScript.java"
        print(path)
        with open(path, "w", encoding="utf-8") as e:
            e.write(text)

    def generateAllElements(self):
        imports = []
        create = []
        for plugname, plugin in self.main.loadedPlugins.items():
            if not plugin.hasConstructor(): continue
            x = plugin.getConstructor().saveElements(self.elementsData, self.package)
            for im, ex in x:
                imports.append(im)
                create.append(ex)
        text = self.generateImportJavaCode(imports, create)
        self.saveInitScript(text)

    def createItem(self, item: TreeWidgetItem | TreeWidget):
        def check():
            items = [_ for _ in self.tree.find_child_by_text(item if isinstance(item, TreeWidgetItem) else None,
                                                             dil.name_edit.text()) if
                     _.data.get("type") != "category"]
            print(items)
            if len(items) > 1 or len(items) > 0 and items[0] != item:
                QMessageBox.warning(self, "Error", Language.Lang.Editor.Dialog.name_exist_item)
            elif dil.name_edit.text() in self.elementsData:
                QMessageBox.warning(self, "Error", Language.Lang.Editor.Dialog.name_exist_item)
            else:
                dil.accept()

        print("Create Item at path:", item.get_path())
        dil = CreateElementDialog(item.get_path())
        dil.save_button.clicked.connect(check)
        r = dil.exec()
        if r == QDialog.DialogCode.Accepted:
            p = dil.category_edit.text().split("/")
            p.append(dil.name_edit.text())
            it = self.add_item_from_name(dil.name_edit.text(), p)
            self.elementsData.add(dil.name_edit.text(), dil.category_edit.text(), id(it), {
                "data": {
                    "data": {},
                    "path": dil.category_edit.text(),
                    "content": dil.type_edit.input_field.text(),
                    "end": LIST_TYPES.get(dil.type_edit.input_field.text())["end"]
                },
                "item": it,
                "tab": None,
                "tab_content": {},
                "name": dil.name_edit.text()
            })
            self.saveElementsData()
            print(self.elementsData.data)
            self.setActionLabel(Language.Lang.Editor.ActionPanel.item_has_been_created_path
                                .format(name=dil.name_edit.text(), path='\'/' + '/'.join(item.get_path())) + '\'')

    def createDirectory(self, item):
        index = 0
        while True:
            p = item.get_path() if item else []
            new_category_name = f"NewCategory_{index}"
            print(new_category_name)
            p.append(new_category_name)
            found = self.tree.find_path_by_text(p)
            print(found, "found")
            if found:
                index += 1
            else:
                it = self.tree.add_item(p, {"type": "category", "flag": []})
                self.createPath(it)
                break

    def createPath(self, item):
        folder = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(item.get_path())).format(
            package="/".join(self.package.split('.')))
        print(folder)
        os.makedirs(folder, exist_ok=True)

    def getDirs(self, directory):
        try:
            return [
                os.path.join(directory, item)
                for item in os.listdir(directory)
                if os.path.isdir(os.path.join(directory, item))
            ]
        except:
            return []

    def loadDirsForContent(self, directory, fname=""):
        folders = self.getDirs(directory + "/" + fname)
        for name in folders:
            name = name.replace(
                CONTENT_FOLDER.format(package="/".join(self.package.split('.'))).replace("~", self.path), "").replace(
                "\\",
                "/").replace(
                "//", "/")
            path = [_ for _ in name.split("/") if _ != ""]
            it = self.tree.add_item(path, {"type": "category", "flag": []})
            self.loadDirsForContent(directory, name)

    def loadElementsFromFile(self):
        path = os.path.join(self.path, "Elements.mmg_j")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as e:
                    data = json.load(e)
                    print(data)
                    for name in data:
                        print("load name...")
                        path = data[name]["path"].split("/")
                        path.append(name)
                        item = self.add_item_from_name(name, path)
                        # Принудительно устанавливаем _canResearch: True для wall1
                        if name == "wall1":
                            data[name]["data"]["_canResearch"] = True
                        self.elementsData.add(name, "/".join(item.get_path()), id(item), {
                            "data": data[name],
                            "tab": None,
                            "tab_content": {},
                            "item": item,
                            "name": name
                        })
            except Exception as err:
                QMessageBox.warning(self, Language.Lang.Editor.Dialog.error,
                                    Language.Lang.Editor.Dialog.error_load_elements_save.format(err=str(err)))

    def add_item_from_name(self, name: str, path: List[str]) -> TreeWidgetItem:
        path = [_ for _ in path if _.strip() != '']
        print(path)
        return self.tree.add_item(path, {"type": "item", "flag": [], 'name': name})

    def saveElementsData(self):
        data = {}
        for el in self.elementsData.data:
            d = self.elementsData.data[el]
            data[d["name"]] = d["data"]
        with open(self.path + "/Elements.mmg_j", "w", encoding="utf-8") as e:
            json.dump(data, e, indent=4)

    def handle_item_selected(self, item):
        if item.data.get('type') == 'item':
            self.show_item_content(item)

    def show_item_content(self, item: TreeWidgetItem):
        if self.elementsData[id(item)]['tab'] is not None:
            self.central_tab.setCurrentIndex(self.elementsData[id(item)]['tab'])
            return
        content = self.elementsData[id(item)]['data']['content']
        if content in LIST_TYPES:
            canvas: PreviewWidget = LIST_TYPES.get(self.elementsData[id(item)]['data']['content'])['centralWidget']()
            editor_widget = TabbedCustomEditor(
                id=id(item),
                name=item.text(0),
                classe=LIST_TYPES[content]["type"],
                changed_params=self.elementsData[id(item)]['data']['data']
            )
            right_widget = editor_widget
            self.right_content.addWidget(right_widget)
            self.create_tab(canvas, right_widget, item)
            right_widget.pack()
            right_widget.saveFromSelf.connect(self.saveFromSelf)
            return
        canvas = QLabel('Unknown content type')
        right_widget = QLabel("Unknown type")
        self.right_content.addWidget(right_widget)
        self.create_tab(canvas, right_widget, item)

    def saveFromSelf(self, widget: TabbedCustomEditor, data: dict):
        for identifier in self.elementsData.data:
            elementData = self.elementsData.data[identifier]
            if elementData['tab'] is None: continue
            tab = elementData['tab_content']
            if tab["w2"] == widget:
                item_text = tab["item"].text(0)
                self.elementsData[item_text]["data"]["data"] = tab["item"].data["data"] = data
                self.saveElementsData()
                self.setActionLabel(Language.Lang.Editor.ActionPanel.item_has_been_saved.format(name=item_text))
                return True
        return False

    def set_index_tab(self, index):
        self.central_tab.setCurrentIndex(index)

    def create_tab(self, w1, w2, item):
        index = self.central_tab.addTab(w1, item.text(0))
        self.elementsData[id(item)]["tab_content"] = {
            "w1": w1,
            "w2": w2,
            "item": item,
            "index": index
        }
        ALL_TABS[id(item)] = (w1, w2, item)
        self.elementsData[id(item)]["tab"] = index
        self.set_index_tab(index)
        self.set_right_panel_content(w2)

    def close_tab(self, index):
        for el in self.elementsData.data:
            data = self.elementsData.data[el]
            w1 = self.central_tab.widget(index)
            if data.get("tab_content", {}).get("w1") == w1 and w1 is not None:
                tab = data["tab_content"]
                tab["w1"].deleteLater()
                tab["w2"].deleteLater()
                data["tab_content"] = {}
                data["tab"] = None
                del ALL_TABS[id(data["item"])]
                self.central_tab.removeTab(index)
                return

    def change_tab(self, index):
        key = self.central_tab.tabText(index)
        if key in self.elementsData:
            if self.elementsData[key]['tab'] is None: return
            data = self.elementsData[key]["tab_content"]
            self.set_right_panel_content(data["w2"])

    def set_right_panel_content(self, widget):
        self.right_content.setCurrentWidget(widget)

    def _emit_splitter_changes(self):
        self.splitterPosChanged.emit(self.splitter.sizes())

    def apply_settings(self, settings):
        if 'splitter_sizes' in settings:
            self.splitter.setSizes(settings['splitter_sizes'])
        if 'main_splitter' in settings:
            self.main_splitter.setSizes(settings['main_splitter'])
        if 'window_geometry' in settings:
            self.restoreGeometry(QByteArray.fromHex(bytes(settings['window_geometry'], 'utf-8')))

    def closeEvent(self, event):
        self.console.terminate_process()
        save_data = {
            'splitter_sizes': self.splitter.sizes(),
            'main_splitter': self.main_splitter.sizes(),
            'window_geometry': bytes(self.saveGeometry()).hex()
        }
        self.saveRequested.emit(save_data)
        self.closeSignal.emit(event, self.notExitOnLauncher)