"""

Lockfuncs

Lock functions are functions available when defining lock strings,
which in turn limits access to various game systems.

All functions defined globally in this module are assumed to be
available for use in lockstrings to determine access. See the
Evennia documentation for more info on locks.

A lock function is always called with two arguments, accessing_obj and
accessed_obj, followed by any number of arguments. All possible
arguments should be handled with *args, **kwargs. The lock function
should handle all eventual tracebacks by logging the error and
returning False.

Lock functions in this module extend (and will overload same-named)
lock functions from evennia.locks.lockfuncs.

"""

# def myfalse(accessing_obj, accessed_obj, *args, **kwargs):
#    """
#    called in lockstring with myfalse().
#    A simple logger that always returns false. Prints to stdout
#    for simplicity, should use utils.logger for real operation.
#    """
#    print "%s tried to access %s. Access denied." % (accessing_obj, accessed_obj)
#    return False

# lock function for checking whether a character is of sufficient level to
# wear/wield equipment

def equipment_level_check(accessing_obj, accessed_obj, *args, **kwargs):
    """
    lockstring called with equipment_level_check().
    checks to make sure user is of correct level.
    """

    if accessing_obj.db.level >= (accessed_obj.db.level - 5):
        return True
    return False

def is_open(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Lock function for checking whether a door or container is open.
    """

    if "object" in accessed_obj.tags.all():
        if "open" in accessed_obj.db.state:
            return True
        else:
            return False
    else:
        if "open" in accessed_obj.db.door_attributes:
            return True
        else:
            accessing_obj.msg("The door is closed in that direction.")
            return False

def can_open(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Lock function for checking whether a character can open a door or
    container.
    """

    if "object" in accessed_obj.tags.all():
        if not "open" in accessed_obj.db.state and not "locked" in \
                accessed_obj.db.state:
            return True
        return False
    else:
        if not "open" in accessed_obj.db.door_attributes and not "locked" in \
           accessed_obj.db.door_attributes:
                return True
        return False

def can_close(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Lock function for checking whether a character can close a door or
    container.
    """

    if "object" in accessed_obj.tags.all():
        if "open" in accessed_obj.db.state and "closeable" in \
                accessed_obj.db.state:
            return True
        return False
    else:
        if "open" in accessed_obj.db.door_attributes and "closeable" in \
           accessed_obj.db.door_attributes:
            return True
        return False

def can_lock(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Lock function for checking whether a character can unlock a door.
    """

    if "object" in accessed_obj.tags.all():
        if not "open" in accessed_obj.db.state \
                and not "locked" in accessed_obj.db.state \
                and "lockable" in accessed_obj.db.state \
                and accessing_obj.check_key(accessed_obj.db.key):
            return True
        return False
    else:
        if not "open" in accessed_obj.db.door_attributes \
           and not "locked" in accessed_obj.db.door_attributes \
           and "lockable" in accessed_obj.db.door_attributes \
           and accessing_obj.check_key(accessed_obj.db.key):
            return True
        else:
            return False

def can_unlock(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Lock function for checking whether a character can unlock a door.
    """

    if "object" in accessed_obj.tags.all():
        if not "open" in accessed_obj.db.state \
                and "locked" in accessed_obj.db.state \
                and accessing_obj.check_key(accessed_obj.db.key):
            return True
        return False
    else:
        if not "open" in accessed_obj.db.door_attributes \
           and "locked" in accessed_obj.db.door_attributes \
           and accessing_obj.check_key(accessed_obj.db.key):
            return True
        else:
            return False
