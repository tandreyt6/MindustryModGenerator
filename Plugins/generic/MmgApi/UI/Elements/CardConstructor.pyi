from typing import Any, Dict, List, Optional, Tuple, Type, Union
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QTabWidget, QLineEdit, QScrollArea
from collections import defaultdict

from UI.Elements import BaseCustomWidget


class SyncSignals(QObject):
    """Central signal hub for cross-widget parameter synchronization"""
    global_value_changed = pyqtSignal(str, object)
    """Emits when any parameter changes (param_name: str, new_value: object)"""


class TabbedCustomEditor(QWidget):
    """Customizable parameter editor with tabbed interface and dynamic UI generation"""

    # Signals
    saved = pyqtSignal(dict)
    """Emits on save with dictionary of {param_name: value}"""
    saveFromSelf = pyqtSignal(QObject, dict)
    """Emits instance and changes when saving occurs"""

    def __init__(
            self,
            classe: Type[Any],
            changed_params: Optional[Dict[str, Any]] = None,
            id: int = 0,
            name: str = "Block",
            parent: Optional[QWidget] = None
    ) -> None:
        """
        Initialize parameter editor
        Args:
            classe: Content class providing parameter configuration
            changed_params: Initial modified parameters
            id: Unique identifier for this editor instance
            name: Display name for the edited object
        """

    # Instance variables
    param_configs: defaultdict[str, Tuple[Any, ...]]
    """Parameter configurations (type, default, group, visible, etc)"""

    param_widgets: Dict[str, Dict[str, List[QWidget]]]
    """Registry of created parameter widgets"""

    custom_widgets: Dict[str, Tuple[Type[BaseCustomWidget], bool]]
    """Custom widget classes with show_title flags"""

    hidden_params: set[str]
    """Parameters excluded from UI"""

    def pack(self) -> None:
        """Finalize UI setup - must be called after initial configuration"""

    def register_custom_widget(
            self,
            param_name: str,
            widget_class: Type[BaseCustomWidget]
    ) -> None:
        """Register custom widget for parameter
        Args:
            param_name: Target parameter name
            widget_class: Custom widget class inheriting from BaseCustomWidget
        """

    def create_main_tabs(self) -> None:
        """Build tabbed interface with:
        - Variables tab with collapsible categories
        - Methods tab (placeholder)
        - Custom tabs from content class"""

    def create_param_widget(self, param: str) -> Optional[QWidget]:
        """Generate appropriate input widget for parameter
        Returns:
            Configured widget or None for hidden params"""

    def on_param_changed(self, param: str, value: Any) -> None:
        """Handle parameter value changes
        Effects:
            - Updates changed_params
            - Emits synchronization signals"""

    def update_all_widgets(self, param: str, value: Any) -> None:
        """Synchronize all widgets for a parameter
        Args:
            param: Parameter name to update
            value: New value to set"""

    def register_widget(
            self,
            param: str,
            widget: QWidget,
            meta: Dict[str, Any]
    ) -> None:
        """Track widget instances for a parameter
        Args:
            meta: Configuration dict with 'default' and 'save_mode'"""

    def update_search_tab(self, text: str) -> None:
        """Filter parameters based on search query
        Args:
            text: Search string to match parameter names"""

    def calculate_parameter_mapping(
            self,
            objs: Optional[List[Any]] = None
    ) -> Dict[int, List[str]]:
        """Analyze class structure for parameter ownership
        Returns:
            Mapping of object indices to their parameters"""

    def apply_initial_params(self) -> None:
        """Apply stored parameters to widgets during initialization"""

    def save(self) -> None:
        """Trigger save workflow:
        1. Collect changes based on save modes
        2. Emit saved/saveFromSelf signals
        3. Persist modifications"""

    def previewChange(self) -> None:
        """Display preview dialog with pending changes
        Effects:
            Shows modal dialog with change summary"""

    # Utility methods
    def get_widget_value(self, widget: QWidget) -> Any:
        """Universal widget value extractor
        Returns:
            Current value based on widget type"""

    def set_standard_widget_value(
            self,
            widget: QWidget,
            value: Any
    ) -> None:
        """Universal widget value setter
        Args:
            widget: Target input widget
            value: Value to apply"""


class CollapsibleCategory(QWidget):
    """Expandable/collapsible parameter group widget"""

    def __init__(self, title: str, parent: Optional[QWidget] = None) -> None: ...

    def toggle_collapse(self) -> None: ...

    def add_widget(self, widget: QWidget, has_label: bool, param_name: str) -> None: ...


class clickedWidget(QWidget):
    """Clickable container widget with press detection"""
    clicked = pyqtSignal()