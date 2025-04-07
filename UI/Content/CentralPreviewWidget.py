from UI.Content.CentralAbstractWidget import CentAbsWidget
from UI.Elements.BlockViewOnBackground import CanvasWidget


class PreviewWidget(CentAbsWidget, CanvasWidget):
    def __init__(self):
        super(CentAbsWidget).__init__()
        super(CanvasWidget).__init__()
        super().__init__()
        self.scene_rect.setWidth(3000)
        self.scene_rect.setHeight(3000)
