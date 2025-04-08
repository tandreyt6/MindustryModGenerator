from typing import List, Tuple

from PyQt6.QtWidgets import QWidget


class Content:
    package: str
    def get_java_class_name(self) -> str:
        pass

    def java_code(self) -> str:
        return "element"

    def get_changed_params(self) -> dict:
        return {}

    def create_java_code(self) -> List[str]:
        return []

    def json_save(self) -> dict:
        return {}

    def loadFromDict(self, data: dict):
        pass

    def get_custom_tabs(self) -> List[Tuple[str, QWidget]]:
        return []

    def saveEvent(self):
        pass