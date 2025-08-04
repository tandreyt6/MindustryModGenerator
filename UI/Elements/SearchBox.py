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
        self.paintParent = paintParent or QApplication.activeWindow()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.input_field = FocusLineEdit(self)
        self.input_field.textChanged.connect(self.update_list)
        self.input_field.outFocus.connect(self.outFocus)
        self.input_field.enterFocus.connect(self.onFocusIn)  # Добавляем обработчик получения фокуса

        self.list_widget = QListWidget(self.paintParent or self)
        self.list_widget.setFixedHeight(100)
        self.list_widget.setVisible(False)
        self.list_widget.itemClicked.connect(self.select_item)
        self.list_widget.setStyleSheet("QListWidget { background: #2b2b2b; color: white; }")

        self.layout.addWidget(self.input_field)
        self.setLayout(self.layout)
        self.oldText = ""
        self.updating = True

    def update_list(self):
        if not self.updating:
            return

        text = self.input_field.text().lower()
        if self.oldText == text:
            return

        self.oldText = text
        self.list_widget.clear()

        if text and self.input_field.hasFocus():  # Показываем список только если есть фокус
            filtered_items = [item for item in self.items if text in item.lower()]
            if filtered_items:
                for item in filtered_items:
                    display_text = self.items[item]['displayName']
                    name_text = f"({item})"

                    label = QLabel()
                    label.setText(
                        f"<span style='color:white;'>{display_text}</span> "
                        f"<span style='color:gray;'>{name_text}</span>"
                    )
                    label.setStyleSheet("padding: 5px;")
                    font = QFont()
                    font.setPointSize(10)
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
        if not self.input_field.text() or not self.input_field.hasFocus():
            self.list_widget.setVisible(False)
            return

        pos = self.input_field.mapToGlobal(QPoint(0, self.input_field.height()))
        pos = self.paintParent.mapFromGlobal(pos)

        self.list_widget.setFixedWidth(self.input_field.width())
        self.list_widget.move(pos)
        self.list_widget.setVisible(True)
        self.list_widget.raise_()

    def resizeEvent(self, a0):
        if self.list_widget.isVisible() and self.input_field.hasFocus():
            pos = self.input_field.mapToGlobal(QPoint(0, self.input_field.height()))
            pos = self.paintParent.mapFromGlobal(pos)
            self.list_widget.setFixedWidth(self.input_field.width())
            self.list_widget.move(pos)
        super().resizeEvent(a0)

    def select_item(self, item):
        self.updating = False
        self.input_field.setText(item.get_name())
        self.list_widget.setVisible(False)
        self.updating = True

    def outFocus(self):
        # Немедленно скрываем список при потере фокуса
        self.list_widget.setVisible(False)

    def onFocusIn(self):
        # При получении фокуса обновляем список, если есть текст
        if self.input_field.text():
            self.update_list()