dark_style = """
QWidget, QMainWindow {
    background-color: #1e1e1e;
    color: #FFFFFF;
}
QSizeGrip {
    background: transparent;
}
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
    background-color: #333333;
    color: #FFFFFF;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 3px 5px;
    selection-background-color: #555555;
}
QPushButton, QToolButton {
    background-color: #333333;
    color: #FFFFFF;
    border: 1px solid #FFFFFF;
    border-radius: 4px;
    padding: 5px 10px;
}
QPushButton:hover, QToolButton:hover {
    background-color: #404040;
    border-color: #666666;
}
QPushButton:pressed, QToolButton:pressed {
    background-color: #2a2a2a;
}
#rightPanelStack {
    background-color: #2a2a2a;
}
QTabWidget::pane {
    border: 1px solid #555555;
    top: 1px;
}
QTabBar::tab {
    background: #333333;
    color: #FFFFFF;
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
#SplashTitle {
    background: none;
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
    color: #FFFFFF;
}
QScrollBar::handle {
    background: #777777;
    border-radius: 4px;
}
QMenu {
    background-color: #333333;
    color: #FFFFFF;
    border: 1px solid #555;
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
    background: #FFFFFF;
    margin: 4px;
}
QAction {
    background-color: transparent;
    color: #FFFFFF;
}
QTreeWidgetItem {
    color: #FFFFFF;
}
QTreeWidgetItem:hover {
    background-color: #404040;
}
QCheckBox::indicator:checked {
    background-color: #FFFFFF;
    border-radius: 5px;
}
QCheckBox::indicator {
    width: 15px;
    height: 15px;
    border-radius: 5px;
    border: 1px solid #404040;
}
"""

window_dark_style = """
QWidget#mainWindow {
    background-color: #2B2B2B;
    border-radius: 10px;
}
QFrame#CustomTitleBar {
    background-color: #1E1E1E;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
QLabel {
    color: #FFFFFF;
}
QWidget#contentArea {
    background-color: #353535;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}
QPushButton {
    background-color: #1E1E1E;
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #3C3C3C;
}
QPushButton#closeButton {
    background-color: #D32F2F;
}
QPushButton#closeButton:hover {
    background-color: #F44336;
}
QSizeGrip {
    background-color: transparent;
}
#ActionPanelButton {
    background-color: transparent;
    color: white;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 4px;
}
#ActionPanelButton:hover {
    border: 1px solid #777;
}
"""