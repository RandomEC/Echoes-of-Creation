"""
This module handles the implementation of doors and door commands into the
game. Works with several lock functions and a handful of door_attributes

Added into the Exit class:

        # choices for this are open, closeable, locked, lockable, bashproof,
        # pickproof, passproof
        self.db.door_attributes = list()

        # locks that go along with the above attributes
        self.locks.add("traverse: is_open();open: can_open();close:
        can_close();lock: can_lock();unlock: can_unlock()")

The following are added into lockfuncs.py:

def is_open(accessing_obj, accessed_obj, *args, **kwargs):

    if "open" in accessed_obj.db.door_attributes:
        return True
    else:
        return False

def can_open(accessing_obj, accessed_obj, *args, **kwargs):

    if not "open" in accessed_obj.db.door_attributes \
       and not "locked" in accessed_obj.db.door_attributes:
        return True
    else:
        return False

def can_close(accessing_obj, accessed_obj, *args, **kwargs):

    if "open" in accessed_obj.db.door_attributes \
       and "closeable" in accessed_obj.db.door_attributes:
        return True
    else:
        return False

def can_lock(accessing_obj, accessed_obj, *args, **kwargs):

    if not "open" in accessed_obj.db.door_attributes \
       and not "locked" in accessed_obj.db.door_attributes \
       and "lockable" in accessed_obj.db.door_attributes \
       and accessing_obj.check_key(accessed_obj.db.key):
        return True
    else:
        return False

def can_unlock(accessing_obj, accessed_obj, *args, **kwargs):

    if not "open" in accessed_obj.db.door_attributes \
       and "locked" in accessed_obj.db.door_attributes \
       and accessing_obj.check_key(accessed_obj.db.key):
        return True
    else:
        return False
"""

from commands.command import MuxCommand


class CmdDoorOpen(MuxCommand):
    """
    Open a door or container in the room you are in.

    Usage:
      open <door>
      open <container>

    Opens the door permitting you to exit through it, or the
    container, allowing you to access it.
    """

    key = "open"
    alias = "op"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):

        caller = self.caller

        # Output if open is used with no argument.
        if not self.args:
            caller.msg("What door direction or container do you want to open?")
            return

        # Search everything in the caller's location for the door (or container
        # for the future) referred to.
        door = caller.search(self.args, location=caller.location)

        # Deal with not finding an object named the argument in the room.
        if not door:
            caller.msg("There is no %s here." % self.args)
            return

        # If the searched-for thing is an object, it should be a container.
        if "object" in door.tags.all():
            container = door
            
            # Check to make sure it is actually a container.
            if container.db.item_type != "container":
                caller.msg("%s is neither a container nor a door."
                           % (container.key[0].upper() + container.key[1:])
                           )
                return
            
            # Check to see if the locks for open are met, and give corrective
            # output if not.
            if not container.access(caller, "open"):
                if "open" in container.db.state:
                    caller.msg("The %s is already open." % container.key)
                elif "locked" in container.db.state:
                    caller.msg("The %s is locked." % container.key)
                return

            # If the container state does not already include "open", add it.
            if "open" not in container.db.state:
                container.db.state.append("open")
                caller.msg("You open the %s." % container.key)
            
        else:
            # Check to make sure it is actually a door.
            if "exit" not in door.tags.all():
                caller.msg("%s is neither a container nor a door."
                           % (door.key[0].upper() + door.key[1:])
                           )
                return
            
            # This is making the grammatical string for referring to the door in
            # output.
            if door.key == "north" or door.key == "east" or door.key == "south" \
                    or door.key == "west":
                door_string = ("door to the %s" % door.key)
            elif door.key == "up" or door.key == "down":
                door_string = ("door %s" % door.key)
            else:
                door_string = ("%s" % door.key)

            # Check to see if the locks for open are met, and give corrective
            # output if not.
            if not door.access(caller, "open"):
                if "open" in door.db.door_attributes:
                    caller.msg("The %s is already open." % door_string)
                elif "locked" in door.db.door_attributes:
                    caller.msg("The %s is locked." % door_string)
                return

            # If the door attributes do not already include "open", add it.
            if "open" not in door.db.door_attributes:
                door.db.door_attributes.append("open")
                caller.msg("You open the %s." % door_string)

            # The next section of code is to deal with the fact that each "exit"
            # is actually two paired exits, and does the same to the door in the
            # other direction.
            opposite_direction = ""

            if door.key == "north":
                opposite_direction = "south"
            elif door.key == "east":
                opposite_direction = "west"
            elif door.key == "south":
                opposite_direction = "north"
            elif door.key == "west":
                opposite_direction = "east"
            elif door.key == "up":
                opposite_direction = "down"
            elif door.key == "down":
                opposite_direction = "up"
            else:
                opposite_direction = door.key

            opposite_door = caller.search(opposite_direction,
                                          location=door.destination)

            if "open" not in opposite_door.db.door_attributes:
                opposite_door.db.door_attributes.append("open")


class CmdDoorClose(MuxCommand):
    """
    Closes a door or container in the room you are in.

    Usage:
      close <door>
      close <container>

    Closes the door, preventing to exit through it, or closes a
    container, preventing access.
    """

    key = "close"
    alias = "cl"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):

        caller = self.caller

        # Output if no argument is give with close.
        if not self.args:
            caller.msg("What do you want to close?")
            return

        # Look in the room for the exit being referred to.
        door = caller.search(self.args, location=caller.location)

        # If the exit is not found, give output.
        if not door:
            caller.msg("There is no %s here." % self.args)
            return

                # If the searched-for thing is an object, it should be a container.
        if "object" in door.tags.all():
            container = door
            
            # Check to make sure it is actually a container.
            if container.db.item_type != "container":
                caller.msg("%s is neither a container nor a door."
                           % (container.key[0].upper() + container.key[1:])
                           )
                return
            
            # Check to see if the locks for close are met, and give corrective
            # output if not.
            if not container.access(caller, "close"):
                if "open" not in container.db.state:
                    caller.msg("The %s is already closed." % container.key)
                elif "closeable" not in container.db.state:
                    caller.msg("The %s cannot be closed." % container.key)
                return

            # If the container state includes "open", remove it.
            if "open" not in container.db.state:
                container.db.state.remove("open")
                caller.msg("You close the %s." % container.key)
            
        else:
            # Check to make sure it is actually a door.
            if "exit" not in door.tags.all():
                caller.msg("%s is neither a container nor a door."
                           % (door.key[0].upper() + door.key[1:])
                           )
                return
        
            # This is making the grammatical string for referring to the door in
            # output.
            if door.key == "north" or door.key == "east" or door.key == "south" \
                    or door.key == "west":
                door_string = ("door to the %s" % door.key)
            elif door.key == "up" or door.key == "down":
                door_string = ("door %s" % door.key)
            else:
                door_string = ("%s" % door.key)

            # Check whether the locks for close have been met, and give corrective
            # output if not.
            if not door.access(caller, "close"):
                if "open" not in door.db.door_attributes:
                    caller.msg("The %s is already closed." % door_string)
                elif "closeable" not in door.db.door_attributes:
                    caller.msg("There is no door to close to the %s." % door_string)
                return

            # If the door attributes currently include open, remove it.
            if "open" in door.db.door_attributes:
                door.db.door_attributes.remove("open")
                caller.msg("You close the %s." % door_string)

            # The next section of code is to deal with the fact that each "exit"
            # is actually two paired exits, and does the same to the door in the
            # other direction.
            opposite_direction = ""

            if door.key == "north":
                opposite_direction = "south"
            elif door.key == "east":
                opposite_direction = "west"
            elif door.key == "south":
                opposite_direction = "north"
            elif door.key == "west":
                opposite_direction = "east"
            elif door.key == "up":
                opposite_direction = "down"
            elif door.key == "down":
                opposite_direction = "up"
            else:
                opposite_direction = door.key

            opposite_door = caller.search(opposite_direction,
                                          location=door.destination)

            if "open" in opposite_door.db.door_attributes:
                opposite_door.db.door_attributes.remove("open")


class CmdDoorUnlock(MuxCommand):
    """
    Unlock a door or a container in the room you are in.

    Usage:
      unlock <door>
      unlock <container>

    Unlocks the door or container permitting you to open it.
    """

    key = "unlock"
    alias = "unl"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):

        caller = self.caller

        # Give output if there is no argument with unlock.
        if not self.args:
            caller.msg("What do you want to unlock?")
            return

        # Search the room for an object matching the argument.
        door = caller.search(self.args, location=caller.location)

        # If there is no matching door, give output.
        if not door:
            caller.msg("There is no %s here." % self.args)
            return

        # If the searched-for thing is an object, it should be a container.
        if "object" in door.tags.all():
            container = door
            
            # Check to make sure it is actually a container.
            if container.db.item_type != "container":
                caller.msg("%s is neither a container nor a door."
                           % (container.key[0].upper() + container.key[1:])
                           )
                return
            
            # Check to see if the locks for unlock are met, and give corrective
            # output if not.
            if not container.access(caller, "unlock"):
                if "closeable" not in container.db.state:
                    caller.msg("%s cannot be closed, much less locked."
                               % container.key[0].upper() + container.key[1:]
                               )
                elif "lockable" not in container.db.state:
                    caller.msg("%s does not have a lock."
                               % container.key[0].upper() + container.key[1:]
                               )
                elif "open" in container.db.state:
                    caller.msg("%s cannot be unlocked while open."
                               % container.key[0].upper() + container.key[1:]
                               )
                elif "locked" not in container.db.state:
                    caller.msg("%s is already unlocked."
                               % container.key[0].upper() + container.key[1:]
                               )
                elif not caller.check_key(container.db.key):
                    caller.msg("You do not have the key to %s." % container.key)
                return

            # If the container state includes "locked", remove it.
            if "locked" in container.db.state:
                container.db.state.remove("locked")
                caller.msg("*Click* You unlock %s." % container.key)
            
        else:
            # Check to make sure it is actually a door.
            if "exit" not in door.tags.all():
                caller.msg("%s is neither a container nor a door."
                           % (door.key[0].upper() + door.key[1:])
                           )
                return
        
            # This is making the grammatical string for referring to the door in
            # output.
            if door.key == "north" or door.key == "east" or door.key == "south" \
                    or door.key == "west":
                door_string = ("door to the %s" % door.key)
            elif door.key == "up" or door.key == "down":
                door_string = ("door %s" % door.key)
            else:
                door_string = ("%s" % door.key)

            # Check to see if the locks are met for unlocking the door. If not,
            # provide corrective output.
            if not door.access(caller, "unlock"):
                if "closeable" not in door.db.door_attributes:
                    caller.msg("There is no door to block the %s for there to "
                               "be a lock in." % door_string)
                elif "lockable" not in door.db.door_attributes:
                    caller.msg("The %s does not have a lock." % door_string)
                elif "open" in door.db.door_attributes:
                    caller.msg("The %s cannot be unlocked while open." %
                               door_string)
                elif "locked" not in door.db.door_attributes:
                    caller.msg("The %s is already unlocked." % door_string)
                elif not caller.check_key(door.db.key):
                    caller.msg("You do not have the key to the %s." % door_string)
                return

            # If the door attributes currently include locked, remove it.
            if "locked" in door.db.door_attributes:
                door.db.door_attributes.remove("locked")
                caller.msg("*Click* You unlock the %s." % door.key)

            # The next section of code is to deal with the fact that each "exit"
            # is actually two paired exits, and does the same to the door in the
            # other direction.
            opposite_direction = ""

            if door.key == "north":
                opposite_direction = "south"
            elif door.key == "east":
                opposite_direction = "west"
            elif door.key == "south":
                opposite_direction = "north"
            elif door.key == "west":
                opposite_direction = "east"
            elif door.key == "up":
                opposite_direction = "down"
            elif door.key == "down":
                opposite_direction = "up"
            else:
                opposite_direction = door.key

            opposite_door = caller.search(opposite_direction,
                                          location=door.destination)

            if "locked" in opposite_door.db.door_attributes:
                opposite_door.db.door_attributes.remove("locked")


class CmdDoorLock(MuxCommand):
    """
    Lock a door or container in the room you are in.

    Usage:
        lock <door>
        lock <container>

    Locks the door or container, preventing opening it.
    """

    key = "lock"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):

        caller = self.caller

        # Check to make sure there was an argument with lock.
        if not self.args:
            caller.msg("What do you want to lock?")
            return

        # Search for the argument provided in the room.
        door = caller.search(self.args, location=caller.location)

        # If the argument is not found, give output.
        if not door:
            caller.msg("There is no %s here." % self.args)
            return

        # If the searched-for thing is an object, it should be a container.
        if "object" in door.tags.all():
            container = door
            
            # Check to make sure it is actually a container.
            if container.db.item_type != "container":
                caller.msg("%s is neither a container nor a door."
                           % (container.key[0].upper() + container.key[1:])
                           )
                return
            
            # Check if locks satisfied for lock command. If not, give corrective
            # output.
            if not container.access(caller, "lock"):
                if "closeable" not in container.db.state:
                    caller.msg("There way to close %s, much less lock it."
                               % container.key
                               )
                elif "lockable" not in container.db.state:
                    caller.msg("%s does not have a lock."
                               % (container.key[0].upper() + container.key[1:]))
                elif "open" in container.db.state:
                    caller.msg("%s cannot be locked while open."
                               % (container.key[0].upper() + container.key[1:])
                               )
                elif "locked" in container.db.state:
                    caller.msg("%s is already locked."
                               % (container.key[0].upper() + container.key[1:])
                               )
                elif not caller.check_key(container.db.key):
                    caller.msg("You do not have the key to %s."
                               % container.key)
                return

            # If the container state does not include "locked", add it.
            if "locked" not in container.db.state:
                container.db.state.append("locked")
                caller.msg("*Click* You lock %s." % container.key)
            
        else:
            # Check to make sure it is actually a door.
            if "exit" not in door.tags.all():
                caller.msg("%s is neither a container nor a door."
                           % (door.key[0].upper() + door.key[1:])
                           )
                return
            
            # This is making the grammatical string for referring to the door in
            # output.
            if door.key == "north" or door.key == "east" or door.key == "south" \
                    or door.key == "west":
                door_string = ("door to the %s" % door.key)
            elif door.key == "up" or door.key == "down":
                door_string = ("door %s" % door.key)
            else:
                door_string = ("%s" % door.key)

            # Check if locks satisfied for lock command. If not, give corrective
            # output.
            if not door.access(caller, "lock"):
                if "closeable" not in door.db.door_attributes:
                    caller.msg("There is no door to block the %s for there to "
                               "be a lock in." % door_string)
                elif "lockable" not in door.db.door_attributes:
                    caller.msg("The %s does not have a lock." % door_string)
                elif "open" in door.db.door_attributes:
                    caller.msg("The %s cannot be locked while open." %
                               door_string)
                elif "locked" in door.db.door_attributes:
                    caller.msg("The %s is already locked." % door_string)
                elif not caller.check_key(door.db.key):
                    caller.msg("You do not have the key to the %s."
                               % door.key)
                return

            # If the door attributes do not currently have locked, append it.
            if "locked" not in door.db.door_attributes:
                door.db.door_attributes.append("locked")
                if door.key == "north" or door.key == "east" or door.key \
                        == "south" or door.key == "west":
                    caller.msg("*Click* You lock the door to the %s." % door.key)
                elif door.key == "up" or door.key == "down":
                    caller.msg("*Click* You lock the door %s." % door.key)
                else:
                    caller.msg("*Click* You lock the %s." % door.key)

            # The next section of code is to deal with the fact that each "exit"
            # is actually two paired exits, and does the same to the door in the
            # other direction.
            opposite_direction = ""

            if door.key == "north":
                opposite_direction = "south"
            elif door.key == "east":
                opposite_direction = "west"
            elif door.key == "south":
                opposite_direction = "north"
            elif door.key == "west":
                opposite_direction = "east"
            elif door.key == "up":
                opposite_direction = "down"
            elif door.key == "down":
                opposite_direction = "up"
            else:
                opposite_direction = door.key

            opposite_door = caller.search(opposite_direction,
                                          location=door.destination)

            if "locked" not in opposite_door.db.door_attributes:
                opposite_door.db.door_attributes.append("locked")



