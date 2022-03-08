"""
Scripts

Scripts are powerful jacks-of-all-trades. They have no in-game
existence and can be used to represent persistent game systems in some
circumstances. Scripts can also have a time component that allows them
to "fire" regularly or a limited number of times.

There is generally no "tree" of Scripts inheriting from each other.
Rather, each script tends to inherit from the base Script class and
just overloads its hooks to have it perform its function.

"""

import evennia
from evennia import DefaultScript
from evennia.utils import search
from evennia.utils.evmenu import get_input
from evennia import TICKER_HANDLER as tickerhandler

class Script(DefaultScript):
    """
    A script type is customized by redefining some or all of its hook
    methods and variables.

    * available properties

     key (string) - name of object
     name (string)- same as key
     aliases (list of strings) - aliases to the object. Will be saved
              to database as AliasDB entries but returned as strings.
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation
     permissions (list of strings) - list of permission strings

     desc (string)      - optional description of script, shown in listings
     obj (Object)       - optional object that this script is connected to
                          and acts on (set automatically by obj.scripts.add())
     interval (int)     - how often script should run, in seconds. <0 turns
                          off ticker
     start_delay (bool) - if the script should start repeating right away or
                          wait self.interval seconds
     repeats (int)      - how many times the script should repeat before
                          stopping. 0 means infinite repeats
     persistent (bool)  - if script should survive a server shutdown or not
     is_active (bool)   - if script is currently running

    * Handlers

     locks - lock-handler: use locks.add() to add new lock strings
     db - attribute-handler: store/retrieve database attributes on this
                        self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not
                        create a database entry when storing data

    * Helper methods

     start() - start script (this usually happens automatically at creation
               and obj.script.add() etc)
     stop()  - stop script, and delete it
     pause() - put the script on hold, until unpause() is called. If script
               is persistent, the pause state will survive a shutdown.
     unpause() - restart a previously paused script. The script will continue
                 from the paused timer (but at_start() will be called).
     time_until_next_repeat() - if a timed script (interval>0), returns time
                 until next tick

    * Hook methods (should also include self as the first argument):

     at_script_creation() - called only once, when an object of this
                            class is first created.
     is_valid() - is called to check if the script is valid to be running
                  at the current time. If is_valid() returns False, the running
                  script is stopped and removed from the game. You can use this
                  to check state changes (i.e. an script tracking some combat
                  stats at regular intervals is only valid to run while there is
                  actual combat going on).
      at_start() - Called every time the script is started, which for persistent
                  scripts is at least once every server start. Note that this is
                  unaffected by self.delay_start, which only delays the first
                  call to at_repeat().
      at_repeat() - Called every self.interval seconds. It will be called
                  immediately upon launch unless self.delay_start is True, which
                  will delay the first call of this method by self.interval
                  seconds. If self.interval==0, this method will never
                  be called.
      at_stop() - Called as the script object is stopped and is about to be
                  removed from the game, e.g. because is_valid() returned False.
      at_server_reload() - Called when server reloads. Can be used to
                  save temporary variables you want should survive a reload.
      at_server_shutdown() - called at a full server shutdown.

    """

    pass


class ChooseDrowScript(DefaultScript):
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

class ChooseDwarfScript(DefaultScript):
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

class ChooseEldarScript(DefaultScript):
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

class ChooseElfScript(DefaultScript):
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

class ChooseFemaleScript(DefaultScript):
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

class ChooseGnomeScript(DefaultScript):
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

class ChooseHalfdwarfScript(DefaultScript):
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

class ChooseHalfelfScript(DefaultScript):
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

class ChooseHalfkoboldScript(DefaultScript):
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

class ChooseHobbitScript(DefaultScript):
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

class ChooseHumanScript(DefaultScript):
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

class ChooseLizardmanScript(DefaultScript):
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

class ChooseMaleScript(DefaultScript):
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

class ChooseNeuterScript(DefaultScript):
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

class ChooseOgreScript(DefaultScript):
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

class ChooseOrcScript(DefaultScript):
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

class RaceTableScript(DefaultScript):
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

class ResetScript(DefaultScript):

    def at_script_creation(self):
        self.key = "reset_script"
        self.interval = 300   # 5 minute repeat, make a global
        self.desc = "Handles resets for Echoes of Creation"
        self.persistent = True

        # The below is a list of areas in the MUD, paired with how many cycles
        # have gone by since resetting.

        # Maybe make a command to add an area to this list.

        self.db.area_list = {
            "smurf village": 0,
            "graveyard": 0,
            "haon dor": 0,
            "dwarven daycare": 0,
            "training tower": 0,
            "the circus": 0,
            "the library": 0,
            "edens grove": 0,
            "crystalmir lake": 0,
            "the rats' lair": 0
        }


    def check_for_player(self, area_name):
        """
        This function checks to see if there are players in the area in
        question.
        """

        # Get all the objects in the area
        all_area_objects = search.search_tag(area_name, category="area name")
        # Iterate through all objects to see if there are any players in rooms
        # in the area
        for object in all_area_objects:
            contents = object.contents
            for item in contents:
                # If there is a player, return true.
                if item.account:
                    return True
        return False

    def at_repeat(self):

        for area in self.db.area_list:
            # Reset if there are no players in the area, or if counter is at 2.
            if not self.check_for_player(area) or self.db.area_list[area] == 2:
                objects_to_reset = search.search_tag(area, category = "area name")
                if objects_to_reset:
                    for object in objects_to_reset:
                        object.at_reset()
                # Since you reset, reset the timer on the area.
                self.db.area_list[area] = 0
            else:
                # Iterate up the timer toward the max of two.
                self.db.area_list[area] += 1



class UpdateTimerScript(DefaultScript):

    # Start with scripts/start scripts.UpdateTimerScript

    def at_script_creation(self):
        self.key = "update_timer_script"
        self.desc = "Adds update timers for Echoes Mobiles"
        self.persistent = True

        mobiles = evennia.search_tag("mobile")

        for mobile in mobiles:
            if "training tower" in mobile.tags.all() or \
                    "dwarven daycare" in mobile.tags.all() or \
                    "smurf village" in mobile.tags.all() or \
                    "edens grove" in mobile.tags.all():
                tickerhandler.add(30, mobile.at_update)
