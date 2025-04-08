from typing import Any, Optional, Union, Type, ClassVar
from collections.abc import Callable, Coroutine

from PyQt6.QtWidgets import QListWidgetItem, QLineEdit, QWidget


class CustomListWidgetItem(QListWidgetItem):
    """
    Custom item for QListWidget.

    Stores additional name data for each list item,
    allowing to retrieve it separately from the visible text.
    """

    def __init__(self: Any, text: Any, name: Any, parent: Any) -> None:
        """
        Initialize custom list item.

        Args:
            text: Text displayed in the item.
            name: Hidden name value used for logic.
            parent: Parent widget.
        """

    def get_name(self: Any) -> None:
        """
        Return the hidden name value of the item.
        """


class FocusLineEdit(QLineEdit):
    """
    Extended QLineEdit with additional focus event handling.

    Used to trigger custom behavior when the field gains or loses focus.
    """

    def __init__(self: Any, parent: Any) -> None:
        """
        Initialize FocusLineEdit.

        Args:
            parent: Parent widget.
        """

    def focusOutEvent(self: Any, a0: Any) -> None:
        """
        Called when the field loses focus.

        Args:
            a0: Focus out event.
        """

    def focusInEvent(self: Any, a0: Any) -> None:
        """
        Called when the field gains focus.

        Args:
            a0: Focus in event.
        """


class SearchBox(QWidget):
    """
    SearchBox widget with interactive search and selectable item list.

    Allows user to search for items from a provided list, shows results dynamically,
    and lets the user select from those results.
    """

    def __init__(self: Any, items: Any, paintParent: Any) -> None:
        """
        Initialize SearchBox.

        Args:
            items: List of all available items for searching.
            paintParent: Parent widget used for rendering adjustments.
        """

    def update_list(self: Any) -> None:
        """
        Update displayed list based on current search input.
        """

    def show_list(self: Any) -> None:
        """
        Display the search result list.
        """

    def resizeEvent(self: Any, a0: Any) -> None:
        """
        Handle resize event for dynamically adjusting internal layout.

        Args:
            a0: Resize event.
        """

    def select_item(self: Any, item: Any) -> None:
        """
        Handle logic when an item from the search list is selected.

        Args:
            item: Selected item.
        """

    def outFocus(self: Any) -> None:
        """
        Hide the search list when focus is lost or selection is completed.
        """
