from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget
from typing import Any, Optional

from UI.ContentFormat import Format


class CustomWidgetSignal(QObject):
    """Signal container for custom widget value changes"""

    value_changed = pyqtSignal(object)
    """Emits when widget's value changes. Carries new value as payload."""


class BaseCustomWidget(QWidget):
    """Abstract base class for custom UI widgets with value tracking"""

    TYPE: Any = Format.NoFormat
    """Widget type specifier from Format enum"""

    def __init__(self, initial_value: Any, parent: Optional[QWidget] = None) -> None:
        """
        Initialize base custom widget
        Args:
            initial_value: Starting value for the widget
            parent: Parent Qt widget
        """

    def set_value(self, value: Any) -> None:
        """Abstract method to update widget's value. Must be implemented in subclasses."""
        raise NotImplementedError("Subclasses must implement set_value")

    def value(self) -> Any:
        """Get current widget value
        Returns:
            Currently stored value in widget-specific format"""
        return self._value


class CustomNoneClass(BaseCustomWidget):
    """Placeholder widget implementation with no visual representation"""

    def __init__(self, initial_value: Any, parent: Optional[QWidget] = None) -> None:
        """
        Initialize null widget
        Args:
            initial_value: Dummy value for API compatibility
            parent: Parent Qt widget
        """

    def set_value(self, value: Any) -> None:
        """No-operation implementation for value setting
        Args:
            value: Ignored input value"""