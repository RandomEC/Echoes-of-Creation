"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""
from evennia import DefaultExit


class Exit(DefaultExit):
    """
    Exits are connectors between rooms. Exits are normal Objects except
    they defines the `destination` property. It also does work in the
    following methods:

     basetype_setup() - sets default exit locks (to change, use `at_object_creation` instead).
     at_cmdset_get(**kwargs) - this is called when the cmdset is accessed and should
                              rebuild the Exit cmdset along with a command matching the name
                              of the Exit object. Conventionally, a kwarg `force_init`
                              should force a rebuild of the cmdset, this is triggered
                              by the `@alias` command when aliases are changed.
     at_failed_traverse() - gives a default error message ("You cannot
                            go there") if exit traversal fails and an
                            attribute `err_traverse` is not defined.

    Relevant hooks to overload (compared to other types of Objects):
        at_traverse(traveller, target_loc) - called to do the actual traversal and calling of the other hooks.
                                            If overloading this, consider using super() to use the default
                                            movement implementation (and hook-calling).
        at_after_traverse(traveller, source_loc) - called by at_traverse just after traversing.
        at_failed_traverse(traveller) - called by at_traverse if traversal failed for some reason. Will
                                        not be called if the attribute `err_traverse` is
                                        defined, in which case that will simply be echoed.
    """

    def at_object_creation(self):
        """
        Called once, when this object is first created. This is the
        normal hook to overload for most object types.
        """

        # set persistent attributes

        self.db.key = ""
        self.db.locks = []
        self.db.area_name = ""
        self.tags.add("exit")

        # choices for this are open, closeable, locked, lockable, bashproof,
        # pickproof, passproof
        self.db.door_attributes = ["open",]
        self.db.reset_door_attributes = ["open",]

        # locks that go along with the above attributes
        self.locks.add("traverse: is_open();open: can_open();close: can_close();lock: can_lock();unlock: can_unlock()")

    def at_reset(self):
        """
        This method is called when it is time for the area to reset.
        Simply replaces all of the current door state with the
        reset state
        """

        self.db.door_attributes = self.db.reset_door_attributes
        
    def at_traverse(self, traversing_object, target_location, **kwargs):
        """
        This implements the actual traversal. The traverse lock has
        already been checked (in the Exit command) at this point.

        Args:
            traversing_object (Object): Object traversing us.
            target_location (Object): Where target is going.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).

        """
        source_location = traversing_object.location
        
        terrain = source_location.db.terrain
        
        if terrain:
            if terrain == "inside":
                terrain_cost = 0
            elif terrain == "city":
                terrain_cost = 1
            elif terrain == "field":
                terrain_cost = 2
            elif terrain == "forest":
                terrain_cost = 3
            elif terrain == "hills":
                terrain_cost = 4
            elif terrain == "mountain":
                terrain_cost = 5
            elif terrain == "water swim":
                terrain_cost = 6
            elif terrain == "swamp":
                terrain_cost = 7
            elif terrain == "underwater":
                terrain_cost = 8
            elif terrain == "air":
                terrain_cost = 9
            elif terrain == "desert":
                terrain_cost = 10
            elif terrain == "vacuum":
                terrain_cost = 11
            elif terrain == "max":
                terrain_cost = 12
            else:
                terrain_cost = 0
        
        if terrain cost > traversing_object.moves_current:
            traversing.obj.msg("You are too tired to move further.")
            return
        
        if traversing_object.move_to(target_location):
            traversing_object.moves_spent += terrain_cost
            self.at_after_traverse(traversing_object, source_location)
        else:
            if self.db.err_traverse:
                # if exit has a better error message, let's use it.
                traversing_object.msg(self.db.err_traverse)
            else:
                # No shorthand error message. Call hook.
                self.at_failed_traverse(traversing_object)

