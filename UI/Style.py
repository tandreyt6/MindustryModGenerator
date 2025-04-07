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
    #rightPanelStack {
        background-color: #2a2a2a;
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
    QScrollBar:vertical {
        border: 1px solid #555555;
        border-radius: 4px;
        background-color: #333333;
    }
    QScrollBar::handle:vertical:hover {
        background: #a0a0a0;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;  
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;  
    }
    #ActionPanel {
        border: 1px solid #555555;
        border-radius: 4px;
        background-color: #333333;
    }
    #ActionPanelContent {
        background-color: #333333;
        color: #ffd700;
    }
    QScrollBar::handle {
        background: #777777;
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
    QCheckBox::indicator:checked {
        background-color: #ffd700;
        border-radius: 5px;
    }
    QCheckBox::indicator {
        width: 15px;
        height: 15px;
        border-radius: 5px;
        border: 1px solid #404040
    }
"""

light_style = """
    
"""