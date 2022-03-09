from evennia.utils import search
from evennia.utils.evmenu import get_input
from typeclasses.scripts import Script
from world import rules

class ChooseDrowScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing drow as your player race."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "drow"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose drow as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseDwarfScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing dwarf as your player race."
        self.persistent = True
        self.type = "at_after_say"
 
        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "dwarf"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose dwarf as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseEldarScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing eldar as your player race."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "eldar"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose eldar as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseElfScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing elf as your player race."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "elf"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose elf as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseFemaleScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing female as your player sex."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.sex = "female"
                destination = caller.search("cc2")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the sex you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose female as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseGnomeScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing gnome as your player race."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "gnome"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose gnome as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseHalfdwarfScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing halfdwarf as your player race."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "halfdwarf"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose halfdwarf as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseHalfelfScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing halfelf as your player race."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "halfelf"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose halfelf as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseHalfkoboldScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing halfkobold as your player race."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "halfkobold"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose halfkobold as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseHobbitScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing hobbit as your player race."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "hobbit"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose hobbit as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseHumanScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing human as your player race."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "human"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose human as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseLizardmanScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing lizardman as your player race."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "lizardman"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose lizardman as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseMaleScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing male as your player sex."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.sex = "male"
                destination = caller.search("cc2")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the sex you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose male as the sex of your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseNeuterScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing neuter as your player sex."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.sex = "neuter"
                destination = caller.search("cc2")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the sex you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose neuter as the sex of your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseNormalScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing normal starting difficulty."
        self.persistent = True
        self.type = "at_after_say"

        def make_object(location, equipped, reset_object):
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
                new_object.home = location

            # Either way, put it where it should be.
            new_object.location = location

            # Clear any enchantment/poison/other affects.
            new_object.db.spell_affects = {}

            # Set level, other values, and/or fuzz numbers as necessary
            new_object.db.level = 1
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
            if equipped:
                if not new_object.db.equipped:
                    if new_object.db.item_type == "weapon":
                        new_object.wield_to(self)
                    else:
                        new_object.wear_to(self)


        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":








                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose normal difficulty, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseOgreScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing ogre as your player race."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "ogre"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose ogre as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class ChooseOrcScript(Script):
    def at_script_creation(self):
        self.desc = "Script for choosing orc as your player race."
        self.persistent = True
        self.type = "at_after_say"

        def confirmation_check(caller, prompt, user_input):
            """
            This is a function to confirm a choice that you made
            in the character creation process.
            """
            if user_input.lower() == "yes":
                caller.race = "orc"
                destination = caller.search("cc1")
                caller.home = destination
                caller.move_to(destination, quiet=True)
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the race you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose orc as the race for your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

class RaceTableScript(Script):
    def at_script_creation(self):
        self.desc = "Script for showing the playable race table."
        self.persistent = True
        self.type = "at_after_say"
        self.obj.msg("""=====================================================\
===========
                                     Infra- Detect
  ##  Race       Str Dex Int Wis Con vision Hidden Size Hated By
================================================================
   1  Human                            No     No     3   4 races
   2  Elf             +1  +1      -1  Yes    Yes     2  11 races
   3  Eldar               +1  +1  -1  Yes    Yes     2  11 races
   4  Halfelf         +1              Yes     No     3  10 races
   5  Drow            +1      +1      Yes    Yes     2   6 races
   6  Dwarf           -1          +1  Yes    Yes     2  12 races
   7  Halfdwarf                   +1  Yes     No     2  12 races
   8  Hobbit          +1          -1  Yes     No     2  12 races
   9  Ogre        +1  -1  -1      +1   No     No     5   8 races
  10  Orc         +1      -1      +1  Yes     No     4   8 races
  11  Lizardman   +1  +1  -1  -1  +1   No     No     3   0 races
  12  Gnome       -1  +1      +1  -1  Yes     No     2  10 races
  13  Halfkobold  -2  +3  -1  -2  -2  Yes     No     2   5 races
================================================================"""
)
