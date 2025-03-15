from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QListWidget, QVBoxLayout, QLabel, QListWidgetItem
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QFont


class CustomListWidgetItem(QListWidgetItem):
    def __init__(self, text, name, parent=None):
        super().__init__(parent)
        self.text = text
        self.name = name

    def get_name(self):
        return self.name


class FocusLineEdit(QLineEdit):
    outFocus = pyqtSignal()
    enterFocus = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusOutEvent(self, a0):
        self.outFocus.emit()
        super().focusOutEvent(a0)

    def focusInEvent(self, a0):
        self.enterFocus.emit()
        super().focusInEvent(a0)

class SearchBox(QWidget):
    def __init__(self, items, paintParent=None):
        super().__init__()
        self.items = items
        self.paintParent = paintParent

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.input_field = FocusLineEdit()
        self.input_field.textChanged.connect(self.update_list)
        self.input_field.outFocus.connect(self.outFocus)

        if self.paintParent is None:
            self.paintParent = QApplication.activeWindow()

        self.list_widget = QListWidget(self.paintParent)
        self.list_widget.setFixedHeight(100)
        self.list_widget.setVisible(False)
        self.list_widget.itemClicked.connect(self.select_item)

        self.layout.addWidget(self.input_field)
        self.setLayout(self.layout)
        self.oldText = self.input_field.text()
        self.updating = True

    def update_list(self):
        text = self.input_field.text().lower()
        if not self.updating: return
        if self.oldText == text: return
        else: self.oldText = text
        self.list_widget.clear()
        if text:
            filtered_items = [item for item in self.items if text in item.lower()]
            if filtered_items:
                for item in filtered_items:
                    label = QLabel(self)
                    display_text = self.items[item]['displayName']
                    name_text = f"({item})"

                    label.setText(
                        f"<span style='color:white;'>{display_text}</span> <span style='color:gray; float:right;'>{name_text}</span>")

                    font = QFont()
                    font.setBold(True)
                    label.setFont(font)

                    custom_item = CustomListWidgetItem(display_text, item, self.list_widget)
                    custom_item.setSizeHint(label.sizeHint())

                    self.list_widget.addItem(custom_item)
                    self.list_widget.setItemWidget(custom_item, label)

                self.show_list()
            else:
                self.list_widget.setVisible(False)
        else:
            self.list_widget.setVisible(False)

    def show_list(self):
        print(self.list_widget.isVisible())
        self.list_widget.setFixedWidth(self.input_field.width())
        pos = self.input_field.pos()
        pos.setY(pos.y()+self.height())
        self.list_widget.move(self.mapTo(self.paintParent, pos))
        self.list_widget.setVisible(True)
        self.list_widget.raise_()

    def resizeEvent(self, a0):
        self.list_widget.setFixedWidth(self.input_field.width())
        pos = self.input_field.pos()
        pos.setY(pos.y() + self.height())
        self.list_widget.move(self.mapTo(self.paintParent, pos))
        super().resizeEvent(a0)

    def select_item(self, item):
        self.updating = False
        name = item.get_name()
        self.input_field.setText(name)
        self.list_widget.setVisible(False)
        self.updating = True

    def outFocus(self):
        if not self.list_widget.hasFocus():
            self.list_widget.setVisible(False)
