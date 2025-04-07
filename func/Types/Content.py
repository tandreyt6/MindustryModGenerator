from typing import List


class Content:
    package: str
    def get_java_class_name(self) -> str:
        pass

    def java_code(self) -> str:
        pass

    def get_changed_params(self) -> dict:
        pass

    def create_java_code(self) -> List[str]:
        pass

    def json_save(self) -> dict:
        pass

    def loadFromDict(self, data: dict):
        pass

    def get_custom_tabs(self):
        return []

    def saveEvent(self):
        pass