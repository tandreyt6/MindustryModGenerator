from MmgApi.Libs import UI

CanvasWidget = UI.Elements.BlockViewOnBackground.CanvasWidget

class CanvasDisableGrid(CanvasWidget):
    def __init__(self):
        super().__init__()
        self.grid = False