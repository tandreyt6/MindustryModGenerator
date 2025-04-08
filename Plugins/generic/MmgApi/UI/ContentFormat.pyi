from typing import Any, Optional, Union, Type, ClassVar
from collections.abc import Callable, Coroutine

class Format:
    """The type of data that the widget will save.
    Int - The parameter will be saved as a natural number. Not matching the format will give you an error!
    Float - The parameter will be saved as a fractional number. Not matching the format will give you an error!
    String - Everything that the widget returns will be enclosed in quotation marks "".
    NoFormat - The value will not be formatted or checked in any way!
    Dict - The value will be saved as a dictionary.
    Bool - The value will be saved as true or false, formatted as bool(value)!"""
    Int = 'int'
    Float = 'float'
    String = 'str'
    NoFormat = 'object'
    Dict = 'dict'
    Bool = 'bool'
class saveMode:
    """noSave - This parameter will not be saved and is only temporary.
       isChanged - The parameter will be saved if it does not match the default value!
         Keep in mind that the editor uses its own logic for checking parameter changes, so this parameter should be specified without taking into account the get_changed_params method!
       Force - The parameter will be saved forcibly!"""
    noSave = 0|False
    ifChanged = 1|True
    Force = 2
class uiMethods:
    @staticmethod
    def get_tab_widget(id: int) -> None: ...