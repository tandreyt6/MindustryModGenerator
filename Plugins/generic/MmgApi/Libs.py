import os
from typing import List, Optional, Any

import PyQt6
from PyQt6.QtCore import QTimer

import UI

class Language:
    class EN:
        type = "en"

    class RU:
        type = "ru"

    Langs = {"ru": ("Русский", RU), "en": ("English", EN)}
    Lang: EN = None

class Events:
    @staticmethod
    def on(name: str, executableFunc: object):
        pass
    @staticmethod
    def fire(name: str, argv: list|dict):
        pass

class Main:
    """Main application controller class handling core functionality including:
    - Plugin management
    - Project handling
    - UI window management
    - Settings persistence

    Keep in mind that the Main class has already been created,
    and you will be given an instance of the class, not its structure."""

    projects: list
    """List of recent projects with their metadata"""

    pluginData: dict[str, dict[str, Any]]
    """Storage for plugin metadata and status information"""

    loadedPlugins: dict[str, Any]
    """Active plugins loaded into the application"""

    editor: Optional['EditorWindow']
    """Current editor window instance (None when not editing a project)"""

    settingsWindow: 'SettingsWindow'
    """Application settings dialog instance"""

    launcher_window: 'LauncherWindow'
    """Main launcher window for project selection"""

    timer: QTimer
    """Timer for periodic application updates"""

    def get_folders(self, directory: str) -> list[str]:
        """Retrieve valid plugin directories from specified location
        Args:
            directory: Path to scan for plugin folders
        Returns:
            List of folder names containing valid plugins"""

    def loadPlugins(self) -> None:
        """Load and initialize plugins with dependency resolution:
        1. Scan ./Plugins directory for valid plugins
        2. Check dependencies and conflicts
        3. Topologically sort based on dependencies
        4. Load plugins in safe environment
        5. Register loaded plugins in application"""

    def initContent(self) -> None:
        """Initialize content types from loaded plugins:
        - Populate content registry (LIST_TYPES)
        - Called after plugin loading completes"""

    def initTemplates(self) -> None:
        """Initialize project templates from loaded plugins:
        - Populate template registry (LIST_MOD_TEMPLATES)
        - Called after plugin loading completes"""

    def load_recent(self) -> None:
        """Load recent projects into launcher UI:
        - Read from persisted settings
        - Add entries to launcher_window
        - Handle missing/corrupted project entries"""

    def update(self) -> None:
        """Periodic application update handler:
        - Called every 100ms by QTimer
        - Handles background maintenance tasks"""

    def select_project(self, data: dict[str, Any]) -> None:
        """Handle project selection from launcher UI
        Args:
            data: Project metadata dictionary containing:
                - name: Project display name
                - path: Filesystem path
                - icon: Optional project icon path"""

    def openSettings(self) -> None:
        """Show application settings dialog:
        - Loads current settings values
        - Handles settings persistence on close"""

    def closeEditor(self, event: Any, b: bool) -> None:
        """Handle editor window closure
        Args:
            event: Close event object
            b: Flag indicating whether to persist project state
        Effects:
            - Clears current editor reference
            - Shows launcher window"""

    def create_project(self) -> None:
        """Handle new project creation flow:
        - Shows project creation dialog
        - Initializes selected template
        - Adds new project to recent list"""

    def showExplorerFolder(self, data: dict[str, Any]) -> None:
        """Open OS file explorer for project directory
        Args:
            data: Project metadata containing 'path' key"""

    def editorGeometrySave(self, data: dict[str, Any]) -> None:
        """Persist editor window geometry settings
        Args:
            data: Dictionary containing window position/size"""

    def close(self, b: bool = True) -> None:
        """Shutdown application cleanly
        Args:
            b: If True, force exit application
        Effects:
            - Saves final settings
            - Stops all background processes
            - Closes UI windows"""
class memory:
    @staticmethod
    def put(key: str, valuer: object):
        """A method for setting the parameter value in the settings"""
    @staticmethod
    def get(key: str, default: object = None):
        """A method for getting values in the application settings."""
class Content:
    """An abstract class that must be used to create a content constructor.

    "package" parameter is set by the constructor, it must be used if you want to access the folder, for example:
     the path to the script "~/src/example/content/element.java " in this case, the "example.content" will be stored in the package.
     Keep in mind that the self.package parameter can change at any time!"""

    package: str

    def get_java_class_name(self) -> str:
        """The method should return the name of the content class that will be used to generate the object code."""

    def java_code(self) -> str:
        """The method should return the code that will be generated and inserted into the *.java file!
         The first line should be package where the path is <self.package>."""

    def get_changed_params(self) -> dict:
        """The method should return a dictionary of changed parameters,
         for example: "{"solid": True, "health": 10}", This method is needed only for the element, the editor uses its own verification logic!"""

    def create_java_code(self) -> List[str]:
        """This method returns the code that will be used in the content loading script,
        for example: If your element is named "Block1" and package is "example.content", then the method should
        return ["import example.content.Block1;", "new Block1();"], where the first is that how to import the script,
         the second is how to create it!"""

    def json_save(self) -> dict:
        """The method should return a dictionary of parameters that should be written to the save file.
         The dictionary should contain only data related to variables saved by the editor."""


    def get_custom_tabs(self):
        """The method should return a list of tuple, the tuple should contain ("name tab", QWidget()),
         where QWidget is any object that inherits from the PyQt6.QtWidgets.QWidget class."""

    def saveEvent(self):
        """This method is called every time the editor saves an element and all information about it."""
class settings:
    """This class defines the rules for working with the configuration file."""
    @staticmethod
    def load(self):
        """This method is used to download the application settings.
        Do not use it if you do not know what you are doing!"""
    @staticmethod
    def save_data(key: str, value: object):
        """The method saves the parameter to the settings file.
        Be careful, do not overwrite the parameters required by the editor, something may break!"""
    @staticmethod
    def get_data(key:str, default:object=None):
        """The method returns the value from the settings file."""
class uiMethods:
    """The class defines how to work with interface constructor variables."""
    @staticmethod
    def get_tab_widget(id: int):
        """The method will return the widget value by id, the method will return data such as:
         The Central widget (QWidget), the Right panel Widget (QWidget) and the hierarchy panel element (TreeWidgetItem)."""
