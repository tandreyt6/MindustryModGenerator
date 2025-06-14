import json

from MmgApi.Libs import Content, os, uiMethods, UI
import MmgApi
from PyQt6 import QtWidgets, QtGui

ContentAbstract = Content
print(vars(UI.Content))
CacheLayer = UI.Content.CacheLayer
SoundSelect = UI.Content.SoundSelect
saveMode = UI.ContentFormat.saveMode

class Wall(ContentAbstract):
    def __init__(self, id, name="Wall"):
        self.name = name
        ContentAbstract.__init__(self)
        self._item = None
        self._right_panel = None
        self._convas = None
        self._pixmap = QtGui.QPixmap()
        self._id = id
        # <var name> = tuple(contentType(CustomWidgetType), defaultValue, group, isVisible, eventFilter, saveMode, showTitle, filterIndex)
        # ... = tuple(None, None, "unknown", True, None, saveMode.ifChanged, True, None)
        self.lightningChance = (float, -1.0, "lighting")
        self.lightningDamage = (float, 20.0, "lighting")
        self.lightningLength = (int, 17, "lighting")
        # self.lightningColor = "Pal.surge"
        # self.lightningSound = "Sounds.spark"

        self.chanceDeflect = (float, -1.0, "deflect")
        # self.flashHit = None
        # self.flashColor = "Color.white"
        # self.deflectSound = "Sounds.none"
        self.crushDamageMultiplier = (float, 5, "deflect")

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
            os.makedirs(MmgApi.Libs.Main.editor.path + "/assets/sprites/block/", exist_ok=True)
            self._pixmap.save(MmgApi.Libs.Main.editor.path + "/assets/sprites/block/" + self.name + ".png")

    def saveEvent(self):
        pass

    def json_save(self):
        changed = self.get_changed_params()
        return json.dumps(changed, indent=2, default=str)

    def get_custom_tabs(self):
        if self._convas is None:
            i = uiMethods.get_tab_widget(self._id)
            if i is not None:
                self._convas, self._right_panel, self._item = i
                s = self._convas.scene_rect.width() // 32
                self._convas.add_sprite(self._pixmap, s // 2 * 32, s // 2 * 32, False)
                if MmgApi.Libs.Main and MmgApi.Libs.Main.editor:
                    if os.path.exists(MmgApi.Libs.Main.editor.path + "/assets/sprites/block/" + self.name + ".png"):
                        self._pixmap.load(MmgApi.Libs.Main.editor.path + "/assets/sprites/block/" + self.name + ".png")

        spriteTab = QtWidgets.QWidget()
        lSprite = QtWidgets.QVBoxLayout(spriteTab)
        self.lblSprite = QtWidgets.QLabel("Select file for sprite! (*.png, *.jpg)")
        self.selectSprite = QtWidgets.QPushButton("select")
        self.selectSprite.clicked.connect(self.select_sprite)
        lSprite.addWidget(self.lblSprite)
        lSprite.addWidget(self.selectSprite)
        lSprite.addStretch()

        return [("sprite", spriteTab)]

    def get_changed_params(self):
        changed = {}
        for attr in vars(self):
            value = getattr(self, attr)

            if attr in ('name',) or attr.startswith('_'):
                continue

            if not isinstance(value, tuple):
                continue
            if len(value) > 5 and value[5] is False:
                continue

            if attr == 'package':
                changed[attr] = value
                continue

            widget_data = self._right_panel.param_widgets.get(attr)
            if not widget_data:
                print(f"{attr} is not editable!")
                continue

            current = widget_data['widgets'][0].value()
            default_val = value[1]
            is_force = len(value) > 5 and value[5] == saveMode.Force

            if value[0] == float:
                default_val = f"{default_val}f"

            if current != default_val or is_force:
                changed[attr] = current

        return changed

    def _convert_to_java(self, value):
        if isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return value
        elif isinstance(value, list):
            return "requirements("+self.category+", ItemStack.with(["+", ".join(", ".join([_[0], str(_[1])]) for _ in value)+"]));"
        elif isinstance(value, dict):
            return json.dumps(value, indent=2)
        elif value is None:
            return "null"
        else:
            return str(value)

    def _get_params(self, params):
        return "\n".join(params)

    def get_java_class_name(self):
        return self.name
