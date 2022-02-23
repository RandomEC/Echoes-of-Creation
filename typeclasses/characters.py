"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from evennia.utils import search
from world import rules_race
from world import rules

class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    def at_object_creation(self):
        """
        Called only at initial creation. These are the base stats
        that get modified further by race and the rest of it.
        """

        # set persistent attributes
        self.db.attributes = {
            "strength":13,
            "intelligence":13,
            "wisdom":13,
            "dexterity":13,
            "constitution":13,
            "hitroll":0,
            "damroll":0,
            "armor class":100,
            "saving throw":0
            }

        # set hitpoints dictionary
        self.db.hitpoints = {
            "maximum":20,
            "damaged":0,
            "trains spent":0
            }

        # set mana dictionary
        self.db.mana = {
            "maximum":100,
            "spent":0,
            "trains spent":0
            }

        # set moves dictionary
        self.db.moves = {
            "maximum":100,
            "spent":0,
            "trains spent":0
            }

        # set other stats
        self.db.sex = ""
        self.db.alignment = 0
        self.db.position = ""
        self.db.character_type = ""

        # set race-based stats
        self.db.race = ""

        # set spell_affects dictionary
        self.db.spell_affects = {}

        # create equipment slot dictionary
        self.db.eq_slots = {
            "light":"",
            "head":"",
            "neck, first":"",
            "neck, second":"",
            "body":"",
            "arms":"",
            "wrist, left":"",
            "wrist, right":"",
            "hands":"",
            "finger, left":"",
            "finger, right":"",
            "waist":"",
            "about body":"",
            "legs":"",
            "feet":"",
            "pride":"",
            "wielded, primary":"",
            "shield":"",
            "held, in hands":"",
            "wielded, secondary":""
            }

    @property
    def hitpoints_maximum(self):
        modifier = 0
        
        for wear_location in self.db.eq_slots:
            equipment = self.db.eq_slots[wear_location]
            if equipment:
                modifier = modifier + equipment.db.stat_modifiers["hitpoints"]
        return modifier + self.db.hitpoints["maximum"]

    @hitpoints_maximum.setter
    def hitpoints_maximum(self, value):
        self.db.hitpoints["maximum"] = self.db.hitpoints["maximum"] + value

    @property
    def mana_maximum(self):
        modifier = 0
        
        for wear_location in self.db.eq_slots:
            equipment = self.db.eq_slots[wear_location]
            if equipment:
                modifier = modifier + equipment.db.stat_modifiers["mana"]
        return modifier + self.db.mana["maximum"]

    @mana_maximum.setter
    def mana_maximum(self, value):
        self.db.mana["maximum"] = self.db.mana["maximum"] + value

    @property
    def moves_maximum(self):
        modifier = 0
       
        for wear_location in self.db.eq_slots:
            equipment = self.db.eq_slots[wear_location]
            if equipment:
                modifier = modifier + equipment.db.stat_modifiers["move"]
        return modifier + self.db.moves["maximum"]

    @moves_maximum.setter
    def moves_maximum(self, value):
        self.db.moves["maximum"] = self.db.moves["maximum"] + value

    @property
    def hitpoints_current(self):
        return self.hitpoints_maximum - self.db.hitpoints["damaged"]
    
    @property
    def mana_current(self):
        return self.mana_maximum - self.db.mana["spent"]
    
    @property
    def moves_current(self):
        return self.moves_maximum - self.db.moves["spent"]

    def get_affect_status(self, affect_name):
        """
        Method that returns a boolean for whether the affect is currently
        in existence on the character, checking, in preferential order,
        spell affects, inherent racial affects, and finally the default of
        False.
        """

        if affect_name in self.db.spell_affects.keys():
            return True

        # get the dictionary for the current race of the character
        race_stats = rules_race.get_race(self.race)

        if "inherent affects" in race_stats.keys():
            if affect_name in race_stats["inherent affects"]:
                return True
            else:
                return False
        else:
            return False
        

    def get_base_attribute(self, attribute_name):
        """
        Method to access a base attribute, and the modifiers that are
        considered "inherent" - race and trains.
        """

        # get the dictionary for the current race of the character
        race_stats = rules_race.get_race(self.race)

        # check to see if the race has a modifier for this stat
        if "attribute modifier" in race_stats and attribute_name in race_stats["attribute modifier"]:
            base_attribute = self.db.attributes[attribute_name] + race_stats["attribute modifier"][attribute_name]
        else:
            base_attribute = self.db.attributes[attribute_name]

        if "player" in self.tags.all():
            base_attribute += self.db.attribute_trains[attribute_name]

        return base_attribute

    def get_modified_attribute(self, attribute_name):
        """
        Method to access an attribute, access all of the modifiers of that
        attribute (trains, equipment, and affects), and return the overall
        modified value.
        """
        
        modifier = 0
        
        for wear_location in self.db.eq_slots:

            equipment = self.db.eq_slots.get(wear_location)

            if equipment:
            
                modifier = modifier + equipment.db.stat_modifiers[attribute_name]
            
                # armor class needs to be handled separately due to stats for inherent armor in items and their multiplier, in addition to the separate armor class modifier

                if attribute_name == "armor class":
                
                    if wear_location == "body":
                        multiplier = 3
                    elif wear_location == "legs" or wear_location == "head" or wear_location == "about body":
                        multiplier = 2
                    else:
                        multiplier = 1

                    # The other wear locations don't have armor, and will choke on this.
                    if self.db.item_type == "armor" or self.db.item_type == "light":
                        modifier = modifier - (equipment.db.armor*multiplier)

                    dexterity = self.dexterity

                    if dexterity < 1:
                        modifier += 60
                    elif dexterity < 2:
                        modifier += 50
                    elif dexterity < 3:
                        modifier += 40
                    elif dexterity < 4:
                        modifier += 30
                    elif dexterity < 5:
                        modifier += 20
                    elif dexterity < 6:
                        modifier += 10
                    elif dexterity < 15:
                        modifier += 0
                    elif dexterity < 16:
                        modifier += -10
                    elif dexterity < 17:
                        modifier += -15
                    elif dexterity < 18:
                        modifier += -20
                    elif dexterity < 19:
                        modifier += -30
                    elif dexterity < 20:
                        modifier += -40
                    elif dexterity < 21:
                        modifier += -50
                    elif dexterity < 22:
                        modifier += -65
                    elif dexterity < 23:
                        modifier += -75
                    elif dexterity < 24:
                        modifier += -90
                    elif dexterity < 25:
                        modifier += -105
                    elif dexterity < 26:
                        modifier += -120
                    
                    if "mobile" in self.tags.all():
                        level_bonus = int((self.db.level-1)*(-500)/100)
                        modifier += level_bonus

                if attribute_name == "hitroll":

                    strength = self.strength

                    if strength < 2:
                        modifier += -5
                    elif strength < 4:
                        modifier += -3
                    elif strength < 6:
                        modifier += -2
                    elif strength < 8:
                        modifier += -1
                    elif strength < 15:
                        modifier += 0
                    elif strength < 17:
                        modifier += 1
                    elif strength < 19:
                        modifier += 2
                    elif strength < 21:
                        modifier += 3
                    elif strength < 22:
                        modifier += 4
                    elif strength < 23:
                        modifier += 5
                    elif strength < 24:
                        modifier += 6
                    elif strength < 25:
                        modifier += 8
                    elif strength < 26:
                        modifier += 10
                    
                if attribute_name == "damroll":
                    strength = self.strength

                    if strength < 2:
                        modifier += -4
                    elif strength < 3:
                        modifier += -2
                    elif strength < 6:
                        modifier += -1
                    elif strength < 14:
                        modifier += 0
                    elif strength < 16:
                        modifier += 1
                    elif strength < 17:
                        modifier += 2
                    elif strength < 18:
                        modifier += 3
                    elif strength < 19:
                        modifier += 4
                    elif strength < 20:
                        modifier += 5
                    elif strength < 21:
                        modifier += 6
                    elif strength < 23:
                        modifier += 7
                    elif strength < 24:
                        modifier += 8
                    elif strength < 25:
                        modifier += 10
                    elif strength < 26:
                        modifier += 12
                    

        # assemble modifier with base stat, first for the "trainable" stats, which have an extra modifier for that

        if attribute_name == "strength" or attribute_name == "intelligence" or attribute_name == "wisdom" or attribute_name == "dexterity" or attribute_name == "constitution":
            return self.get_base_attribute(attribute_name) + modifier
            
        # then, with everything else
        
        else:
            return self.db.attributes[attribute_name] + modifier

    # All of the below properties are designed for ease of reference to the current
    # status of the relevant attribute, inclusive of trains (as applicable), equipment,
    # and spell affects.

    @property
    def strength(self):
        return self.get_modified_attribute("strength")

    @property
    def dexterity(self):
        self.msg("")
        return self.get_modified_attribute("dexterity")

    @property
    def intelligence(self):
        return self.get_modified_attribute("intelligence")

    @property
    def wisdom(self):
        return self.get_modified_attribute("wisdom")

    @property
    def constitution(self):
        return self.get_modified_attribute("constitution")

    @property
    def hitroll(self):
        return self.get_modified_attribute("hitroll")

    @property
    def damroll(self):
        return self.get_modified_attribute("damroll")

    @property
    def armor_class(self):
        return self.get_modified_attribute("armor class")

    @property
    def size(self):
        if "size" in rules_race.get_race(self.race).keys():
            size = rules_race.get_race(self.race)["size"]
        else:
            size = 2
        return size

    @property
    def race(self):
        """
        Method that will check to see if there is a spell affect
        changing race, and, if not, will return base race.
        """

        # once we implement spell affects, check for them here on race
        return self.db.race

    def take_damage(self, damage):
        """
        Method to use to do damage to a character.
        """
        
        self.db.hitpoints["damaged"] += damage
        
    def get_score_info(self): # add caller into score command
        """
        Simple access method to return ability scores as a tuple
        (str,dex,int,wis,con,current hp, maximum hp, current mana, maximum
        mana,current moves,maximum moves,sex,race)
        """
        return self.get_base_attribute("strength"), self.get_base_attribute("dexterity"), \
            self.get_base_attribute("intelligence"), self.get_base_attribute("wisdom"),\
            self.get_base_attribute("constitution"), self.hitpoints_current, \
            self.hitpoints_maximum, self.mana_current, \
            self.mana_maximum, self.moves_current, self.moves_maximum\
            , self.db.sex, self.race.capitalize(), self.db.died, self.db.kills, \
            self.db.damage_maximum, self.db.kill_experience_maximum, \
            self.get_modified_attribute("hitroll"), self.db.experience_total, self.db.experience_spent\
            , self.get_modified_attribute("damroll"), self.db.gold, self.db.bank_balance, \
            self.get_modified_attribute("armor class"), self.db.alignment, self.get_modified_attribute("saving throw"), \
            self.db.staff_position, self.db.immortal_invisible, \
            self.db.immortal_cloak, self.db.immortal_ghost, self.db.holy_light,\
            self.db.level, self.db.age, self.db.wimpy, self.db.items,\
            self.db.weight

    def get_equipment_table(self):
        """
        Method that cycles through worn equipment and returns a formatted table
        string.
        """

        equipment_output = ""

        for wear_location in self.db.eq_slots:
            if self.db.eq_slots[wear_location]:
                if(wear_location == "neck, first" or wear_location == "neck, second" or wear_location == "waist" or wear_location == "wrist, left" or wear_location == "wrist, right"):
                    wear_string = "worn around "
                elif(wear_location == "light"):
                    wear_string = "used as a "
                elif(wear_location == "about_body"):
                    wear_string = "worn "
                elif(wear_location == "pride"):
                    wear_string = "worn, with "
                elif(wear_location == "held "):
                    wear_string = ""
                elif(wear_location == "shield"):
                    wear_string = "held as a "
                elif(wear_location == "wielded, primary" or wear_location == "wielded, secondary"):
                    wear_string = ""
                else:
                    wear_string = "worn on "

                output_string = wear_string + wear_location + ":"
                space_buffer = 26 - len(output_string)
                output_string = output_string + " " * space_buffer + self.db.eq_slots[wear_location].key + "\n"
                equipment_output += output_string

        return equipment_output
        
class Mobile(Character):
    """
    The Mobile class is intended to be used for the npcs on the MUD, and inherits from the
    base Character class.
    """

    def at_object_creation(self):
        """
        Called only at initial creation. These are the base stats
        that get modified further by race and the rest of it.
        """
        super().at_object_creation()
        self.db.gold = 0
        self.db.level_base = 0
        self.db.look_description = ""
        self.db.experience_current = 0
        self.db.experience_total = 0
        self.db.reset_objects = {}
        self.db.special_function = []
        self.db.act_flags = []
        self.db.talk = ""
        self.db.shop = {}
        self.db.character_type = "mobile"
        self.tags.add("mobile")
        self.db.spell_affects_reset = {}

    def at_reset(self):
        
        # Check to see if mobile is dead, and at "none".
        if self.location == None:
            self.move_to(self.home, quiet = True)

            # Reset spell affects on the mobile.
            self.db.spell_affects = self.db.spell_affects_reset

            # Heal it up.
            self.db.hitpoints["damaged"] = 0

            # Fuzz up the mobile's level.
            self.db.level = rules.fuzz_number(self.db.level_base)

            # Check to see if there are objects that should be reset to it. This
            # dictionary takes the form of
            # reset_objects = {
            #     <onum>:{
            #         "location":<equipped, inventory, onum of container>
            #            }
            #                 }
            if self.db.reset_objects:

                # Iterate through the onums reset to this mobile.
                for reset_object in self.db.reset_objects:

                    reset_object = reset_object.lower()
                    new_object = ""

                    # Search the mobile's inventory for the object already existing.
                    for object in self.contents:
                        aliases = object.aliases.get()
                        if aliases:
                            if reset_object in aliases:
                                new_object = object

                    # If the object does not already exist on the mobile/in the room,
                    # continue on.
                    if not new_object:


                        # First, search for all objects of that type and pull out
                        # any that are at "None".
                        object_candidates = search.search_object(reset_object)

                        for object in object_candidates:
                            if not object.location:
                                new_object = object

                        # If it is not in "None", find the existing object in the world
                        # and copy it.
                        if not new_object:

                            object_to_copy = object_candidates[0]
                            new_object = object_to_copy.copy()
                            new_object.key = object_to_copy.key
                            new_object.alias = object_to_copy.aliases
                            if new_object.db.equipped:
                                new_object.db.equipped = False
                            new_object.home = self

                        # Either way, bring the new object to the mobile.
                        new_object.location = self

                    # Clear any enchantment/poison/other affects.
                    new_object.db.spell_affects = {}

                    # Set level, other values, and/or fuzz numbers as necessary
                    new_object.db.level = self.db.level
                    if new_object.db.item_type == "armor":
                        new_object.db.armor = rules.set_armor(new_object.db.level)
                    elif new_object.db.item_type == "weapon":
                        new_object.db.damage_low, new_object.db.damage_high = rules.set_weapon_low_high(new_object.db.level)
                    elif new_object.db.item_type == "scroll":
                        new_object.db.spell_level = rules.fuzz_number(new_object.db.spell_level_base)
                    elif new_object.db.item_type == "wand" or new_object.db.item_type == "staff":
                        new_object.db.spell_level = rules.fuzz_number(new_object.db.spell_level_base)
                        new_object.db.charges_maximum = rules.fuzz_number(new_object.db.charges_maximum_base)
                        new_object.db.charges_current = new_object.db.charges_maximum
                    elif new_object.db.item_type == "potion" or new_object.db.item_type == "pill":
                        new_object.db.spell_level = rules.fuzz_number(rules.fuzz_number(new_object.db.spell_level_base))

                    # If it should be equipped, equip it.
                    if self.db.reset_objects[reset_object]["location"] == "equipped":
                        if not new_object.db.equipped:
                            if new_object.db.item_type == "armor" or new_object.db.item_type == "light":
                                new_object.wear_to(self)
                            else:
                                new_object.wield_to(self)

            self.db.experience_total = rules.calculate_experience(self)
            self.db.experience_current = self.db.experience_total

        # If it wasn't dead, just reset spell affects.
        else:
            # Reset spell affects on the mobile.
            self.db.spell_affects = self.db.spell_affects_reset

    def return_appearance(self, looker, **kwargs):
        """
        This formats a description for mobiles. It is the hook a 'look' command
        should call.
        Args:
            looker (Object): Object doing the looking.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        """
        if not looker:
            return ""

        # get description, build string
        string = "|c%s, the %s:|n\n" % (self.get_display_name(looker), self.race)
        desc = self.db.desc
        look_desc = self.db.look_description
        if look_desc:
            string += "%s\n" % look_desc
        else:
            string += "%s\n" % desc

        if not all(value == "" for value in self.db.eq_slots.values()):

            equipment_list = self.get_equipment_table()

            string += "%s is wearing:\n%s" % ((self.key[0].upper() + self.key[1:]), equipment_list)

        return string


class Player(Character):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    def at_object_creation(self):
        """
        Called only at initial creation. These are the base stats
        that get modified further by race and the rest of it.
        """
        super().at_object_creation()

        # set training dictionary
        self.db.attribute_trains = {
            "strength":0,
            "intelligence":0,
            "wisdom":0,
            "dexterity":0,
            "constitution":0
            }

        # set experience/level stats
        self.db.experience_total = 0
        self.db.experience_spent = 0
        self.db.level = 1

        # set monetary stats
        self.db.gold = 0
        self.db.bank_balance = 0
            
        # set fighting counting stats
        self.db.died = 0
        self.db.kills = 0
        self.db.damage_maximum = 0
        self.db.kill_experience_maximum = 0

        self.db.age = 18
        self.db.wimpy = 4
        self.db.character_type = "player"

        # set item stats
        self.db.items = 2
        self.db.weight = 12

        # set immortal stats - UNUSED FOR MORTALS
        self.db.staff_position = ""
        self.db.immortal_invisible = 0
        self.db.immortal_cloak = 0
        self.db.immortal_ghost = 0
        self.db.holy_light = False
        
        self.tags.add("player")
        
    def check_key(self,key_vnum): 
        """
        Simple method to check whether character has a specific key in their
        inventory, and return True if so.
        """

        inventory = self.contents

        for item in inventory:
            if item.db.vnum == key_vnum:
                return True
        return False
        











