import json
from abc import ABC, abstractmethod

class Block(ABC):
    def __init__(self, name="Block"):
        self.name = name
        # Инициализация всех параметров по умолчанию
        self.hasItems = False
        self.hasLiquids = False
        self.hasPower = False
        self.outputsLiquid = False
        self.consumesPower = True
        self.outputsPower = False
        self.connectedPower = True
        self.conductivePower = False
        self.outputsPayload = False
        self.acceptsPayload = False
        self.acceptsItems = False
        self.separateItemCapacity = False
        self.itemCapacity = 10
        self.liquidCapacity = 10.0
        self.liquidPressure = 1.0
        self.outputFacing = True
        self.noSideBlend = False
        self.displayFlow = True
        self.inEditor = True
        self.lastConfig = None
        self.saveConfig = False
        self.copyConfig = True
        self.clearOnDoubleTap = False
        self.update = False
        self.destructible = False
        self.unloadable = True
        self.isDuct = False
        self.allowResupply = False
        self.solid = False
        self.solidifes = False
        self.teamPassable = False
        self.underBullets = False
        self.rotate = False
        self.rotateDraw = True
        self.lockRotation = True
        self.invertFlip = False
        self.variants = 0
        self.drawArrow = True
        self.drawTeamOverlay = True
        self.saveData = False
        self.breakable = False
        self.rebuildable = True
        self.privileged = False
        self.requiresWater = False
        self.placeableLiquid = False
        self.placeablePlayer = True
        self.placeableOn = True
        self.insulated = False
        self.squareSprite = True
        self.absorbLasers = False
        self.enableDrawStatus = True
        self.drawDisabled = True
        self.autoResetEnabled = True
        self.noUpdateDisabled = False
        self.updateInUnits = True
        self.alwaysUpdateInUnits = False
        self.useColor = True
        self.itemDrop = None
        self.playerUnmineable = False
        self.attributes = {}
        self.scaledHealth = -1.0
        self.health = -1
        self.armor = 0.0
        self.baseExplosiveness = 0.0
        self.destroyBullet = None
        self.destroyBulletSameTeam = False
        self.lightLiquid = None
        self.drawCracks = True
        self.createRubble = True
        self.floating = False
        self.size = 1
        self.offset = 0.0
        self.sizeOffset = 0
        self.clipSize = -1.0
        self.placeOverlapRange = 50.0
        self.crushDamageMultiplier = 1.0
        self.timers = 0
        self.cacheLayer = "CacheLayer.normal"
        self.fillsTile = True
        self.forceDark = False
        self.alwaysReplace = False
        self.replaceable = True
        self.group = "BlockGroup.none"
        self.flags = set()
        self.priority = "TargetPriority.base"
        self.unitCapModifier = 0
        self.configurable = False
        self.commandable = False
        self.allowConfigInventory = True
        self.selectionRows = 5
        self.selectionColumns = 4
        self.logicConfigurable = False
        self.consumesTap = False
        self.drawLiquidLight = True
        self.envRequired = 0
        self.envEnabled = "Env.terrestrial"
        self.envDisabled = 0
        self.sync = False
        self.conveyorPlacement = False
        self.allowDiagonal = True
        self.swapDiagonalPlacement = False
        self.schematicPriority = 0
        self.mapColor = "new Color(0, 0, 0, 1)"
        self.hasColor = False
        self.targetable = True
        self.attacks = False
        self.suppressable = False
        self.canOverdrive = True
        self.outlineColor = "Color.valueOf(\"404049\")"
        self.outlineIcon = False
        self.outlineRadius = 4
        self.outlinedIcon = -1
        self.hasShadow = True
        self.customShadow = False
        self.placePitchChange = True
        self.breakPitchChange = True
        self.placeSound = "Sounds.place"
        self.breakSound = "Sounds.breaks"
        self.destroySound = "Sounds.boom"
        self.albedo = 0.0
        self.lightColor = "Color.white.cpy()"
        self.emitLight = False
        self.lightRadius = 60.0
        self.fogRadius = -1
        self.loopSound = "Sounds.none"
        self.loopSoundVolume = 0.5
        self.ambientSound = "Sounds.none"
        self.ambientSoundVolume = 0.05
        self.requirements = []
        self.category = "Category.distribution"
        self.buildCost = 20.0
        self.buildVisibility = "BuildVisibility.hidden"
        self.buildCostMultiplier = 1.0
        self.deconstructThreshold = 0.0
        self.instantDeconstruct = False
        self.placeEffect = "Fx.placeBlock"
        self.breakEffect = "Fx.breakBlock"
        self.destroyEffect = "Fx.dynamicExplosion"
        self.researchCostMultiplier = 1.0
        self.researchCostMultipliers = {}
        self.researchCost = None
        self.instantTransfer = False
        self.quickRotate = True
        self.subclass = None
        self.selectScroll = 0.0
        self.buildType = None
        self.configurations = {}
        self.itemFilter = []
        self.liquidFilter = []
        self.consumers = []
        self.optionalConsumers = []
        self.nonOptionalConsumers = []
        self.updateConsumers = []
        self.hasConsumers = False
        self.consPower = None

    def loadFromDict(self, a0: dict):
        for i in a0:
            setattr(self, i, a0[i])

    def get_changed_params(self):
        default = Block("Block")
        changed = {}
        for attr in vars(self):
            if attr == 'name':
                continue
            current = getattr(self, attr)
            default_val = getattr(default, attr)
            if current != default_val:
                changed[attr] = current
        del default
        return changed

    def json_save(self):
        changed = self.get_changed_params()
        return json.dumps(changed, indent=2, default=str)

    def java_code(self):
        changed = self.get_changed_params()
        params = []
        for key, value in changed.items():
            java_value = self._convert_to_java(value)
            if key == "requirements":
                params.append(f"{java_value};")
                continue
            params.append(f"    {key} = {java_value};")
        return f'new {self.get_java_class_name()}("{self.name}") {self._get_params(params)};'

    def _get_params(self, params):
        return "{{\n"+"\n".join(params)+"\n}}"

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

    def get_java_class_name(self):
        return "Block"
