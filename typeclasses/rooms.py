"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from evennia.utils import search
from world import rules


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_creation(self):
        """
        Called once, when this object is first created. This is the
        normal hook to overload for most object types.
        """

        # set persistent attributes

        self.db.room_flags = []
        self.db.terrain = ""
        self.db.extra_description = {}
        self.db.area_name = ""
        self.db.reset_objects = {}

    def at_reset(self):

        # Check to see if there are objects that should be reset to it. This
        # dictionary takes the form of
        # reset_objects = {
        #     <onum>:{
        #         "location":<equipped, inventory, onum of container>
        #            }
        #                 }
        if self.db.reset_objects:

            # Iterate through the onums reset to this room.
            for reset_object in self.db.reset_objects:

                reset_object = reset_object.lower()
                new_object = ""
                container = ""

                # Search the room's inventory for the object already existing.

                if self.db.reset_objects[reset_object]["location"] == \
                        "inventory":
                    for object in self.contents:
                        aliases = object.aliases.get()
                        if aliases:
                            if reset_object in aliases:
                                new_object = object
                else:
                    # If the object does not belong in room inventory, find the
                    # object that the reset object should reset in, WHICH MUST
                    # ALWAYS RESET BEFORE IT.
                    for object in self.contents:
                        # May need object.aliases.get() below
                        aliases = object.aliases.get()
                        if aliases:
                            if self.db.reset_objects[reset_object]["location"] \
                                    in aliases:
                                # Set the object as the container, for later.
                                container = object

                                # Iterate through objects in each container.
                                for contained_object in object.contents:
                                    aliases = contained_object.aliases.get()
                                    if aliases:
                                        if reset_object in aliases:
                                            new_object = contained_object

                # If the object does not already exist in the room, continue
                # on.
                if not new_object:

                    # First, search for all objects of that type and pull out
                    # any that are at "None".
                    object_candidates = search.search_object(reset_object)

                    for object in object_candidates:
                        if not object.location:
                            new_object = object

                    # If it is not in "None", find the existing object in the
                    # world and copy it.
                    if not new_object:

                        object_to_copy = object_candidates[0]
                        new_object = object_to_copy.copy()
                        new_object.key = object_to_copy.key
                        new_object.alias = object_to_copy.aliases
                        if new_object.db.equipped:
                            new_object.db.equipped = False
                        new_object.home = self

                    # Either way, bring the new object to the room or put it
                    # in the container it resets in.
                    if container:
                        new_object.location = container
                    else:
                        new_object.location = self

                # Clear any enchantment/poison/other affects.
                new_object.db.spell_affects = {}

                # Set level, other values, and/or fuzz numbers as necessary
                new_object.db.level == new_object.db.level_base
                if new_object.db.item_type == "armor":
                    new_object.db.armor = rules.set_armor(new_object.db.level)
                elif new_object.db.item_type == "weapon":
                    new_object.db.damage_low, new_object.db.damage_high = \
                        rules.set_weapon_low_high(new_object.db.level)
                elif new_object.db.item_type == "scroll":
                    new_object.db.spell_level = \
                        rules.fuzz_number(new_object.db.spell_level_base)
                elif new_object.db.item_type == "wand" or \
                        new_object.db.item_type == "staff":
                    new_object.db.spell_level = \
                        rules.fuzz_number(new_object.db.spell_level_base)
                    new_object.db.charges_maximum = \
                        rules.fuzz_number(new_object.db.charges_maximum_base)
                    new_object.db.charges_current = \
                        new_object.db.charges_maximum
                elif new_object.db.item_type == "potion" or \
                        new_object.db.item_type == "pill":
                    new_object.db.spell_level = \
                        rules.fuzz_number(rules.fuzz_number(
                            new_object.db.spell_level_base))

        self.msg_contents("The mobs come scrambling back!")

    def return_appearance(self, looker, **kwargs):
        """
        This formats a description. It is the hook a 'look' command
        should call.
        Args:
            looker (Object): Object doing the looking.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        """
        if not looker:
            return ""
        # get and identify all objects
        visible = (con for con in self.contents if con != looker and con.access(looker, "view"))
        exits, users, things = [], [], defaultdict(list)
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                if "locked" in con.db.door_attributes:
                    doorl = "{"
                    doorr = "}"
                elif "open" not in con.db.door_attributes:
                    doorl = "["
                    doorr = "]"
                else:
                    doorl = ""
                    doorr = ""
                keystring = doorl + key + doorr
                exits.append(keystring)
            elif con.has_account:
                users.append("|c%s|n" % key)
            else:
                # things can be pluralized
                things[key].append(con)
        # get description, build string
        string = "|M%s|n\n" % self.get_display_name(looker)
        desc = self.db.desc
        if desc:
            string += "|C%s|n" % desc
        if exits:
            string += "\n|wExits:|n " + list_to_string(exits)
        if users or things:
            # handle pluralization of things (never pluralize users)
            thing_strings = []
            for key, itemlist in sorted(things.items()):
                nitem = len(itemlist)
                if nitem == 1:
                    key, _ = itemlist[0].get_numbered_name(nitem, looker, key=key)
                else:
                    key = [item.get_numbered_name(nitem, looker, key=key)[1] for item in itemlist][
                        0
                    ]
                thing_strings.append(key)

            string += "\n|wYou see:|n " + list_to_string(users + thing_strings)

        return string
