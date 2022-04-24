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

from evennia.utils import search
from commands.command import MuxCommand
from world import rules


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
    aliases = ["op"]
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
            
            if not rules.is_visible(container, caller):
                caller.msg("There is no %s here." % self.args)
                return               
                
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
                    caller.msg("%s is already open." % (container.key[0].upper() + container.key[1:]))
                elif "locked" in container.db.state:
                    caller.msg("%s is locked." % (container.key[0].upper() + container.key[1:]))
                return

            # If the container state does not already include "open", add it.
            if "open" not in container.db.state:
                container.db.state.append("open")
                caller.msg("You open %s." % container.key)
                
                # Deal with invisible objects/characters for output.
                # Assemble a list of all possible lookers.
                lookers = list(cont for cont in caller.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
                for looker in lookers:
                    # Exclude the caller, who got their output above.
                    if looker != caller:
                        # Address visibility of character opening.
                        if rules.is_visible(caller, looker):
                            opener = (caller.key[0].upper() + caller.key[1:])
                        else:
                            opener = "Someone"

                        # Address visibility of object opened.
                        if rules.is_visible(container, looker):
                            opened = container.key
                        else:
                            opened = "something"

                        # As long as something was visible, give output.
                        if opener != "Someone" or opened != "something":
                            looker.msg("%s opens %s" % (opener, opened))

            # Check if the container resets in the room. If so, add the room to objects to reset
            # if not there already.
            if container.db.vnum in container.location.db.reset_objects:
                reset_script = search.script_search("reset_script")[0]
                area = rules.get_area_name(container.location)
        
                if container.location not in reset_script.db.area_list[area]["resets"]:
                    reset_script.db.area_list[area]["resets"].append(container.location)        
                
            # Call at_after_open.
            container.at_after_open(caller)

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

                # Deal with invisible objects/characters for output.
                # Assemble a list of all possible lookers.
                lookers = list(cont for cont in caller.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
                for looker in lookers:
                    # Exclude the caller, who got their output above.
                    if looker != caller:
                        # Address visibility of character opening.
                        if rules.is_visible(caller, looker):
                            opener = (caller.key[0].upper() + caller.key[1:])
                        else:
                            opener = "Someone"

                        # As long as something was visible, give output.
                        looker.msg("%s opens %s." % (opener, door_string))
                
            # Add exit to objects to reset if not there already.
            reset_script = search.script_search("reset_script")[0]
            area = rules.get_area_name(door)
            
            if door not in reset_script.db.area_list[area]["resets"]:
                reset_script.db.area_list[area]["resets"].append(door)        
                
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

            # This is making the grammatical string for referring to the opposite door in
            # output.
            if opposite_door.key == "north" or opposite_door.key == "east" or opposite_door.key == "south" \
                    or opposite_door.key == "west":
                opposite_door_string = ("door to the %s" % opposite_door.key)
            elif opposite_door.key == "up" or opposite_door.key == "down":
                opposite_door_string = ("door %s" % opposite_door.key)
            else:
                opposite_door_string = ("%s" % opposite_door.key)
            
            if "open" not in opposite_door.db.door_attributes:
                opposite_door.db.door_attributes.append("open")

            # Give output in that room
            door.destination.msg_contents("The %s opens." % opposite_door_string)
                
            # Add exit to objects to reset if not there already.
            reset_script = search.script_search("reset_script")[0]
            area = rules.get_area_name(opposite_door)
            
            if door not in reset_script.db.area_list[area]["resets"]:
                reset_script.db.area_list[area]["resets"].append(opposite_door)

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
    aliases = ["cl"]
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

            if not rules.is_visible(container, caller):
                    caller.msg("There is no %s here." % self.args)
                    return               
        
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
                    caller.msg("%s is already closed." % (container.key[0].upper + container[1:]))
                elif "closeable" not in container.db.state:
                    caller.msg("%s cannot be closed." % (container.key[0].upper + container[1:]))
                return

            # If the container state includes "open", remove it.
            if "open" in container.db.state:
                container.db.state.remove("open")
                caller.msg("You close %s." % container.key)

                # Deal with invisible objects/characters for output.
                # Assemble a list of all possible lookers.
                lookers = list(cont for cont in caller.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
                for looker in lookers:
                    # Exclude the caller, who got their output above.
                    if looker != caller:
                        # Address visibility of character opening.
                        if rules.is_visible(caller, looker):
                            closer = (caller.key[0].upper() + caller.key[1:])
                        else:
                            closer = "Someone"

                        # Address visibility of object opened.
                        if rules.is_visible(container, looker):
                            closed = container.key
                        else:
                            closed = "something"

                        # As long as something was visible, give output.
                        if closer != "Someone" or closed != "something":
                            looker.msg("%s closes %s" % (closer, closed))

                
            # Check if the container resets in the room. If so, add the room to objects to reset
            # if not there already.
            if container.db.vnum in container.location.db.reset_objects:
                reset_script = search.script_search("reset_script")[0]
                area = rules.get_area_name(container.location)
        
                if container.location not in reset_script.db.area_list[area]["resets"]:
                    reset_script.db.area_list[area]["resets"].append(container.location)        
                
            # Call at_after_close.
            container.at_after_close(caller)

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

                # Deal with invisible objects/characters for output.
                # Assemble a list of all possible lookers.
                lookers = list(cont for cont in caller.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
                for looker in lookers:
                    # Exclude the caller, who got their output above.
                    if looker != caller:
                        # Address visibility of character opening.
                        if rules.is_visible(caller, looker):
                            closer = (caller.key[0].upper() + caller.key[1:])
                        else:
                            closer = "Someone"

                        # As long as something was visible, give output.
                        looker.msg("%s closes %s" % (closer, door_string))

                
            # Add exit to objects to reset if not there already.
            reset_script = search.script_search("reset_script")[0]

            area = rules.get_area_name(door)
            
            if door not in reset_script.db.area_list[area]["resets"]:
                reset_script.db.area_list[area]["resets"].append(door)
                
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
         
            # This is making the grammatical string for referring to the opposite door in
            # output.
            if opposite_door.key == "north" or opposite_door.key == "east" or opposite_door.key == "south" \
                    or opposite_door.key == "west":
                opposite_door_string = ("door to the %s" % opposite_door.key)
            elif opposite_door.key == "up" or opposite_door.key == "down":
                opposite_door_string = ("door %s" % opposite_door.key)
            else:
                opposite_door_string = ("%s" % opposite_door.key)
            
            if "open" in opposite_door.db.door_attributes:
                opposite_door.db.door_attributes.remove("open")

            # Give output in that room.
            door.destination.msg_contents("The %s closes." % opposite_door_string)
                
            # Add exit to objects to reset if not there already.
            reset_script = search.script_search("reset_script")[0]
            area = rules.get_area_name(opposite_door)
            
            if door not in reset_script.db.area_list[area]["resets"]:
                reset_script.db.area_list[area]["resets"].append(opposite_door)

class CmdDoorUnlock(MuxCommand):
    """
    Unlock a door or a container in the room you are in.

    Usage:
      unlock <door>
      unlock <container>

    Unlocks the door or container permitting you to open it.
    """

    key = "unlock"
    aliases = ["unl"]
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
            
            if not rules.is_visible(container, caller):
                caller.msg("There is no %s here." % self.args)
                return               
                        
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
                
                # Deal with invisible objects/characters for output.
                # Assemble a list of all possible lookers.
                lookers = list(cont for cont in caller.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
                for looker in lookers:
                    # Exclude the caller, who got their output above.
                    if looker != caller:
                        # Address visibility of character opening.
                        if rules.is_visible(caller, looker):
                            unlocker = (caller.key[0].upper() + caller.key[1:])
                        else:
                            unlocker = "Someone"

                        # Address visibility of object opened.
                        if rules.is_visible(container, looker):
                            unlocked = container.key
                        else:
                            unlocked = "something"

                        # As long as something was visible, give output.
                        if unlocker != "Someone" or unlocked != "something":
                            looker.msg("*Click* %s unlocks %s" % (unlocker, unlocked))

            
            # Check if the container resets in the room. If so, add the room to objects to reset
            # if not there already.
            if container.db.vnum in container.location.db.reset_objects:
                reset_script = search.script_search("reset_script")[0]
                area = rules.get_area_name(container.location)
        
                if container.location not in reset_script.db.area_list[area]["resets"]:
                    reset_script.db.area_list[area]["resets"].append(container.location)        
            
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
                if door.key == "north" or door.key == "east" or door.key \
                        == "south" or door.key == "west":
                    door_string = "door to the %s" % door.key
                elif door.key == "up" or door.key == "down":
                    door_string = "door %s" % door.key
                else:
                    door_string = "%s" % door.key
                caller.msg("*Click* You unlock the %s." % door_string)
                
                # Deal with invisible objects/characters for output.
                # Assemble a list of all possible lookers.
                lookers = list(cont for cont in caller.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
                for looker in lookers:
                    # Exclude the caller, who got their output above.
                    if looker != caller:
                        # Address visibility of character opening.
                        if rules.is_visible(caller, looker):
                            unlocker = (caller.key[0].upper() + caller.key[1:])
                        else:
                            unlocker = "Someone"

                        # As long as something was visible, give output.
                        looker.msg("*Click* %s unlocks %s." % (unlocker, door_string))

            # Add exit to objects to reset if not there already.
            reset_script = search.script_search("reset_script")[0]
            area = rules.get_area_name(door)
            
            if door not in reset_script.db.area_list[area]["resets"]:
                reset_script.db.area_list[area]["resets"].append(door)
                    
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

            # This is making the grammatical string for referring to the opposite door in
            # output.
            if opposite_door.key == "north" or opposite_door.key == "east" or opposite_door.key == "south" \
                    or opposite_door.key == "west":
                opposite_door_string = ("door to the %s" % opposite_door.key)
            elif opposite_door.key == "up" or opposite_door.key == "down":
                opposite_door_string = ("door %s" % opposite_door.key)
            else:
                opposite_door_string = ("%s" % opposite_door.key)
            
            if "locked" in opposite_door.db.door_attributes:
                opposite_door.db.door_attributes.remove("locked")

            # Give output in that room.
            door.destination.msg_contents("*Click* The %s was unlocked." % opposite_door_string)
                
            # Add exit to objects to reset if not there already.
            reset_script = search.script_search("reset_script")[0]
            area = rules.get_area_name(opposite_door)
            
            if door not in reset_script.db.area_list[area]["resets"]:
                reset_script.db.area_list[area]["resets"].append(opposite_door)

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
            
            if not rules.is_visible(container, caller):
                caller.msg("There is no %s here." % self.args)
                return               
                        
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

                # Deal with invisible objects/characters for output.
                # Assemble a list of all possible lookers.
                lookers = list(cont for cont in caller.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
                for looker in lookers:
                    # Exclude the caller, who got their output above.
                    if looker != caller:
                        # Address visibility of character opening.
                        if rules.is_visible(caller, looker):
                            locker = (caller.key[0].upper() + caller.key[1:])
                        else:
                            locker = "Someone"

                        # Address visibility of object opened.
                        if rules.is_visible(container, looker):
                            locked = container.key
                        else:
                            locked = "something"

                        # As long as something was visible, give output.
                        if locker != "Someone" or locked != "something":
                            looker.msg("*Click* %s locks %s" % (locker, locked))

                
            # Check if the container resets in the room. If so, add the room to objects to reset
            # if not there already.
            if container.db.vnum in container.location.db.reset_objects:
                reset_script = search.script_search("reset_script")[0]
                area = rules.get_area_name(container.location)
        
                if container.location not in reset_script.db.area_list[area]["resets"]:
                    reset_script.db.area_list[area]["resets"].append(container.location)        
                
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
                    door_string = "door to the %s" % door.key
                elif door.key == "up" or door.key == "down":
                    door_string = "door %s" % door.key
                else:
                    door_string = "%s" % door.key
                caller.msg("*Click* You lock the %s." % door_string)
                
                # Deal with invisible objects/characters for output.
                # Assemble a list of all possible lookers.
                lookers = list(cont for cont in caller.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
                for looker in lookers:
                    # Exclude the caller, who got their output above.
                    if looker != caller:
                        # Address visibility of character opening.
                        if rules.is_visible(caller, looker):
                            locker = (caller.key[0].upper() + caller.key[1:])
                        else:
                            locker = "Someone"

                        # As long as something was visible, give output.
                        looker.msg("*Click* %s locks %s" % (locker, door_string))
                    
            # Add exit to objects to reset if not there already.
            reset_script = search.script_search("reset_script")[0]
            area = rules.get_area_name(door)
            
            if door not in reset_script.db.area_list[area]["resets"]:
                reset_script.db.area_list[area]["resets"].append(door)
                    
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

            # This is making the grammatical string for referring to the opposite door in
            # output.
            if opposite_door.key == "north" or opposite_door.key == "east" or opposite_door.key == "south" \
                    or opposite_door.key == "west":
                opposite_door_string = ("door to the %s" % opposite_door.key)
            elif opposite_door.key == "up" or opposite_door.key == "down":
                opposite_door_string = ("door %s" % opposite_door.key)
            else:
                opposite_door_string = ("%s" % opposite_door.key)
            
            if "locked" not in opposite_door.db.door_attributes:
                opposite_door.db.door_attributes.append("locked")

            # Give output in that room.
            door.destination.msg_contents("*Click* The %s was locked." % opposite_door_string)
                
            # Add exit to objects to reset if not there already.
            reset_script = search.script_search("reset_script")[0]
            area = rules.get_area_name(opposite_door)
            
            if door not in reset_script.db.area_list[area]["resets"]:
                reset_script.db.area_list[area]["resets"].append(opposite_door)


