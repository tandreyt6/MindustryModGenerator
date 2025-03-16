from .Block import Block
from .Wall import Wall

class Plugin:
    def __init__(self, app: Main):
        self.app = app
        print("generic loaded!")

    def getName(self):
        return "generic"

    def getDescription(self):
        return "This is template plugin."

    def getContent(self):
        return {
            "wall": {"displayName": "Wall", "plugin": "generic", "type": [Wall, Block], "end": ".java", "centralWidget": UI.Content.CentralPreviewWidget.PreviewWidget,
                 "paramCategory": {
                    "Basic": ["breakable", "scaledHealth", "health", "armor", "size"],
                    "Storage": ["hasItems", "acceptsItems", "separateItemCapacity", "itemCapacity", "itemDrop", "itemFilter"],
                    "Consumes": ["hasConsumers", "consumers", "consumesTap", "consumesPower", "optionalConsumers",
                                 "nonOptionalConsumers", "updateConsumers"],
                    "Liquids": ["hasLiquids", "outputsLiquid", "liquidCapacity", "liquidPressure", "placeableLiquid",
                                "lightLiquid", "drawLiquidLight", "liquidFilter"],
                    "Powers": ["hasPower", "outputsPower", "connectedPower", "conductivePower", "consPower"],
                    "Payload": ["outputsPayload", "acceptsPayload"],
                    "InGame": ["lastConfig", "saveConfig", "copyConfig", "saveData", "clearOnDoubleTap", "displayFlow",
                               "drawTeamOverlay", "teamPassable", "inEditor", "invertFlip", "drawArrow", "rebuildable",
                               "enableDrawStatus", "drawDisabled", "useColor", "mapColor"],
                    "World": ["solid", "solidifes", "rotate", "rotateDraw", "lockRotation", "requiresWater", "placeablePlayer",
                              "placeableOn", "absorbLasers", "canOverdrive"],
                    "Light": ["emitLight", "lightColor", "lightRadius"],
                    "Build": ["category", "buildCost", "buildVisibility", "buildCostMultiplier", "placeSound", "placeEffect",
                              "buildType"],
                    "Research": ["researchCost", "researchCostMultiplier", "researchCostMultipliers"],
                    "View": ["outputFacing"]
            }, "customParam": {
                "name": [CustomNoneClass, False],
                "package": [CustomNoneClass, False],
                "lightningChance": [FloatSpinBox, True],
                "lightningDamage": [FloatSpinBox, True],
                "chanceDeflect": [FloatSpinBox, True],
                "liquidCapacity": [FloatSpinBox, True],
                "liquidPressure": [FloatSpinBox, True],
                "armor": [FloatSpinBox, True],
                "baseExplosiveness": [FloatSpinBox, True],
                "offset": [FloatSpinBox, True],
                "clipSize": [FloatSpinBox, True],
                "placeOverlapRange": [FloatSpinBox, True],
                "crushDamageMultiplier": [FloatSpinBox, True],
                "albedo": [FloatSpinBox, True],
                "lightRadius": [FloatSpinBox, True],
                "loopSoundVolume": [FloatSpinBox, True],
                "ambientSoundVolume": [FloatSpinBox, True],
                "buildCost": [FloatSpinBox, True],
                "buildCostMultiplier": [FloatSpinBox, True],
                "deconstructThreshold": [FloatSpinBox, True],
                "placeSound": [SoundSelectWidget, True],
                "breakSound": [SoundSelectWidget, True],
                "destroySound": [SoundSelectWidget, True],
                "loopSound": [SoundSelectWidget, True],
                "ambientSound": [SoundSelectWidget, True],
            }}
        }

    def getStructuresMod(self):
        return {
            "145": self.generateCode
        }

    def generateCode(self, window=None):
        print("plugin close window!")
        window.close()