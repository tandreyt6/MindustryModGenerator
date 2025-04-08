import json
from generic import UI

CacheLayer = UI.Content.CacheLayer
SoundSelect = UI.Content.SoundSelect
saveMode = UI.ContentFormat.saveMode

class Block():
    def __init__(self, name="Block"):
        # <var name> = tuple(contentType(CustomWidgetType), defaultValue, group, isVisible, eventFilter, saveMode, showTitle, filterIndex)
        # ... = tuple(None, None, "unknown", True, None, saveMode.ifChanged, True, None)
        self.name = (str, name, "settings", False, None, False)
        self.flags = (None, set(), "settings", False, None, False)
        # self.attributes = (Attributes, {}, "settings", False, None, False)
        self.hasItems = (bool, False, "items", True, None, True)
        self.acceptsItems = (bool, False, "items", True, None, True)
        self.separateItemCapacity = (bool, False, "items", True, None, True)
        self.itemCapacity = (int, 10, "items", True, None, True)
        self.hasLiquids = (bool, False, "liquids", True, None, True)
        self.outputsLiquid = (bool, False, "liquids", True, None, True)
        self.liquidCapacity = (float, 10.0, "liquids", True, None, True)
        self.liquidPressure = (float, 1.0, "liquids", True, None, True)
        # self.lightLiquid = (LiquidSelect, None, "liquid", True, None, True)
        self.hasPower = (bool, False, "power", True, None, True)
        self.consumesPower = (bool, True, "power", True, None, True)
        self.outputsPower = (bool, False, "power", True, None, True)
        self.connectedPower = (bool, True, "power", True, None, True)
        self.conductivePower = (bool, False, "power", True, None, True)
        self.outputsPayload = (bool, False, "Payload", True, None, True)
        self.acceptsPayload = (bool, False, "Payload", True, None, True)
        self.updateInUnits = (bool, True, "payload", True, None, True)
        self.alwaysUpdateInUnits = (bool, False, "payload", True, None, True)
        self.allowResupply = (bool, False, "ammo", True, None, True)
        self.isDuct = (bool, False, "duct", True, None, True)
        self.outputFacing = (bool, True, "inGame", True, None, True)
        self.noSideBlend = (bool, False, "inGame", True, None, True)
        self.displayFlow = (bool, True, "inGame", True, None, True)
        self.inEditor = (bool, True, "inGame", True, None, True)
        self.lastConfig = (None, None, "inGame", False, None, False)
        self.saveConfig = (bool, False, "inGame", True, None, True)
        self.copyConfig = (bool, True, "inGame", True, None, True)
        self.clearOnDoubleTap = (bool, False, "inGame", True, None, True)
        self.update = (bool, False, "inGame", True, None, True)
        self.destructible = (bool, False, "inGame", True, None, True)
        self.unloadable = (bool, True, "inGame", True, None, True)
        self.solid = (bool, False, "inGame", True, None, True)
        self.solidifes = (bool, False, "inGame", True, None, True)
        self.teamPassable = (bool, False, "inGame", True, None, True)
        self.underBullets = (bool, False, "inGame", True, None, True)
        self.rotate = (bool, False, "inGame", True, None, True)
        self.rotateDraw = (bool, False, "inGame", True, None, True)
        self.lockRotation = (bool, True, "inGame", True, None, True)
        self.invertFlip = (bool, False, "inGame", True, None, True)
        self.variants = (int, 0, "inGame", True, None, True)
        self.drawArrow = (bool, True, "inGame", True, None, True)
        self.drawTeamOverlay = (bool, True, "inGame", True, None, True)
        self.saveData = (bool, False, "inGame", True, None, True)
        self.breakable = (bool, False, "inGame", True, None, True)
        self.rebuildable = (bool, True, "inGame", True, None, True)
        self.privileged = (bool, False, "inGame", True, None, True)
        self.requiresWater = (bool, False, "inGame", True, None, True)
        self.placeableLiquid = (bool, False, "inGame", True, None, True)
        self.placeablePlayer = (bool, True, "inGame", True, None, True)
        self.placeableOn = (bool, True, "inGame", True, None, True)
        self.insulated = (bool, False, "inGame", True, None, True)
        self.squareSprite = (bool, True, "inGame", True, None, True)
        self.absorbLasers = (bool, False, "inGame", True, None, True)
        self.enableDrawStatus = (bool, True, "inGame", True, None, True)
        self.drawDisabled = (bool, True, "inGame", True, None, True)
        self.autoResetEnabled = (bool, True, "inGame", True, None, True)
        self.noUpdateDisabled = (bool, False, "inGame", True, None, True)
        self.useColor = (bool, True, "inGame", True, None, True)
        self.drawCracks = (bool, True, "inGame", True, None, True)
        self.floating = (bool, False, "inGame", True, None, True)
        self.offset = (float, 0.0, "inGame", True, None, True)
        self.sizeOffset = (int, 0, "inGame", True, None, True)
        self.clipSize = (float, -1.0, "inGame", True, None, True)
        self.placeOverlapRange = (float, 50.0, "inGame", True, None, True)
        self.timers = (int, 1, "inGame", True, None, True)
        self.cacheLayer = (CacheLayer, "CacheLayer.normal", "inGame", True, None, True)
        self.fillsTile = (bool, True, "inGame", True, None, True)
        self.forceDark = (bool, False, "inGame", True, None, True)
        self.alwaysReplace = (bool, False, "inGame", True, None, True)
        self.replaceable = (bool, True, "inGame", True, None, True)
        # self.group = (BlockGroup, "BlockGroup.none", "inGame", True, None, True)
        # self.priority = (TargetPriority, "TargetPriority.base", "inGame", True, None, True)
        self.unitCapModifier = (int, 0, "inGame", True, None, True)
        self.configurable = (bool, False, "inGame", True, None, True)
        self.commandable = (bool, False, "inGame", True, None, True)
        self.allowConfigInventory = (bool, True, "inGame", True, None, True)
        self.selectionRows = (int, 5, "inGame", True, None, True)
        self.selectionColumns = (int, 4, "inGame", True, None, True)
        self.logicConfigurable = (bool, False, "inGame", True, None, True)
        self.consumesTap = (bool, False, "inGame", True, None, True)
        self.drawLiquidLight = (bool, True, "inGame", True, None, True)
        self.envRequired = (int, 0, "inGame", True, None, True)
        self.envDisabled = (int, 0, "inGame", True, None, True)
        self.sync = (bool, False, "inGame", True, None, True)
        self.conveyorPlacement = (bool, False, "inGame", True, None, True)
        self.allowDiagonal = (bool, True, "inGame", True, None, True)
        self.swapDiagonalPlacement = (bool, False, "inGame", True, None, True)
        self.schematicPriority = (int, 0, "inGame", True, None, True)
        # self.mapColor = (ColorSelect, (0, 0, 0, 1), "inGame", True, None, True)
        self.hasColor = (bool, False, "inGame", True, None, True)
        self.targetable = (bool, True, "inGame", True, None, True)
        self.attacks = (bool, False, "inGame", True, None, True)
        self.suppressable = (bool, False, "inGame", True, None, True)
        self.canOverdrive = (bool, True, "inGame", True, None, True)
        # self.outlineColor = (ColorHexSelect, "404049", "inGame", True, None, True)
        self.outlineIcon = (bool, False, "inGame", True, None, True)
        self.outlineRadius = (int, 4, "inGame", True, None, True)
        self.outlinedIcon = (int, -1, "inGame", True, None, True)
        self.hasShadow = (bool, True, "inGame", True, None, True)
        self.customShadow = (bool, False, "inGame", True, None, True)
        self.placePitchChange = (bool, True, "inGame", True, None, True)
        self.breakPitchChange = (bool, True, "inGame", True, None, True)
        self.placeSound = (SoundSelect.Widget, "Sounds.place", "inGame", True, None, True)
        self.breakSound = (SoundSelect.Widget, "Sounds.breaks", "inGame", True, None, True)
        self.destroySound = (SoundSelect.Widget, "Sounds.boom", "inGame", True, None, True)
        self.albedo = (float, 0.0, "inGame", True, None, True)
        # self.lightColor = (ColorHexSelect, "404049", "inGame", True, None, True)
        self.emitLight = (bool, False, "inGame", True, None, True)
        self.lightRadius = (float, 60.0, "inGame", True, None, True)
        self.fogRadius = (int, -1, "inGame", True, None, True)
        self.loopSound = (SoundSelect.Widget, "Sounds.none", "inGame", True, None, True)
        self.loopSoundVolume = (float, 0.5, "inGame", True, None, True)
        self.ambientSound = (SoundSelect.Widget, "Sounds.none", "inGame", True, None, True)
        self.ambientSoundVolume = (float, 0.05, "inGame", True, None, True)
        # self.requirements = (RequirementsSelect, [], "inGame", True, None, True)
        # self.category = (CategorySelect, "Category.distribution", "inGame", True, None, True)
        self.buildCost = (float, 20.0, "inGame", True, None, True)
        self.buildCostMultiplier = (float, 1.0, "inGame", True, None, True)
        self.deconstructThreshold = (float, 0.0, "inGame", True, None, True)
        self.instantDeconstruct = (bool, False, "inGame", True, None, True)
        # self.placeEffect = (FxSelect, "Fx.placeBlock", "inGame", True, None, True)
        # self.breakEffect = (FxSelect, "Fx.breakBlock", "inGame", True, None, True)
        # self.destroyEffect = (FxSelect, "Fx.dynamicExplosion", "inGame", True, None, True)
        self.researchCostMultiplier = (float, 1.0, "inGame", True, None, True)
        # self.researchCostMultipliers = (researchCostMultipliersSelect, {}, "inGame", True, None, True)
        self.instantTransfer = (bool, False, "inGame", True, None, True)
        self.quickRotate = (bool, True, "inGame", True, None, True)
        self.selectScroll = (float, 0.0, "inGame", True, None, True)
        self.hasConsumers = (bool, False, "inGame", True, None, True)
        # self.envEnabled =  (envSelect, "Env.terrestrial", "inGame", True, None, True)

        # Group: Ore
        # self.itemDrop = (ItemSelect, False, "ore", True, None, True)
        self.playerUnmineable = (bool, False, "ore", True, None, True)

        # Group: Basic
        self.scaledHealth = (float, -1.0, "basic", True, None, True)
        self.health = (int, -1, "basic", True, None, True)
        self.armor = (float, 0.0, "basic", True, None, True)
        # self.size = (SizeInt, 1, "basic", True, None, True)

        # Group: Effect & onBrake
        self.baseExplosiveness = (float, 0.0, "effect", True, None, True)
        # self.destroyBullet = (BulletType, None, "onBrake", True, None, True)
        self.destroyBulletSameTeam = (bool, False, "onBrake", True, None, True)
        self.createRubble = (bool, True, "onBrake", True, None, True)
        self.crushDamageMultiplier = (float, 1.0, "onBrake", True, None, True)

        self.buildVisibility = "BuildVisibility.hidden"
        self.researchCost = None
        self.subclass = None
        self.buildType = None
        self.configurations = {}
        self.itemFilter = []
        self.liquidFilter = []
        self.consumers = []
        self.optionalConsumers = []
        self.nonOptionalConsumers = []
        self.updateConsumers = []
        self.consPower = None

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
