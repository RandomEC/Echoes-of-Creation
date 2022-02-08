"""

Races module.

This module contains data and functions relating to Races. Its public module
functions are to be used primarily during the character and mobile creation
process.

Module Functions:

    - `load_race(str)`:

        loads an instance of the named Race class

    - `apply_race(char, race, focus)`:

        have a character "become" a member of the specified race with
        the specified focus

"""

ALL_RACES = (    )

def load_race(race):

    """

    Returns an instance of the named race class.

    Args:
        race (str): case-insensitive name of race to load

    Returns:
        (Race): instance of the appropriate subclass of `Race`

    """

    race = race.lower()

    if race in ALL_RACES:
        return globals()[race]()

    # else:
        # raise RaceException("Invalid race specified.")

def apply_race(char, race, focus):
    """Causes a Character to "become" the named race.
    Args:
        char (Character): the character object becoming a member of race
        race (str, Race): the name of the race to apply, or the
        focus (str, Focus): the name of the focus the player has selected
    """
    # if objects are passed in, reload Race and Focus objects
    # by name to ensure we have un-modified versions of them
    if isinstance(race, Race):
        race = race.name

    race = load_race(race)

    # set race and related attributes on the character
    char.db.race = race.name
    char.db.size = race.size
    char.db.strength = char.db.strength + race.strength_mod
    char.db.dexterity = char.db.dexterity + race.dexterity_mod
    char.db.intelligence = char.db.intelligence + race.intelligence_mod
    char.db.wisdom = char.db.wisdom + race.wisdom_mod
    char.db.constitution = char.db.constitution + race.constitution_mod
    char.db.damage_message = race.damage_message
    char.db.hate_list = race.hate_list
    char.db.can_wield = race.can_wield
    char.db.detect_hidden = race.detect_hidden
    char.db.infravision = race.infravision
    char.db.mute = race.mute
    char.db.fly = race.fly
    char.db.detect_alignment = race.detect_alignment
    char.db.sanctuary = race.sanctuary
    char.db.protection = race.protection
    char.db.detect_invisible = race.detect_invisible
    char.db.pass_door = race.pass_door
    char.db.waterwalk = race.waterwalk
    char.db.swim = race.swim
    char.db.waterbreath = race.waterbreath

class Race(object):
    """Base class for race attributes"""
    def __init__(self):
        self.name = ""
        self.size = 2
        self.desc = ""
        self.pc_available = False
        self.can_wield = False
        self.detect_hidden = False
        self.infravision = False
        self.mute = False
        self.fly = False
        self.detect_alignment = False
        self.sanctuary = False
        self.protection = False
        self.detect_invisible = False
        self.pass_door = False
        self.waterwalk = False
        self.swim = False
        self.waterbreath = False
        self.strength_mod = 0
        self.intelligence_mod = 0
        self.wisdom_mod = 0
        self.dexterity_mod = 0
        self.constitution_mod = 0
        self.damage_message = "punch"
        self.hate_list = ()

    @property
    def desc(self):
        """Returns a formatted description of the Race.
        Note:
            The setter for this property only modifies the content
            of the first paragraph of what is returned.
        """
        desc = "|g{}|n\n".format(self.name)
        desc += fill(self._desc)
        desc += '\n\n'
        desc += fill("{} have a ".format(self.plural) +
                     "|y{}|n body type and can ".format(self.size) +
                     "select a |wfocus|n from among {}".format(
                         self._format_focus_list(self.foci)
                     ))
        if len(self.bonuses) > 0:
            desc += '\n\n'
            desc += fill("{} also gain {} of {}".format(
                        self.plural,
                        'bonuses' if len(self.bonuses) > 1 else 'a bonus',
                        _format_bonuses(self.bonuses))
                    )
        desc += '\n\n'
        return desc

class Human(Race):
    """Class representing human attributes"""
    def __init__(self):
        super(Human, self).__init__()
        self.name = "human"
        self.size = 3
        self.pc_available = True
        self.can_wield = True
        self.hate_list = ("githyanki","vampire","werewolf","mindflayer")

class Elf(Race):
    """Class representing elf attributes"""
    def __init__(self):
        super(Elf, self).__init__()
        self.name = "elf"
        self.detect_hidden = True
        self.infravision = True
        self.can_wield = True
        self.pc_available = True
        self.intelligence_mod = 1
        self.dexterity_mod = 1
        self.constitution_mod = -1
        self.hate_list = ("drow","ogre","orc","kobold","troll","hobgoblin","dragon","vampire","werewolf","goblin","halfkobold")

class Eldar(Race):
    """Class representing eldar attributes"""
    def __init__(self):
        super(Eldar, self).__init__()
        self.name = "eldar"
        self.detect_hidden = True
        self.infravision = True
        self.can_wield = True
        self.pc_available = True
        self.intelligence_mod = 1
        self.wisdom_mod = 1
        self.constitution_mod = -1
        self.hate_list = ("drow","ogre","orc","kobold","troll","hobgoblin","dragon","vampire","werewolf","goblin","halfkobold")

class Halfelf(Race):
    """Class representing halfelf attributes"""
    def __init__(self):
        super(Halfelf, self).__init__()
        self.name = "halfelf"
        self.size = 3
        self.infravision = True
        self.can_wield = True
        self.pc_available = True
        self.dexterity_mod = 1
        self.hate_list = ("drow","ogre","orc","kobold","troll","hobgoblin","dragon","vampire","werewolf","goblin")

class Drow(Race):
    """Class representing drow attributes"""
    def __init__(self):
        super(Drow, self).__init__()
        self.name = "drow"
        self.detect_hidden = True
        self.infravision = True
        self.can_wield = True
        self.pc_available = True
        self.wisdom_mod = 1
        self.dexterity_mod = 1
        self.hate_list = ("elf","halfelf","hobbit","githyanki","vampire","werewolf")

class Dwarf(Race):
    """Class representing dwarf attributes"""
    def __init__(self):
        super(Dwarf, self).__init__()
        self.name = "dwarf"
        self.detect_hidden = True
        self.infravision = True
        self.can_wield = True
        self.pc_available = True
        self.dexterity_mod = -1
        self.constitution_mod = 1
        self.hate_list = ("giant","ogre","orc","kobold","minotaur","troll","hobgoblin","dragon","vampire","werewolf","goblin","halfkobold")

class Halfdwarf(Race):
    """Class representing halfdwarf attributes"""
    def __init__(self):
        super(Halfdwarf, self).__init__()
        self.name = "halfdwarf"
        self.infravision = True
        self.can_wield = True
        self.pc_available = True
        self.constitution_mod = 1
        self.hate_list = ("giant","ogre","orc","kobold","minotaur","troll","hobgoblin","dragon","vampire","werewolf","goblin")

class Hobbit(Race):
    """Class representing hobbit attributes"""
    def __init__(self):
        super(Hobbit, self).__init__()
        self.name = "hobbit"
        self.detect_hidden = True
        self.infravision = True
        self.can_wield = True
        self.pc_available = True
        self.dexterity_mod = 1
        self.constitution_mod = -1
        self.hate_list = ("giant","ogre","orc","kobold","minotaur","troll","hobgoblin","dragon","vampire","werewolf","goblin","halfkobold")

class Giant(Race):
    """Class representing giant attributes"""
    def __init__(self):
        super(Giant, self).__init__()
        self.name = "giant"
        self.size = 6
        self.can_wield = True
        self.strength_mod = 2
        self.intelligence_mod = -1
        self.dexterity_mod = -1
        self.constitution_mod = 1
        self.damage_message = "fist"
        self.hate_list = ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome")

class Ogre(Race):
    """Class representing ogre attributes"""
    def __init__(self):
        super(Ogre, self).__init__()
        self.name = "ogre"
        self.size = 5
        self.can_wield = True
        self.pc_available = True
        self.strength_mod = 1
        self.intelligence_mod = -1
        self.dexterity_mod = -1
        self.constitution_mod = 1
        self.damage_message = "fist"
        self.hate_list = ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome")

class Orc(Race):
    """Class representing orc attributes"""
    def __init__(self):
        super(Orc, self).__init__()
        self.name = "orc"
        self.size = 4
        self.can_wield = True
        self.pc_available = True
        self.infravision = True
        self.strength_mod = 1
        self.intelligence_mod = -1
        self.constitution_mod = 1
        self.hate_list = ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome")

class Kobold(Race):
    """Class representing kobold attributes"""
    def __init__(self):
        super(Kobold, self).__init__()
        self.name = "kobold"
        self.can_wield = True
        self.infravision = True
        self.strength_mod = -1
        self.intelligence_mod = -1
        self.dexterity_mod = 1
        self.hate_list = ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome","halfkobold")

class Minotaur(Race):
    """Class representing minotaur attributes"""
    def __init__(self):
        super(Minotaur, self).__init__()
        self.name = "minotaur"
        self.size = 5
        self.can_wield = True
        self.detect_hidden = True
        self.strength_mod = 2
        self.dexterity_mod = -1
        self.constitution_mod = 1
        self.damage_message = "fist"
        self.hate_list = ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome")

class Troll(Race):
    """Class representing troll attributes"""
    def __init__(self):
        super(Troll, self).__init__()
        self.name = "troll"
        self.can_wield = True
        self.detect_hidden = True
        self.infravision = True
        self.size = 7
        self.strength_mod = 2
        self.intelligence_mod = -1
        self.constitution_mod = 1
        self.damage_message = "fist"
        self.hate_list = ("human","elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome")
        
class Hobgoblin(Race):
    """Class representing hobgoblin attributes"""
    def __init__(self):
        super(Hobgoblin, self).__init__()
        self.name = "hobgoblin"
        self.can_wield = True
        self.infravision = True
        self.size = 3
        self.strength_mod = 1
        self.wisdom_mod = -1
        self.constitution_mod = 1
        self.hate_list = ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome")

class Insect(Race):
    """Class representing insect attributes"""
    def __init__(self):
        super(Insect, self).__init__()
        self.name = "insect"
        self.mute = True
        self.size = 0
        self.constitution_mod = -1
        self.damage_message = "bite"

class Dragon(Race):
    """Class representing dragon attributes"""
    def __init__(self):
        super(Dragon, self).__init__()
        self.name = "dragon"
        self.size = 9
        self.strength_mod = 2
        self.intelligence_mod = 2
        self.wisdom_mod = 1
        self.dexterity_mod = -3
        self.constitution_mod = 2
        self.damage_message = "claw"
        self.can_wield = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.detect_alignment = True
        self.infravision = True
        self.fly = True
                
class Demon(Race):
    """Class representing demon attributes"""
    def __init__(self):
        super(Demon, self).__init__()
        self.name = "demon"
        self.can_wield = True
        self.detect_hidden = True
        self.infravision = True
        self.size = 5
        self.strength_mod = 2
        self.intelligence_mod = -2
        self.wisdom_mod = -1
        self.dexterity_mod = -1
        self.constitution_mod = 3
        self.damage_message = "claw"
        
class Animal(Race):
    """Class representing animal attributes"""
    def __init__(self):
        super(Animal, self).__init__()
        self.name = "animal"
        self.dexterity_mod = 1
        self.damage_message = "bite"
        self.hate_list = ("kobold","halfkobold")
        self.mute = True
        self.detect_hidden = True

class God(Race):
    """Class representing god attributes"""
    def __init__(self):
        super(God, self).__init__()
        self.name = "god"
        self.can_wield = True
        self.sanctuary = True
        self.protection = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.detect_alignment = True
        self.infravision = True
        self.pass_door = True
        self.waterwalk = True
        self.swim = True
        self.fly = True
        self.waterbreath = True
        self.size = 8
        self.strength_mod = 3
        self.intelligence_mod = 3
        self.wisdom_mod = 3
        self.dexterity_mod = 3
        self.constitution_mod = 3
        self.damage_message = "smite"
        
class Undead(Race):
    """Class representing undead (other than lich, zombie, vampire) attributes"""
    def __init__(self):
        super(Undead, self).__init__()
        self.name = "undead"
        self.size = 3
        self.strength_mod = 1
        self.dexterity_mod = -2
        self.constitution_mod = 1
        self.can_wield = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.detect_alignment = True
        self.infravision = True
        self.pass_door = True
        self.damage_message = "touch"
        self.hate_list = ("human","elf","halfelf","drow","dwarf","halfdwarf","hobbit","giant","ogre","orc","kobold","minotaur","troll","hobgoblin","goblin","faerie","gnome")

class Lich(Race):
    """Class representing lich attributes"""
    def __init__(self):
        super(Lich, self).__init__()
        self.name = "lich"
        self.can_wield = True
        self.detect_alignment = True
        self.infravision = True
        self.size = 3
        self.strength_mod = 1
        self.dexterity_mod = -2
        self.constitution_mod = 1
        self.damage_message = "touch"
        self.hate_list = ("human","elf","halfelf","dwarf","halfdwarf","hobbit","faerie")

class Harpy(Race):
    """Class representing harpy attributes"""
    def __init__(self):
        super(Harpy, self).__init__()
        self.name = "harpy"
        self.hate_list = ("human","elf","halfelf","dwarf","halfdwarf","hobbit","gnome")
        self.detect_invisible = True
        self.fly = True
        self.size = 3
        self.dexterity_mod = 2
        
class Bear(Race):
    """Class representing bear attributes"""
    def __init__(self):
        super(Bear, self).__init__()
        self.name = "bear"
        self.mute = True
        self.detect_hidden = True
        self.swim = True
        self.size = 3
        self.strength_mod = 1
        self.dexterity_mod = -1
        self.constitution_mod = 1
        self.damage_message = "swipe"        
        
class Sloth(Race):
    """Class representing sloth attributes"""
    def __init__(self):
        super(Sloth, self).__init__()
        self.name = "sloth"
        self.damage_message = "swipe"
        self.constitution_mod = 3
        self.dexterity_mod = -2
        self.mute = True
        self.infravision = True
        
class Githyanki(Race):
    """Class representing githyanki attributes"""
    def __init__(self):
        super(Githyanki, self).__init__()
        self.name = "githyanki"
        self.can_wield = True
        self.size = 3
        self.intelligence_mod = 1
        self.hate_list = ("Mindflayer")
        
class Elemental(Race):
    """Class representing elemental attributes"""
    def __init__(self):
        super(Elemental, self).__init__()
        self.name = "elemental"
        self.constitution_mod = 1
        self.strength_mod = 1
        self.size = 4
        
class Bat(Race):
    """Class representing bat attributes"""
    def __init__(self):
        super(Bat, self).__init__()
        self.name = "bat"
        self.mute = True
        self.infravision = True
        self.fly = True
        self.strength_mod = -1
        self.dexterity_mod = 2
        self.constitution_mod = -1
        self.damage_message = "bite"
        self.size = 1
        
class Plant(Race):
    """Class representing plant attributes"""
    def __init__(self):
        super(Plant, self).__init__()
        self.name = "plant"
        self.damage_message = "swipe"
        self.constitution_mod = 1
        self.dexterity_mod = -1
        self.mute = True
        self.swim = True
        self.size = 1
        
class Rat(Race):
    """Class representing rat attributes"""
    def __init__(self):
        super(Rat, self).__init__()
        self.name = "rat"
        self.mute = True
        self.pass_door = True
        self.size = 0
        self.strength_mod = -1
        self.dexterity_mod = 2
        self.constitution_mod = -1
        self.damage_message = "bite"
        
class Vampire(Race):
    """Class representing vampire attributes"""
    def __init__(self):
        super(Vampire, self).__init__()
        self.name = "vampire"
        self.can_wield = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.detect_alignment = True
        self.infravision = True
        self.pass_door = True
        self.fly = True
        self.size = 3
        self.strength_mod = 1
        self.intelligence_mod = 1
        self.dexterity_mod = 1
        self.constitution_mod = 2
        self.damage_message = "claw"
        self.hate_list = ("human","elf","halfelf","drow","dwarf","halfdwarf","hobbit","giant","ogre","orc","kobold","minotaur","troll","hobgoblin","werewolf","goblin","faerie","gnome")
        
class Werewolf(Race):
    """Class representing werewolf attributes"""
    def __init__(self):
        super(Werewolf, self).__init__()
        self.name = "werewolf"
        self.damage_message = "claw"
        self.constitution_mod = 3
        self.dexterity_mod = 2
        self.wisdom_mod = 1
        self.strength_mod = 2
        self.size = 3
        self.can_wield = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.detect_alignment = True
        self.infravision = True
        self.hate_list = ("human","elf","halfelf","drow","dwarf","halfdwarf","hobbit","giant","ogre","orc","kobold","minotaur","troll","hobgoblin","werewolf","goblin","faerie","gnome")

class Goblin(Race):
    """Class representing goblin attributes"""
    def __init__(self):
        super(Goblin, self).__init__()
        self.name = "goblin"
        self.can_wield = True
        self.infravision = True
        self.strength_mod = -1
        self.intelligence_mod = -1
        self.wisdom_mod = -1
        self.dexterity_mod = 1
        self.hate_list = ("elf","halfelf","dwarf","halfdwarf","hobbit","vampire","werewolf","gnome")
        
class Faerie(Race):
    """Class representing faerie attributes"""
    def __init__(self):
        super(Faerie, self).__init__()
        self.name = "faerie"
        self.can_wield = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.infravision = True
        self.fly = True
        self.size = 1
        self.strength_mod = -2
        self.intelligence_mod = 1
        self.wisdom_mod = 1
        self.dexterity_mod = 1
        self.constitution_mod = -1
        
class Pixie(Race):
    """Class representing pixie attributes"""
    def __init__(self):
        super(Pixie, self).__init__()
        self.name = "pixie"
        self.constitution_mod = -1
        self.dexterity_mod = 1
        self.wisdom_mod = 1
        self.intelligence_mod = 1
        self.strength_mod = -2
        self.size = 1
        self.can_wield = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.infravision = True
        
class Arachnid(Race):
    """Class representing arachnid attributes"""
    def __init__(self):
        super(Arachnid, self).__init__()
        self.name = "arachnid"
        self.mute = True
        self.can_wield = True
        self.dexterity_mod = 1
        self.damage_message = "bite"
        
class Mindflayer(Race):
    """Class representing attributes"""
    def __init__(self):
        super(Mindflayer, self).__init__()
        self.name = "mindflayer"
        self.hate_list = ("githyanki")
        self.dexterity_mod = -1
        self.wisdom_mod = 1
        self.intelligence_mod = 2
        self.strength_mod = 1
        self.can_wield = True
        self.infravision = True
        self.size = 3
        
class ObjectRace(Race):
    """Class representing object attributes"""
    def __init__(self):
        super(ObjectRace, self).__init__()
        self.name = "object"
        self.mute = True
        self.waterbreath = True
        self.size = 3
        self.strength_mod = 3
        self.constitution_mod = 3
        self.damage_message = "swing"
        
class Mist(Race):
    """Class representing mist attributes"""
    def __init__(self):
        super(Mist, self).__init__()
        self.name = "mist"
        self.damage_message = "gas"
        self.dexterity_mod = 3
        self.strength_mod = -1
        self.mute = True
        self.pass_door = True
        self.fly = True
        
class Snake(Race):
    """Class representing snake attributes"""
    def __init__(self):
        super(Snake, self).__init__()
        self.name = "snake"
        self.mute = True
        self.size = 1
        self.dexterity_mod = 1
        self.damage_message = "bite"
        
class Worm(Race):
    """Class representing worm attributes"""
    def __init__(self):
        super(Worm, self).__init__()
        self.name = "worm"
        self.damage_message = "slime"
        self.size = 0
        self.mute = True
        self.pass_door = True
        
class Fish(Race):
    """Class representing fish attributes"""
    def __init__(self):
        super(Fish, self).__init__()
        self.name = "fish"
        self.mute = True
        self.swim = True
        self.waterbreath = True
        self.size = 1
        self.dexterity_mod = 2
        self.damage_message = "bite"
        
class Hydra(Race):
    """Class representing hydra attributes"""
    def __init__(self):
        super(Hydra, self).__init__()
        self.name = "hydra"
        self.damage_message = "bite"
        self.constitution_mod = 2
        self.dexterity_mod = -1
        self.strength_mod = 2
        self.size_mod = 8
        self.mute = True
        self.detect_hidden = True
        
class Lizard(Race):
    """Class representing lizard attributes"""
    def __init__(self):
        super(Lizard, self).__init__()
        self.name = "lizard"
        self.mute = True
        self.size = 1
        self.strength_mod = -1
        self.dexterity_mod = 1
        self.damage_message = "lash"
        
class Lizardman(Race):
    """Class representing lizardman attributes"""
    def __init__(self):
        super(Lizardman, self).__init__()
        self.name = "lizardman"
        self.damage_message = "lash"
        self.constitution_mod = 1
        self.dexterity_mod = 1
        self.wisdom_mod = -1
        self.intelligence_mod = -1
        self.strength_mod = 1
        self.size = 3
        self.can_wield = True
        self.pc_available = True
        
class Gnome(Race):
    """Class representing gnome attributes"""
    def __init__(self):
        super(Gnome, self).__init__()
        self.name = "gnome"
        self.can_wield = True
        self.pc_available = True
        self.infravision = True
        self.strength_mod = -1
        self.wisdom_mod = 1
        self.dexterity_mod = 1
        self.constitution_mod = -1
        self.hate_list = ("drow","ogre","orc","kobold","troll","hobgoblin","dragon","vampire","werewolf","goblin")
        
class Halfkobold(Race):
    """Class representing halfkobold attributes"""
    def __init__(self):
        super(Halfkobold, self).__init__()
        self.name = "halfkobold"
        self.strength_mod = -2
        self.intelligence_mod = -1
        self.wisdom_mod = -2
        self.dexterity_mod = 3
        self.constitution_mod = -2
        self.can_wield = True
        self.infravision = True
        self.pc_available = True
        self.hate_list = ("ogre","orc","giant","troll","hobgoblin")
        
class Troglodyte(Race):
    """Class representing troglodyte attributes"""
    def __init__(self):
        super(Troglodyte, self).__init__()
        self.name = "troglodyte"
        self.can_wield = True
        self.infravision = True
        self.size = 3
        self.strength_mod = 1
        self.dexterity_mod = -2
        self.constitution_mod = 1
        self.damage_message = "claw"
        self.hate_list = ("dwarf","elf","gnome","halfelf","hobbit","human")
        
class Tabaxi(Race):
    """Class representing tabaxi attributes"""
    def __init__(self):
        super(Tabaxi, self).__init__()
        self.name = "tabaxi"
        self.size = 4
        self.dexterity_mod = 1
        self.damage_message = "claw"
        self.can_wield = True
        self.detect_hidden = True
        self.infravision = True
        
class Rakshasa(Race):
    """Class representing rakshasa attributes"""
    def __init__(self):
        super(Rakshasa, self).__init__()
        self.name = "rakshasa"
        self.can_wield = True
        self.protection = True
        self.size = 3
        self.intelligence_mod = 1
        self.wisdom_mod = 1
        self.constitution_mod = -1
        self.hate_list = ("human","elf","halfelf")
        
class Kenku(Race):
    """Class representing kenku attributes"""
    def __init__(self):
        super(Kenku, self).__init__()
        self.name = "kenku"
        self.size = 3
        self.can_wield = True
        self.fly = True
        
class Halfdemon(Race):
    """Class representing halfdemon attributes"""
    def __init__(self):
        super(Halfdemon, self).__init__()
        self.name = "halfdemon"
        self.can_wield = True
        self.infravision = True
        self.strength_mod = 2
        self.dexterity_mod = -1
        self.constitution_mod = -1
        
class Grugach(Race):
    """Class representing grugach attributes"""
    def __init__(self):
        super(Grugach, self).__init__()
        self.name = "grugach"
        self.hate_list = ("halfelf","human","drow","dwarf","orc","gnome","hobbit")
        self.strength_mod = 2
        self.dexterity_mod = 1
        self.constitution_mod = -1
        self.can_wield = True
        self.detect_hidden = True
        self.infravision = True
        
class Ape(Race):
    """Class representing ape attributes"""
    def __init__(self):
        super(Ape, self).__init__()
        self.name = "ape"
        self.mute = True
        self.size = 4
        self.strength_mod = 4
        self.intelligence_mod = -4
        self.wisdom_mod = -4
        self.constitution_mod = 4
        
class Feline(Race):
    """Class representing feline (e.g. housecat) attributes"""
    def __init__(self):
        super(Feline, self).__init__()
        self.name = "feline"
        self.damage_message = "claw"
        self.dexterity_mod = 3
        self.size = 1
        self.mute = True
        self.infravision = True
        self.hate_list = ("dog")
        
class BigCat(Race):
    """Class representing big cat (e.g. tiger) attributes"""
    def __init__(self):
        super(BigCat, self).__init__()
        self.name = "big cat"
        self.mute = True
        self.infravision = True
        self.size = 5
        self.strength_mod = 3
        self.dexterity_mod = 3
        self.damage_message = "claw"
        
class Cyclops(Race):
    """Class representing cyclops attributes"""
    def __init__(self):
        super(Cyclops, self).__init__()
        self.name = "cyclops"
        self.constitution_mod = 2
        self.dexterity_mod = -2
        self.strength_mod = 2
        self.size = 4
        self.can_wield = True
        
class Dinosaur(Race):
    """Class representing dinosaur attributes"""
    def __init__(self):
        super(Dinosaur, self).__init__()
        self.name = "dinosaur"
        self.mute = True
        self.size = 10
        self.strength_mod = 7
        self.dexterity_mod = -7
        self.damage_message = "bite"
        
class Horse(Race):
    """Class representing horse attributes"""
    def __init__(self):
        super(Horse, self).__init__()
        self.name = "horse"
        self.damage_message = "pound"
        self.strength_mod = 4
        self.size = 6
        self.mute = True
        
class Centaur(Race):
    """Class representing centaur attributes"""
    def __init__(self):
        super(Centaur, self).__init__()
        self.name = "centaur"
        self.can_wield = True
        self.size = 6
        self.strength_mod = 3
        self.dexterity_mod = -2
        self.damage_message = "pound"
        
class ThriKreen(Race):
    """Class representing thri-kreen attributes"""
    def __init__(self):
        super(ThriKreen, self).__init__()
        self.name = "thri-kreen"
        self.damage_message = "bite"
        self.dexterity_mod = 2
        self.strength_mod = 2
        self.size = 3
        self.can_wield = True
        
class Pudding(Race):
    """Class representing pudding attributes"""
    def __init__(self):
        super(Pudding, self).__init__()
        self.name = "pudding"
        self.mute = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.pass_door = True
        self.size = 3
        self.damage_message = "slime"
        
class Chimera(Race):
    """Class representing chimera attributes"""
    def __init__(self):
        super(Chimera, self).__init__()
        self.name = "chimera"
        self.damage_message = "claw"
        self.size = 4
        self.protection = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.swim = True
        self.fly = True
        
class Dog(Race):
    """Class representing dog attributes"""
    def __init__(self):
        super(Dog, self).__init__()
        self.name = "dog"
        self.mute = True
        self.detect_hidden = True
        self.size = 3
        self.damage_message = "bite"
        self.hate_list = ("feline")

class Elephant(Race):
    """Class representing elephant attributes"""
    def __init__(self):
        super(Elephant, self).__init__()
        self.name = "elephant"
        self.damage_message = "pound"
        self.dexterity_mod = -3
        self.strength_mod = 3
        self.size = 7
        self.mute = True
        
class Ettin(Race):
    """Class representing ettin attributes"""
    def __init__(self):
        super(Ettin, self).__init__()
        self.name = "ettin"
        self.can_wield = True
        self.size = 7
        self.strength_mod = 3
        self.dexterity_mod = -2
        self.constitution_mod = 1
        self.hate_list = ("human","elf","halfelf","dwarf","gnome","hobbit")
        
class Amphibian(Race):
    """Class representing amphibian attributes"""
    def __init__(self):
        super(Amphibian, self).__init__()
        self.name = "amphibian"
        self.damage_message = "bite"
        self.size = 1
        self.mute = True
        self.swim = True
        self.waterbreath = True
        
class Gnoll(Race):
    """Class representing gnoll attributes"""
    def __init__(self):
        super(Gnoll, self).__init__()
        self.name = "gnoll"
        self.can_wield = True
        self.infravision = True
        self.size = 4
        self.strength_mod = 2
        self.dexterity_mod = -2
        self.hate_list = ("elf","hobbit","dwarf","human","halfelf")
        
class Automaton(Race):
    """Class representing automaton attributes"""
    def __init__(self):
        super(Automaton, self).__init__()
        self.name = "automaton"
        self.dexterity_mod = -4
        self.constitution_mod = 2
        self.strength_mod = 2
        self.size = 4
        self.mute = True
        
class Griffon(Race):
    """Class representing griffon attributes"""
    def __init__(self):
        super(Griffon, self).__init__()
        self.name = "griffon"
        self.mute = True
        self.fly = True
        self.size = 5
        self.damage_message = "bite"
        self.hate_list = ("horse")
        
class Imp(Race):
    """Class representing imp attributes"""
    def __init__(self):
        super(Imp, self).__init__()
        self.name = "imp"
        self.hate_list = ("elf","halfelf")
        self.damage_message = "bite"
        self.constitution_mod = -3
        self.dexterity_mod = 3
        self.strength_mod = -3
        self.size = 1
        self.infravision = True
        
class Leprechaun(Race):
    """Class representing leprechaun attributes"""
    def __init__(self):
        super(Leprechaun, self).__init__()
        self.name = "leprechaun"
        self.can_wield = True
        self.detect_invisible = True
        self.size = 1
        self.strength_mod = -3
        self.intelligence_mod = 1
        self.dexterity_mod = 3
        
class Medusa(Race):
    """Class representing medusa attributes"""
    def __init__(self):
        super(Medusa, self).__init__()
        self.name = "medusa"
        self.hate_list = ("human", "elf","halfelf","gnome","hobbit","dwarf")
        self.dexterity_mod = -1
        self.wisdom_mod = 1
        self.size = 3
        self.can_wield = True
        self.detect_hidden = True
        self.detect_invisible = True
        
class Monster(Race):
    """Class representing monster attributes"""
    def __init__(self):
        super(Monster, self).__init__()
        self.name = "monster"
        self.detect_hidden = True
        self.detect_invisible = True
        self.swim = True
        self.fly = True
        self.size = 10
        self.strength_mod = 7
        self.dexterity_mod = 7
        self.constitution_mod = 7
        self.damage_mod = "bite"

class Pegasus(Race):
    """Class representing pegasus attributes"""
    def __init__(self):
        super(Pegasus, self).__init__()
        self.name = "pegasus"
        self.damage_message = "pound"
        self.strength_mod = 4
        self.size = 6
        self.mute = True
        self.fly = True
        
class Unicorn(Race):
    """Class representing unicorn attributes"""
    def __init__(self):
        super(Unicorn, self).__init__()
        self.name = "unicorn"
        self.mute = True
        self.size = 6
        self.strength_mod = 4
        self.damage_message = "pierce"
        self.hate_list = ("drow","demon","halfdemon","monster")
        
class Ru(Race):
    """Class representing ru attributes"""
    def __init__(self):
        super(Ru, self).__init__()
        self.name = "ru"
        self.mute = True
        self.size = 3
        self.damage_message = "grep"
        
class Parasite(Race):
    """Class representing parasite attributes"""
    def __init__(self):
        super(Parasite, self).__init__()
        self.name = "parasite"
        self.damage_message = "bite"
        self.dexterity_mod = 10
        self.strength_mod = -10
        self.mute = True
        self.pass_door = True
        self.swim = True
        self.fly = True
        self.waterbreath = True
        self.size = 0
        
class Satyr(Race):
    """Class representing satyr attributes"""
    def __init__(self):
        super(Satyr, self).__init__()
        self.name = "satyr"
        self.can_wield = True
        self.protection = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.infravision = True
        self.size = 3
        self.dexterity_mod = 2
        self.damage_message = "pound"
        
class Sphinx(Race):
    """Class representing sphinx attributes"""
    def __init__(self):
        super(Sphinx, self).__init__()
        self.name = "sphinx"
        self.strength_mod = 2
        self.dexterity_mod = -2
        self.sanctuary = True
        self.protection = True
        self.fly = True
        self.size = 6
        
class Titan(Race):
    """Class representing titan attributes"""
    def __init__(self):
        super(Titan, self).__init__()
        self.name = "titan"
        self.can_wield = True
        self.size = 9
        self.strength_mod = 5
        self.damage_message = "pound"
        self.hate_list = ("demon","halfdemon")
        
class Treant(Race):
    """Class representing treant attributes"""
    def __init__(self):
        super(Treant, self).__init__()
        self.name = "treant"
        self.damage_message = "pound"
        self.dexterity_mod = -5
        self.strength_mod = 3
        self.size_mod = 8
        self.mute = True
        
class Wolf(Race):
    """Class representing wolf attributes"""
    def __init__(self):
        super(Wolf, self).__init__()
        self.name = "wolf"
        self.mute = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.infravision = True
        self.size = 3
        self.intelligence_mod = -2
        self.dexterity_mod = 2
        self.constitution_mod = 2
        self.damage_message = "bite"
        
class Wolverine(Race):
    """Class representing wolverine attributes"""
    def __init__(self):
        super(Wolverine, self).__init__()
        self.name = "wolverine"
        self.mute = True
        self.size = 1
        self.dexterity_mod = 3
        self.damage_message = "claw"
        
class Yeti(Race):
    """Class representing yeti attributes"""
    def __init__(self):
        super(Yeti, self).__init__()
        self.name = "yeti"
        self.damage_message = "pound"
        self.constitution_mod = 5
        self.dexterity_mod = -1
        self.wisdom_mod = -2
        self.intelligence_mod = -2
        self.strength_mod = 5
        self.size = 5
        self.mute = True
        
class Beastman(Race):
    """Class representing beastman attributes"""
    def __init__(self):
        super(Beastman, self).__init__()
        self.name = "beastman"
        self.mute = True
        self.can_wield = True
        self.detect_hidden = True
        self.size = 3
        self.strength_mod = 2
        self.intelligence_mod = -1
        self.wisdom_mod = -1
        self.constitution_mod = 2
        
class Bird(Race):
    """Class representing bird attributes"""
    def __init__(self):
        super(Bird, self).__init__()
        self.name = "bird"
        self.damage_message = "bite"
        self.dexterity_mod = 2
        self.strength_mod = -1
        self.size = 1
        self.mute = True
        self.fly = True
        
class Gargoyle(Race):
    """Class representing gargoyle attributes"""
    def __init__(self):
        super(Gargoyle, self).__init__()
        self.name = "gargoyle"
        self.can_wield = True
        self.detect_hidden = True
        self.detect_invis = True
        self.infravision = True
        self.fly = True
        self.size = 3
        self.strength_mod = 2
        self.dexterity_mod = 2
        self.constitution_mod = 3
        self.damage_message = "claw"
        
class Ghoul(Race):
    """Class representing ghoul attributes"""
    def __init__(self):
        super(Ghoul, self).__init__()
        self.name = "ghoul"
        self.can_wield = True
        self.infravision = True
        self.size = 3
        self.strength_mod = 1
        self.intelligence_mod = -2
        self.wisdom_mod = -2
        self.constitution_mod = 1
        self.damage_message = "claw"
                
class Golem(Race):
    """Class representing golem attributes"""
    def __init__(self):
        super(Golem, self).__init__()
        self.name = "golem"
        self.constitution_mod = 4
        self.wisdom_mod = -4
        self.intelligence_mod = -4
        self.strength_mod = 4
        self.size = 5
        self.can_wield = True
        
class Lycanthrope(Race):
    """Class representing lycanthrope attributes"""
    def __init__(self):
        super(Lycanthrope, self).__init__()
        self.name = "lycanthrope"
        self.can_wield = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.detect_alignment = True
        self.infravision = True
        self.size = 3
        self.strength_mod = 2
        self.dexterity_mod = 2
        self.constitution_mod = 3
        self.damage_message = "claw"
        self.hate_list = ("human","elf","halfelf","drow","dwarf","halfdwarf","hobbit","giant","ogre","orc","kobold","minotaur","troll","hobgoblin","vampire","goblin","faerie","gnome")
                
class Merfolk(Race):
    """Class representing merfolk attributes"""
    def __init__(self):
        super(Merfolk, self).__init__()
        self.name = "merfolk"
        self.can_wield = True
        self.swim = True
        self.waterbreath = True
        self.size = 3
        
class Ooze(Race):
    """Class representing ooze attributes"""
    def __init__(self):
        super(Ooze, self).__init__()
        self.name = "ooze"
        self.damage_message = "slime"
        self.size = 0
        self.mute = True
        self.pass_door = True
        
class Skeleton(Race):
    """Class representing skeleton attributes"""
    def __init__(self):
        super(Skeleton, self).__init__()
        self.name = "skeleton"
        self.can_wield = True
        self.size = 3
        self.intelligence_mod = -4
        self.wisdom_mod = -4
        self.damage_message = "claw"
        
class Zombie(Race):
    """Class representing zombie attributes"""
    def __init__(self):
        super(Zombie, self).__init__()
        self.name = "zombie"
        self.damage_message = "bite"
        self.constitution_mod = 1
        self.dexterity_mod = -2
        self.wisdom_mod = -4
        self.intelligence_mod = -4
        self.size_mod = 3
        self.can_wield = 3
        self.detect_hidden = True
        self.detect_invisible = True
        self.detect_alignment = True
        
class Mutant(Race):
    """Class representing mutant attributes"""
    def __init__(self):
        super(Mutant, self).__init__()
        self.name = "mutant"
        self.can_wield = True
        self.size = 3
        self.strength_mod = 2
        self.intellligence_mod = -1
        self.wisdom_mod = -1
        
class Robot(Race):
    """Class representing robot attributes"""
    def __init__(self):
        super(Robot, self).__init__()
        self.name = "robot"
        self.can_wield = True
        self.detect_hidden = True
        self.size = 3
        self.intelligence_mod = 3
        self.wisdom_mod = -3
        self.damage_message = "pound"
    
class Alien(Race):
    """Class representing alien attributes"""
    def __init__(self):
        super(Alien, self).__init__()
        self.name = "alien"
        self.damage_message = "pound"
        self.size = 3
        self.can_wield = True
        
class Energy(Race):
    """Class representing energy attributes"""
    def __init__(self):
        super(Energy, self).__init__()
        self.name = "energy"
        self.mute = True
        self.detect_hidden = True
        self.detect_invisible = True
        self.detect_alignment = True
        self.infravision = True
        self.pass_door = True
        self.fly = True
        self.size = 4
        self.strength_mod = -2
        self.intelligence_mod = 3
        self.wisdom_mod = 3
        self.damage_message = "zap"
        
class Ghost(Race):
    """Class representing ghost attributes"""
    def __init__(self):
        super(Ghost, self).__init__()
        self.name = "ghost"
        self.damage_message = "touch"
        self.constitution_mod = -2
        self.intelligence_mod = 1
        self.strength_mod = 1
        self.pass_door = True
        self.waterwalk = True
        self.fly = True
