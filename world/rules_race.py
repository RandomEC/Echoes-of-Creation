def get_race(race):

    requested_race = race
    
    races = {
        "default": {
            "size": 2,
            "pc available": False,
            "can wield": False,
            "damage message": "punch",
            "hate list": tuple(),
            "inherent affects": tuple(),
            "attribute modifier": {
                "strength": 0,
                "intelligence": 0,
                "wisdom": 0,
                "dexterity": 0,
                "constitution": 0
                },
            "heal modifier": 0,
            "mana modifier": 0,
            "moves modifier": 0
            },
        "human": {
            "size": 3,
            "pc available": True,
            "can wield": True,
            "hate list": ("githyanki", "vampire", "werewolf", "mindflayer")
            },

        "elf": {
            "inherent affects": (
                "detect hidden",
                "infravision",
                ),
            "can wield": True,
            "pc available": True,
            "attribute modifier": {
                "intelligence": 1,
                "dexterity": 1,
                "constitution": -1
                },
            "hate list": ("drow", "ogre", "orc", "kobold", "troll", "hobgoblin", "dragon", "vampire", "werewolf", "goblin", "halfkobold"),
            "mana modifier": 0.5
            },

        "eldar": {
            "inherent affects": (
                "detect hidden",
                "infravision"
                ),
            "can wield": True,
            "pc available": True,
            "attribute modifier": {
                "intelligence": 1,
                "wisdom": 1,
                "constitution": -1
                },
            "hate list": ("drow", "ogre", "orc", "kobold", "troll", "hobgoblin", "dragon", "vampire", "werewolf", "goblin", "halfkobold"),
            "mana modifier": 0.5
            },

        "halfelf": {
            "size": 3,
            "inherent affects": (
                "infravision",
                ),
            "can wield": True,
            "pc available": True,
            "attribute modifier": {
                "dexterity": 1
                },
            "hate list": ("drow","ogre","orc","kobold","troll","hobgoblin","dragon","vampire","werewolf","goblin")
            },

        "drow": {
            "inherent affects": (
                "detect hidden",
                "infravision"
                ),
            "can wield": True,
            "pc available": True,
            "attribute modifier": {
                "wisdom": 1,
                "dexterity": 1
                },
            "hate list": ("elf","halfelf","hobbit","githyanki","vampire","werewolf")
            },

        "dwarf": {
            "inherent affects": (
                "detect hidden",
                "infravision"
                ),
            "can wield": True,
            "pc available": True,
            "attribute modifier": {
                "dexterity": -1,
                "constitution": 1
                },
            "hate list": ("giant","ogre","orc","kobold","minotaur","troll","hobgoblin","dragon","vampire","werewolf","goblin","halfkobold")
            },
        
        "halfdwarf": {
            "inherent affects": (
                "infravision",
                ),
            "can wield": True,
            "pc available": True,
            "attribute modifier": {
                "constitution": 1
                },
            "hate list": ("giant","ogre","orc","kobold","minotaur","troll","hobgoblin","dragon","vampire","werewolf","goblin")
            },

        "hobbit": {
            "inherent affects": (
                "detect hidden",
                "infravision"
                ),
            "can wield": True,
            "pc available": True,
            "attribute modifier": {
                "dexterity": 1,
                "constitution": -1
                },
            "hate list": ("giant","ogre","orc","kobold","minotaur","troll","hobgoblin","dragon","vampire","werewolf","goblin","halfkobold")
            },

        "giant": {
            "size": 6,
            "can wield": True,
            "attribute modifier": {
                "strength": 2,
                "intelligence": -1,
                "dexterity": -1,
                "constitution": 1
                },
            "damage message": "fist",
            "hate list": ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome"),
            "heal modifier": 3
            },

        "ogre": {
            "size": 5,
            "can wield": True,
            "pc available": True,
            "attribute modifier": {
                "strength": 1,
                "intelligence": -1,
                "dexterity": -1,
                "constitution": 1
                },
            "damage message": "fist",
            "hate list": ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome"),
            "heal modifier": 2
            },
        
        "orc": {
            "size": 4,
            "can wield": True,
            "pc available": True,
            "inherent affects": (
                "infravision",
                ),
            "attribute modifier": {
                "strength": 1,
                "intelligence": -1,
                "constitution": 1
                },
            "hate list": ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome"),
            "heal modifier": 2
            },

        "kobold": {
            "can wield": True,
            "inherent affects": (
                "infravision",
                ),
            "attribute modifier": {
                "strength": -1,
                "intelligence": -1,
                "dexterity": 1
                },
            "hate list": ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome","halfkobold")
            },

        "minotaur": {
            "size": 5,
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                ),
            "attribute modifier": {
                "strength": 2,
                "dexterity": -1,
                "constitution": 1
                },
            "damage message": "fist",
            "hate list": ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome"),
            "heal modifier": 3
            },

        "troll": {
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "infravision"
                ),
            "size": 7,
            "attribute modifier": {
                "strength": 2,
                "intelligence": -1,
                "constitution": 1
                },
            "damage message": "fist",
            "hate list": ("human","elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome"),
            "heal modifier": 10
            },
        
        "hobgoblin": {
            "can wield": True,
            "inherent affects": (
                "infravision",
                ),
            "size": 3,
            "attribute modifier": {
                "strength": 1,
                "wisdom": -1,
                "constitution": 1
                },
            "hate list": ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome")
            },

        "insect": {
            "inherent affects": (
                "mute",
                ),
            "size": 0,
            "attribute modifier": {
                "constitution": -1
                },
            "damage message": "bite"
            },

        "dragon": {
            "size": 9,
            "attribute modifier": {
                "strength": 2,
                "intelligence": 2,
                "wisdom": 1,
                "dexterity": -3,
                "constitution": 2
                },
            "damage message": "claw",
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "detect invisible",
                "detect alignment",
                "infravision",
                "fly"
                ),
            "heal modifier": 15
            },
                    
        "demon": {
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "infravision"
                ),
            "size": 5,
            "attribute modifier": {
                "strength": 2,
                "intelligence": -2,
                "wisdom": -1,
                "dexterity": -1,
                "constitution": 3,
                },
            "damage message": "claw",
            "heal modifier": 3,
            "mana modifier": 0.75
            },
            
        "animal": {
            "attribute modifier": {
                "dexterity": 1
                },
            "damage message": "bite",
            "hate list": ("kobold","halfkobold"),
            "inherent affects": (
                "mute",
                "detect hidden"
                )
            },

        "god": {
            "can wield": True,
            "inherent affects": (
                "sanctuary",
                "protection",
                "detect hidden",
                "detect invisible",
                "detect alignment",
                "infravision",
                "pass door",
                "waterwalk",
                "swim",
                "fly",
                "waterbreath"
                ),
            "size": 8,
            "attribute modifier": {
                "strength": 3,
                "intelligence": 3,
                "wisdom": 3,
                "dexterity": 3,
                "constitution": 3
                },
            "damage message": "smite",
            "heal modifier": 20
            },
            
        "undead": {
            "size": 3,
            "attribute modifier": {
                "strength": 1,
                "dexterity": -2,
                "constitution": 1
                },
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "detect invisible",
                "detect alignment",
                "infravision",
                "pass door"
                ),
            "damage message": "touch",
            "hate list": ("human","elf","halfelf","drow","dwarf","halfdwarf","hobbit","giant","ogre","orc","kobold","minotaur","troll","hobgoblin","goblin","faerie","gnome")
            },

        "lich": {
            "can wield": True,
            "inherent affects": (
                "detect alignment",
                "infravision"
                ),
            "size": 3,
            "attribute modifier": {
                "strength": 1,
                "dexterity": -2,
                "constitution": 1
                },
            "damage message": "touch",
            "hate list": ("human","elf","halfelf","dwarf","halfdwarf","hobbit","faerie")
            },

        "harpy": {
            "hate list": ("human","elf","halfelf","dwarf","halfdwarf","hobbit","gnome"),
            "inherent affects": (
                "detect invisible",
                "fly"
                ),
            "size": 3,
            "attribute modifier": {
                "dexterity": 2
                },
            "moves modifier": 0.5
            },
            
        "bear": {
            "inherent affects": (
                "mute",
                "detect hidden",
                "swim"
                ),
            "size": 3,
            "attribute modifier": {
                "strength": 1,
                "dexterity": -1,
                "constitution": 1
                },
            "damage message": "swipe"
            },
            
        "sloth": {
            "damage message": "swipe",
            "attribute modifier": {
                "constitution": 3,
                "dexterity": -2
                },
            "inherent affects": (
                "mute",
                "infravision"
                )
            },
            
        "githyanki": {
            "can wield": True,
            "size": 3,
            "attribute modifier": {
                "intelligence": 1
                },
            "hate list": ("Mindflayer")
            },
            
        "elemental": {
            "attribute modifier": {
                "constitution": 1,
                "strength": 1
                },
            "size": 4
            },
            
        "bat": {
            "inherent affects": (
                "mute",
                "infravision",
                "fly"
                ),
            "attribute modifier": {
                "strength": -1,
                "dexterity": 2,
                "constitution": -1
                },
            "damage message": "bite",
            "size": 1,
            "moves modifier": 0.5
            },
            
        "plant": {
            "damage message": "swipe",
            "attribute modifier": {
                "constitution": 1,
                "dexterity": -1
                },
            "inherent affects": (
                "mute",
                "swim"
                ),
            "size": 1
            },
            
        "rat": {
            "inherent affects": (
                "mute",
                "pass door"
                ),
            "size": 0,
            "attribute modifier": {
                "strength": -1,
                "dexterity": 2,
                "constitution": -1
                },
            "damage message": "bite"
            },
            
        "vampire": {
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "detect invisible",
                "detect alignment",
                "infravision",
                "pass door",
                "fly"
                ),
            "size": 3,
            "attribute modifier": {
                "strength": 1,
                "intelligence": 1,
                "dexterity": 1,
                "constitution": 2
                },
            "damage message": "claw",
            "hate list": ("human","elf","halfelf","drow","dwarf","halfdwarf","hobbit","giant","ogre","orc","kobold","minotaur","troll","hobgoblin","werewolf","goblin","faerie","gnome"),
            "heal modifier": 10,
            "moves modifier": 0.5
            },
            
        "werewolf": {
            "damage message": "claw",
            "attribute modifier": {
                "constitution": 3,
                "dexterity": 2,
                "wisdom": 1,
                "strength": 2
                },
            "size": 3,
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "detect invisible",
                "detect alignment",
                "infravision"
                ),
            "hate list": ("human","elf","halfelf","drow","dwarf","halfdwarf","hobbit","giant","ogre","orc","kobold","minotaur","troll","hobgoblin","werewolf","goblin","faerie","gnome"),
            "heal modifier": 10
            },

        "goblin": {
            "can wield": True,
            "inherent affects": (
                "infravision",
                ),
            "attribute modifier": {
                "strength": -1,
                "intelligence": -1,
                "wisdom": -1,
                "dexterity": 1
                },
            "hate list": ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome")
            },
            
        "faerie": {
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "detect invisible",
                "infravision",
                "fly"
                ),
            "size": 1,
            "attribute modifier": {
                "strength": -2,
                "intelligence": 1,
                "wisdom": 1,
                "dexterity": 1,
                "constitution": -1
                }
            },
            
        "pixie": {
            "attribute modifier": {
                "constitution": -1,
                "dexterity": 1,
                "wisdom": 1,
                "intelligence": 1,
                "strength": -2
                },
            "size": 1,
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "detect invisible",
                "infravision"
                )
            },
            
        "arachnid": {
            "inherent affects": (
                "mute",
                ),
            "can wield": True,
            "attribute modifier": {
                "dexterity": 1
                },
            "damage message": "bite"
            },
            
        "mindflayer": {
            "hate list": ("githyanki"),
            "attribute modifier": {
                "dexterity": -1,
                "wisdom": 1,
                "intelligence": 2,
                "strength": 1
                },
            "can wield": True,
            "inherent affects": (
                "infravision",
                ),
            "size": 3
            },
            
        "object": {
            "inherent affects": (
                "mute",
                "waterbreath"
                ),
            "size": 3,
            "attribute modifier": {
                "strength": 3,
                "constitution": 3
                },
            "damage message": "swing"
            },
            
        "mist": {
            "damage message": "gas",
            "attribute modifier": {
                "dexterity": 3,
                "strength": -1
                },
            "inherent affects": (
                "mute",
                "pass door",
                "fly"
                ),
            "moves modifier": 0.5
            },
            
        "snake": {
            "inherent affects": (
                "mute",
                ),
            "size": 1,
            "attribute modifier": {
                "dexterity": 1
                },
            "damage message": "bite"
            },
        
        "worm": {
            "damage message": "slime",
            "size": 0,
            "inherent affects": (
                "mute",
                "pass door"
                )
            },
            
        "fish": {
            "inherent affects": (
                "mute",
                "swim",
                "waterbreath"
                ),
            "size": 1,
            "attribute modifier": {
                "dexterity": 2
                },
            "damage message": "bite"
            },
            
        "hydra": {
            "damage message": "bite",
            "attribute modifier": {
                "constitution": 2,
                "dexterity": -1,
                "strength": 2
                },
            "size": 8,
            "inherent affects": (
                "mute",
                "detect hidden"
                )
            },
            
        "lizard": {
            "inherent affects": (
                "mute",
                ),
            "size": 1,
            "attribute modifier": {
                "strength": -1,
                "dexterity": 1
                },
            "damage message": "lash"
            },
            
        "lizardman": {
            "damage message": "lash",
            "attribute modifier": {
                "constitution": 1,
                "dexterity": 1,
                "wisdom": -1,
                "intelligence": -1,
                "strength": 1
                },
            "size": 3,
            "can wield": True,
            "pc available": True
            },
            
        "gnome": {
            "can wield": True,
            "pc available": True,
            "inherent affects": (
                "infravision",
                ),
            "attribute modifier": {
                "strength": -1,
                "wisdom": 1,
                "dexterity": 1,
                "constitution": -1
                },
            "hate list": ("drow","ogre","orc","kobold","troll","hobgoblin","dragon","vampire","werewolf","goblin"),
            "mana modifier": 0.5
            },
            
        "halfkobold": {
            "attribute modifier": {
                "strength": -2,
                "intelligence": -1,
                "wisdom": -2,
                "dexterity": 3,
                "constitution": -2
                },
            "can wield": True,
            "inherent affects": (
                "infravision",
                ),
            "pc available": True,
            "hate list": ("ogre","orc","giant","troll","hobgoblin")
            },
            
        "troglodyte": {
            "can wield": True,
            "inherent affects": (
                "infravision",
                ),
            "size": 3,
            "attribute modifier": {
                "strength": 1,
                "dexterity": -2,
                "constitution": 1
                },
            "damage message": "claw",
            "hate list": ("dwarf","elf","gnome","halfelf","hobbit","human"),
            "heal modifier": 3
            },
        
        "tabaxi": {
            "size": 4,
            "attribute modifier": {
                "dexterity": 1
                },
            "damage message": "claw",
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "infravision"
                ),
            "moves modifier": 0.5
            },
            
        "rakshasa": {
            "can wield": True,
            "inherent affects": (
                "protection",
                ),
            "size": 3,
            "attribute modifier": {
                "intelligence": 1,
                "wisdom": 1,
                "constitution": -1
                },
            "hate list": ("human","elf","halfelf"),
            "mana modifier": 0.75
            },
        
        "kenku": {
            "size": 3,
            "can wield": True,
            "inherent affects": (
                "fly",
                )
            },
            
        "halfdemon": {
            "can wield": True,
            "inherent affects": (
                "infravision",
                ),
            "attribute modifier": {
                "strength": 2,
                "dexterity": -1,
                "constitution": -1
                },
            "heal modifier": 3,
            "mana modifier": 0.75
            },
            
        "grugach": {
            "hate list": ("halfelf","human","drow","dwarf","orc","gnome","hobbit"),
            "attribute modifier": {
                "strength": 2,
                "dexterity": 1,
                "constitution": -1
                },
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "infravision"
                )
            },
            
        "ape": {
            "inherent affects": (
                "mute",
                ),
            "size": 4,
            "attribute modifier": {
                "strength": 4,
                "intelligence": -4,
                "wisdom": -4,
                "constitution": 4
                }
            },    
            
        "feline": {
            "damage message": "claw",
            "attribute modifier": {
                "dexterity": 3
                },
            "size": 1,
            "inherent affects": (
                "mute",
                "infravision"
                ),
            "hate list": ("dog"),
            "moves modifier": 0.5
            },
        
        "big cat": {
            "inherent affects": (
                "mute",
                "infravision"
                ),
            "size": 5,
            "attribute modifier": {
                "strength": 3,
                "dexterity": 3
                },
            "damage message": "claw"
            },
                
        "cyclops": {
            "attribute modifier": {
                "constitution": 2,
                "dexterity": -2,
                "strength": 2
                },
            "size": 4,
            "can wield": True
            },
            
        "dinosaur": {
            "inherent affects": (
                "mute",
                ),
            "size": 10,
            "attribute modifier": {
                "strength": 7,
                "dexterity": -7
                },
            "damage message": "bite"
            },

        "horse": {
            "damage message": "pound",
            "attribute modifier": {
                "strength": 4
                },
            "size": 6,
            "inherent affects": (
                "mute",
                )
            },
            
        "centaur": {
            "can wield": True,
            "size": 6,
            "attribute modifier": {
                "strength": 3,
                "dexterity": -2
                },
            "damage message": "pound"
            },
            
        "thri-kreen": {
            "damage message": "bite",
            "attribute modifier": {
                "dexterity": 2,
                "strength": 2
                },
            "size": 3,
            "can wield": True
            },
            
        "pudding": {
            "inherent affects": (
                "mute",
                "detect hidden",
                "detect invisible",
                "pass door"
                ),
            "size": 3,
            "damage message": "slime"
            },
        
        "chimera": {
            "damage message": "claw",
            "size": 4,
            "inherent affects": (
                "protection",
                "detect hidden",
                "detect invisible",
                "swim",
                "fly"
                ),
            "heal modifier": 3
            },
            
        "dog": {
            "inherent affects": (
                "mute",
                "detect hidden"
                ),
            "size": 3,
            "damage message": "bite",
            "hate list": ("feline")
            },

        "elephant": {
            "damage message": "pound",
            "attribute modifier": {
                "dexterity": -3,
                "strength": 3
                },
            "size": 7,
            "inherent affects": (
                "mute",
                )
            },
            
        "ettin": {
            "can wield": True,
            "size": 7,
            "attribute modifier": {
                "strength": 3,
                "dexterity": -2,
                "constitution": 1
                },
            "hate list": ("human","elf","halfelf","dwarf","gnome","hobbit"),
            "heal modifier": 10
            },
        
        "amphibian": {
            "damage message": "bite",
            "size": 1,
            "inherent affects": (
                "mute",
                "swim",
                "waterbreath"
                )
            },
            
        "gnoll": {
            "can wield": True,
            "inherent affects": (
                "infravision",
                ),
            "size": 4,
            "attribute modifier": {
                "strength": 2,
                "dexterity": -2
                },
            "hate list": ("elf","hobbit","dwarf","human","halfelf"),
            "heal modifier": 2
            },
        
        "automaton": {
            "attribute modifier": {
                "dexterity": -4,
                "constitution": 2,
                "strength": 2
                },
            "size": 4,
            "inherent affects": (
                "mute",
                )
            },
            
        "griffon": {
            "inherent affects": (
                "mute",
                "fly"
                ),
            "size": 5,
            "damage message": "bite",
            "hate list": ("horse")
            },
            
        "imp": {
            "hate list": ("elf","halfelf"),
            "damage message": "bite",
            "attribute modifier": {
                "constitution": -3,
                "dexterity": 3,
                "strength": -3
                },
            "size": 1,
            "inherent affects": (
                "infravision",
                ),
            "heal modifier": 2,
            "mana modifier": 0.75
            },
            
        "leprechaun": {
            "can wield": True,
            "inherent affects": (
                "detect invisible",
                ),
            "size": 1,
            "attribute modifier": {
                "strength": -3,
                "intelligence": 1,
                "dexterity": 3
                },
            "mana modifier": 0.5
            },
            
        "medusa": {
            "hate list": ("human", "elf","halfelf","gnome","hobbit","dwarf"),
            "attribute modifier": {
                "dexterity": -1,
                "wisdom": 1
                },
            "size": 3,
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "detect invisible"
                )
            },
            
        "monster": {
            "inherent affects": (
                "detect hidden",
                "detect invisible",
                "swim",
                "fly"
                ),
            "size": 10,
            "attribute modifier": {
                "strength": 7,
                "dexterity": 7,
                "constitution": 7
                },
            "damage message": "bite"
            },

        "pegasus": {
            "damage message": "pound",
            "attribute modifier": {
                "strength": 4
                },
            "size": 6,
            "inherent affects": (
                "mute",
                "fly"
                )
            },
            
        "unicorn": {
            "inherent affects": (
                "mute",
                ),
            "size": 6,
            "attribute modifier": {
                "strength": 4
                },
            "damage message": "pierce",
            "hate list": ("drow","demon","halfdemon","monster")
            },
            
        "ru": {
            "inherent affects": (
                "mute",
                ),
            "size": 3,
            "damage message": "grep"
            },
            
        "parasite": {
            "damage message": "bite",
            "attribute modifier": {
                "dexterity": 10,
                "strength": -10
                },
            "inherent affects": (
                "mute",
                "pass door",
                "swim",
                "fly",
                "waterbreath"
                ),        
            "size": 0
            },
            
        "satyr": {
            "can wield": True,
            "inherent affects": (
                "protection",
                "detect hidden",
                "detect invisible",
                "infravision"
                ),
            "size": 3,
            "attribute modifier": {
                "dexterity": 2
                },
            "damage message": "pound"
            },
        
        "sphinx": {
            "attribute modifier": {
                "strength": 2,
                "dexterity": -2
                },
            "inherent affects": (
                "sanctuary",
                "protection",
                "fly"
                ),
            "size": 6,
            "heal modifier": 10,
            "mana modifier": 0.75
            },
            
        "titan": {
            "can wield": True,
            "size": 9,
            "attribute modifier": {
                "strength": 5
                },
            "damage message": "pound",
            "hate list": ("demon","halfdemon"),
            "heal modifier": 15
            },
            
        "treant": {
            "damage message": "pound",
            "attribute modifier": {
                "dexterity": -5,
                "strength": 3
                },
            "size": 8,
            "inherent affects": (
                "mute",
                )
            },
            
        "wolf": {
            "inherent affects": (
                "mute",
                "detect hidden",
                "detect invisible",
                "infravision"
                ),
            "size": 3,
            "attribute modifier": {
                "intelligence": -2,
                "dexterity": 2,
                "constitution": 2
                },
            "damage message": "bite"
            },
        
        "wolverine": {
            "inherent affects": (
                "mute",
                ),
            "size": 1,
            "attribute modifier": {
                "dexterity": 3
                },
            "damage message": "claw",
            "moves modifier": 0.5
            },
        
        "yeti": {
            "damage message": "pound",
            "attribute modifier": {
                "constitution": 5,
                "dexterity": -1,
                "wisdom": -2,
                "intelligence": -2,
                "strength": 5
                },
            "size": 5,
            "inherent affects": (
                "mute",
                )
            },
            
        "beastman": {
            "can wield": True,
            "inherent affects": (
                "mute",
                "detect hidden",
                ),
            "size": 3,
            "attribute modifier": {
                "strength": 2,
                "intelligence": -1,
                "wisdom": -1,
                "constitution": 2
                }
            },
            
        "bird": {
            "damage message": "bite",
            "attribute modifier": {
                "dexterity": 2,
                "strength": -1
                },
            "size": 1,
            "inherent affects": (
                "mute",
                "fly"
                )
            },
            
        "gargoyle": {
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "detect invisible",
                "infravision",
                "fly"
                ),
            "size": 3,
            "attribute modifier": {
                "strength": 2,
                "dexterity": 2,
                "constitution": 3
                },
            "damage message": "claw"
            },
            
        "ghoul": {
            "can wield": True,
            "inherent affects": (
                "infravision",
                ),
            "size": 3,
            "attribute modifier": {
                "strength": 1,
                "intelligence": -2,
                "wisdom": -2,
                "constitution": 1
                },
            "damage message": "claw"
            },
                    
        "golem": {
            "attribute modifier": {
                "constitution": 4,
                "wisdom": -4,
                "intelligence": -4,
                "strength": 4
                },
            "size": 5,
            "can wield": True
            },
            
        "lycanthrope": {
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "detect invisible",
                "detect alignment",
                "infravision"
                ),
            "size": 3,
            "attribute modifier": {
                "strength": 2,
                "dexterity": 2,
                "constitution": 3
                },
            "damage message": "claw",
            "hate list": ("human","elf","halfelf","drow","dwarf","halfdwarf","hobbit","giant","ogre","orc","kobold","minotaur","troll","hobgoblin","vampire","goblin","faerie","gnome")
            },

        "merfolk": {
            "can wield": True,
            "inherent affects": (
                "swim",
                "waterbreath"
                ),
            "size": 3
            },
            
        "ooze": {
            "damage message": "slime",
            "size": 0,
            "inherent affects": (
                "mute",
                "pass door"
                )
            },
            
        "skeleton": {
            "can wield": True,
            "size": 3,
            "attribute modifier": {
                "intelligence": -4,
                "wisdom": -4
                },
            "damage message": "claw"
            },
        
        "zombie": {
            "damage message": "bite",
            "attribute modifier": {
                "constitution": 1,
                "dexterity": -2,
                "wisdom": -4,
                "intelligence": -4
                },
            "size": 3,
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                "detect invisible",
                "detect alignment"
                )
            },
        

        "mutant": {
            "can wield": True,
            "size": 3,
            "attribute modifier": {
                "strength": 2,
                "intelligence": -1,
                "wisdom": -1
                }
            },
            
        "robot": {
            "can wield": True,
            "inherent affects": (
                "detect hidden",
                ),
            "size": 3,
            "attribute modifier": {
                "intelligence": 3,
                "wisdom": -3
                },
            "damage message": "pound"
            },
        
        "alien": {
            "damage message": "pound",
            "size": 3,
            "can wield": True
            },
            
        "energy": {
            "inherent affects": (
                "mute"
                "detect hidden",
                "detect invisible",
                "detect alignment",
                "infravision",
                "pass door",
                "fly"
                ),
            "size": 4,
            "attribute modifier": {
                "strength": -2,
                "intelligence": 3,
                "wisdom": 3
                },
            "damage message": "zap"
            },
        
        "ghost": {
            "damage message": "touch",
            "attribute modifier": {
                "constitution": -2,
                "intelligence": 1,
                "strength": 1
                },
            "inherent affects": (
                "pass door",
                "waterwalk",
                "fly"
                )
            }
        }

    if requested_race in races:
        return races[requested_race]
    else:
        return     
    
