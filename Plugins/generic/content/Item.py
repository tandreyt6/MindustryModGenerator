import json

from MmgApi.Libs import Content, os, uiMethods, UI
import MmgApi
from PyQt6 import QtWidgets, QtGui

from Widgets.ColorWidget import ColorWidget
from Widgets.RequirementsWidget import RequirementsWidget

BaseCustomWidget = MmgApi.Libs.UI.Elements.BaseCustomWidget.BaseCustomWidget

ContentAbstract = Content
print(vars(UI.Content))
CacheLayer = UI.Content.CacheLayer
SoundSelect = UI.Content.SoundSelect
IntSelect = UI.Content.IntSelect
FloatSelect = UI.Content.FloatSelect
saveMode = UI.ContentFormat.saveMode

class Item(ContentAbstract):
    def __init__(self, id, name="Item"):
        self.name = name
        ContentAbstract.__init__(self)
        self._item = None
        self._right_panel = None
        self._convas = None
        self._pixmap = QtGui.QPixmap()
        self._id = id

        # <var name> = tuple(contentType(CustomWidgetType), defaultValue, group, isVisible, eventFilter, saveMode, showTitle, filterIndex)
        # ... = tuple(None, None, "unknown", True, None, saveMode.ifChanged, True, None, None)

        self.color = (ColorWidget, "#ffffff", "Base")
        self.cost = (float, 1.0, "Base")

        self.package = None

    def get_all_methods(self):
        return {  }

    def select_sprite(self):
        filters = '''
            ALL Images (*.png *.jpg *.jpeg *.ico);;
            PNG Images (*.png);;
            JPEG Images (*.jpg *.jpeg);;
            ICO Images (*.ico)
        '''
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(filter=filters)
        print(file_path, "select sprite")
        if file_path and self._pixmap:
            self._pixmap.load(file_path)
            self.lblSprite.setText(file_path)
            self._convas.view_scale = 0.3
            self._convas.update()
            os.makedirs(MmgApi.Libs.Main.editor.path + "/assets/sprites/items/", exist_ok=True)
            self._pixmap.save(MmgApi.Libs.Main.editor.path + "/assets/sprites/items/" + self.name + ".png")

    def saveEvent(self):
        pass

    def getSpriteTab(self) -> QtWidgets.QWidget:
        if self._convas is None:
            i = uiMethods.get_tab_widget(self._id)
            if i is not None:
                self._convas, self._right_panel, self._item = i
                s = self._convas.scene_rect.width() // 32
                self._convas.add_sprite(self._pixmap, s // 2 * 32, s // 2 * 32, False)
                if MmgApi.Libs.Main and MmgApi.Libs.Main.editor:
                    if os.path.exists(MmgApi.Libs.Main.editor.path + "/assets/sprites/items/" + self.name + ".png"):
                        self._pixmap.load(MmgApi.Libs.Main.editor.path + "/assets/sprites/items/" + self.name + ".png")

        spriteTab = QtWidgets.QWidget()
        lSprite = QtWidgets.QVBoxLayout(spriteTab)
        self.lblSprite = QtWidgets.QLabel("Select file for sprite! (*.png, *.jpg)")
        self.selectSprite = QtWidgets.QPushButton("select")
        self.selectSprite.clicked.connect(self.select_sprite)
        lSprite.addWidget(self.lblSprite)
        lSprite.addWidget(self.selectSprite)
        lSprite.addStretch()
        return spriteTab

    def get_custom_tabs(self):
        spriteTab = self.getSpriteTab()

        return [("sprite", spriteTab)]

    def get_java_class_name(self):
        return self.name
