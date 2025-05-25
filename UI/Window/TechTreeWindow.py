import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem,
    QSplitter, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QListWidget, QInputDialog, QMessageBox,
    QToolBar, QGroupBox, QStatusBar, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsPathItem, QGraphicsTextItem, QComboBox, QTabWidget, QDockWidget, QAbstractItemView,
    QFileDialog
)
from PyQt6.QtCore import Qt, QSize, QRectF, QPointF, QRect, QEvent, QMimeData
from PyQt6.QtGui import QFont, QIcon, QKeySequence, QAction, QPalette, QColor, QPen, QPainterPath, QBrush, QPainter, QDrag

from SerpuloTechTree import SerpuloTree
from UI.Window.WindowAbs import WindowAbs

DARK_PALETTE = {
    'window': QColor(45, 45, 45),
    'base': QColor(35, 35, 35),
    'highlight': QColor(64, 64, 64),
    'text': QColor(224, 224, 224),
    'button': QColor(64, 64, 64),
    'border': QColor(69, 69, 69)
}

class TechNode:
    def __init__(self, name: str, can_save = True):
        self.name = name
        self.children = []
        self.requirements = []
        self.parent = None
        self.subtree = None
        self.can_save = can_save
        self.direction = "down"

    def add_requirement(self, req_type: str, *args):
        self.requirements.append((req_type, *args))

    def to_dict(self):
        return {
            'name': self.name,
            'can_save': self.can_save,
            'direction': self.direction,
            'requirements': [list(req) for req in self.requirements],
            'children': [c.to_dict() for c in self.children]
        }

    @staticmethod
    def from_dict(d: dict) -> 'TechNode':
        node = TechNode(d['name'], can_save=d.get('can_save', True))
        node.direction = d.get('direction', 'down')
        for req in d.get('requirements', []):
            node.add_requirement(req[0], *req[1:])
        for cd in d.get('children', []):
            child = TechNode.from_dict(cd)
            child.parent = node
            node.children.append(child)
        return node

class TechTree:
    def __init__(self):
        self.root = None
        self.name = "serpulo"
        self.planet_name = "serpulo"
        self.nodes = {}

    def to_dict(self) -> dict:
        if not self.root:
            return None
        return {
            'planet_name': self.planet_name,
            'nodes': self.root.to_dict()
        }

    @staticmethod
    def from_dict(d: dict) -> 'TechTree':
        if d is None:
            return None
        tree = TechTree()
        tree.planet_name = d.get('planet_name')
        root = TechNode.from_dict(d['nodes'])
        tree.root = root

        # пробежимся по всем узлам, занесём в tree.nodes
        def index(node: TechNode):
            tree.nodes[node.name] = node
            for c in node.children:
                c.parent = node
                index(c)

        index(root)
        return tree

    def generate_java_code(self, builder_var: str = None) -> str:
        start_nodes = [node for node in self.nodes.values()
                       if node.can_save and (node.parent is None or not node.parent.can_save)]

        lines = []
        indent = 0

        def add_line(line: str):
            lines.append("    " * indent + line)

        def recurse(node: TechNode):
            nonlocal indent
            prefix = "nodeRoot" if node is self.root else "node"
            if prefix == "nodeRoot":
                add_line(f"{builder_var}.{self.planet_name}.techTree = {prefix}(\"{node.name}\", {builder_var}, () -> {{")
            else:
                if node.requirements:
                    reqs = []
                    for req in node.requirements:
                        rtype, *params = req
                        if rtype == 'sector':
                            reqs.append(f"new SectorComplete({params[0]})")
                        elif rtype == 'research':
                            reqs.append(f"new ResearchComplete({params[0]})")
                    add_line(f"{prefix}({node.name}, Seq.with({', '.join(reqs)}), () -> {{")
                else:
                    add_line(f"{prefix}({node.name}, () -> {{")

            indent += 1
            for child in node.children:
                if child.can_save:
                    recurse(child)
            indent -= 1
            add_line("});")

        for root_node in start_nodes:
            if not builder_var:
                builder_var = self.planet_name
            recurse(root_node)

        return "\n".join(lines)

    def add_node(self, parent_name: str, node: TechNode, requirements: list = None):
        if node.name in self.nodes:
            raise ValueError(f"Node {node.name} already exists")
        if not self.root and parent_name is None:
            self.root = node
            self.nodes[node.name] = node
            return
        parent = self.nodes.get(parent_name)
        if not parent:
            parent = TechNode(parent_name, True)
            self.nodes[parent_name] = parent
        node.parent = parent
        parent.children.append(node)
        self.nodes[node.name] = node
        if requirements:
            for req in requirements:
                node.add_requirement(*req)

    def clear(self):
        self.root = None
        self.nodes.clear()

    def find_node(self, name: str):
        return self.nodes.get(name)

class NodeItem(QGraphicsRectItem):
    def __init__(self, tech_node, x, y, width=200, height=80, parent=None):
        super().__init__(0, 0, width, height)
        self.parent = parent
        self.tech_node = tech_node
        self.setPos(x, y)
        self.setBrush(QBrush(QColor(100, 100, 100)))
        self.setPen(QPen(QColor(200, 200, 200)))
        self.setAcceptHoverEvents(True)
        self.setToolTip(self.tech_node.name)
        text = QGraphicsTextItem(self.tech_node.name, self)
        text.setDefaultTextColor(QColor(255, 255, 255))
        text.setPos(10, 10)
        text.setTextWidth(width - 20)
        font = QFont()
        font.setPointSize(14)
        text.setFont(font)
        text_rect = text.boundingRect()
        if text_rect.width() > width - 20:
            scale_factor = (width - 20) / text_rect.width()
            text.setScale(min(scale_factor, 1.0))

    def mousePressEvent(self, event):
        window = self.parent
        window.select_node_in_tree(self.tech_node)

    def hoverEnterEvent(self, event):
        self.setPen(QPen(QColor(255, 0, 0), 2))

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(QColor(200, 200, 200)))

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setAcceptDrops(True)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self._zoom = 1.0
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

    def wheelEvent(self, event):
        zoom_in_factor = 1.1
        zoom_out_factor = 1 / zoom_in_factor
        delta = event.angleDelta().y()
        zoom_factor = zoom_in_factor if delta > 0 else zoom_out_factor
        new_zoom = self._zoom * zoom_factor
        if 0.1 <= new_zoom <= 2.0:
            self._zoom = new_zoom
            self.resetTransform()
            self.scale(self._zoom, self._zoom)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        pos = event.position().toPoint()
        scene_pos = self.mapToScene(pos)
        items = self.scene().items(scene_pos)
        for it in items:
            if isinstance(it, NodeItem):
                src = event.mimeData().text()
                node = it.tech_node
                if src not in [c.name for c in node.children]:
                    resp = QMessageBox.question(self, "Add Node", f"Добавить «{src}» к «{node.name}»?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if resp == QMessageBox.StandardButton.Yes:
                        new_node = TechNode(src)
                        new_node.direction = node.direction
                        self.parent().tech_tree.add_node(node.name, new_node)
                        self.parent()._populate_tree(new_node, None)
                        self.parent().build_scene()
                break
        event.acceptProposedAction()

class DropGraphicsView(CustomGraphicsView):
    def __init__(self, scene, parent_editor):
        super().__init__(scene)
        self.parent_editor = parent_editor
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if not event.mimeData().hasText():
            return super().dropEvent(event)

        src = event.mimeData().text()
        pos = event.position().toPoint()
        scene_pos = self.mapToScene(pos)
        items = self.scene().items(scene_pos)
        for it in items:
            if isinstance(it, NodeItem):
                node = it.tech_node
                if src in [c.name for c in node.children]:
                    QMessageBox.information(self, "Info", f"Узел «{src}» уже есть в «{node.name}»")
                    event.ignore()
                    return
                reply = QMessageBox.question(
                    self, "Добавить узел",
                    f"Добавить «{src}» к «{node.name}»?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    new_node = TechNode(src)
                    new_node.direction = node.direction
                    self.parent_editor.tech_tree.add_node(node.name, new_node)
                    self.parent_editor.tree.clear()
                    self.parent_editor.load_tree()
                    self.parent_editor.build_scene()
                break

        event.acceptProposedAction()

class ElementsTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item and item.childCount() == 0:  # Only allow dragging leaf nodes
            mimeData = QMimeData()
            mimeData.setText(item.text(0))
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec(Qt.DropAction.CopyAction)

class DropTree(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setDragEnabled(False)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.DropAction.CopyAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if not event.mimeData().hasText():
            return super().dropEvent(event)

        src = event.mimeData().text()
        pos = event.position().toPoint()
        target = self.itemAt(pos)
        if not target:
            event.ignore()
            return

        node = target.tech_node
        if src in [c.name for c in node.children]:
            QMessageBox.information(self, "Info", f"Узел «{src}» уже есть в «{node.name}»")
            event.ignore()
            return

        reply = QMessageBox.question(
            self, "Добавить узел",
            f"Добавить «{src}» к «{node.name}»?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            new_node = TechNode(src)
            new_node.direction = node.direction
            self.parent().tech_tree.add_node(node.name, new_node)
            self.parent()._populate_tree(new_node, target)
            self.parent().build_scene()

        event.acceptProposedAction()

class TechTreeEditor(QWidget):
    def __init__(self, tech_tree, name="Tree"):
        super().__init__()
        self.name = name
        self.tech_tree = tech_tree
        self.current_item = None
        self.node_positions = {}
        self.init_ui()
        self.setAcceptDrops(True)
        self.tree.viewport().setAcceptDrops(True)
        self.graphics_view.viewport().setAcceptDrops(True)
        self.tree.viewport().installEventFilter(self)
        self.graphics_view.viewport().installEventFilter(self)
        self.load_tree()
        self.setup_shortcuts()
        self.build_scene()

    def init_ui(self):
        self.tree = DropTree()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.on_item_selected)
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search...")
        self.search_field.textChanged.connect(self.filter_tree)

        self.add_action = QAction(QIcon.fromTheme("list-add"), "Add Node", self)
        self.remove_action = QAction(QIcon.fromTheme("list-remove"), "Remove Node", self)
        self.save_action = QAction(QIcon.fromTheme("document-save"), "Save", self)
        self.create_subtree_action = QAction("Create Subtree", self)
        self.create_subtree_action.setIcon(QIcon.fromTheme("document-new"))
        self.create_subtree_action.triggered.connect(self.create_subtree)
        details_panel = QWidget()
        details_layout = QVBoxLayout(details_panel)
        self.name_edit = QLineEdit()
        self.requirements_list = QListWidget()
        req_buttons = QHBoxLayout()
        self.add_req_btn = QPushButton("Add Requirement")
        self.remove_req_btn = QPushButton("Remove Requirement")
        req_buttons.addWidget(self.add_req_btn)
        req_buttons.addWidget(self.remove_req_btn)

        details_layout.addWidget(QLabel("Node Name:"))
        details_layout.addWidget(self.name_edit)
        details_layout.addWidget(QLabel("Requirements:"))
        details_layout.addWidget(self.requirements_list)
        details_layout.addLayout(req_buttons)
        self.scene = QGraphicsScene()
        self.graphics_view = DropGraphicsView(self.scene, self)
        splitter = QSplitter()
        splitter.addWidget(self.create_tree_panel())
        splitter.addWidget(self.graphics_view)
        splitter.addWidget(details_panel)
        splitter.setSizes([300, 500, 300])
        v = QVBoxLayout(self)
        v.setSpacing(0)
        v.setContentsMargins(0, 0, 0, 0)
        v.addWidget(splitter)

    def create_subtree(self):
        if not self.current_item:
            QMessageBox.warning(self, "Error", "Select a node first")
            return
        node = self.current_item.tech_node
        if node.subtree:
            QMessageBox.warning(self, "Error", "This node already has a subtree")
            return
        name, ok = QInputDialog.getText(self, "Subtree Name", "Enter subtree name:")
        if not ok or not name:
            return
        subtree = TechTree()
        subtree.root = node
        subtree.nodes = {node.name: node}
        node.subtree = (name, subtree)
        main = self.window()
        main.add_subtree_tab(subtree, name, parent_item=self.current_item)
        self.build_scene()

    def create_tree_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.addWidget(self.search_field)
        layout.addWidget(self.tree)
        return panel

    def setup_shortcuts(self):
        self.add_action.triggered.connect(self.add_node)
        self.remove_action.triggered.connect(self.remove_node)
        self.save_action.triggered.connect(self.save_tree)
        self.add_req_btn.clicked.connect(self.add_requirement)
        self.remove_req_btn.clicked.connect(self.remove_requirement)
        self.add_action.setShortcut("Ctrl+T")
        self.remove_action.setShortcut(QKeySequence.StandardKey.Delete)
        self.save_action.setShortcut("Ctrl+S")

    def load_tree(self):
        self.tree.clear()
        self._populate_tree(self.tech_tree.root, None)

    def _populate_tree(self, node, parent_item):
        item = QTreeWidgetItem([node.name])
        item.tech_node = node
        if parent_item is None:
            self.tree.addTopLevelItem(item)
        else:
            parent_item.addChild(item)
        for child in node.children:
            self._populate_tree(child, item)

    def on_item_selected(self, item):
        self.current_item = item
        node = item.tech_node
        self.name_edit.setText(node.name)
        self.requirements_list.clear()
        for req in node.requirements:
            self.requirements_list.addItem(f"{req[0]}: {', '.join(map(str, req[1:]))}")

        self.highlight_path(node)

    def update_direction(self, direction_text):
        if not self.current_item:
            return
        node = self.current_item.tech_node
        if node.parent == self.tech_tree.root:
            node.direction = "up" if direction_text == "Up" else "down"
            self._propagate_direction(node, node.direction)
            self.build_scene()

    def _propagate_direction(self, node, direction):
        for child in node.children:
            child.direction = direction
            self._propagate_direction(child, direction)

    def add_node(self):
        parent_item = self.tree.currentItem()
        if not parent_item:
            QMessageBox.warning(self, "Warning", "Select a parent node first!")
            return
        name, ok = QInputDialog.getText(self, "New Node", "Node name:")
        if ok and name:
            try:
                new_node = TechNode(name)
                new_node.direction = parent_item.tech_node.direction
                self.tech_tree.add_node(parent_item.tech_node.name, new_node)
                self._populate_tree(new_node, parent_item)
                self.build_scene()
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))

    def remove_node(self):
        item = self.tree.currentItem()
        if not item or item.tech_node == self.tech_tree.root:
            return
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete '{item.tech_node.name}' and all children?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            parent = item.parent()
            if parent:
                parent.tech_node.children.remove(item.tech_node)
                del self.tech_tree.nodes[item.tech_node.name]
                parent.removeChild(item)
                self.build_scene()

    def save_tree(self):
        java_code = self.tech_tree.generate_java_code(
            builder_var=self.name
        )
        return java_code


    def add_requirement(self):
        if not self.current_item:
            return
        req_type, ok = QInputDialog.getItem(
            self, "Requirement Type", "Type:", ["sector", "research"], 0, False
        )
        if not ok:
            return
        values, ok = QInputDialog.getText(
            self, "Requirement Values", "Enter values (comma separated):"
        )
        if ok and values:
            args = [v.strip() for v in values.split(",")]
            self.current_item.tech_node.add_requirement(req_type, *args)
            self.on_item_selected(self.current_item)

    def remove_requirement(self):
        if not self.current_item and self.requirements_list.currentRow() >= 0:
            del self.current_item.tech_node.requirements[self.requirements_list.currentRow()]
            self.on_item_selected(self.current_item)

    def filter_tree(self, text):
        for i in range(self.tree.topLevelItemCount()):
            self._filter_item(self.tree.topLevelItem(i), text.lower())

    def _filter_item(self, item, text):
        visible = text in item.text(0).lower()
        item.setHidden(not visible)
        for i in range(item.childCount()):
            child = item.child(i)
            if self._filter_item(child, text) or visible:
                item.setExpanded(True)
                item.setHidden(False)
        return visible

    def build_scene(self):
        self.scene.clear()
        self.node_positions = {}
        self._layout_tree(self.tech_tree.root)
        self._draw_scene(self.tech_tree.root)
        self._center_scene()

    def _layout_tree(self, node, level=0, x_offset=0, level_width=400, level_height=250, parent_y=0):
        node_y = 0 if node == self.tech_tree.root else parent_y + (level_height if node.direction == "down" else -level_height)
        up_children = [c for c in node.children if c.direction == "up"]
        down_children = [c for c in node.children if c.direction == "down"]
        def layout_subtree(children, base_x_offset, y_base):
            total_width = 0
            child_bounds = []
            for child in children:
                min_x, max_x, width = self._layout_tree(
                    child, level + 1, base_x_offset + total_width, level_width, level_height, y_base
                )
                child_bounds.append((min_x, max_x, width))
                total_width += width + level_width
            if total_width > 0:
                total_width -= level_width
            first_x = child_bounds[0][0] if child_bounds else base_x_offset
            last_x = child_bounds[-1][1] if child_bounds else base_x_offset
            center = (first_x + last_x) / 2
            return child_bounds, total_width, center
        up_bounds, up_width, up_center = layout_subtree(up_children, x_offset, node_y)
        down_bounds, down_width, down_center = layout_subtree(down_children, x_offset, node_y)
        if up_children and down_children:
            node_x = (up_center + down_center) / 2
        elif up_children:
            node_x = up_center
        elif down_children:
            node_x = down_center
        else:
            node_x = x_offset
        self.node_positions[node] = (node_x, node_y)
        all_min_x = [node_x] + [b[0] for b in up_bounds + down_bounds]
        all_max_x = [node_x] + [b[1] for b in up_bounds + down_bounds]
        return min(all_min_x), max(all_max_x), max(all_max_x) - min(all_min_x)

    def _draw_scene(self, node):
        if node in self.node_positions:
            x, y = self.node_positions[node]
            width, height = 200, 80
            item = NodeItem(node, x, y, width=width, height=height, parent=self)
            self.scene.addItem(item)

            if node.subtree:
                tree_name, _ = node.subtree
                label = QGraphicsTextItem(tree_name)
                label.setDefaultTextColor(QColor(255, 215, 0))
                br = label.boundingRect()
                label.setPos(x + width/2 - br.width()/2, y - br.height() - 10)
                self.scene.addItem(label)
                path = QPainterPath()
                path.moveTo(x + width/2, y)
                path.lineTo(x + width/2, y - br.height() - 10)
                connector = QGraphicsPathItem(path)
                connector.setPen(QPen(QColor(255, 215, 0), 2, Qt.PenStyle.DashLine))
                self.scene.addItem(connector)

            for child in node.children:
                self._draw_scene(child)
                cx, cy = self.node_positions[child]
                path = QPainterPath()
                if child.direction == "down":
                    path.moveTo(x + width/2, y + height)
                    path.lineTo(x + width/2, y + height + 50)
                    path.lineTo(cx + width/2, y + height + 50)
                    path.lineTo(cx + width/2, cy)
                else:
                    path.moveTo(x + width/2, y)
                    path.lineTo(x + width/2, y - 50)
                    path.lineTo(cx + width/2, y - 50)
                    path.lineTo(cx + width/2, cy + height)
                line = QGraphicsPathItem(path)
                line.setPen(QPen(QColor(200, 200, 200), 2))
                self.scene.addItem(line)

    def _center_scene(self):
        if not self.node_positions:
            return
        xs, ys = zip(*self.node_positions.values())
        min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
        scene_w, scene_h = max_x - min_x + 600, max_y - min_y + 800
        center_x, center_y = (min_x + max_x) / 2, (min_y + max_y) / 2
        vw, vh = self.graphics_view.viewport().width(), self.graphics_view.viewport().height()
        scale = min(vw / scene_w, vh / scene_h, 1.0)
        scale = max(scale, 0.8)
        self.graphics_view.resetTransform()
        self.graphics_view.scale(scale, scale)
        self.graphics_view.centerOn(center_x, center_y)

    def highlight_path(self, node):
        path_nodes = set()
        n = node
        while n:
            path_nodes.add(n)
            n = n.parent
        for item in self.scene.items():
            if isinstance(item, NodeItem):
                if item.tech_node in path_nodes:
                    item.setOpacity(1.0)
                else:
                    item.setOpacity(0.3)

    def select_node_in_tree(self, node):
        items = self.tree.findItems(node.name, Qt.MatchFlag.MatchRecursive)
        if items:
            self.tree.setCurrentItem(items[0])
            self.on_item_selected(items[0])

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.DragEnter:
            if event.mimeData().hasText():
                event.acceptProposedAction()
                return True
        if event.type() == QEvent.Type.Drop:
            src = event.mimeData().text()
            if source is self.tree.viewport():
                pos = event.position().toPoint()
                item = self.tree.itemAt(pos)
                if item:
                    node = item.tech_node
                    if src not in [c.name for c in node.children]:
                        resp = QMessageBox.question(self, "Добавить узел", f"Добавить «{src}» к «{node.name}»?",
                                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                        if resp == QMessageBox.StandardButton.Yes:
                            new_node = TechNode(src)
                            new_node.direction = node.direction
                            self.tech_tree.add_node(node.name, new_node)
                            self._populate_tree(new_node, item)
                            self.build_scene()
                event.acceptProposedAction()
                return True
            if source is self.graphics_view.viewport():
                pos = event.position().toPoint()
                scene_pos = self.graphics_view.mapToScene(pos)
                items = self.scene.items(scene_pos)
                for it in items:
                    if isinstance(it, NodeItem):
                        node = it.tech_node
                        if src in self.tech_tree.nodes:
                            QMessageBox.critical(QApplication.activeWindow(), "Error", "Эта нода уже существует!")
                            return True
                        if src not in [c.name for c in node.children]:
                            resp = QMessageBox.question(self, "Добавить узел", f"Добавить «{src}» к «{node.name}»?",
                                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                            if resp == QMessageBox.StandardButton.Yes:
                                new_node = TechNode(src)
                                new_node.direction = node.direction
                                self.tech_tree.add_node(node.name, new_node)
                                self.load_tree()
                                self.build_scene()
                        break
                event.acceptProposedAction()
                return True
        return super().eventFilter(source, event)

def create_serpulo_tree():
    tree = TechTree()
    def build_tree(parent_name, node_data):
        node = TechNode(node_data['name'], False)
        if parent_name == 'serpulo':
            if node.name in ['conveyor', 'coreFoundation', 'mechanicalDrill', 'duo']:
                node.direction = "up"
            else:
                node.direction = "down"
        else:
            if parent_name:
                node.direction = tree.find_node(parent_name).direction
        tree.add_node(parent_name, node)
        for req in node_data.get('requirements', []):
            node.add_requirement(req[0], req[1])
        for child in node_data.get('children', []):
            build_tree(node_data['name'], child)
    build_tree(None, SerpuloTree)
    return tree

class TechTreeWindow(WindowAbs):
    def __init__(self):
        super().__init__()
        self.planetsData = {}
        self.setWindowTitle("Tab Manager")

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.dock = QDockWidget()
        self.elements_tree = ElementsTree()
        self.elements_tree.setHeaderHidden(True)
        self.dock.setWidget(self.elements_tree)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

        self.toolbar = QToolBar("Управление вкладками")
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        add_tab_action = QAction("Создать вкладку", self)
        add_tab_action.triggered.connect(self.add_tab)
        self.toolbar.addAction(add_tab_action)

        close_tab_action = QAction("Закрыть текущую", self)
        close_tab_action.triggered.connect(self.close_current_tab)
        self.toolbar.addAction(close_tab_action)

        self.add_tab()

    def closeEvent(self, a0):
        self.tabs.widget(0).save_tree()
        super().closeEvent(a0)

    def update_elements(self, elements):
        self.elements_tree.clear()
        for element in elements:
            path_parts = element['data']['path'].split('/') if element['data']['path'] else []
            current = self.elements_tree
            for part in path_parts:
                current = self.find_or_create_child(current, part)
            leaf = QTreeWidgetItem([element['name']])
            leaf.setData(0, Qt.ItemDataRole.UserRole, element)
            if current == self.elements_tree:
                self.elements_tree.addTopLevelItem(leaf)
            else:
                current.addChild(leaf)

    def find_or_create_child(self, parent, text):
        if isinstance(parent, QTreeWidget):
            for i in range(parent.topLevelItemCount()):
                item = parent.topLevelItem(i)
                if item.text(0) == text:
                    return item
            new_item = QTreeWidgetItem([text])
            parent.addTopLevelItem(new_item)
            return new_item
        else:
            for i in range(parent.childCount()):
                item = parent.child(i)
                if item.text(0) == text:
                    return item
            new_item = QTreeWidgetItem([text])
            parent.addChild(new_item)
            return new_item

    def add_subtree_tab(self, tree, name, parent_item):
        tab = TechTreeEditor(tree, name)
        tab.parent_link = parent_item
        self.tabs.addTab(tab, name)
        self.tabs.setCurrentWidget(tab)

    def add_tab(self):
        free_planets = [
            planet_name
            for planet_name, pdata in self.planetsData.items()
            if pdata.get('tree') is None
        ]
        if not free_planets:
            QMessageBox.information(self, "Нет свободных планет", "Все планеты уже заняты деревьями.")
            return

        planet, ok = QInputDialog.getItem(
            self, "Выбор планеты", "Планета:", free_planets, 0, False
        )
        if not ok or not planet:
            return

        tree = create_serpulo_tree()
        tree.name = planet
        tab = TechTreeEditor(tree, planet)
        tab.parent_link = None
        self.tabs.addTab(tab, planet)
        self.tabs.setCurrentWidget(tab)

        self.planetsData[planet]['tree'] = tree

    def close_tab(self, index):
        widget = self.tabs.widget(index)
        planet = widget.name

        reply = QMessageBox.question(
            self,
            "Удалить дерево",
            f"Вы действительно хотите удалить дерево технологии для планеты '{planet}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        if planet in self.planetsData:
            self.planetsData[planet]['tree'] = None

        self.tabs.removeTab(index)

    def get_save_dict(self) -> dict:
        out = {}
        for planet, pdata in self.planetsData.items():
            tree = pdata.get('tree')
            out[planet] = tree.to_dict() if tree else None
        return out

    def load_from_dict(self, data: dict):
        for planet, tree_d in data.items():
            if tree_d is None:
                self.planetsData[planet]['tree'] = None
            else:
                tree = TechTree.from_dict(tree_d)
                tree.name = planet
                tree.planet_name = planet
                self.planetsData[planet]['tree'] = tree
                tab = TechTreeEditor(tree, planet)
                self.tabs.addTab(tab, planet)

    def close_current_tab(self):
        index = self.tabs.currentIndex()
        if index != -1:
            self.tabs.removeTab(index)
        else:
            QMessageBox.information(self, "Нет вкладок", "Нет открытых вкладок для закрытия.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TechTreeWindow()
    window.show()
    sys.exit(app.exec())