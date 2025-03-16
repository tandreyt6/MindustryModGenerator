import json
import os.path
import shutil
import uuid
from typing import List

import hjson
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from UI.Content.CentralPreviewWidget import PreviewWidget
from UI.Elements.CardConstructor import TabbedCustomEditor
from UI.Elements.CreateElementDialog import CreateElementDialog
from UI.Elements.DragTab import DraggableTabWidget
from func.GLOBAL import CONTENT_FOLDER, LIST_TYPES
from func.Types.Content import Content


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
        return self.parent().parent().handle_rename_validation(old_text, new_text, item)

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
            open_action = menu.addAction("Open")
        rename_action = None
        if item and 'NoChange' not in item.data.get('flag', []):
            rename_action = menu.addAction("Rename")
        delete_action = None
        if item and 'NoDelete' not in item.data.get('flag', []):
            delete_action = menu.addAction("Delete")
        create_category = None
        if not item or (item and item.data.get("type", "") == "category"):
            create_category = menu.addAction("Create Category")
        create_element = None
        if not item or (item and item.data.get("type", "") == "category"):
            create_element = menu.addAction("Create Item")

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


class EditorWindow(QMainWindow):
    splitterPosChanged = pyqtSignal(list)
    saveRequested = pyqtSignal(dict)
    closeSignal = pyqtSignal(object, bool)
    settingsWindowRequest = pyqtSignal()

    def __init__(self, path):
        super().__init__()
        self.elementsData = ElementsDict()
        self.path = path
        self.data = {}
        self.notExitOnLauncher = True
        if path:
            with open(os.path.join(path, "mod.hjson"), "r", encoding="utf-8") as e:
                self.data = hjson.load(e)
        self.package = self.data.get("main", "example.javaMod").split(".")[0]
        self.init_ui()


    def handle_rename_validation(self, old_name, new_name, item):
        if not new_name.strip():
            QMessageBox.warning(self, "Error", "Name cannot be empty")
            return False
        if len(new_name) < 3:
            QMessageBox.warning(self, "Error", "Name is long!")
            return False
        if new_name[0].isdigit():
            QMessageBox.warning(self, "Error", "The first character should not be a digit")
            return False
        items = [_ for _ in self.tree.find_child_by_text(item.parent(), new_name) if _.data.get("type") != "category"]
        folders = [_ for _ in self.tree.find_child_by_text(item.parent(), new_name) if _.data.get("type") == "category"]
        print(items)
        print(folders)
        path = item.get_path()
        path[-1] = new_name
        if ((len(items)>1 or len(items)>0 and items[0] != item) and item.data.get("type") != "category") or (item.data.get("type") == "category" and any(_.get_path() == path for _ in folders)):
            QMessageBox.warning(self, "Error", "This name is already exist")
            return False
        if new_name in self.elementsData and item.data.get("type") != "category":
            QMessageBox.warning(self, "Error", "This name is already exist")
            return False
        if item.data.get("type") != "category" and self.elementsData[old_name]['item'] != id(item) and new_name in self.elementsData.key_map:
            QMessageBox.warning(self, "Error", "Name must be unique")
            return False
        return True

    def init_ui(self):
        self.setWindowTitle(self.data.get("displayName", "") + " - Editor")
        if self.path:
            self.setWindowIcon(QIcon(os.path.join(self.path, "icon.png")))
        self.setGeometry(100, 100, 1200, 800)

        menubar = self.menuBar()

        FileMenu:QMenu = menubar.addMenu('File')

        self.settingsAct = QAction("Settings...")
        self.settingsAct.triggered.connect(self.settingsWindowRequest.emit)
        FileMenu.addAction(self.settingsAct)
        self.openModFolder = QAction("Show project folder")
        self.openModFolder.triggered.connect(self.ShowModFolder)
        FileMenu.addAction(self.openModFolder)
        FileMenu.addSeparator()
        self.exitOnLauncherAct = QAction("Exit project")
        self.exitOnLauncherAct.triggered.connect(self.exitOnLauncher)
        FileMenu.addAction(self.exitOnLauncherAct)

        menubar.addMenu('View')
        menubar.addMenu('Build')
        menubar.addMenu('Gradle')

        self.splitter = QSplitter()
        self.setCentralWidget(self.splitter)

        self.tree = TreeWidget()
        self.tree.itemRenamed.connect(self.handle_rename_item)
        self.splitter.addWidget(self.tree)

        self.central_tab = DraggableTabWidget()
        self.central_tab.setTabsClosable(True)
        self.central_tab.tabCloseRequested.connect(self.close_tab)
        self.central_tab.currentChanged.connect(self.change_tab)
        self.splitter.addWidget(self.central_tab)

        self.right_panel = QScrollArea()
        self.right_panel.setWidgetResizable(True)
        self.right_content = QStackedWidget()
        self.right_panel.setWidget(self.right_content)
        self.splitter.addWidget(self.right_panel)

        self.tree.openRequested.connect(self.handle_open)
        self.tree.renameRequested.connect(self.handle_rename)
        self.tree.deleteRequested.connect(self.handle_delete)
        self.tree.itemSelected.connect(self.handle_item_selected)
        self.tree.createItemRequested.connect(self.createItem)
        self.tree.createCategoryRequested.connect(self.createDirectory)
        self.tree.createCategoryPath.connect(self.createPath)
        self.tree.itemMoved.connect(self.movedItem)
        self.splitter.splitterMoved.connect(self._emit_splitter_changes)

        self.init_test_data()

        self.loadDirsForContent(CONTENT_FOLDER.replace("~", self.path).format(package=self.package))
        self.loadElementsFromFile()

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
        if self.elementsData.__contains__(id(item)) and item.data['type'] == "item":
            path1 = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(path)).format(
                package=self.package) + self.elementsData[id(item)]['data']['end']
            path[-1] = new_text
            path2 = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(path)).format(
                package=self.package) + self.elementsData[id(item)]['data']['end']
            print(path1, "->", path2)
            if os.path.exists(path1) and not os.path.exists(path2):
                os.rename(path1, path2)
        elif item.data['type'] != "item":
            path1 = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(path)).format(
                package=self.package)
            path[-1] = new_text
            path2 = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(path)).format(
                package=self.package)
            print(path1, "->", path2)
            if os.path.exists(path1) and not os.path.exists(path2):
                os.rename(path1, path2)
        if self.elementsData.__contains__(old_text):
            print("renamed in data")
            self.elementsData.rename_key(old_text, new_text)
            self.elementsData[new_text]['name'] = new_text
        self.saveElementsData()

    def movedItem(self, item: TreeWidgetItem, oldParent: TreeWidgetItem|None):
        oldPath = CONTENT_FOLDER.format(package=self.package).replace("~/", self.path+"/")+"/"+"/".join(item.get_path())+self.elementsData[id(item)]["data"]['end']
        item.wParent = item.parent()
        path = item.get_path()
        path.pop(-1)
        self.elementsData[id(item)]["data"]["path"] = "/".join(path)
        self.saveElementsData()
        full = CONTENT_FOLDER.format(package=self.package).replace("~/", self.path+"/")+"/"+"/".join(item.get_path())+self.elementsData[id(item)]["data"]['end']
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
                reply = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to proceed?',
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                if reply != QMessageBox.StandardButton.Yes:
                    return

            file = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(item.get_path())).format(
                package=self.package)
            if os.path.exists(file+self.elementsData[id(item)]['data']['end']):
                os.remove(file+self.elementsData[id(item)]['data']['end'])
            del self.elementsData[id(item)]
            self.saveElementsData()
        else:
            if item.childCount() > 0:
                if not force:
                    reply = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to proceed?',
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if reply != QMessageBox.StandardButton.Yes:
                        return
                for i in range(item.childCount()):
                    it: TreeWidgetItem = item.child(0)
                    self.handle_delete(it, True)
            folder = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(item.get_path())).format(
                package=self.package)
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

    def generateImportJavaCode(self) -> str:
        imports = ""
        inits = []
        variabeles = ""

        for key in self.elementsData.data:
            name = self.elementsData.data[key]['name']
            cls: Content = LIST_TYPES.get(self.elementsData[name]['data']['content'])["type"][0](name)
            cls.package = self.package+".content."+".".join(self.elementsData[name]['data']['path'].split("/"))
            codes = cls.create_java_code()
            imports += f"{codes[0]}\n"
            var = "    public "+cls.name+" var_"+name.strip()+";"
            variabeles += var+"\n"
            inits.append( f"        this."+"var_"+name.strip()+" = "+codes[1])
        inits = "\n".join(inits)
        template = \
f"""package {self.package};

{imports}

public class initScript {{

{variabeles}

    void initScript(){{

    }}
    
    public void loadContent() 
    {{
{inits}
    }}
}}
        """
        return template

    def saveInitScript(self):
        text = self.generateImportJavaCode()
        path = self.path+f"/src/{self.package}/initScript.java"
        print(path)
        with open(path, "w", encoding="utf-8") as e:
            e.write(text)

    def createItem(self, item: TreeWidgetItem | TreeWidget):
        def check():
            items = [_ for _ in self.tree.find_child_by_text(item if isinstance(item, TreeWidgetItem) else None, dil.name_edit.text()) if
                     _.data.get("type") != "category"]
            print(items)
            if len(items) > 1 or len(items) > 0 and items[0] != item:
                QMessageBox.warning(self, "Error", "This name is already exist")
            elif dil.name_edit.text() in self.elementsData:
                QMessageBox.warning(self, "Error", "This name is already exist")
            else: dil.accept()

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
        folder = (CONTENT_FOLDER.replace("~", self.path) + "/" + "/".join(item.get_path())).format(package=self.package)
        print(folder)
        os.makedirs(folder, exist_ok=True)

    def getDirs(self, directory):
        return [
            os.path.join(directory, item)
            for item in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, item))
        ]

    def loadDirsForContent(self, directory, fname=""):
        folders = self.getDirs(directory+"/"+fname)
        for name in folders:
            name = name.replace(CONTENT_FOLDER.format(package=self.package).replace("~", self.path), "").replace("\\", "/").replace("//", "/")
            path = [_ for _ in name.split("/") if _ != ""]
            it = self.tree.add_item(path, {"type": "category", "flag": []})
            self.loadDirsForContent(directory, name)

    def loadElementsFromFile(self):
        path = os.path.join(self.path, "elements.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as e:
                    data = json.load(e)
                    for name in data:
                        path = data[name]["path"].split("/")
                        path.append(name)
                        item = self.add_item_from_name(name, path)
                        self.elementsData.add(name, "/".join(item.get_path()), id(item), {"data": data[name],
                                                                                      "tab": None,
                                                                                      "tab_content": {},
                                                                                      "item": item,
                                                                                      "name": name})
            except Exception as err:
                QMessageBox.warning(self, "Error load saves!", "Load elements failed!\n"+str(err))

    def add_item_from_name(self, name: str, path: List[str]) -> TreeWidgetItem:
        path = [_ for _ in path if _.strip() != '']
        print(path)
        return self.tree.add_item(path, {"type": "item", "flag": [], 'name': name})

    def saveElementsData(self):
        data = {}
        for el in self.elementsData.data:
            d = self.elementsData.data[el]
            data[d["name"]] = d["data"]
        with open(self.path+"/elements.json", "w", encoding="utf-8") as e:
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
                classes=LIST_TYPES[content]["type"],
                changed_params=self.elementsData[id(item)]['data']['data'],
                categories=LIST_TYPES[content]['paramCategory']
            )
            for custom in LIST_TYPES[content]['customParam']:
                editor_widget.register_custom_widget(custom, LIST_TYPES[content]['customParam'][custom])
            editor_widget.pack()
            editor_widget.saveFromSelf.connect(self.saveFromSelf)
            right_widget = editor_widget
        else:
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

                cls: Content = widget.classes[0](item_text)
                cls.loadFromDict(data)

                pkg = [self.package + ".content"] + tab["item"].get_path()[:-1]
                cls.package = ".".join(pkg)

                path = os.path.join(CONTENT_FOLDER.format(package=self.package), *pkg[1:]).replace("~", self.path)
                os.makedirs(path, exist_ok=True)
                with open(os.path.join(path, item_text + self.elementsData[item_text]['data']['end']), "w", encoding="utf-8") as e:
                    e.write(cls.java_code())

                self.saveInitScript()

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
        self.elementsData[id(item)]["tab"] = index
        self.set_index_tab(index)
        self.set_right_panel_content(w2)

    def close_tab(self, index):
        for el in self.elementsData.data:
            data = self.elementsData.data[el]
            if data["tab"] == index:
                tab = data["tab_content"]
                tab["w1"].deleteLater()
                tab["w2"].deleteLater()
                data["tab_content"] = {}
                data["tab"] = None
                self.central_tab.removeTab(index)

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
        if 'window_geometry' in settings:
            self.restoreGeometry(QByteArray.fromHex(bytes(settings['window_geometry'], 'utf-8')))

    def closeEvent(self, event):
        save_data = {
            'splitter_sizes': self.splitter.sizes(),
            'window_geometry': bytes(self.saveGeometry()).hex()
        }
        self.saveRequested.emit(save_data)
        self.closeSignal.emit(event, self.notExitOnLauncher)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)


    def handle_save(data):
        print("Save data:", data)


    window = EditorWindow("")
    window.saveRequested.connect(handle_save)

    example_settings = {
        'splitter_sizes': [250, 800, 300],
        'window_geometry': '...'
    }
    window.apply_settings(example_settings)

    window.show()
    sys.exit(app.exec())
