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

ALL_TABS = {}

class uiMethods:
    @staticmethod
    def get_tab_widget(id: int):
        return ALL_TABS.get(id, None)
