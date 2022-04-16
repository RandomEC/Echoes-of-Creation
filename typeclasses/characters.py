"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
import random
from evennia import DefaultCharacter
from evennia import create_script
from evennia.utils import search
from world import rules_race, rules, rules_combat
from evennia import TICKER_HANDLER as tickerhandler

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

        # set hitpoints dictionary
        self.db.hitpoints = {
            "maximum":20,
            "damaged":0,
            "trains spent":0
            }

        # set mana dictionary
        self.db.mana = {
            "maximum": 100,
            "spent": 0,
            "trains spent": 0
            }

        # set moves dictionary
        self.db.moves = {
            "maximum":100,
            "spent":0,
            "trains spent":0
            }

        # set persistent attributes
        self.db.attributes = {
            "strength": 13,
            "intelligence": 13,
            "wisdom": 13,
            "dexterity": 13,
            "constitution": 13,
            "hitroll": 0,
            "damroll": 0,
            "armor class": 100,
            "saving throw": 0
            }
        self.db.level = 1

        # set other stats
        self.db.sex = ""
        self.db.alignment = 0
        self.db.position = "standing"

        # set race-based stats
        self.db.race = "default"

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
        
        # Modification for equipment.
        for wear_location in self.db.eq_slots:
            equipment = self.db.eq_slots[wear_location]
            if equipment:
                modifier = modifier + equipment.db.stat_modifiers["hitpoints"]
        return modifier + self.db.hitpoints["maximum"]
    
        # Modification for affects, to be determined.

    @hitpoints_maximum.setter
    def hitpoints_maximum(self, new_value):
        if "player" in self.tags.all():
            if new_value >= (self.hitpoints_maximum + 3) and new_value <= (self.hitpoints_maximum + 27):
                self.db.hitpoints["maximum"] = new_value
            else:
                self.msg("There was a problem setting your new hitpoints, as %s is outside the expected range." % (new_value - self.hitpoints_maximum))
        else:
            self.db.hitpoints["maximum"] = new_value

    @property
    def hitpoints_damaged(self):
        return self.db.hitpoints["damaged"]
    
    @hitpoints_damaged.setter
    def hitpoints_damaged(self, new_value):
        if new_value >= 0:
            self.db.hitpoints["damaged"] = new_value
        else:
            self.msg("There was a problem setting your new damage, as having negative damage is impossible.")

    @property
    def hitpoints_trains_spent(self):
        return self.db.hitpoints["trains spent"]
    
    @hitpoints_trains_spent.setter
    def hitpoints_trains_spent(self, new_value):
        if new_value > self.hitpoints_trains_spent + 1 or new_value < self.hitpoints_trains_spent + 1:
            self.msg("There was a problem setting your new trains spent on hitpoints. This should increment one at a time.")
        else:
            self.db.hitpoints["trains spent"] = new_value

            
    @property
    def mana_maximum(self):
        modifier = 0
        
        # Modification for equipment.
        for wear_location in self.db.eq_slots:
            equipment = self.db.eq_slots[wear_location]
            if equipment:
                modifier = modifier + equipment.db.stat_modifiers["mana"]
        return modifier + self.db.mana["maximum"]
    
        # Modification for affects, to be determined.

    @mana_maximum.setter
    def mana_maximum(self, new_value):
        if "player" in self.tags.all():
            if new_value >= (self.mana_maximum + 7) and new_value <= (self.mana_maximum + 29):
                self.db.mana["maximum"] = new_value
            else:
                self.msg("There was a problem setting your new mana, as %s is outside the expected range." % (new_value - self.hitpoints_maximum))
        else:
            self.db.mana["maximum"] = new_value

    @property
    def mana_spent(self):
        return self.db.mana["spent"]

    @mana_spent.setter
    def mana_spent(self, new_value):
        if new_value >= 0:
            self.db.mana["spent"] = new_value
        else:
            self.msg("There was a problem setting your new spent mana, as having negative spent mana is impossible.")
            
    @property
    def mana_trains_spent(self):
        return self.db.mana["trains spent"]
    
    @mana_trains_spent.setter
    def mana_trains_spent(self, new_value):
        if new_value > self.mana_trains_spent + 1 or new_value < self.mana_trains_spent + 1:
            self.msg("There was a problem setting your new trains spent on mana. This should increment one at a time.")
        else:
            self.db.mana["trains spent"] = new_value
            
    @property
    def moves_maximum(self):
        modifier = 0
       
        for wear_location in self.db.eq_slots:
            equipment = self.db.eq_slots[wear_location]
            if equipment:
                modifier = modifier + equipment.db.stat_modifiers["move"]
        return modifier + self.db.moves["maximum"]

    @moves_maximum.setter
    def moves_maximum(self, new_value):
        if "player" in self.tags.all():
            if new_value >= (self.moves_maximum + 5) and new_value <= (self.moves_maximum + 13):
                self.db.moves["maximum"] = new_value
            else:
                self.msg("There was a problem setting your new moves, as %s is outside the expected range." % (new_value - self.hitpoints_maximum))
        else:
            self.db.moves["maximum"] = new_value
 
    @property
    def moves_spent(self):
        return self.db.moves["spent"]
    
    @moves_spent.setter
    def moves_spent(self, new_value):
        if new_value >= 0:
            self.db.moves["spent"] = new_value
        else:
            self.msg("There was a problem setting your new spent moves, as having negative spent moves is impossible.")
            
    @property
    def moves_trains_spent(self):
        return self.db.moves["trains spent"]
    
    @moves_trains_spent.setter
    def moves_trains_spent(self, new_value):
        if new_value > self.moves_trains_spent + 1 or new_value < self.moves_trains_spent + 1:
            self.msg("There was a problem setting your new trains spent on moves. This should increment one at a time.")
        else:
            self.db.moves["trains spent"] = new_value
            
    @property
    def hitpoints_current(self):
        return self.hitpoints_maximum - self.hitpoints_damaged
    
    @property
    def mana_current(self):
        return self.mana_maximum - self.mana_spent
    
    @property
    def moves_current(self):
        return self.moves_maximum - self.moves_spent

    @property
    def level(self):
        return self.db.level

    @level.setter
    def level(self, new_value):
        self.db.level = new_value

    @property
    def spell_affects(self):
        return self.db.spell_affects
    
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

        # Get modifiers from spell_affects first.
        if self.db.spell_affects:
            for affect in self.db.spell_affects:
                for key in self.db.spell_affects[affect]:
                    if key == attribute_name:
                       modifier += self.db.spell_affects[affect][key]

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
                    if wear_location != "wielded, primary" and wear_location != "wielded, secondary":
                        modifier = modifier - (equipment.db.armor*multiplier)

        if attribute_name == "armor class":

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
                level_bonus = int((self.db.level - 1) * (-500) / 100)
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

            total_attribute = self.get_base_attribute(attribute_name) + modifier

            if attribute_name == "strength" and total_attribute > 22:
                if "warrior" in rules.classes_current(self) or "paladin" in rules.classes_current(self):
                    if total_attribute > 25:
                        total_attribute = 25
                else:
                    total_attribute = 22
            elif attribute_name == "dexterity" and total_attribute > 22:
                if "thief" in rules.classes_current(self) or "bard" in rules.classes_current(self):
                    if total_attribute > 25:
                        total_attribute = 25
                else:
                    total_attribute = 22
            elif attribute_name == "intelligence" and total_attribute > 22:
                if "mage" in rules.classes_current(self):
                    if total_attribute > 25:
                        total_attribute = 25
                else:
                    total_attribute = 22
            elif attribute_name == "wisdom" and total_attribute > 22:
                if "druid" in rules.classes_current(self) or "cleric" in rules.classes_current(self) or "psionist" in rules.classes_current(self):
                    if total_attribute > 25:
                        total_attribute = 25
                else:
                    total_attribute = 22
            elif attribute_name == "constitution" and total_attribute > 22:
                if "ranger" in rules.classes_current(self):
                    if total_attribute > 25:
                        total_attribute = 25
                else:
                    total_attribute = 22

            return total_attribute
            
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
    def saving_throw(self):
        return self.get_modified_attribute("saving throw")
    
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

    @race.setter
    def race(self, race):
        self.db.race = race

    @property
    def sex(self):
        return self.db.sex

    @sex.setter
    def sex(self, sex):
        self.db.sex = sex

    @property
    def items(self):
        item_count = 0

        for object in self.contents:
            if not object.db.equipped:
                item_count += 1

        return item_count

    @property
    def weight_carried(self):
        return rules.weight_contents(self)

    @property
    def alignment(self):
        return self.db.alignment
    
    @alignment.setter
    def alignment(self, new_value):
        if new_value > 1000 or new_value < -1000:
            self.msg("There was a problem setting your new alignment. Value should be between 1000 and -1000.\n")
            if new_value > 1000:
                self.db.alignment = 1000
                self.msg("Alignment was set to 1000 instead of exceeding it.")
            elif new_value < -1000:
                self.db.alignment = -1000
                self.msg("Alignment was set to -1000 instead of lower than that.")
        else:
            self.db.alignment = new_value

    @property
    def position(self):
        if self.db.spell_affects:
            for affect in self.db.spell_affects:
                if "position" in self.db.spell_affects[affect]:
                    return self.db.spell_affects[affect]["position"]
        else:
            return self.db.position
    
    @position.setter
    def position(self, new_value):
        spell_position_affect = ""
        if self.db.spell_affects:
            for affect in self.db.spell_affects:
                if "position" in self.db.spell_affects[affect]:
                    spell_position_affect = affect

        if new_value != "standing" and new_value != "sleeping" and new_value != "resting" and new_value != "sitting":
            self.msg("There was a problem setting your new position, as %s is not a valid value." % new_value)
        elif spell_position_affect:
            del self.db.spell_affects[spell_position_affect]
            if self.ndb.affects_return[spell_position_affect]:
                del self.ndb.affects_return[spell_position_affect]
            self.db.position = new_value
        else:
            self.db.position = new_value


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
            self.db.level, self.db.age, self.db.wimpy, self.items,\
            self.weight_carried, self.db.damage_maximum_mobile, self.db.kill_experience_maximum_mobile

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

    def at_update(self):
        """
        This function updates all that needs updating about the
        character.
        """

        healing = 0
        if self.db.hitpoints["damaged"] > 0:
            hp_gain = rules.gain_hitpoints(self)
            self.db.hitpoints["damaged"] -= hp_gain
        else:
            healing += 1

        if self.db.mana["spent"] > 0:
            mana_gain = rules.gain_mana(self)
            self.db.mana["spent"] -= mana_gain
        else:
            healing += 1

        if self.db.moves["spent"] > 0:
            moves_gain = rules.gain_moves(self)
            self.db.moves["spent"] -= moves_gain
        else:
            healing += 1

        if healing == 3:
            tickerhandler.remove(30, self.at_update, self.db.heal_ticker)
            self.db.heal_ticker = None

        if "mobile" in self.tags.all():
            if self.db.experience_current != self.db.experience_total:
                experience_gain = rules.gain_experience(self, hp_gain)
                gain_left = self.db.experience_total - self.db.experience_current

                if experience_gain > gain_left:
                    self.db.experience_current += gain_left
                else:
                    self.db.experience_current += experience_gain

            # Check to see if the mobile is going to move.
            tag = self.location.tags.all(return_key_and_category=True)
            total_tags = len(tag)

            for index in range(0, total_tags):
                if tag[index][1] == "area name":
                    area = tag[index][0]

            if rules.player_in_area(area):

                if (self.hitpoints_current < (self.hitpoints_maximum * 0.5) and random.randint(1, 8) < 7) or (random.randint(1, 32) < 7):

                    if "sentinel" not in self.db.act_flags and not self.nattributes.hasattr("combat_handler"):
                        door = random.randint(1, 6)
                        if door == 1:
                            door = "north"
                        elif door == 2:
                            door = "east"
                        elif door == 3:
                            door = "south"
                        elif door == 4:
                            door = "west"
                        elif door == 5:
                            door = "up"
                        else:
                            door = "down"

                        for exit in self.location.exits:
                            if exit.key == door and "open" in exit.db.door_attributes:
                                destination = exit.destination

                                if "no mob" not in destination.db.room_flags:
                                    if ("solitary" not in destination.db.room_flags and "private" not in destination.db.room_flags) or self.home == destination:
                                        for tag in self.location.tags.all():

                                            if tag in destination.tags.all():
                                                self.move_to(destination)

    def at_before_move(self, destination):
        """
        This hook is called just before trying to move. Anything that would
        prevent you from moving is dealt with here.
        """
    
        if self.db.position == "fighting":
            self.msg("You can only move from a fight by successfully fleeing!")
            return False
        elif self.db.position == "sleeping":
            self.msg("What, in your dreams? You are sleeping!")
            return False
        elif self.db.position == "sitting" or self.db.position == "resting":
            self.msg("Perhaps you should try standing first, before moving.")
            return False
        
        # Add movement cost function here, after check for all the reasons why you couldn't move.
        
        return True

    def at_after_say(self, speaker, message):
        """
        This is a hook for starting mobile scripts that trigger on
        say.
        """

        if self.db.scripts:
            if message in self.db.say_scripts:
                create_script(self.db.say_scripts[message], key=message, obj=speaker)
                speaker.scripts.delete(message)


    def at_give(self, player, given_object):
        """
        Hook called on a mobile after it is given an object.
        """

        if "mobile" in self.tags.all():
            if self.db.quests:
                if not player.db.quests:
                    player.db.quests = {}

                for quest in self.db.quests:
                    if quest not in player.db.quests:
                        if "give" in self.db.quests[quest]:
                            quest_script = create_script(self.db.quests[quest]["give"], obj=self)
                            quest_script.db.player = player
                            quest_script.db.given_object = given_object
                            quest_script.quest_give()
                    elif player.db.quests[quest] != "done":
                        if "give" in self.db.quests[quest]:
                            quest_script = create_script(self.db.quests[quest]["give"], obj=self)
                            quest_script.db.player = player
                            quest_script.db.given_object = given_object
                            quest_script.quest_give()
        else:
            pass


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

        # If the mobile is involved in a quest, the dictionary for that quest
        # takes the following form:
        # "questname": {"trigger type 1": "script 1", "trigger type 2": "script 2", ...}

        self.db.quests = {}

    def at_reset(self):

        # Check to see if mobile is dead, and at "none".
        if self.location == None:

            self.move_to(self.home, quiet=True)

            # Reset spell affects on the mobile.
            self.db.spell_affects = self.db.spell_affects_reset

            # Heal it up.
            self.db.hitpoints["damaged"] = 0

            # Fuzz up the mobile's level.
            self.db.level = rules.fuzz_number(self.db.level_base)
            if self.db.level < 1:
                self.db.level = 1
            level = self.db.level
            
            # Set hitpoint maximum based on level.
            self.hitpoints_maximum = level*8 + random.randint(
                                                     int(level/4),
                                                     (level*level)
                                                     )

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
                            new_object.aliases = object_to_copy.aliases
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
                            if new_object.db.item_type == "weapon":
                                new_object.wield_to(self)
                            else:
                                new_object.wear_to(self)
                                

            self.db.experience_total = rules.calculate_experience(self)
            self.db.experience_current = self.db.experience_total

            self.db.gold = rules.calculate_gold(self)

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

    def at_player_entered(self, character):
        """
        Hook used to implement various actions on a player entering the room.
        """
        if "aggressive" in self.db.act_flags and character.level < 103 and rules.is_visible(character, self):
            if not character.ndb.combat_handler and not self.ndb.combat_handler:
                character.msg("%s jumps forward and ATTACKS you!" % (self.key[0].upper() + self.key[1:]))
                rules_combat.create_combat(self, character)
            if not self.ndb.combat_handler:
                combat = character.ndb.combat_handler
                combat.add_combatant(self, character)
        if "talk on enter" in self.tags.all():
            character.msg('On entering the room, %s says to you, "%s"' % (self.key, self.db.talk))

    def at_death(self, player):
        """
        Hook called on a mobile after it is killed.
        """

        if self.db.quests:
            if not player.db.quests:
                player.db.quests = {}

            for quest in self.db.quests:
                if quest not in player.db.quests:
                    if "death" in self.db.quests[quest]:
                        quest_script = create_script(self.db.quests[quest]["death"], obj=self)
                        quest_script.db.player = player
                        quest_script.quest_death()
                elif player.db.quests[quest] != "done":
                    if "death" in self.db.quests[quest]:
                        quest_script = create_script(self.db.quests[quest]["death"], obj=self)
                        quest_script.db.player = player
                        quest_script.quest_death()
        else:
            pass

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
        self.db.experience_spent_practices = 0
        self.db.level = 1
        self.db.skills = {}
        self.db.practices_spent = 0
        self.db.quests = {}
        
        # set monetary stats
        self.db.gold = 0
        self.db.bank_balance = 0
            
        # set fighting counting stats
        self.db.died = 0
        self.db.kills = 0
        self.db.damage_maximum = 0
        self.db.damage_maximum_mobile = ""
        self.db.kill_experience_maximum = 0
        self.db.kill_experience_maximum_mobile = ""

        self.db.age = 18
        self.db.wimpy = 4
        self.db.character_type = "player"
        
        # All three of the below are capped at 4000.
        self.db.hunger = 4000
        self.db.thirst = 4000
        self.db.drunk = 0

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

        tickerhandler.add(30, self.at_update)

    @property
    def experience_total(self):
        return self.db.experience_total

    @experience_total.setter
    def experience_total(self, new_value):
        if new_value >= self.experience_total:
            self.db.experience_total = new_value
        else:
            self.msg("There was a problem setting your new total experience, as you can never have less total experience.")

    @property
    def experience_spent(self):
        return self.db.experience_spent

    @experience_spent.setter
    def experience_spent(self, new_value):
        if new_value >= 0:
            self.db.experience_spent = new_value
        else:
            self.msg("There was a problem setting your new spent experience, as having negative spent experience is impossible.")

    @property
    def experience_available(self):
        return self.db.experience_total - self.db.experience_spent


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

    def at_after_move(self, source_location, **kwargs):
        """
        We make sure to look around after a move.
        """
        if self.location.access(self, "view"):
            self.msg(self.at_look(self.location))
            self.location.at_player_arrive(self)
        
        # If a player is leaving an area and entering a new area, may need to
        # change areas where mobiles can move.
        start_area = rules.get_area_name(source_location)
        new_area = rules.get_area_name(self.location)
        
        if start_area != new_area:
            players = search.search_tag("player")
            
            # Get a list of all areas with players in them.
            player_areas = list(rules.get_area_name(player.location) for player in players if player.location)
            
            # Make sure that there is a mobile movement script.
            mobile_movement_script = search.search_script("mobile_movement_script")[0]
            if mobile_movement_script:
                
                # If there are no players left in the old area, clear the mobile movement list.
                if start_area not in player_areas:
                    mobile_movement_script.db.area_movement[start_area] = []
                
                # If there is no list already for the new area, make one.
                if not mobile_movement_script.db.area_movement[new_area]:
                    # Get all objects in area.
                    new_area_objects = search.search_tag(new_area)
                    # Filter for mobiles.
                    candidate_mobiles = list(object for objects in new_area_objects if "mobile" in object.tags.all())
                    # Filter for non-sentinel mobiles.
                    mobiles = list(mobile for mobile in candidate_mobiles if "sentinel" not in mobile.db.act_flags)
                    
                    mobile_movement_script.db.area_movement[new_area] = mobiles


