class Format:
    Int = 'int'
    Float = 'float'
    String = 'str'
    NoFormat = 'object'
    Dict = 'dict'
    Bool = 'bool'

class saveMode:
    noSave = 0
    ifChanged = 1
    Force = 2

class PanelsPos:
    Left_Right = 0
    Right_Left = 1
    Right_right = 2
    Left_left = 3
    right_Right = 4
    left_Left = 5

ALL_TABS = {}

class uiMethods:
    @staticmethod
    def get_tab_widget(id: int):
        return ALL_TABS.get(id, None)
