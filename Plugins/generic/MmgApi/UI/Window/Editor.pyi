from typing import Any, Dict, List, Optional, Union
from PyQt6.QtCore import QByteArray, pyqtSignal, QObject, Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMainWindow, QWidget, QDialog, QMessageBox, QMenu, QLabel, QSplitter, QScrollArea
from pathlib import Path
import os


class ElementsDict:
    """Custom dictionary for managing editor elements with triple-key access"""

    def __init__(self) -> None: ...

    def add(self, key1: str, key2: str, key3: int, value: Dict) -> None: ...

    def rename_key(self, old: str, new: str) -> None: ...

    def __getitem__(self, key: Union[str, int]) -> Dict: ...

    def __delitem__(self, key: Union[str, int]) -> None: ...

    def __contains__(self, key: Union[str, int]) -> bool: ...


class EditorWindow(QMainWindow):
    """Main editor window for managing mod projects with content editing capabilities"""

    splitterPosChanged = pyqtSignal(list)
    """Emits splitter position changes [left_panel_width, center_width, right_panel_width]"""

    saveRequested = pyqtSignal(dict)
    """Triggers when editor state needs saving (geometry/layout changes)"""

    closeSignal = pyqtSignal(object, bool)
    """Notifies about window closure (event: QCloseEvent, persist_state: bool)"""

    settingsWindowRequest = pyqtSignal()
    """Requests settings dialog display"""

    elementsData: ElementsDict
    """Registry of all loaded content elements"""

    path: str
    """Current project directory path"""

    data: Dict[str, Any]
    """Parsed mod.hjson project data"""

    package: str
    """Java package name derived from mod.hjson"""

    notExitOnLauncher: bool
    """Flag for direct closure vs returning to launcher"""

    def __init__(self, path: str) -> None:
        """Initialize editor window for specified project
        Args:
            path: Filesystem path to mod project directory
        """

    def handle_rename_validation(self, old_name: str, new_name: str, item: 'TreeWidgetItem') -> bool:
        """Validate element rename operations
        Returns:
            True if rename is permitted, False otherwise
        """

    def init_ui(self) -> None:
        """Initialize main UI components:
        - Menu bar
        - Splitter layout
        - Content tree
        - Tabbed editor
        - Right panel"""

    def setActionLabel(self, text: str) -> None:
        """Update status bar notification
        Args:
            text: Message to display with timestamp"""

    def ShowModFolder(self) -> None:
        """Open OS file explorer at project directory"""

    def exitOnLauncher(self) -> None:
        """Handle return to launcher action"""

    def handle_rename_item(self, old_text: str, new_text: str, item: 'TreeWidgetItem') -> None:
        """Process completed item rename
        Effects:
            - Updates filesystem
            - Modifies element registry
            - Persists changes"""

    def movedItem(self, item: 'TreeWidgetItem', oldParent: Optional['TreeWidgetItem']) -> None:
        """Handle item relocation in content tree
        Effects:
            - Updates filesystem structure
            - Adjusts element paths"""

    def handle_open(self, item: 'TreeWidgetItem') -> None:
        """Open content element or expand category
        Args:
            item: TreeWidgetItem to open"""

    def handle_rename(self, item: 'TreeWidgetItem') -> None:
        """Initiate item rename process"""

    def handle_delete(self, item: 'TreeWidgetItem', force: bool = False) -> None:
        """Delete content element or category
        Args:
            force: Bypass confirmation dialog"""

    def generateImportJavaCode(self) -> str:
        """Generate Java init script code
        Returns:
            Complete Java class code with imports and variables"""

    def saveInitScript(self) -> None:
        """Persist generated Java code to project files"""

    def createItem(self, item: Union['TreeWidgetItem', 'TreeWidget']) -> None:
        """Create new content element
        Effects:
            - Adds to content tree
            - Registers in elementsData
            - Creates filesystem entries"""

    def createDirectory(self, item: 'TreeWidgetItem') -> None:
        """Create new content category
        Args:
            item: Parent category item"""

    def createPath(self, item: 'TreeWidgetItem') -> None:
        """Create filesystem directory for category
        Args:
            item: Category tree item"""

    def loadDirsForContent(self, directory: str, fname: str = "") -> None:
        """Recursively load content directory structure
        Args:
            directory: Base path to scan
            fname: Current relative path fragment"""

    def loadElementsFromFile(self) -> None:
        """Load persisted elements from elements.json"""

    def add_item_from_name(self, name: str, path: List[str]) -> 'TreeWidgetItem':
        """Register element in content tree
        Returns:
            Created TreeWidgetItem instance"""

    def saveElementsData(self) -> None:
        """Persist elements registry to elements.json"""

    def show_item_content(self, item: 'TreeWidgetItem') -> None:
        """Display content editor for selected element
        Args:
            item: Content element to edit"""

    def saveFromSelf(self, widget: 'TabbedCustomEditor', data: Dict) -> bool:
        """Handle content saves from editor tabs
        Returns:
            True if save succeeded, False otherwise"""

    def create_tab(self, w1: QWidget, w2: QWidget, item: 'TreeWidgetItem') -> None:
        """Create new editor tab
        Args:
            w1: Preview widget
            w2: Editing controls
            item: Associated tree item"""

    def close_tab(self, index: int) -> None:
        """Close editor tab by index
        Args:
            index: Tab position in tab widget"""

    def apply_settings(self, settings: Dict[str, Any]) -> None:
        """Apply layout preferences
        Args:
            settings: Geometry and splitter sizes"""

    def closeEvent(self, event: Any) -> None:
        """Handle window closure
        Effects:
            - Persists UI state
            - Emits closure signals"""


class TreeWidgetItem(QWidget):
    """Custom tree item for content hierarchy representation"""
    data: Dict[str, Any]
    """Metadata storage for content items"""

    def get_path(self) -> List[str]: ...

    """Get hierarchical path as string list"""

    def get_item_path(self) -> List['TreeWidgetItem']: ...

    """Get hierarchical path as item list"""


class TabbedCustomEditor(QWidget):
    """Custom tab widget for content editing"""
    pack = pyqtSignal()
    """Triggers UI layout refresh"""

    saveFromSelf = pyqtSignal(object, dict)
    """Emits save requests with edited data"""

    def __init__(self, id: int, name: str, classe: type, changed_params: Dict) -> None: ...