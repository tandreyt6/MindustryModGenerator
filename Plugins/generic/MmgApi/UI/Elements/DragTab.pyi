from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QTabWidget


class DraggableTabWidget(QTabWidget):
    """
    Extended QTabWidget with support for dragging and reordering tabs using the mouse.

    This widget allows the user to rearrange tabs interactively by clicking and dragging them
    within the tab bar.
    """

    _drag_start_pos: QPoint  # Position where the left mouse button was initially pressed
    _dragging: bool          # Flag indicating if a tab dragging operation is in progress

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the draggable tab widget.

        Args:
            *args: Standard positional arguments for QTabWidget.
            **kwargs: Standard keyword arguments for QTabWidget.
        """

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse press events.

        If the left mouse button is pressed, start tracking for a potential tab drag operation.

        Args:
            event: Mouse press event containing button and position information.
        """

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse move events.

        If dragging is active and the mouse has moved enough distance,
        attempt to move the tab from the original position to the new one.

        Args:
            event: Mouse move event containing current position of the mouse.
        """

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse release events.

        If the left mouse button is released, finish the dragging operation.

        Args:
            event: Mouse release event.
        """
