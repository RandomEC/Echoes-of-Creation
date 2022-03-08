from typeclasses.scripts import Script

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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
                repeat = False
            elif user_input.lower() == "no":
                caller.msg("Please say the name of the sex you choose. You may enter look to see the description again.")
                repeat = False
            else:
                caller.msg("Please answer yes or no.")
                repeat = True

            return repeat

        get_input(self.obj, "You chose neuter as the sex of your character, %s. Is that correct? yes/(no):" % self.obj.key, confirmation_check)

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
                caller.msg("You are moving on now.")
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
                caller.msg("You are moving on now.")
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
