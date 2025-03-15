from func.Types.Block import Block


class Wall(Block):
    def __init__(self, name="Wall"):
        super().__init__(name)
        self.lightningChance = float(-1)
        self.lightningDamage = float(20)
        self.lightningLength = 17
        self.lightningColor = "Pal.surge"
        self.lightningSound = "Sounds.spark"

        self.chanceDeflect = float(-1)
        self.flashHit = None
        self.flashColor = "Color.white"
        self.deflectSound = "Sounds.none"
        self.solid = True
        self.destructible = True
        self.group = "BlockGroup.walls"
        self.buildCostMultiplier = float(6)
        self.canOverdrive = False
        self.drawDisabled = False
        self.crushDamageMultiplier = float(5)
        self.priority = "TargetPriority.wall"
        self.envEnabled = "Env.any"

        self.package = "example"
    def get_changed_params(self):
        default = Wall("Wall")
        changed = {}
        for attr in vars(self):
            if attr == 'name':
                continue
            elif attr == 'package':
                changed[attr] = getattr(self, attr)
                continue
            current = getattr(self, attr)
            default_val = getattr(default, attr)
            if current != default_val:
                changed[attr] = current
        return changed

    def java_code(self):
        changed = self.get_changed_params()
        params = []
        for key, value in changed.items():
            java_value = self._convert_to_java(value)
            if key == "requirements":
                params.append(f"        {java_value}")
                continue
            elif key == "package":
                continue
            params.append(f"        {key} = {java_value};")
        return f"package {self.package}\n" \
               f"\nimport mindustry.content.Items;\n" \
               f"import mindustry.type.Category;\n" \
               f"import mindustry.type.ItemStack;\n" \
               f"import mindustry.world.blocks.defense.Wall;\n" \
               f"\npublic class {self.name} extends Wall {{\n" \
               f"    public {self.name}() {{\n" \
               f'        super("{self.name}");\n' \
               f"{self._get_params(params)}\n" \
               f"    }}\n" \
               f"}}"

    def create_java_code(self):
        return [
            f"import {self.package}.{self.name};",
            f"new {self.name}();"
        ]

    def _get_params(self, params):
        return "\n".join(params)

    def get_java_class_name(self):
        return "Wall"
