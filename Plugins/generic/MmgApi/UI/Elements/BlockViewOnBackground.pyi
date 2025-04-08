from PyQt6.QtCore import QPointF, QRectF, Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QMouseEvent, QWheelEvent, QKeyEvent, QDragEnterEvent, \
    QDropEvent, QPaintEvent
from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from typing import List, Tuple, Optional


class Sprite:
    """Representation of a graphical element on the canvas"""

    def __init__(self, pixmap: QPixmap, x: float, y: float, movable: bool = True) -> None:
        """
        Create a new sprite
        Args:
            pixmap: Image data for visualization
            x: Initial X position
            y: Initial Y position
            movable: Whether the sprite can be moved interactively
        """

    pixmap: QPixmap
    pos: QPointF
    rotation: float
    scale: float
    movable: bool
    selected: bool
    dragging: bool
    canDelete: bool


class CanvasWidget(QWidget):
    """Interactive canvas widget with sprite management and grid visualization"""

    GRID_SIZE: int = 32
    """Base size for grid snapping and visualization"""

    def __init__(self) -> None:
        """Initialize canvas with default settings and empty sprite list"""

    # Scene state properties
    scene_rect: QRectF
    """Virtual scene dimensions in logical coordinates"""
    sprites: List[Sprite]
    """List of all sprites in the scene"""
    view_offset: QPointF
    """Current viewport offset in pixels"""
    view_scale: float
    """Zoom factor (1.0 = 100%)"""
    selected_sprite: Optional[Sprite]
    """Currently selected sprite reference"""
    snap_to_grid: bool
    """Current grid snapping state"""

    def add_sprite(self, pixmap: QPixmap, x: float, y: float, movable: bool = True) -> int:
        """
        Add new sprite to canvas
        Returns:
            Index of created sprite in sprites list
        """

    def paintEvent(self, event: QPaintEvent) -> None:
        """Handle widget repainting: render sprites and grid"""

    def visible_rect(self) -> QRectF:
        """Calculate visible area in scene coordinates
        Returns:
            QRectF representing visible portion of virtual scene
        """

    def wheelEvent(self, e: QWheelEvent) -> None:
        """Handle mouse wheel zoom operations"""

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """Handle mouse clicks: sprite selection and view dragging"""

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """Handle mouse movement: coordinate display, sprite dragging and view panning"""

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        """Finalize interaction states on mouse release"""

    def leaveEvent(self, e: QMouseEvent) -> None:
        """Hide coordinate display when cursor leaves widget"""

    def timeUpdate(self) -> None:
        """Periodic state update handler for interaction tracking"""

    def keyPressEvent(self, e: QKeyEvent) -> None:
        """Handle keyboard input: sprite deletion with Delete key"""

    def mapToScene(self, pos: QPointF) -> QPointF:
        """Convert widget coordinates to scene coordinates
        Returns:
            Transformed position in virtual scene space
        """

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Accept drag operations containing image files"""

    def dropEvent(self, event: QDropEvent) -> None:
        """Handle image file drops: create new sprites at cursor position
        Effects:
            - Creates new sprite from dropped image
            - Snaps position to grid if enabled
            - Selects new sprite automatically
        """