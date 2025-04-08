from typing import List
from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton
from UI.Elements.SearchBox import SearchBox


class CreateElementDialog(QDialog):
    """Dialog window for creating new elements with validated input fields"""

    # Validation character sets
    valid_symbol: List[str]
    valid_path: List[str]

    # UI components
    type_edit: SearchBox
    name_edit: QLineEdit
    category_edit: QLineEdit
    save_button: QPushButton

    def __init__(self, path: List[str] = []) -> None:
        """
        Initialize element creation dialog
        Args:
            path: Default directory path for new element
        """

    def validSymbols(self, text: str) -> None:
        """Sanitize name input against allowed symbols
        Args:
            text: Raw input from name field
        """

    def validPath(self, text: str) -> None:
        """Sanitize path input against allowed characters
        Args:
            text: Raw input from path field
        """