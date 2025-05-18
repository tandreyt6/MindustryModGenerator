# color1 - текст #FFFFFF
# color2 - фон (глобальный) #1e1e1e
# color3 - элементы ввода #333333
# color4 - границы #555555
# color5 - ховер-элементы #404040
# color6 - панели #2a2a2a
# color7 - акцентные границы #666666
# color8 - скроллбар ховер #a0a0a0
# color9 - скроллбар #777777
# color10 - меню ховер #4d4d4d
# color11 - разделитель #FFFFFF
# color12 - красная кнопка #D32F2F
# color13 - красный ховер #F44336
# color14 - кнопки ховер #3C3C3C
# color15 - фон окна #2B2B2B
# color16 - контент #353535
# color17 - прозрачность элементов #00000000 (для QAction)
# color18 - кнопки панели приложения окно (для QPushButton)
# color19 - фон кнопки панели приложения окно (для QPushButton)

style_original = """
QWidget {{
    background-color: {color2};
    color: {color1};
}}
QMainWindow {{
    background-color: {color2};
    color: {color1};
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}}
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {{
    background-color: {color3};
    color: {color1};
    border: 1px solid {color4};
    border-radius: 4px;
    selection-background-color: {color4};
}}
QLabel {{
    background: none;
}}
QPushButton, QToolButton {{
    background-color: {color3};
    color: {color1};
    border: 1px solid {color1};
    border-radius: 4px;
}}
QPushButton:hover, QToolButton:hover {{
    background-color: {color5};
    border-color: {color7};
}}
QPushButton:pressed, QToolButton:pressed {{
    background-color: {color6};
}}
#rightPanelStack {{
    background-color: {color6};
}}
QTabWidget::pane {{
    border: 1px solid {color4};
    top: 1px;
}}
QTabBar::tab {{
    background: {color3};
    color: {color1};
    padding: 6px 12px;
    border: 1px solid {color4};
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}}
QTabBar::tab:selected {{
    background: {color5};
    border-color: {color7};
}}
QTreeWidget, QScrollArea {{
    border: 1px solid {color4};
    border-radius: 4px;
    background-color: {color3};
}}
QScrollBar:vertical {{
    border: 1px solid {color4};
    border-radius: 4px;
    background-color: {color3};
}}
QScrollBar::handle:vertical:hover {{
    background: {color8};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}
QScrollBar::handle {{
    background: {color9};
    border-radius: 4px;
}}
QMenu {{
    background-color: {color3};
    color: {color1};
    border: 1px solid {color4};
    border-radius: 4px;
}}
QMenu::item {{
    padding: 6px 25px 6px 20px;
    border-radius: 4px;
    margin: 2px;
}}
QMenu::item:selected {{
    background-color: {color10};
}}
QMenu::separator {{
    height: 1px;
    background-color: {color11};
    margin: 4px;
}}
QAction {{
    background-color: {color17};
    color: {color1};
}}
QTreeWidgetItem {{
    color: {color1};
}}
QTreeWidgetItem:hover {{
    background-color: {color5};
}}
QCheckBox::indicator:checked {{
    background-color: {color1};
    border-radius: 5px;
}}
QCheckBox::indicator {{
    width: 15px;
    height: 15px;
    border-radius: 5px;
    border: 1px solid {color5};
}}
"""

window_style_original = """
QWidget#mainWindow {{
    background-color: {color15};
    border: solid 2px #000000;
    border-radius: 10px;
}}
QFrame#CustomTitleBar {{
    background-color: {color2};
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}}
#WindowTitleButtons {{
    color: {color18};
    background-color: {color19};
}}
QLabel {{
    color: {color1};
}}
QWidget#contentArea {{
    background-color: {color2};
    color: {color1};
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}}
QPushButton {{
    background-color: {color2};
    color: {color1};
    border: none;
    border-radius: 4px;
}}
QPushButton:hover {{
    background-color: {color14};
}}
QPushButton#closeButton {{
    background-color: {color12};
}}
QPushButton#closeButton:hover {{
    background-color: {color13};
}}
#ActionPanelButton {{
    background-color: transparent;
    color: {color1};
    border: 1px solid {color4};
    border-radius: 4px;
}}
#ActionPanelButton:hover {{
    border: 1px solid {color7};
}}
"""


THEME_COLORS = {
    # Тёмные темы
    "dark_classic": {
        "color1": "#FFFFFF",
        "color2": "#1E1E1E",
        "color3": "#2D2D30",
        "color4": "#3E3E42",
        "color5": "#404040",
        "color6": "#252526",
        "color7": "#007ACC",
        "color8": "#A0A0A0",
        "color9": "#606060",
        "color10": "#2A2D2E",
        "color11": "#FFFFFF",
        "color12": "#D32F2F",
        "color13": "#FF5252",
        "color14": "#333333",
        "color15": "#252526",
        "color16": "#2D2D30",
        "color17": "transparent",
        "color18": "#FFFFFF",
        "color19": "#00000000",
    },
    "dark_amber": {
        "color1": "#FFF8E1",
        "color2": "#212121",
        "color3": "#33302E",
        "color4": "#4D4235",
        "color5": "#423D36",
        "color6": "#2B2A27",
        "color7": "#FFA000",
        "color8": "#FFC107",
        "color9": "#FFB300",
        "color10": "#3E3A32",
        "color11": "#FFECB3",
        "color12": "#D32F2F",
        "color13": "#FF6659",
        "color14": "#38342E",
        "color15": "#2B2A27",
        "color16": "#36332E",
        "color17": "transparent",
        "color18": "#FFFFFF",
        "color19": "#00000000",
    },
    "dark_emerald": {
        "color1": "#E8F5E9",
        "color2": "#1B262C",
        "color3": "#2A3E44",
        "color4": "#355A65",
        "color5": "#3B4A50",
        "color6": "#22333C",
        "color7": "#4DB6AC",
        "color8": "#80CBC4",
        "color9": "#66BB6A",
        "color10": "#2D4A50",
        "color11": "#A5D6A7",
        "color12": "#D32F2F",
        "color13": "#EF5350",
        "color14": "#30444A",
        "color15": "#222D33",
        "color16": "#2A373E",
        "color17": "transparent",
        "color18": "#FFFFFF",
        "color19": "#00000000",
    },
    # Темная медово-желтая тема
    "dark_honey": {
        "color1": "#FFF3D7",
        "color2": "#2B2B1E",
        "color3": "#3D3D2B",
        "color4": "#665C45",
        "color5": "#4F4A38",
        "color6": "#353523",
        "color7": "#8C7C5C",
        "color8": "#A3936D",
        "color9": "#8C7C5C",
        "color10": "#666045",
        "color11": "#FFD740",
        "color12": "#D32F2F",
        "color13": "#FF6B6B",
        "color14": "#4A4734",
        "color15": "#333325",
        "color16": "#3C3C2D",
        "color17": "transparent",
        "color18": "#FFFFFF",
        "color19": "#00000000",
    },

    # Светлые темы
    "light_classic": {
        "color1": "#212121",
        "color2": "#FAFAFA",
        "color3": "#FFFFFF",
        "color4": "#E0E0E0",
        "color5": "#F5F5F5",
        "color6": "#EEEEEE",
        "color7": "#1976D2",
        "color8": "#BDBDBD",
        "color9": "#9E9E9E",
        "color10": "#EDEDED",
        "color11": "#757575",
        "color12": "#D32F2F",
        "color13": "#FF5252",
        "color14": "#F0F0F0",
        "color15": "#FFFFFF",
        "color16": "#F5F5F5",
        "color17": "transparent",
        "color18": "#000000",
        "color19": "#00000000",
    },
    "light_sunshine": {
        "color1": "#3E2723",
        "color2": "#FFFDE7",
        "color3": "#FFF9C4",
        "color4": "#FFEE58",
        "color5": "#FFF59D",
        "color6": "#FFF8E1",
        "color7": "#FBC02D",
        "color8": "#FFD54F",
        "color9": "#FFCA28",
        "color10": "#FFF176",
        "color11": "#FFA000",
        "color12": "#D32F2F",
        "color13": "#FF8A80",
        "color14": "#FFECB3",
        "color15": "#FFFFFF",
        "color16": "#FFF9C4",
        "color17": "transparent",
        "color18": "#000000",
        "color19": "#00000000",
    },
    "light_lavender": {
        "color1": "#4A148C",
        "color2": "#F3E5F5",
        "color3": "#EDE7F6",
        "color4": "#D1C4E9",
        "color5": "#E8DAEF",
        "color6": "#F5EEF8",
        "color7": "#7E57C2",
        "color8": "#B39DDB",
        "color9": "#9575CD",
        "color10": "#D1C4E9",
        "color11": "#7E57C2",
        "color12": "#D32F2F",
        "color13": "#EF5350",
        "color14": "#E1BEE7",
        "color15": "#FFFFFF",
        "color16": "#F5F0FA",
        "color17": "transparent",
        "color18": "#000000",
        "color19": "#00000000",
    },
    "light_golden": {
        "color1": "#2F2A1F",
        "color2": "#FFF9E6",
        "color3": "#FFEEB3",
        "color4": "#FFD54F",
        "color5": "#FFE082",
        "color6": "#FFF3CC",
        "color7": "#FFB300",
        "color8": "#FFCA28",
        "color9": "#FFD740",
        "color10": "#FFE57F",
        "color11": "#FFA000",
        "color12": "#D32F2F",
        "color13": "#FF5252",
        "color14": "#FFECB3",
        "color15": "#FFFFFF",
        "color16": "#FFF5D9",
        "color17": "transparent",
        "color18": "#000000",
        "color19": "#00000000",
    }
}

def create_theme(colors, style_template, window_style_template):
    return (
        style_template.format(**colors),
        window_style_template.format(**colors)
    )

ALL_THEMES = {
    name: create_theme(colors, style_original, window_style_original)
    for name, colors in THEME_COLORS.items()
}