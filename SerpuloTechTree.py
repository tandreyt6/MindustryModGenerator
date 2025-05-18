SerpuloTree = {
    "name": "serpulo",
    "requirements": [],
    "children": [
        {
            "name": "conveyor",
            "requirements": [],
            "children": [
                {
                    "name": "junction",
                    "requirements": [],
                    "children": [
                        {
                            "name": "router",
                            "requirements": [],
                            "children": [
                                {
                                    "name": "advancedLaunchPad",
                                    "requirements": [
                                        ["sector", "extractionOutpost"]
                                    ],
                                    "children": [
                                        {
                                            "name": "landingPad",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "interplanetaryAccelerator",
                                                    "requirements": [
                                                        ["sector", "planetaryTerminal"]
                                                    ],
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": "distributor",
                                    "requirements": [],
                                    "children": []
                                },
                                {
                                    "name": "sorter",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "invertedSorter",
                                            "requirements": [],
                                            "children": []
                                        },
                                        {
                                            "name": "overflowGate",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "underflowGate",
                                                    "requirements": [],
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": "container",
                                    "requirements": [
                                        ["sector", "biomassFacility"]
                                    ],
                                    "children": [
                                        {
                                            "name": "unloader",
                                            "requirements": [],
                                            "children": []
                                        },
                                        {
                                            "name": "vault",
                                            "requirements": [
                                                ["sector", "stainedMountains"]
                                            ],
                                            "children": []
                                        }
                                    ]
                                },
                                {
                                    "name": "itemBridge",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "titaniumConveyor",
                                            "requirements": [
                                                ["sector", "craters"]
                                            ],
                                            "children": [
                                                {
                                                    "name": "phaseConveyor",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "massDriver",
                                                            "requirements": [],
                                                            "children": []
                                                        }
                                                    ]
                                                },
                                                {
                                                    "name": "payloadConveyor",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "payloadRouter",
                                                            "requirements": [],
                                                            "children": []
                                                        }
                                                    ]
                                                },
                                                {
                                                    "name": "armoredConveyor",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "plastaniumConveyor",
                                                            "requirements": [],
                                                            "children": []
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "name": "coreFoundation",
            "requirements": [],
            "children": [
                {
                    "name": "coreNucleus",
                    "requirements": [],
                    "children": []
                }
            ]
        },
        {
            "name": "mechanicalDrill",
            "requirements": [],
            "children": [
                {
                    "name": "mechanicalPump",
                    "requirements": [],
                    "children": [
                        {
                            "name": "conduit",
                            "requirements": [],
                            "children": [
                                {
                                    "name": "liquidJunction",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "liquidRouter",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "liquidContainer",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "liquidTank",
                                                            "requirements": [],
                                                            "children": []
                                                        }
                                                    ]
                                                },
                                                {
                                                    "name": "bridgeConduit",
                                                    "requirements": [],
                                                    "children": []
                                                },
                                                {
                                                    "name": "pulseConduit",
                                                    "requirements": [
                                                        ["sector", "windsweptIslands"]
                                                    ],
                                                    "children": [
                                                        {
                                                            "name": "phaseConduit",
                                                            "requirements": [],
                                                            "children": []
                                                        },
                                                        {
                                                            "name": "platedConduit",
                                                            "requirements": [],
                                                            "children": []
                                                        },
                                                        {
                                                            "name": "rotaryPump",
                                                            "requirements": [],
                                                            "children": [
                                                                {
                                                                    "name": "impulsePump",
                                                                    "requirements": [],
                                                                    "children": []
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "graphitePress",
                    "requirements": [],
                    "children": [
                        {
                            "name": "pneumaticDrill",
                            "requirements": [
                                ["sector", "frozenForest"]
                            ],
                            "children": [
                                {
                                    "name": "cultivator",
                                    "requirements": [
                                        ["sector", "biomassFacility"]
                                    ],
                                    "children": []
                                },
                                {
                                    "name": "laserDrill",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "blastDrill",
                                            "requirements": [
                                                ["sector", "nuclearComplex"]
                                            ],
                                            "children": []
                                        },
                                        {
                                            "name": "waterExtractor",
                                            "requirements": [
                                                ["sector", "saltFlats"]
                                            ],
                                            "children": [
                                                {
                                                    "name": "oilExtractor",
                                                    "requirements": [],
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "name": "pyratiteMixer",
                            "requirements": [],
                            "children": [
                                {
                                    "name": "blastMixer",
                                    "requirements": [
                                        ["sector", "facility32m"]
                                    ],
                                    "children": []
                                }
                            ]
                        },
                        {
                            "name": "siliconSmelter",
                            "requirements": [
                                ["sector", "frozenForest"]
                            ],
                            "children": [
                                {
                                    "name": "sporePress",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "coalCentrifuge",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "multiPress",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "siliconCrucible",
                                                            "requirements": [],
                                                            "children": []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "name": "plastaniumCompressor",
                                            "requirements": [
                                                ["sector", "windsweptIslands"]
                                            ],
                                            "children": [
                                                {
                                                    "name": "phaseWeaver",
                                                    "requirements": [
                                                        ["sector", "tarFields"]
                                                    ],
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": "kiln",
                                    "requirements": [
                                        ["sector", "craters"]
                                    ],
                                    "children": [
                                        {
                                            "name": "pulverizer",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "incinerator",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "melter",
                                                            "requirements": [],
                                                            "children": [
                                                                {
                                                                    "name": "surgeSmelter",
                                                                    "requirements": [],
                                                                    "children": []
                                                                },
                                                                {
                                                                    "name": "separator",
                                                                    "requirements": [],
                                                                    "children": [
                                                                        {
                                                                            "name": "disassembler",
                                                                            "requirements": [],
                                                                            "children": []
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "name": "cryofluidMixer",
                                                                    "requirements": [],
                                                                    "children": []
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": "microProcessor",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "switchBlock",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "message",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "logicDisplay",
                                                            "requirements": [],
                                                            "children": [
                                                                {
                                                                    "name": "largeLogicDisplay",
                                                                    "requirements": [],
                                                                    "children": []
                                                                },
                                                                {
                                                                    "name": "logicDisplayTile",
                                                                    "requirements": [],
                                                                    "children": []
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "name": "memoryCell",
                                                            "requirements": [],
                                                            "children": [
                                                                {
                                                                    "name": "memoryBank",
                                                                    "requirements": [],
                                                                    "children": []
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "name": "logicProcessor",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "hyperProcessor",
                                                            "requirements": [],
                                                            "children": []
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": "illuminator",
                                    "requirements": [],
                                    "children": []
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "combustionGenerator",
                    "requirements": [
                        ["research", "Items.coal"]
                    ],
                    "children": [
                        {
                            "name": "powerNode",
                            "requirements": [],
                            "children": [
                                {
                                    "name": "powerNodeLarge",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "diode",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "surgeTower",
                                                    "requirements": [],
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": "battery",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "batteryLarge",
                                            "requirements": [],
                                            "children": []
                                        }
                                    ]
                                },
                                {
                                    "name": "mender",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "mendProjector",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "forceProjector",
                                                    "requirements": [
                                                        ["sector", "impact0078"]
                                                    ],
                                                    "children": [
                                                        {
                                                            "name": "overdriveProjector",
                                                            "requirements": [
                                                                ["sector", "impact0078"]
                                                            ],
                                                            "children": [
                                                                {
                                                                    "name": "overdriveDome",
                                                                    "requirements": [
                                                                        ["sector", "impact0078"]
                                                                    ],
                                                                    "children": []
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "name": "repairPoint",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "repairTurret",
                                                            "requirements": [],
                                                            "children": []
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": "steamGenerator",
                                    "requirements": [
                                        ["sector", "craters"]
                                    ],
                                    "children": [
                                        {
                                            "name": "thermalGenerator",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "differentialGenerator",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "thoriumReactor",
                                                            "requirements": [
                                                                ["research", "Liquids.cryofluid"]
                                                            ],
                                                            "children": [
                                                                {
                                                                    "name": "impactReactor",
                                                                    "requirements": [],
                                                                    "children": []
                                                                },
                                                                {
                                                                    "name": "rtgGenerator",
                                                                    "requirements": [],
                                                                    "children": []
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": "solarPanel",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "largeSolarPanel",
                                            "requirements": [],
                                            "children": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "name": "duo",
            "requirements": [],
            "children": [
                {
                    "name": "copperWall",
                    "requirements": [],
                    "children": [
                        {
                            "name": "copperWallLarge",
                            "requirements": [],
                            "children": [
                                {
                                    "name": "scrapWall",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "scrapWallLarge",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "scrapWallHuge",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "scrapWallGigantic",
                                                            "requirements": [],
                                                            "children": []
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": "titaniumWall",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "titaniumWallLarge",
                                            "requirements": [],
                                            "children": []
                                        },
                                        {
                                            "name": "door",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "doorLarge",
                                                    "requirements": [],
                                                    "children": []
                                                }
                                            ]
                                        },
                                        {
                                            "name": "plastaniumWall",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "plastaniumWallLarge",
                                                    "requirements": [],
                                                    "children": []
                                                }
                                            ]
                                        },
                                        {
                                            "name": "thoriumWall",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "thoriumWallLarge",
                                                    "requirements": [],
                                                    "children": []
                                                },
                                                {
                                                    "name": "surgeWall",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "surgeWallLarge",
                                                            "requirements": [],
                                                            "children": []
                                                        },
                                                        {
                                                            "name": "phaseWall",
                                                            "requirements": [],
                                                            "children": [
                                                                {
                                                                    "name": "phaseWallLarge",
                                                                    "requirements": [],
                                                                    "children": []
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "scatter",
                    "requirements": [],
                    "children": [
                        {
                            "name": "hail",
                            "requirements": [
                                ["sector", "craters"]
                            ],
                            "children": [
                                {
                                    "name": "salvo",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "swarmer",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "cyclone",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "spectre",
                                                            "requirements": [
                                                                ["sector", "nuclearComplex"]
                                                            ],
                                                            "children": []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "name": "ripple",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "fuse",
                                                    "requirements": [],
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "scorch",
                    "requirements": [],
                    "children": [
                        {
                            "name": "arc",
                            "requirements": [],
                            "children": [
                                {
                                    "name": "wave",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "parallax",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "segment",
                                                    "requirements": [],
                                                    "children": []
                                                }
                                            ]
                                        },
                                        {
                                            "name": "tsunami",
                                            "requirements": [],
                                            "children": []
                                        }
                                    ]
                                },
                                {
                                    "name": "lancer",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "meltdown",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "foreshadow",
                                                    "requirements": [],
                                                    "children": []
                                                }
                                            ]
                                        },
                                        {
                                            "name": "shockMine",
                                            "requirements": [],
                                            "children": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "name": "groundFactory",
            "requirements": [],
            "children": [
                {
                    "name": "dagger",
                    "requirements": [],
                    "children": [
                        {
                            "name": "mace",
                            "requirements": [],
                            "children": [
                                {
                                    "name": "fortress",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "scepter",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "reign",
                                                    "requirements": [],
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "name": "nova",
                            "requirements": [
                                ["sector", "fungalPass"]
                            ],
                            "children": [
                                {
                                    "name": "pulsar",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "quasar",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "vela",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "corvus",
                                                            "requirements": [],
                                                            "children": []
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "name": "crawler",
                            "requirements": [],
                            "children": [
                                {
                                    "name": "atrax",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "spiroct",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "arkyid",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "toxopid",
                                                            "requirements": [
                                                                ["sector", "mycelialBastion"]
                                                            ],
                                                            "children": []
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "airFactory",
                    "requirements": [],
                    "children": [
                        {
                            "name": "flare",
                            "requirements": [],
                            "children": [
                                {
                                    "name": "horizon",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "zenith",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "antumbra",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "eclipse",
                                                            "requirements": [],
                                                            "children": []
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": "mono",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "poly",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "mega",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "quad",
                                                            "requirements": [],
                                                            "children": [
                                                                {
                                                                    "name": "oct",
                                                                    "requirements": [],
                                                                    "children": []
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "name": "navalFactory",
                            "requirements": [
                                ["sector", "windsweptIslands"]
                            ],
                            "children": [
                                {
                                    "name": "risso",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "minke",
                                            "requirements": [],
                                            "children": [
                                                {
                                                    "name": "bryde",
                                                    "requirements": [],
                                                    "children": [
                                                        {
                                                            "name": "sei",
                                                            "requirements": [],
                                                            "children": [
                                                                {
                                                                    "name": "omura",
                                                                    "requirements": [],
                                                                    "children": []
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "name": "retusa",
                                            "requirements": [
                                                ["sector", "windsweptIslands"]
                                            ],
                                            "children": [
                                                {
                                                    "name": "oxynoe",
                                                    "requirements": [
                                                        ["sector", "coastline"]
                                                    ],
                                                    "children": [
                                                        {
                                                            "name": "cyerce",
                                                            "requirements": [],
                                                            "children": [
                                                                {
                                                                    "name": "aegires",
                                                                    "requirements": [],
                                                                    "children": [
                                                                        {
                                                                            "name": "navanax",
                                                                            "requirements": [
                                                                                ["sector", "navalFortress"]
                                                                            ],
                                                                            "children": []
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "additiveReconstructor",
                    "requirements": [
                        ["sector", "fungalPass"]
                    ],
                    "children": [
                        {
                            "name": "multiplicativeReconstructor",
                            "requirements": [
                                ["sector", "frontier"]
                            ],
                            "children": [
                                {
                                    "name": "exponentialReconstructor",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "tetrativeReconstructor",
                                            "requirements": [],
                                            "children": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "name": "groundZero",
            "requirements": [],
            "children": [
                {
                    "name": "frozenForest",
                    "requirements": [
                        ["sector", "groundZero"],
                        ["research", "junction"],
                        ["research", "router"]
                    ],
                    "children": [
                        {
                            "name": "craters",
                            "requirements": [
                                ["sector", "frozenForest"],
                                ["research", "mender"],
                                ["research", "combustionGenerator"]
                            ],
                            "children": [
                                {
                                    "name": "fungalPass",
                                    "requirements": [
                                        ["sector", "craters"],
                                        ["research", "groundFactory"],
                                        ["research", "dagger"]
                                    ],
                                    "children": [
                                        {
                                            "name": "frontier",
                                            "requirements": [
                                                ["sector", "biomassFacility"],
                                                ["sector", "fungalPass"],
                                                ["research", "groundFactory"],
                                                ["research", "airFactory"],
                                                ["research", "additiveReconstructor"],
                                                ["research", "mace"],
                                                ["research", "mono"]
                                            ],
                                            "children": [
                                                {
                                                    "name": "overgrowth",
                                                    "requirements": [
                                                        ["sector", "frontier"],
                                                        ["sector", "windsweptIslands"],
                                                        ["research", "multiplicativeReconstructor"],
                                                        ["research", "fortress"],
                                                        ["research", "ripple"],
                                                        ["research", "salvo"],
                                                        ["research", "cultivator"],
                                                        ["research", "sporePress"]
                                                    ],
                                                    "children": [
                                                        {
                                                            "name": "mycelialBastion",
                                                            "requirements": [
                                                                ["research", "atrax"],
                                                                ["research", "spiroct"],
                                                                ["research", "arkyid"],
                                                                ["research", "multiplicativeReconstructor"],
                                                                ["research", "exponentialReconstructor"]
                                                            ],
                                                            "children": []
                                                        },
                                                        {
                                                            "name": "atolls",
                                                            "requirements": [
                                                                ["sector", "windsweptIslands"],
                                                                ["research", "multiplicativeReconstructor"],
                                                                ["research", "mega"]
                                                            ],
                                                            "children": []
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "name": "Items.copper",
            "requirements": [],
            "children": [
                {
                    "name": "Liquids.water",
                    "requirements": [],
                    "children": []
                },
                {
                    "name": "Items.lead",
                    "requirements": [],
                    "children": [
                        {
                            "name": "Items.titanium",
                            "requirements": [],
                            "children": [
                                {
                                    "name": "Liquids.cryofluid",
                                    "requirements": [],
                                    "children": []
                                },
                                {
                                    "name": "Items.thorium",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "Items.surgeAlloy",
                                            "requirements": [],
                                            "children": []
                                        },
                                        {
                                            "name": "Items.phaseFabric",
                                            "requirements": [],
                                            "children": []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "name": "Items.metaglass",
                            "requirements": [],
                            "children": []
                        }
                    ]
                },
                {
                    "name": "Items.sand",
                    "requirements": [],
                    "children": [
                        {
                            "name": "Items.scrap",
                            "requirements": [],
                            "children": [
                                {
                                    "name": "Liquids.slag",
                                    "requirements": [],
                                    "children": []
                                }
                            ]
                        },
                        {
                            "name": "Items.coal",
                            "requirements": [],
                            "children": [
                                {
                                    "name": "Items.graphite",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "Items.silicon",
                                            "requirements": [],
                                            "children": []
                                        }
                                    ]
                                },
                                {
                                    "name": "Items.pyratite",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "Items.blastCompound",
                                            "requirements": [],
                                            "children": []
                                        }
                                    ]
                                },
                                {
                                    "name": "Items.sporePod",
                                    "requirements": [],
                                    "children": []
                                },
                                {
                                    "name": "Liquids.oil",
                                    "requirements": [],
                                    "children": [
                                        {
                                            "name": "Items.plastanium",
                                            "requirements": [],
                                            "children": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}