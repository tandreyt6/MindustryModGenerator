import os
import sys
import json
import traceback
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem,
    QSplitter, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QListWidget, QInputDialog, QMessageBox,
    QToolBar, QGroupBox, QStatusBar, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsPathItem, QGraphicsTextItem, QComboBox, QTabWidget, QDockWidget, QAbstractItemView,
    QFileDialog, QMenu
)
from PyQt6.QtCore import Qt, QSize, QRectF, QPointF, QRect, QEvent, QMimeData
from PyQt6.QtGui import QFont, QIcon, QKeySequence, QAction, QPalette, QColor, QPen, QPainterPath, QBrush, QPainter, QDrag

from UI import Language
from UI.Elements.TechTreeReq import RequirementsPanel
from UI.Window.WindowAbs import WindowAbs

EXISTING_ITEMS = [
    'coreShard', 'coreFoundation', 'coreNucleus', 'conveyor', 'junction', 'router',
    'mechanicalDrill', 'duo', 'graphitePress', 'copperWall', 'titaniumWall',
    'scatter', 'scorch', 'hail', 'wave', 'tsunami', 'lancer', 'arc'
]

elementsData = []

DARK_PALETTE = {
    'window': QColor(45, 45, 45),
    'base': QColor(35, 35, 35),
    'highlight': QColor(64, 64, 64),
    'text': QColor(224, 224, 224),
    'button': QColor(64, 64, 64),
    'border': QColor(69, 69, 69)
}

def node_to_dict(node):
    result = {
        'name': node.name,
        'direction': node.direction,
        'can_save': node.can_save,
        'requirements': node.requirements,
        'children': [node_to_dict(child) for child in node.children]
    }
    return result

class TechNode:
    def __init__(self, name: str, can_save=True, direction="down"):
        self.name = name
        self.children = []
        self.requirements = []
        self.parent = None
        self.can_save = can_save
        self.direction = direction

    def add_requirement(self, req_type: str, *args):
        if req_type == 'resource':
            self.requirements.append((req_type, args[0]))
        else:
            self.requirements.append((req_type, *args))

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    @classmethod
    def from_dict(cls, d):
        node = cls(d['name'], can_save=d.get('can_save', True), direction=d.get('direction', 'down'))
        node.requirements = d.get('requirements', [])
        for child_data in d.get('children', []):
            child = cls.from_dict(child_data)
            child.parent = node
            node.children.append(child)
        return node

class TechTree:
    def __init__(self, name, allows_multiple_roots=False):
        self.roots = []
        self.name = name
        self.planet_name = name
        self.nodes = {}
        self.allows_multiple_roots = allows_multiple_roots

    def to_dict(self) -> dict:
        return {
            'planet_name': self.planet_name,
            'allows_multiple_roots': self.allows_multiple_roots,
            'roots': [node_to_dict(root) for root in self.roots]
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'TechTree':
        tree = cls(d['planet_name'], d.get('allows_multiple_roots', False))
        tree.roots = [TechNode.from_dict(root_d) for root_d in d.get('roots', [])]
        for root in tree.roots:
            def index(node):
                tree.nodes[node.name] = node
                for c in node.children:
                    c.parent = node
                    index(c)
            index(root)
        return tree

    def generate_java_code(self, builder_var: str = None) -> str:
        if not builder_var:
            builder_var = 'TechTree'
        lines = []

        def get_ref(name: str) -> str:
            return f"Blocks.{name}" if name in EXISTING_ITEMS else f"_mcl.var_{name}"

        for root in self.roots:
            var_node = f"{root.name}Node"
            root_ref = get_ref(root.name)
            lines.append(f"var {var_node} = TechTree.all.find(t -> t.content == {root_ref});")
            lines.append(f"if ({var_node} != null) {{")
            parent_var = var_node
            for child in root.children:
                child_ref = get_ref(child.name)
                lines.append(f"    new TechTree.TechNode({parent_var}, {child_ref}, {child_ref}.researchRequirements());")
            lines.append("}")
        return "\n".join(lines)

    def add_node(self, parent_name: str, node: TechNode, requirements: list = None):
        if parent_name is None and node.name in [root.name for root in self.roots]:
            raise ValueError(f"Node '{node.name}' already exists as a root node")
        if node.name in self.nodes and node in self.roots:
            self.roots.pop(self.roots.index(node))
            self.nodes.pop(node.name)
        if parent_name == node.name:
            raise ValueError("An item cannot be added to itself.")
        if parent_name is None:
            if self.allows_multiple_roots or len(self.roots) == 0:
                self.roots.append(node)
                self.nodes[node.name] = node
                node.can_save = True
            else:
                raise ValueError("Only one root allowed for this planet")
        else:
            parent = self.nodes.get(parent_name)
            if not parent:
                raise ValueError(f"Parent node {parent_name} does not exist")
            node.parent = parent
            node.can_save = True
            parent.children.append(node)
            self.nodes[node.name] = node
        if requirements:
            for req in requirements:
                node.add_requirement(*req)

    def clear(self):
        self.roots = []
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
        self.setAcceptDrops(True)
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
        if event.button() == Qt.MouseButton.LeftButton:
            window = self.parent
            window.select_node_in_tree(self.tech_node)
        elif event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event)

    def show_context_menu(self, event):
        menu = QMenu()
        show_action = menu.addAction(Language.Lang.TechTreeWindow.Dialog.select)
        delete_action = menu.addAction(Language.Lang.TechTreeWindow.Dialog.remove)
        action = menu.exec(event.screenPos())
        if action == show_action:
            window = self.parent
            window.select_node_in_tree(self.tech_node)

        elif action == delete_action:
            reply = QMessageBox.question(
                self.parent,
                "",
                Language.Lang.TechTreeWindow.Dialog.remove_selected_item.format(name=self.tech_node.name),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.parent.remove_node(self.tech_node)

    def hoverEnterEvent(self, event):
        self.setPen(QPen(QColor(255, 0, 0), 2))

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(QColor(200, 200, 200)))

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if not event.mimeData().hasText():
            return
        text = event.mimeData().text()
        node = self.tech_node
        if text.startswith("move:"):
            src = text[5:]
            if src == node.name:
                event.ignore()
                return
            if self.parent.is_descendant(src, node.name):
                QMessageBox.critical(self.parent, Language.Lang.Editor.Dialog.error,
                                     Language.Lang.TechTreeWindow.Dialog.error_join_parent_to_parent)
                event.ignore()
                return
            reply = QMessageBox.question(
                self.parent, "",
                Language.Lang.TechTreeWindow.Dialog.rejoin_item_to_child.format(child=src, parent=node.name),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.parent.reparent_node(src, node.name)
                self.parent.load_tree()
                self.parent.build_scene()
            event.acceptProposedAction()

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

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

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
        text = event.mimeData().text()
        pos = event.position().toPoint()
        scene_pos = self.mapToScene(pos)
        items = self.scene.items(scene_pos)
        for it in items:
            if isinstance(it, NodeItem):
                node = it.tech_node
                if text.startswith("move:"):
                    src = text[5:]
                    if src == node.name:
                        event.ignore()
                        return
                    if self.parent_editor.is_descendant(src, node.name):
                        QMessageBox.critical(self, Language.Lang.Editor.Dialog.error,
                                             Language.Lang.TechTreeWindow.Dialog.error_join_parent_to_parent)
                        event.ignore()
                        return
                    reply = QMessageBox.question(
                        self, "",
                        Language.Lang.TechTreeWindow.Dialog.rejoin_item_to_child.format(child=src, parent=node.name),
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.Yes:
                        self.parent_editor.reparent_node(src, node.name)
                        self.parent_editor.tree.clear()
                        self.parent_editor.load_tree()
                        self.parent_editor.build_scene()
                else:
                    src = text
                    if src == node.name:
                        event.ignore()
                        return
                    if src in self.parent_editor.tech_tree.nodes:
                        if self.parent_editor.is_descendant(src, node.name):
                            QMessageBox.critical(self, Language.Lang.Editor.Dialog.error,
                                                 Language.Lang.TechTreeWindow.Dialog.error_join_parent_to_parent)
                            event.ignore()
                            return
                        reply = QMessageBox.question(
                            self, "",
                            Language.Lang.TechTreeWindow.Dialog.rejoin_item_to_child.format(child=src,
                                                                                            parent=node.name),
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                        )
                        if reply == QMessageBox.StandardButton.Yes:
                            self.parent_editor.reparent_node(src, node.name)
                            self.parent_editor.tree.clear()
                            self.parent_editor.load_tree()
                            self.parent_editor.build_scene()
                    else:
                        reply = QMessageBox.question(
                            self, "",
                            Language.Lang.TechTreeWindow.Dialog.join_item_to_parent.format(child=src, parent=node.name),
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                        )
                        if reply == QMessageBox.StandardButton.Yes:
                            new_node = TechNode(src, can_save=True, direction=node.direction)
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
        if item and item.childCount() == 0:
            mimeData = QMimeData()
            mimeData.setText(item.text(0))
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec(Qt.DropAction.CopyAction)

class DropTree(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item and item.childCount() == 0:
            mimeData = QMimeData()
            mimeData.setText(f"move:{item.text(0)}")
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec(Qt.DropAction.MoveAction)

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
        text = event.mimeData().text()
        pos = event.position().toPoint()
        target = self.itemAt(pos)
        if not target:
            event.ignore()
            return
        node = target.tech_node
        if text.startswith("move:"):
            src = text[5:]
            if src == node.name or self.parent().is_descendant(src, node.name):
                event.ignore()
                return
            reply = QMessageBox.question(
                self, "",
                Language.Lang.TechTreeWindow.Dialog.rejoin_item_to_child.format(child=src,
                                                                                parent=node.name),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.parent().reparent_node(src, node.name)
                self.parent().tree.clear()
                self.parent().load_tree()
                self.parent().build_scene()
        else:
            src = text
            if src == node.name or self.parent().is_descendant(src, node.name):
                event.ignore()
                return
            if src in self.parent().tech_tree.nodes:
                reply = QMessageBox.question(
                    self, "",
                    Language.Lang.TechTreeWindow.Dialog.rejoin_item_to_child.format(child=src,
                                                                                    parent=node.name),
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.parent().reparent_node(src, node.name)
                    self.parent().tree.clear()
                    self.parent().load_tree()
                    self.parent().build_scene()
            else:
                reply = QMessageBox.question(
                    self, "",
                    Language.Lang.TechTreeWindow.Dialog.join_item_to_parent.format(child=src, parent=node.name),
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    new_node = TechNode(src, can_save=True, direction=node.direction)
                    self.parent().tech_tree.add_node(node.name, new_node)
                    self.parent().tree.clear()
                    self.parent().load_tree()
                    self.parent().build_scene()
        event.acceptProposedAction()

class TechTreeEditor(QWidget):
    def __init__(self, tech_tree: TechTree, name="Tree"):
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
        self.build_scene()

    def init_ui(self):
        self.tree = DropTree()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self.on_item_selected)
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText(Language.Lang.TechTreeWindow.Dialog.search_)
        self.search_field.textChanged.connect(self.filter_tree)
        self.name_edit = QLineEdit()
        self.requirements_panel = RequirementsPanel(parent=self)
        self.scene = QGraphicsScene()
        self.graphics_view = DropGraphicsView(self.scene, self)
        splitter = QSplitter()
        splitter.addWidget(self.create_tree_panel())
        splitter.addWidget(self.graphics_view)
        splitter.addWidget(self.requirements_panel)
        splitter.setSizes([300, 500, 300])
        v = QVBoxLayout(self)
        v.setSpacing(0)
        v.setContentsMargins(0, 0, 0, 0)
        v.addWidget(splitter)

    def create_tree_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.addWidget(self.search_field)
        layout.addWidget(self.tree)
        return panel

    def load_tree(self):
        self.tree.clear()
        for root in self.tech_tree.roots:
            self._populate_tree(root, None)

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
        self.requirements_panel.set_tech_node(node)
        self.highlight_path(node)

    def update_direction(self, direction_text):
        if not self.current_item:
            return
        node = self.current_item.tech_node
        node.direction = "up" if direction_text.lower() == "up" else "down"
        self._propagate_direction(node, node.direction)
        self.build_scene()

    def _propagate_direction(self, node, direction):
        for child in node.children:
            child.direction = direction
            self._propagate_direction(child, direction)

    def add_root_node(self):
        if self.name in ["Serpulo", "Erekir"]:
            items_list = EXISTING_ITEMS
        else:
            items_list = [item['name'] for item in elementsData]
        title = Language.Lang.TechTreeWindow.Dialog.select_existing_root_item
        if not items_list:
            QMessageBox.warning(self, Language.Lang.Editor.Dialog.error, Language.Lang.TechTreeWindow.Dialog.item_list_empty_error)
            return
        name, ok = QInputDialog.getItem(self, "", title, items_list, 0, False)
        if ok and name:
            try:
                new_node = TechNode(name, can_save=True, direction="down")
                self.tech_tree.add_node(None, new_node)
                item = QTreeWidgetItem([name])
                item.tech_node = new_node
                self.tree.addTopLevelItem(item)
                self.build_scene()
                if hasattr(self.window(), 'update_add_root_button'):
                    self.window().update_add_root_button()
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))

    def remove_node(self, node=None):
        if node is None:
            item = self.tree.currentItem()
            if not item:
                return
            node = item.tech_node
        if node in self.tech_tree.roots:
            self.tech_tree.roots.remove(node)
        self._remove_node_recursive(node)
        self.load_tree()
        self.build_scene()
        if hasattr(self.window(), 'update_add_root_button'):
            self.window().update_add_root_button()

    def _remove_node_recursive(self, node):
        for child in node.children[:]:
            self._remove_node_recursive(child)
        if node.parent:
            node.parent.children.remove(node)
        if node.name in self.tech_tree.nodes:
            del self.tech_tree.nodes[node.name]

    def reparent_node(self, node_name: str, new_parent_name: str):
        node = self.tech_tree.find_node(node_name)
        if not node or node_name == new_parent_name:
            QMessageBox.warning(self, Language.Lang.Editor.Dialog.error, Language.Lang.TechTreeWindow.Dialog.rejoin_item_error)
            return
        if node in self.tech_tree.roots:
            self.tech_tree.roots.remove(node)
        elif node.parent:
            node.parent.children.remove(node)
        self.tech_tree.add_node(new_parent_name, node)

    def is_descendant(self, node_name: str, potential_descendant_name: str) -> bool:
        node = self.tech_tree.find_node(node_name)
        if not node:
            return False

        def check_descendants(current_node):
            if current_node.name == potential_descendant_name:
                return True
            for child in current_node.children:
                if check_descendants(child):
                    return True
            return False

        return check_descendants(node)

    def build_scene(self):
        self.scene.clear()
        self.node_positions = {}
        x_offset = 0
        for root in self.tech_tree.roots:
            min_x, max_x, width = self._layout_tree(root, level=0, x_offset=x_offset)
            x_offset += width + 400
        self._draw_scene()
        self._center_scene()

    def _layout_tree(self, node: TechNode, level=0, x_offset=0, level_width=400, level_height=250,
                     parent_y=0):
        node_y = parent_y if node.parent else 0
        up_children = [c for c in node.children if c.direction == "up"]
        down_children = [c for c in node.children if c.direction == "down"]

        def layout_subtree(children, base_x_offset, y_base):
            total_width = 0
            child_bounds = []
            for child in children:
                min_x, max_x, width = self._layout_tree(child, level + 1, base_x_offset + total_width,
                                                        level_width, level_height, y_base)
                child_bounds.append((min_x, max_x, width))
                total_width += width + level_width
            if total_width > 0:
                total_width -= level_width
            first_x = child_bounds[0][0] if child_bounds else base_x_offset
            last_x = child_bounds[-1][1] if child_bounds else base_x_offset
            center = (first_x + last_x) / 2
            return child_bounds, total_width, center

        up_bounds, up_w, up_c = layout_subtree(up_children, x_offset, node_y - level_height)
        down_bounds, down_w, down_c = layout_subtree(down_children, x_offset, node_y + level_height)
        if up_children and down_children:
            node_x = (up_c + down_c) / 2
        elif up_children:
            node_x = up_c
        elif down_children:
            node_x = down_c
        else:
            node_x = x_offset
        self.node_positions[node] = (node_x, node_y)
        all_min = [node_x] + [b[0] for b in up_bounds + down_bounds]
        all_max = [node_x] + [b[1] for b in up_bounds + down_bounds]
        return min(all_min), max(all_max), max(all_max) - min(all_min)

    def _draw_scene(self):
        for root in self.tech_tree.roots:
            self._draw_subtree(root)

    def _draw_subtree(self, node):
        x, y = self.node_positions[node]
        w, h = 200, 80
        item = NodeItem(node, x, y, width=w, height=h, parent=self)
        self.scene.addItem(item)
        for child in node.children:
            self._draw_subtree(child)
            cx, cy = self.node_positions[child]
            path = QPainterPath()
            if child.direction == "down":
                path.moveTo(x + w / 2, y + h)
                path.lineTo(x + w / 2, y + h + 50)
                path.lineTo(cx + w / 2, y + h + 50)
                path.lineTo(cx + w / 2, cy)
            else:
                path.moveTo(x + w / 2, y)
                path.lineTo(x + w / 2, y - 50)
                path.lineTo(cx + w / 2, y - 50)
                path.lineTo(cx + w / 2, cy + h)
            line = QGraphicsPathItem(path)
            line.setPen(QPen(QColor(200, 200, 200), 2))
            self.scene.addItem(line)

    def _center_scene(self):
        if not self.node_positions:
            return
        xs, ys = zip(*self.node_positions.values())
        min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
        sw, sh = max_x - min_x + 600, max_y - min_y + 800
        cx, cy = (min_x + max_x) / 2, (min_y + max_y) / 2
        vw, vh = self.graphics_view.viewport().width(), self.graphics_view.viewport().height()
        scale = min(vw / sw, vh / sh, 1.0)
        scale = max(scale, 0.8)
        self.graphics_view.resetTransform()
        self.graphics_view.scale(scale, scale)
        self.graphics_view.centerOn(cx, cy)

    def highlight_path(self, node):
        path_nodes = set()
        n = node
        while n:
            path_nodes.add(n)
            n = n.parent
        for it in self.scene.items():
            if isinstance(it, NodeItem):
                it.setOpacity(1.0 if it.tech_node in path_nodes else 0.3)

    def select_node_in_tree(self, node):
        items = self.tree.findItems(node.name, Qt.MatchFlag.MatchRecursive)
        if items:
            self.tree.setCurrentItem(items[0])
            self.on_item_selected(items[0])

    def save_tree(self):
        try:
            main = self.window()
            main.save_all_to_java()
            main.save_to_file()
        except Exception as e:
            QMessageBox.warning(self, Language.Lang.TechTreeWindow.Dialog.save_error, str(e))

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

    def add_requirement(self):
        if not self.current_item:
            QMessageBox.warning(self, "", Language.Lang.Editor.Dialog.error)
            return
        req_type, ok = QInputDialog.getItem(self, Language.Lang.TechTreeWindow.Dialog.research_type, "", ["sector", "research", "resource"],
                                            0, False)
        if not ok:
            return
        if req_type == "resource":
            inp, ok = QInputDialog.getText(self, Language.Lang.TechTreeWindow.Dialog.resources, "")
            if ok and inp:
                lst = []
                for seg in inp.split(','):
                    k, v = seg.split(':')
                    lst.append((k.strip(), int(v.strip())))
                self.current_item.tech_node.add_requirement(req_type, lst)
        else:
            vals, ok = QInputDialog.getText(self, Language.Lang.TechTreeWindow.Dialog.value, "")
            if ok and vals:
                args = [v.strip() for v in vals.split(',')]
                self.current_item.tech_node.add_requirement(req_type, *args)
        self.on_item_selected(self.current_item)

    def remove_requirement(self):
        if not self.current_item or self.requirements_list.currentRow() < 0:
            QMessageBox.warning(self, "", Language.Lang.Editor.Dialog.error)
            return
        del self.current_item.tech_node.requirements[self.requirements_list.currentRow()]
        self.on_item_selected(self.current_item)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.DragEnter and event.mimeData().hasText():
            event.acceptProposedAction()
            return True
        if event.type() == QEvent.Type.Drop:
            text = event.mimeData().text()
            if source is self.tree.viewport():
                pos = event.position().toPoint()
                item = self.tree.itemAt(pos)
                if item:
                    node = item.tech_node
                    if text.startswith("move:"):
                        src = text[5:]
                        if src == node.name or self.is_descendant(src, node.name):
                            event.ignore()
                            return True
                        reply = QMessageBox.question(
                            self, "",
                            Language.Lang.TechTreeWindow.Dialog.rejoin_item_to_child.format(child=src,
                                                                                            parent=node.name),
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                        )
                        if reply == QMessageBox.StandardButton.Yes:
                            self.reparent_node(src, node.name)
                            self.tree.clear()
                            self.load_tree()
                            self.build_scene()
                    else:
                        src = text
                        if src == node.name or self.is_descendant(src, node.name):
                            event.ignore()
                            return True
                        if src in self.tech_tree.nodes:
                            reply = QMessageBox.question(
                                self, "",
                                Language.Lang.TechTreeWindow.Dialog.rejoin_item_to_child.format(child=src,
                                                                                                parent=node.name),
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                            )
                            if reply == QMessageBox.StandardButton.Yes:
                                self.reparent_node(src, node.name)
                                self.tree.clear()
                                self.load_tree()
                                self.build_scene()
                        else:
                            resp = QMessageBox.question(
                                self, "",
                                Language.Lang.TechTreeWindow.Dialog.join_item_to_parent.format(child=src,
                                                                                               parent=node.name),
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                            )
                            if resp == QMessageBox.StandardButton.Yes:
                                new_node = TechNode(src, can_save=True, direction=node.direction)
                                self.tech_tree.add_node(node.name, new_node)
                                self._populate_tree(new_node, item)
                                self.build_scene()
                    event.acceptProposedAction()
                    return True
            if source is self.graphics_view.viewport():
                pos = event.position().toPoint()
                scene_pos = self.graphics_view.mapToScene(pos)
                for it in self.scene.items(scene_pos):
                    if isinstance(it, NodeItem):
                        node = it.tech_node
                        if text.startswith("move:"):
                            src = text[5:]
                            if src == node.name or self.is_descendant(src, node.name):
                                event.ignore()
                                return True
                            reply = QMessageBox.question(
                                self, "",
                                Language.Lang.TechTreeWindow.Dialog.rejoin_item_to_child.format(child=src,
                                                                                                parent=node.name),
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                            )
                            if reply == QMessageBox.StandardButton.Yes:
                                self.reparent_node(src, node.name)
                                self.tree.clear()
                                self.load_tree()
                                self.build_scene()
                        else:
                            src = text
                            if src == node.name or self.is_descendant(src, node.name):
                                event.ignore()
                                return True
                            if src in self.tech_tree.nodes:
                                resp = QMessageBox.question(
                                    self, "",
                                    Language.Lang.TechTreeWindow.Dialog.rejoin_item_to_child.format(child=src,
                                                                                                    parent=node.name),
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                )
                                if resp == QMessageBox.StandardButton.Yes:
                                    self.reparent_node(src, node.name)
                                    self.tree.clear()
                                    self.load_tree()
                                    self.build_scene()
                            else:
                                resp = QMessageBox.question(
                                    self, "",
                                    Language.Lang.TechTreeWindow.Dialog.join_item_to_parent.format(child=src,
                                                                                                   parent=node.name),
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                )
                                if resp == QMessageBox.StandardButton.Yes:
                                    new_node = TechNode(src, can_save=True, direction=node.direction)
                                    self.tech_tree.add_node(node.name, new_node)
                                    self.load_tree()
                                    self.build_scene()
                        break
                event.acceptProposedAction()
                return True
        return super().eventFilter(source, event)

class TechTreeWindow(WindowAbs):
    def __init__(self):
        super().__init__()
        self._can_full_close = False
        self._package = ""
        self.project_path = None

        self.setWindowTitle("Tech Tree - editor")

        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.addContentWidget(central_widget)

        self.elements_tree = ElementsTree()
        self.elements_tree.setHeaderHidden(True)
        main_layout.addWidget(self.elements_tree, 1)

        central_panel = QWidget()
        central_layout = QVBoxLayout()
        central_panel.setLayout(central_layout)
        main_layout.addWidget(central_panel, 4)

        self.toolbar_panel = QWidget()
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        self.toolbar_panel.setLayout(toolbar_layout)

        self.add_tab_action = QPushButton(Language.Lang.TechTreeWindow.Dialog.create_tree)
        self.add_tab_action.clicked.connect(self.add_tab)
        toolbar_layout.addWidget(self.add_tab_action)

        self.close_tab_action = QPushButton(Language.Lang.TechTreeWindow.Dialog.remove_tree)
        self.close_tab_action.clicked.connect(self.close_tab)
        toolbar_layout.addWidget(self.close_tab_action)

        self.add_root_button = QPushButton(Language.Lang.TechTreeWindow.Dialog.add_root_node)
        self.add_root_button.clicked.connect(self.add_root_to_current_tab)
        toolbar_layout.addWidget(self.add_root_button)

        self.remove_button = QPushButton(Language.Lang.TechTreeWindow.Dialog.remove_node)
        self.remove_button.clicked.connect(self.remove_from_current_tab)
        toolbar_layout.addWidget(self.remove_button)

        self.save_button = QPushButton(Language.Lang.Editor.Dialog.save)
        self.save_button.clicked.connect(self.save_all)
        toolbar_layout.addWidget(self.save_button)

        central_layout.addWidget(self.toolbar_panel)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_add_root_button)
        central_layout.addWidget(self.tabs)

        serpulo_tree = TechTree("Serpulo", allows_multiple_roots=True)
        serpulo_tab = TechTreeEditor(serpulo_tree, "Serpulo")
        self.tabs.addTab(serpulo_tab, "Serpulo")

        erekir_tree = TechTree("Erekir", allows_multiple_roots=True)
        erekir_tab = TechTreeEditor(erekir_tree, "Erekir")
        self.tabs.addTab(erekir_tab, "Erekir")

        self.update_add_root_button()

    def add_root_to_current_tab(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.add_root_node()

    def remove_from_current_tab(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.remove_node()

    def save_all(self):
        self.save_to_file()
        self.save_all_to_java()

    def update_add_root_button(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            tree = current_tab.tech_tree
            if tree.allows_multiple_roots or len(tree.roots) == 0:
                self.add_root_button.setEnabled(True)
            else:
                self.add_root_button.setEnabled(False)
        else:
            self.add_root_button.setEnabled(False)

    def closeEvent(self, a0):
        self.save_to_file()
        if self._can_full_close:
            super().closeEvent(a0)
        else:
            a0.ignore()
            self.hide()


    def update_elements(self, elements):
        global elementsData
        elementsData = elements
        self.elements_tree.clear()
        for element in elements:
            parts = element['data']['path'].split('/') if element['data']['path'] else []
            current = self.elements_tree
            for part in parts:
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

    def add_tab(self):
        used_names = [self.tabs.tabText(i) for i in range(self.tabs.count())]

        mod_items = [item['name'] for item in elementsData]
        if not mod_items:
            QMessageBox.warning(self, Language.Lang.Editor.Dialog.error,
                                Language.Lang.TechTreeWindow.Dialog.item_list_empty_error)
            return

        name, ok = QInputDialog.getText(self, "", Language.Lang.TechTreeWindow.Dialog.enter_tree_name)
        if not ok or not name.strip():
            return
        name = name.strip()
        if name in used_names:
            QMessageBox.warning(self, Language.Lang.Editor.Dialog.error,
                                Language.Lang.TechTreeWindow.Dialog.tech_tree_name_exist_error)
            return

        root_name, ok = QInputDialog.getItem(
            self,
            "",
            Language.Lang.TechTreeWindow.Dialog.select_existing_root_item,
            mod_items,
            0,
            False
        )

        tree = TechTree(name, allows_multiple_roots=False)
        root_node = TechNode(root_name, can_save=True)
        tree.add_node(None, root_node)
        tab = TechTreeEditor(tree, name)
        self.tabs.addTab(tab, name)
        self.tabs.setCurrentWidget(tab)
        self.update_add_root_button()

    def close_tab(self, index):
        widget = self.tabs.widget(index)
        planet = widget.name
        if planet in ["Serpulo", "Erekir"]:
            QMessageBox.information(self, "Info", "")
            return
        reply = QMessageBox.question(self, "", Language.Lang.TechTreeWindow.Dialog.remove_tree_question,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.tabs.removeTab(index)
            self.update_add_root_button()

    def get_save_dict(self) -> dict:
        out = {}
        for i in range(self.tabs.count()):
            tree = self.tabs.widget(i).tech_tree
            out[tree.planet_name] = tree.to_dict()
        return out

    def load_from_dict(self, data: dict):
        self.tabs.clear()
        for planet, td in data.items():
            tree = TechTree.from_dict(td)
            self.tabs.addTab(TechTreeEditor(tree, planet), planet)
        for p in ["Serpulo", "Erekir"]:
            if p not in data:
                t = TechTree(p, allows_multiple_roots=True)
                self.tabs.addTab(TechTreeEditor(t, p), p)
        self.update_add_root_button()

    def save_to_file(self):
        if not self.project_path:
            self.project_path = QFileDialog.getExistingDirectory(self, "")
        if not self.project_path:
            return
        os.makedirs(self.project_path, exist_ok=True)
        path = os.path.join(self.project_path, "tech_trees.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.get_save_dict(), f, indent=2, ensure_ascii=False)

    def load_from_file(self):
        if not self.project_path:
            self.project_path = QFileDialog.getExistingDirectory(self, "")
        if not self.project_path:
            return
        path = os.path.join(self.project_path, "tech_trees.json")
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {}
            traceback.print_exc()
        self.load_from_dict(data)

    def save_all_to_java(self):
        if not self.project_path:
            self.project_path = QFileDialog.getExistingDirectory(self, "")
        if not self.project_path:
            return
        os.makedirs(self.project_path, exist_ok=True)
        path = os.path.join(self.project_path, f"src/{'/'.join(self._package.split('.'))}/ModTechTree.java")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"package {self._package};\n\n")
            f.write(
                "import arc.struct.Seq;\n"
                "import mindustry.content.Items;\n"
                "import mindustry.content.TechTree;\n"
                "import mindustry.content.Blocks;\n"
                "import mindustry.ctype.UnlockableContent;\n"
                "import mindustry.game.Objectives.*;\n"
                "import mindustry.type.ItemStack;\n"
                "import mindustry.type.Planet;\n"
            )
            f.write(
                f"import {self._package}.initScript;\n\n"
                "public class ModTechTree {\n"
                "    initScript _mcl;\n"
                "    public ModTechTree(initScript ModContentLoader) { _mcl = ModContentLoader; }\n\n"
                "    public void load() {\n"
            )
            for i in range(self.tabs.count()):
                tree = self.tabs.widget(i).tech_tree
                f.write(f"        // Tech tree '{tree.planet_name}'\n")
                if tree.planet_name in ["Serpulo", "Erekir"]:
                    for root in tree.roots:
                        var_node = f"{root.name}Node"
                        root_ref = f"Blocks.{root.name}" if root.name in EXISTING_ITEMS else f"_mcl.var_{root.name}"
                        f.write(f"        var {var_node} = TechTree.all.find(t -> t.content == {root_ref});\n")
                        f.write(f"        if ({var_node} != null) {{\n")
                        parent_var = var_node
                        for child in root.children:
                            child_ref = f"Blocks.{child.name}" if child.name in EXISTING_ITEMS else f"_mcl.var_{child.name}"
                            if child.requirements:
                                req_str = ", ".join(
                                    f"{req[1][0][0]}, {req[1][0][1]}"
                                    if req[0] == "resource" else f"{req[0]}({','.join(req[1:])})"
                                    for req in child.requirements
                                )
                                f.write(f"            new TechTree.TechNode({parent_var}, {child_ref}, ItemStack.with({req_str}));\n")
                            else:
                                f.write(f"            new TechTree.TechNode({parent_var}, {child_ref}, {child_ref}.researchRequirements());\n")
                        f.write("        }\n")
                else:
                    for root in tree.roots:
                        root_ref = f"Blocks.{root.name}" if root.name in EXISTING_ITEMS else f"_mcl.var_{root.name}"
                        f.write(f"        TechTree.nodeRoot(\"{tree.planet_name}\", {root_ref}, () -> {{\n")
                        f.write(f"            var {root.name}Node = TechTree.all.find(t -> t.content == {root_ref});\n")
                        f.write(f"            if ({root.name}Node != null) {{\n")
                        for child in root.children:
                            child_ref = f"Blocks.{child.name}" if child.name in EXISTING_ITEMS else f"_mcl.var_{child.name}"
                            if child.requirements:
                                req_str = ", ".join(
                                    f"{req[1][0][0]}, {req[1][0][1]}"
                                    if req[0] == "resource" else f"{req[0]}({','.join(req[1:])})"
                                    for req in child.requirements
                                )
                                f.write(f"                new TechTree.TechNode({root.name}Node, {child_ref}, ItemStack.with({req_str}));\n")
                            else:
                                f.write(f"                new TechTree.TechNode({root.name}Node, {child_ref}, {child_ref}.researchRequirements());\n")
                        f.write("            }\n")
                        f.write("        });\n")
            f.write("    }\n}\n")