"""
Object

The Object is the "naked" base class for things in the game world.

Note that the default Character, Room and Exit does not inherit from
this Object, but from their respective default implementations in the
evennia library. If you want to use this class as a parent to change
the other types, you can do so by adding this as a multiple
inheritance.

"""
from evennia import DefaultObject
from evennia import TICKER_HANDLER as tickerhandler
from server.conf import settings

class Object(DefaultObject):
    """
    This is the root typeclass object, implementing an in-game Evennia
    game object, such as having a location, being able to be
    manipulated or looked at, etc. If you create a new typeclass, it
    must always inherit from this object (or any of the other objects
    in this file, since they all actually inherit from BaseObject, as
    seen in src.object.objects).

    The BaseObject class implements several hooks tying into the game
    engine. By re-implementing these hooks you can control the
    system. You should never need to re-implement special Python
    methods, such as __init__ and especially never __getattribute__ and
    __setattr__ since these are used heavily by the typeclass system
    of Evennia and messing with them might well break things for you.


    * Base properties defined/available on all Objects

     key (string) - name of object
     name (string)- same as key
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation

     account (Account) - controlling account (if any, only set together with
                       sessid below)
     sessid (int, read-only) - session id (if any, only set together with
                       account above). Use `sessions` handler to get the
                       Sessions directly.
     location (Object) - current location. Is None if this is a room
     home (Object) - safety start-location
     has_account (bool, read-only)- will only return *connected* accounts
     contents (list of Objects, read-only) - returns all objects inside this
                       object (including exits)
     exits (list of Objects, read-only) - returns all exits from this
                       object, if any
     destination (Object) - only set if this object is an exit.
     is_superuser (bool, read-only) - True/False if this user is a superuser

    * Handlers available

     aliases - alias-handler: use aliases.add/remove/get() to use.
     permissions - permission-handler: use permissions.add/remove() to
                   add/remove new perms.
     locks - lock-handler: use locks.add() to add new lock strings
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().
     sessions - sessions-handler. Get Sessions connected to this
                object with sessions.get()
     attributes - attribute-handler. Use attributes.add/remove/get.
     db - attribute-handler: Shortcut for attribute-handler. Store/retrieve
            database attributes using self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create
            a database entry when storing data

    * Helper methods (see src.objects.objects.py for full headers)

     search(ostring, global_search=False, attribute_name=None,
             use_nicks=False, location=None, ignore_errors=False, account=False)
     execute_cmd(raw_string)
     msg(text=None, **kwargs)
     msg_contents(message, exclude=None, from_obj=None, **kwargs)
     move_to(destination, quiet=False, emit_to_obj=None, use_destination=True)
     copy(new_key=None)
     delete()
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hooks (these are class methods, so args should start with self):

     basetype_setup()     - only called once, used for behind-the-scenes
                            setup. Normally not modified.
     basetype_posthook_setup() - customization in basetype, after the object
                            has been created; Normally not modified.

     at_object_creation() - only called once, when object is first created.
                            Object customizations go here.
     at_object_delete() - called just before deleting an object. If returning
                            False, deletion is aborted. Note that all objects
                            inside a deleted object are automatically moved
                            to their <home>, they don't need to be removed here.

     at_init()            - called whenever typeclass is cached from memory,
                            at least once every server restart/reload
     at_cmdset_get(**kwargs) - this is called just before the command handler
                            requests a cmdset from this object. The kwargs are
                            not normally used unless the cmdset is created
                            dynamically (see e.g. Exits).
     at_pre_puppet(account)- (account-controlled objects only) called just
                            before puppeting
     at_post_puppet()     - (account-controlled objects only) called just
                            after completing connection account<->object
     at_pre_unpuppet()    - (account-controlled objects only) called just
                            before un-puppeting
     at_post_unpuppet(account) - (account-controlled objects only) called just
                            after disconnecting account<->object link
     at_server_reload()   - called before server is reloaded
     at_server_shutdown() - called just before server is fully shut down

     at_access(result, accessing_obj, access_type) - called with the result
                            of a lock access check on this object. Return value
                            does not affect check result.

     at_before_move(destination)             - called just before moving object
                        to the destination. If returns False, move is cancelled.
     announce_move_from(destination)         - called in old location, just
                        before move, if obj.move_to() has quiet=False
     announce_move_to(source_location)       - called in new location, just
                        after move, if obj.move_to() has quiet=False
     at_after_move(source_location)          - always called after a move has
                        been successfully performed.
     at_object_leave(obj, target_location)   - called when an object leaves
                        this object in any fashion
     at_object_receive(obj, source_location) - called when this object receives
                        another object

     at_traverse(traversing_object, source_loc) - (exit-objects only)
                              handles all moving across the exit, including
                              calling the other exit hooks. Use super() to retain
                              the default functionality.
     at_after_traverse(traversing_object, source_location) - (exit-objects only)
                              called just after a traversal has happened.
     at_failed_traverse(traversing_object)      - (exit-objects only) called if
                       traversal fails and property err_traverse is not defined.

     at_msg_receive(self, msg, from_obj=None, **kwargs) - called when a message
                             (via self.msg()) is sent to this obj.
                             If returns false, aborts send.
     at_msg_send(self, msg, to_obj=None, **kwargs) - called when this objects
                             sends a message to someone via self.msg().

     return_appearance(looker) - describes this object. Used by "look"
                                 command by default
     at_desc(looker=None)      - called by 'look' whenever the
                                 appearance is requested.
     at_get(getter)            - called after object has been picked up.
                                 Does not stop pickup.
     at_drop(dropper)          - called when this object has been dropped.
     at_say(speaker, message)  - by default, called if an object inside this
                                 object speaks

    """

    def at_object_creation(self):
        self.db.vnum = ""
        self.db.level = 1
        self.db.level_base = 1
        self.db.special_function = []

    def at_reset(self):
        # just here to keep objects from erroring on call to at_reset
        pass

class Item(Object):

    """

    This is the class for actual, real objects in the MUD (not Characters,
    Mobiles, Rooms or Exits), which will be further broken down by the item
    type information from the original data from the mud areas.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.extra_flags = []
        self.db.extra_descriptions = {}
        self.db.alignment_restriction = []
        self.db.cost = 0
        self.tags.add("object")

        # This lock added to enable the use of nodrop items

        self.locks.add("drop: true()")
        
    def at_disintegrate(self):
        if self.contents:
            if len(self.contents) == 1:
                number = "an item drops"
            else:
                number = "items drop"
            self.location.msg_contents("As %s crumbles away to dust, %s to the floor."
                                         % (self.name, number),
                                         exclude=self)

            for item in self.contents:
                item.move_to(self.location, quiet=True)
                tickerhandler.add(settings.DEFAULT_DISINTEGRATE_TIME, item.at_disintegrate)

        else:
            self.location.msg_contents("%s crumbles away to dust."
                                         % (self.name[0].upper() + self.name[1:]), exclude=self)

        if "pc corpse" in self.tags.all():
            tickerhandler.remove(settings.PC_CORPSE_DISINTEGRATE_TIME, self.at_disintegrate)
        else:
            tickerhandler.remove(settings.DEFAULT_DISINTEGRATE_TIME, self.at_disintegrate)

        self.location = None

class Equipment(Item):

    """

    This is the class for equipment that can be worn or wielded on the MUD,
    which is a subset of the Item class.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.stat_modifiers = {
            "strength":0,
            "dexterity":0,
            "intelligence":0,
            "wisdom":0,
            "constitution":0,
            "mana":0,
            "hitpoints":0,
            "move":0,
            "armor class":0,
            "hitroll":0,
            "damroll":0,
            "saving throw":0
        }
        self.db.wear_location = ""
        self.db.equipped = False

        # Lock to prevent characters using equipment that is more than five levels
        # above them.

        self.locks.add("equip: equipment_level_check()")

        # Lock to enable noremove equipment 

        self.locks.add("remove: true()")

    def remove_from(
        self,
        caller
    ):
        """
        Removes this object from a wear location.

        Args:
            caller: Reference to the character trying to wear the object.
            quiet (bool): If true, turn off the calling of the emit hooks
                (announce_move_to/from etc)
            emit_to_obj (Object): object to receive error messages
            use_destination (bool): Default is for objects to use the "destination"
                 property of destinations as the target to move to. Turning off this
                 keyword allows objects to move "inside" exit objects.

        Returns:
            result (bool): True/False depending on if there were problems with the
                 wear action.
                    This method may also return various error messages to the
                    `emit_to_obj`.

        """

        def logerr(string="", err=None):
            """Simple log helper method"""
            logger.log_trace()
            self.msg("%s%s" % (string, "" if err is None else " (%s)" % err))
            return

        wear_location = self.db.wear_location

        if wear_location == "wrist":
            if caller.db.eq_slots["wrist, left"] == self:
                wear_location = "wrist, left"
            else:
                wear_location = "wrist, right"
        elif wear_location == "neck":
            if caller.db.eq_slots["neck, first"] == self:
                wear_location = "neck, first"
            else:
                wear_location = "neck, second"
        elif wear_location == "finger":
            if caller.db.eq_slots["finger, left"] == self:
                wear_location = "finger, left"
            else:
                wear_location = "finger, right"
        elif wear_location == "wield":
            if caller.db.eq_slots["wielded, primary"] == self:
                wear_location = "wielded, primary"
            else:
                wear_location = "wielded, secondary"


        # Perform remove action
        try:
            self.db.equipped = False
            caller.db.eq_slots[wear_location] = ""
        except Exception as err:
            logerr(errtxt % "location change", err)
            return False
        return True

    def at_after_equip(self,caller):
        """
        
        This method is intended to create the effect of equipment shocking the character and
        dropping after the character tries to equip it when the equipment is not permitted
        to be used by characters of the character's alignment.
        
        """
        
        # if there is no alignment restriction on the equipment, go no further.
        
        if not self.db.alignment_restriction:
            return
        
        # determine alignment of prospective wearer
        
        if caller.db.alignment > 333:
            alignment = "good"
        elif caller.db.alignment < -333:
            alignment = "evil"
        else:
            alignment = "neutral"
        
        # check prohibited alignments against character alignment
        
        for prohibited_alignment in self.db.alignment_restriction:

            if alignment == prohibited_alignment:
                self.db.equipped = False # set the equipment to not equipped.
                
                # set the wear_location to empty.
                
                for wear_location in caller.db.eq_slots:
                    if caller.db.eq_slots[wear_location] == self:
                        caller.db.eq_slots[wear_location] = ""
                
                # drop the equipment and send appropriate messages.
                
                success = self.move_to(caller.location, quiet = True)
                if not success:
                    caller.msg("Your alignment-restricted equipment did not drop. Contact Random.")
                else:
                    caller.msg("%s shocks you as you try to wear it, and drops to the ground." % (self.name[0].upper() + self.name[1:]))
                    caller.location.msg_contents("%s's %s drops to the ground after wearing it." % (caller.name, self.name), exclude = caller)
                    self.at_drop(caller)
                    


  
class Armor(Equipment):

    """

    This is the class for anything that is worn by the players, other than
    weapons.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.item_type = "armor"
        self.db.armor = 0


    def wear_to(
        self,
        caller
    ):
        """
        Equips this object to a wear location.

        Args:
            caller: Reference to the character trying to wear the object.
            quiet (bool): If true, turn off the calling of the emit hooks
                (announce_move_to/from etc)
            emit_to_obj (Object): object to receive error messages
            use_destination (bool): Default is for objects to use the "destination"
                 property of destinations as the target to move to. Turning off this
                 keyword allows objects to move "inside" exit objects.

        Returns:
            result (bool): True/False depending on if there were problems with the
                 wear action.
                    This method may also return various error messages to the
                    `emit_to_obj`.

        """

        def logerr(string="", err=None):
            """Simple log helper method"""
            logger.log_trace()
            self.msg("%s%s" % (string, "" if err is None else " (%s)" % err))
            return

        wear_location = self.db.wear_location

        # Fix wear location for multi-slot locations. First checks whether both 
        # locations are full (assign to first), then if first is empty (assign to
        # first), otherwise assign to second.

        if wear_location == "wrist":
            if caller.db.eq_slots["wrist, left"] and caller.db.eq_slots["wrist, right"]:
                wear_location = "wrist, left"
            elif not caller.db.eq_slots["wrist, left"]:
                wear_location = "wrist, left"
            else:
                wear_location = "wrist, right"
        elif wear_location == "neck":
            if caller.db.eq_slots["neck, first"] and caller.db.eq_slots["neck, second"]:
                wear_location = "neck, first"
            elif not caller.db.eq_slots["neck, first"]:
                wear_location = "neck, first"
            else:
                wear_location = "neck, second"
        elif wear_location == "finger":
            if caller.db.eq_slots["finger, left"] and caller.db.eq_slots["finger, right"]:
                wear_location = "finger, left"
            elif not caller.db.eq_slots["finger, left"]:
                wear_location = "finger, left"
            else:
                wear_location = "finger, right"
            
        # Perform wear action.
        try:
            self.db.equipped = True
            caller.db.eq_slots[wear_location] = self
        except Exception as err:
            logerr(errtxt % "location change", err)
            return False
        return True

class Weapon(Equipment):

    """

    This is the class for weapons, duh.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.item_type = "weapon"
        self.db.damage_low = 0
        self.db.damage_high = 0
        self.db.wear_location = "wield"

        # traditional weapon types are hit, slice, stab, slash, whip, claw,
        # blast, pound, crush, grep, bite, pierce, suction, and chop, but
        # you can use any similar word. Only stab and pierce will be
        # backstab-enabled
        self.db.weapon_type = ""

    def wield_to(
        self,
        caller
    ):
        """
        Equips this object to a wield location.

        Args:
            caller: Reference to the character trying to wield the object.
            quiet (bool): If true, turn off the calling of the emit hooks
                (announce_move_to/from etc)
            emit_to_obj (Object): object to receive error messages
            use_destination (bool): Default is for objects to use the "destination"
                 property of destinations as the target to move to. Turning off this
                 keyword allows objects to move "inside" exit objects.

        Returns:
            result (bool): True/False depending on if there were problems with the
                 wear action.
                    This method may also return various error messages to the
                    `emit_to_obj`.

        """

        def logerr(string="", err=None):
            """Simple log helper method"""
            logger.log_trace()
            self.msg("%s%s" % (string, "" if err is None else " (%s)" % err))
            return

        wear_location = "wielded, primary"
            
        # Perform wear action.
        try:
            self.db.equipped = True
            caller.db.eq_slots[wear_location] = self
        except Exception as err:
            logerr(errtxt % "location change", err)
            return False
        return True


class Light(Armor):

    """

    This is the class for armor worn in the "light" location, which also has
    the ability to provide light.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.item_type = "light"
        self.db.wear_location = "light"
        self.db.armor = 0

        # hours of light can be any number, but -1 is infinite, and 0 is
        # exhausted.
        self.db.light_hours = -1

class Scroll(Item):

    """

    This is the class for scrolls, which can be used by players with the
    scrolls ability to cast spells.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "scroll"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}
        self.db.spell_level = 1
        self.db.spell_level_base = 1
        self.db.spell_name_1 = ""
        self.db.spell_name_2 = ""
        self.db.spell_name_3 = ""

class Wand(Armor):

    """

    This is the class for wands, which can be used by players with the
    wands ability to cast spells.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.item_type = "wand"
        self.db.wear_location = "held, in hands"
        self.db.spell_level = 1
        self.db.spell_level_base = 1
        self.db.charges_maximum = 0
        self.db.charges_maximum_base = 0
        self.db.charges_current = 0
        self.db.spell_name = ""

class Staff(Armor):

    """

    This is the class for staves, which can be used by players with the
    staff ability to cast spells.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.item_type = "staff"
        self.db.wear_location = "held, in hands"
        self.db.spell_level = 1
        self.db.spell_level_base = 1
        self.db.charges_maximum = 0
        self.db.charges_maximum_base = 0
        self.db.charges_current = 0
        self.db.spell_name = ""

class Potion(Item):

    """

    This is the class for potions, which can be quaffed by players to
    cast spells on themselves.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "potion"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}
        self.db.spell_level = 1
        self.db.spell_level_base = 1
        self.db.spell_name_1 = ""
        self.db.spell_name_2 = ""
        self.db.spell_name_3 = ""

class Furniture(Item):

    """

    This is the class for furniture of all types, which can be sat upon,
    at, laid on, etc. by players.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "furniture"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}
        self.db.people_maximum = 0
        self.db.weight_maximum = 0

        # options for the below are any combination of stand/sit/rest/sleep at/on/in
        self.db.use_positions = ""
        self.db.heal_mana_gain = 0

        # can't pick up furniture
        self.locks.add("get:false()")
        self.db.get_err_msg = "This is too heavy to pick up."

class Container(Armor):

    """

    This is the class for containers of all types.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "container"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}
        self.db.weight_maximum = 0
        self.db.state = ["open"]
        self.db.state_base = ["open"]
        self.db.key = -1

        # locks that go along with the above attributes
        self.locks.add("put: is_open();open: can_open();close: can_close();lock: can_lock();unlock: can_unlock()")


class Drink_container(Item):

    """

    This is the class for containers that specifically hold liquids.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "drink_container"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}
        self.db.capacity_maximum = 0
        self.db.capacity_current = 0
        self.db.liquid_type = ""
        self.db.poison = 0
        # Do a table for these in rules
        self.db.liquid_drunk = 0
        self.db.liquid_food = 0
        self.db.liquid_thirst = 0

class Food(Item):

    """

    This is the class for food of all.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "food"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}
        self.db.hours_fed = 0
        self.db.poison = 0

class Pill(Item):

    """

    This is the class for pills, which can be eaten by players to cast spells
    on themselves.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "pill"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}
        self.db.spell_level = 1
        self.db.spell_level_base = 1
        self.db.spell_name_1 = ""
        self.db.spell_name_2 = ""
        self.db.spell_name_3 = ""

class Scuba(Item):

    """

    This is the class for scuba items that players can use to breathe
    underwater.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "scuba"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}

        # Both of the below are in mud hours.
        self.db.charge_maximum = 0
        self.db.charge_current = 0

class Key(Armor):

    """

    This is the class for key items that players can use to unlock
    doors.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "key"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}

class Trash(Item):

    """

    This is the class for trash items.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "trash"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}

class Treasure(Armor):

    """

    This is the class for treasure items. Can sometimes be worn
    or used.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "treasure"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}
        self.db.wear_location = ""

class Boat(Item):

    """

    This is the class for boat items that players can use to traverse
    water.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "boat"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}

class Money(Item):

    """

    This is the class for money items.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "money"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}

class Fly(Item):

    """

    This is the class for items that players can use to fly.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.object_type = "item"
        self.db.item_type = "fly"
        self.db.vnum = 0
        self.db.level = 1
        self.db.extra_flags = []
        self.db.extra_descriptions = {}

class NPC_Corpse(Container):

    """

    This is the class for mobile corpses.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.tags.add("npc corpse")


class PC_Corpse(Container):
    """

    This is the class for player corpses.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.gold = 0
        self.db.experience = 0
        self.tags.add("pc corpse")
