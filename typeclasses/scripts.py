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

import random
import evennia
from evennia import DefaultScript
from evennia.utils import search
from evennia import TICKER_HANDLER as tickerhandler
from server.conf import settings
from world import rules

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


class ResetScript(DefaultScript):

    def at_script_creation(self):
        self.key = "reset_script"
        self.interval = settings.EMPTY_AREA_RESET_TIME
        self.desc = "Handles resets for Echoes of Creation"
        self.persistent = True

        # The below is a list of areas in the MUD, paired with how many cycles
        # have gone by since resetting.

        # Maybe make a command to add an area to this list.

        # Get all the current areas.
        areas = rules.get_area_info("all")
        
        # The below creates a dictionary of all areas then in the mud, by
        # tag name, paired with a timer and an empty list of resets, to 
        # be used as below.
        self.db.area_list = dict((area, {"timer": 0, "resets": [], "repop message": areas[area]["repop message"]}) for area in areas)
        
    def at_repeat(self):

        for area in self.db.area_list:

            # Reset if there are things to reset.
            if self.db.area_list[area]["resets"]:
                
                # But only if no players in the area, or if counter is at 2.
                if not rules.player_in_area(area) or self.db.area_list[area]["timer"] >= 2:

                    for object in self.db.area_list[area]["resets"]:
                        object.at_reset()
                    self.db.area_list[area]["timer"] = 0
                    self.db.area_list[area]["resets"] = []

                    players = search.search_tag("player")
                    players_in_area = list(player for player in players if rules.get_area_name(player.location) == area)
                    if players_in_area:
                        for player in players_in_area:
                            player.msg(self.db.area_list[area]["repop message"])

                else:
                    # Iterate up the timer toward the max of two.
                    self.db.area_list[area]["timer"] += 1
            else:
                # Iterate up the timer toward the max of two.
                self.db.area_list[area]["timer"] += 1                                            

class MobileMovementScript(Script):
    """
    This is the script for handling all autonomous mobile
    movement in Echoes.
    """

    def at_script_creation(self):
        self.key = "mobile_movement_script"
        self.desc = "Handles mobile autonomous movement"
        self.interval = 5
        self.persistent = True

        # Get all the current areas.
        areas = rules.get_area_info("all")
        
        # The below creates a dictionary of all areas then in the mud, by
        # tag name, paired with an empty list to be populated with the
        # mobiles potentially eligible to move.
        self.db.area_movement = dict((area, []) for area in areas)
        
    def at_repeat(self):

        for area in self.db.area_movement:

            # Do movement if there are mobiles to move.
            if self.db.area_movement[area]:

                for mobile in self.db.area_movement[area]:
                    # More likely to move if hurt.
                    if (mobile.hitpoints_current < (mobile.hitpoints_maximum * 0.5) and random.randint(1, 8) < 7) or (random.randint(1, 32) < 7):
                        # No moving if in a fight, unless by wimpy through fight code.
                        if not mobile.nattributes.has("combat_handler"):
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

                            for exit in mobile.location.exits:
                                if exit.key == door and "open" in exit.db.door_attributes:
                                    destination = exit.destination
                                    if area in destination.tags.all():
                                        if destination.db.room_flags:
                                            if "no mob" not in destination.db.room_flags:
                                                if ("solitary" not in destination.db.room_flags and "private" not in destination.db.room_flags) or mobile.home == destination:
                                                    if area in destination.tags.all():
                                                        mobile.move_to(destination)
                                        else:
                                            mobile.move_to(destination)
   
                                            
class UpdateTimerScript(DefaultScript):

    # Start with scripts/start scripts.UpdateTimerScript

    def at_script_creation(self):
        self.key = "update_timer_script"
        self.desc = "Adds update timers for Echoes Players"
        self.persistent = True

        mobiles = evennia.search_tag("player")

        for mobile in mobiles:
            tickerhandler.add(30, mobile.at_update)

class FixAreaNames(DefaultScript):

    # Start with scripts/start scripts.FixAreaNames

    def at_script_creation(self):
        self.key = "area_name_fix_script"
        self.desc = "Corrects area name screwup"
        self.persistent = True

        self.db.area_list = {
            "#area { 5 15 } nirrad land of the fire newts": 0,
            "#area { 5 25 } sandman dragon cult": 0
        }

        for area in self.db.area_list:

            if area == "#area { 5 15 } nirrad land of the fire newts":
                area_rename = "fire newts"
            else:
                area_rename = "dragon cult"

            objects_to_retag = search.search_tag(area, category="area name")
            if objects_to_retag:
                for object in objects_to_retag:
                    object.tags.remove(area, category="area name")
                    object.tags.add(area_rename, category="area name")

class TickerCleanup(DefaultScript):

    # Start with scripts/start scripts.FixAreaNames

    def at_script_creation(self):
        self.key = "ticker_cleanup_script"
        self.desc = "Cleans up old tickers"
        self.persistent = True

        tickerhandler.clear(interval=30)
        tickerhandler.clear(interval=900)
        tickerhandler.clear(interval=1800)
        tickerhandler.save()
