from UI.Elements.CardConstructor import TabbedCustomEditor
from PyQt6.QtWidgets import QApplication

from func.Content.Wall import Wall
from func.Types.Block import Block

app = QApplication([])

editor = TabbedCustomEditor(
    classes=[Wall, Block],
    changed_params={

    }
)
editor.pack()

editor.saved.connect(lambda x: print("Изменения:", x))
editor.show()

app.exec()