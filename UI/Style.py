dark_style = """
    QWidget, QMainWindow {
        background-color: #1e1e1e;
        color: #ffd700;
    }
    QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
        background-color: #333333;
        color: #ffd700;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 3px 5px;
        selection-background-color: #555555;
    }
    QPushButton, QToolButton {
        background-color: #333333;
        color: #ffd700;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 5px 10px;
        min-width: 70px;
    }
    QPushButton:hover, QToolButton:hover {
        background-color: #404040;
        border-color: #666666;
    }
    QPushButton:pressed, QToolButton:pressed {
        background-color: #2a2a2a;
    }
    QTabWidget::pane {
        border: 1px solid #555555;
        top: 1px;
    }
    QTabBar::tab {
        background: #333333;
        color: #ffd700;
        padding: 6px 12px;
        border: 1px solid #555555;
        border-bottom: none;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    QTabBar::tab:selected {
        background: #404040;
        border-color: #666666;
    }
    QTreeWidget, QScrollArea {
        border: 1px solid #555555;
        border-radius: 4px;
        background-color: #333333;
    }
    QScrollBar:vertical, QScrollBar:horizontal {
        background: #333333;
        width: 12px;
    }
    QScrollBar::handle {
        background: #555555;
        border-radius: 4px;
    }
    QMenu {
        background-color: #333333;
        color: #ffd700;
        border: 1px solid #ffd700;
        border-radius: 4px;
    }
    QMenu::item {
        padding: 6px 25px 6px 20px;
        border-radius: 4px;
        margin: 2px;
    }
    QMenu::item:selected {
        background-color: #4d4d4d;
    }
    QMenu::separator {
        height: 1px;
        background: #ffd700;
        margin: 4px;
    }
    QAction {
        background-color: transparent;
        color: #ffd700;
    }
    QTreeWidgetItem {
        color: #ffd700;
    }
    QTreeWidgetItem:hover {
        background-color: #404040;
    }
"""

light_style = """
    QWidget, QMainWindow {
        background-color: #f0f0f0;
        color: #333333;
    }
    QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 3px 5px;
        selection-background-color: #d4d4d4;
    }
    QPushButton, QToolButton {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 5px 10px;
        min-width: 70px;
    }
    QPushButton:hover, QToolButton:hover {
        background-color: #e6e6e6;
        border-color: #b3b3b3;
    }
    QPushButton:pressed, QToolButton:pressed {
        background-color: #d9d9d9;
    }
    QTabWidget::pane {
        border: 1px solid #cccccc;
        top: 1px;
    }
    QTabBar::tab {
        background: #ffffff;
        color: #333333;
        padding: 6px 12px;
        border: 1px solid #cccccc;
        border-bottom: none;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    QTabBar::tab:selected {
        background: #e6e6e6;
        border-color: #b3b3b3;
    }
    QTreeWidget, QScrollArea {
        border: 1px solid #cccccc;
        border-radius: 4px;
        background-color: #ffffff;
    }
    QScrollBar:vertical, QScrollBar:horizontal {
        background: #ffffff;
        width: 12px;
    }
    QScrollBar::handle {
        background: #cccccc;
        border-radius: 4px;
    }
    QMenu, QMenuBar {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #cccccc;
    }
    QMenu::item:selected {
        background-color: #e6e6e6;
    }
    QMenu::separator {
        height: 1px;
        background: #cccccc;
    }
    QAction {
        background-color: transparent;
        color: #333333;
    }
    QTreeWidgetItem {
        color: #333333;
    }
    QTreeWidgetItem:hover {
        background-color: #e6e6e6;
    }
"""