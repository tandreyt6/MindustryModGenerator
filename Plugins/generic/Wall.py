import json

from .Block import Block
from MmgApi.Libs import PyQt6, Content, os, Main, uiMethods, UI
from PyQt6 import QtWidgets, QtGui, QtCore

ContentAbstract = Content

CacheLayer = UI.Content.CacheLayer
SoundSelect = UI.Content.SoundSelect
saveMode = UI.ContentFormat.saveMode


class Wall(Block, ContentAbstract):
    def __init__(self, id, name="Wall"):
        Block.__init__(self, name)
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

        self.package = "example"

    def get_all_methods(self):
        return {
            "info": [("java", saveMode.Force, [
                {"type": "string", "value": [{"type": "var", "value": "var1"}], "code": "   return var1;"}
            ]), {"string": "var1"}]
        }

    def select_sprite(self):
        filters = '''
            PNG Images (*.png);
            JPEG Images (*.jpg *.jpeg);
        '''
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(filter=filters)
        print(file_path, "select sprite")
        if file_path and self._pixmap:
            self._pixmap.load(file_path)
            self.lblSprite.setText(file_path)
            self._convas.view_scale = 0.3
            self._convas.update()


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
                if Main and Main.editor:
                    if os.path.exists(Main.editor.path + "/assets/sprites/block/" + self.name + ".png"):
                        self._pixmap.load(Main.editor.path + "/assets/sprites/block/" + self.name + ".png")

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

    def java_code(self):
        changed = self.get_changed_params()
        print(changed)
        params = []
        for key, value in changed.items():
            java_value = self._convert_to_java(value)
            if key == "requirements":
                params.append(f"        {java_value}")
                continue
            elif key == "package":
                continue
            params.append(f"        {key} = {java_value};")
        return f"package {self.package};\n" \
               f"\nimport mindustry.content.Items;\n" \
               f"import mindustry.type.Category;\n" \
               f"import mindustry.type.ItemStack;\n" \
               f"import mindustry.world.blocks.defense.Wall;\n" \
               f"\npublic class {self.name[1]} extends Wall {{\n" \
               f"    public {self.name[1]}() {{\n" \
               f'        super("{self.name[1]}");\n' \
               f"{self._get_params(params)}\n" \
               f"    }}\n" \
               f"}}"

    def create_java_code(self):
        print(self.package, self.get_java_class_name())
        return [
            f"import {self.package}.{self.get_java_class_name()};",
            f"new {self.get_java_class_name()}();"
        ]

    def _get_params(self, params):
        return "\n".join(params)

    def get_java_class_name(self):
        return self.name[1]
