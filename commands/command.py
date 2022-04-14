"""
Commands

Commands describe the input the account can do to the game.

"""

import math
import re
import random
import time
from evennia import create_script
from evennia.commands.command import Command as BaseCommand
from evennia.utils import utils, search, evtable
from evennia.utils.ansi import raw as raw_ansi
from server.conf import settings
from world import rules, rules_skills

# from evennia import default_cmds


class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns anything truthy, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.

    """

    pass


# -------------------------------------------------------------
#
# The default commands inherit from
#
#   evennia.commands.default.muxcommand.MuxCommand.
#
# If you want to make sweeping changes to default commands you can
# uncomment this copy of the MuxCommand parent and add
#
#   COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
#
# to your settings file. Be warned that the default commands expect
# the functionality implemented in the parse() method, so be
# careful with what you change.
#
# -------------------------------------------------------------

class MuxCommand(Command):
    """
    This sets up the basis for a MUX command. The idea
    is that most other Mux-related commands should just
    inherit from this and don't have to implement much
    parsing of their own unless they do something particularly
    advanced.

    Note that the class's __doc__ string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.
    """

    delimiter = "="
    
    def has_perm(self, srcobj):
        """
        This is called by the cmdhandler to determine
        if srcobj is allowed to execute this command.
        We just show it here for completeness - we
        are satisfied using the default check in Command.
        """
        return super().has_perm(srcobj)

    def at_pre_cmd(self):
        """
        This hook is called before self.parse() on all commands
        """
        caller = self.caller
        if caller.ndb.wait_state:
            caller.msg("You are still recovering from your last action!")
            return True         # Returning true aborts the command.

    def at_post_cmd(self):
        """
        This hook is called after the command has finished executing
        (after self.func()).
        """
        caller = self.caller
        if "combat_handler" not in caller.ndb.all:
            if "wait_state" not in caller.ndb.all:
                prompt_wait = "|gReady!|n"
            elif caller.ndb.wait_state >= 12:
                prompt_wait = "|rCompleting action!"
            elif caller.ndb.wait_state > 0:
                prompt_wait = "|yRecovering.|n"
            else:
                prompt_wait = "|gReady!|n"
            prompt = "<|r%d|n/|R%d hp |b%d|n/|B%d mana |y%d|n/|Y%d moves|n %s>\n" % (caller.hitpoints_current,
                                                                                  caller.hitpoints_maximum,
                                                                                  caller.mana_current,
                                                                                  caller.mana_maximum,
                                                                                  caller.moves_current,
                                                                                  caller.moves_maximum,
                                                                                  prompt_wait)
            caller.msg(prompt = prompt)

    def parse(self):
        """
        This method is called by the cmdhandler once the command name
        has been identified. It creates a new set of member variables
        that can be later accessed from self.func() (see below)

        The following variables are available for our use when entering this
        method (from the command definition, and assigned on the fly by the
        cmdhandler):
           self.key - the name of this command ('look')
           self.aliases - the aliases of this cmd ('l')
           self.permissions - permission string for this command
           self.help_category - overall category of command

           self.caller - the object calling this command
           self.cmdstring - the actual command name used to call this
                            (this allows you to know which alias was used,
                             for example)
           self.args - the raw input; everything following self.cmdstring.
           self.cmdset - the cmdset from which this command was picked. Not
                         often used (useful for commands like 'help' or to
                         list all available commands etc)
           self.obj - the object on which this command was defined. It is often
                         the same as self.caller.

        A MUX command has the following possible syntax:

          name[ with several words][/switch[/switch..]] arg1[^ arg2^...] [[=|^]
              arg[^..]]

        The 'name[ with several words]' part is already dealt with by the
        cmdhandler at this point, and stored in self.cmdname (we don't use
        it here). The rest of the command is stored in self.args, which can
        start with the switch indicator /.

        This parser breaks self.args into its constituents and stores them in
        the following variables:
          self.switches = [list of /switches (without the /)]
          self.raw = This is the raw argument input, including switches
          self.args = This is re-defined to be everything *except* the switches
          self.lhs = Everything to the left of the delimiter (default "=") (lhs:'left-hand side'). If
                     no delimiter is found, this is identical to self.args.
          self.rhs: Everything to the right of the delimiter (rhs:'right-hand side').
                    If no delimiter is found, this is None.
          self.lhslist - [self.lhs split into a list by caret (was a comma)]
          self.rhslist - [list of self.rhs split into a list by caret (was a comma)]
          self.arglist = [list of space-separated args (stripped, including '='
              if it exists)]

          All args and list members are stripped of excess whitespace around
          the strings, but case is preserved.
        """
        raw = self.args
        args = raw.strip()

        # split out switches
        switches = []
        if args and len(args) > 1 and args[0] == "/":
            # we have a switch, or a set of switches. These end with a space.
            switches = args[1:].split(None, 1)
            if len(switches) > 1:
                switches, args = switches
                switches = switches.split('/')
            else:
                args = ""
                switches = switches[0].split('/')
        arglist = [arg.strip() for arg in args.split()]

        # check for arg1, arg2, ... = argA, argB, ... constructs
        lhs, rhs = args, None
        lhslist, rhslist = [arg.strip() for arg in args.split('^')], []
        # if args and self.delimiter in args:
        if args and self.delimiter in args:
            lhs, rhs = [arg.strip() for arg in args.split(self.delimiter, 1)]
            lhslist = [arg.strip() for arg in lhs.split('^')]
            rhslist = [arg.strip() for arg in rhs.split('^')]

        # save to object properties:
        self.raw = raw
        self.switches = switches
        self.args = args.strip()
        self.arglist = arglist
        self.lhs = lhs
        self.lhslist = lhslist
        self.rhs = rhs
        self.rhslist = rhslist

        # if the class has the account_caller property set on itself, we make
        # sure that self.caller is always the account if possible. We also
        # create a special property "character" for the puppeted object, if
        # any. This is convenient for commands defined on the Account only.
        if hasattr(self, "account_caller") and self.account_caller:
            if utils.inherits_from(
                                   self.caller,
                                   "evennia.objects.objects.DefaultObject"
                                   ):
                # caller is an Object/Character
                self.character = self.caller
                self.caller = self.caller.account
            elif utils.inherits_from(
                                     self.caller,
                                     "evennia.accounts.accounts.DefaultAccount"
                                     ):
                # caller was already an Account
                self.character = self.caller.get_puppet(self.session)
            else:
                self.character = None


class CmdAffects(MuxCommand):
    """
    Check all the spells that you are currently affected by.
    Usage:
      affects
    Will report all of the affects that currently exist on your
    character, what statistics they are impacting, if any, as
    well as the duration remaining on them.
    """

    key = "affects"
    aliases = ["aff"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implements the command."""

        caller = self.caller
        output_string = "You are currently affected by the following:\n"

        if caller.db.spell_affects:
            for affect in caller.db.spell_affects:
                # If all the affect has is duration.
                duration = math.ceil((caller.db.spell_affects[affect]["duration"] - time.time()) / settings.TICK_OBJECT_TIMER)
                if len(caller.db.spell_affects[affect]) == 1:
                    output_string += "     %s, for a duration of %d.\n" % ((affect[0].upper() + affect[1:]),
                                                                           duration
                                                                           )
                else:
                    apply = []
                    apply_amount = []
                    index = 0
                    for property in caller.db.spell_affects[affect]:
                        if property == "duration":
                            pass
                        else:
                            apply.append(property)
                            apply_amount.append(caller.db.spell_affects[affect][property])
                            index += 1
                    for apply_index in range(0, index):
                        output_string += "     %s, for a duration of %d, which impacts %s by %s.\n" % ((affect[0].upper() + affect[1:]),
                                                                                                    duration,
                                                                                                    apply[apply_index],
                                                                                                    apply_amount[apply_index],
                                                                                                    )
        else:
            output_string += "    Nothing!\n"

        caller.msg(output_string)


class CmdColleges(MuxCommand):
    """
    Provides you with a ranked list of the colleges in which you
    have currently learned skills.

    Usage:
      colleges

    Returns a ranked list of those colleges that you have learned
    skills in, where you are high enough level to have learned
    that skill in that college. Will not return colleges in which
    you have learned no skills.
    """

    key = "colleges"
    aliases = ["coll"]
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        """implements the actual functionality"""

        caller = self.caller

        if caller.db.skills:
            college_list = rules.classes_current(caller, all=True)

            college_output = "You currently have made progress in the following colleges:\n"\
                             "Colleges currently being considered for statistics are in |ggreen|n.\n\n"
            index = 1

            for college in college_list:
                if index <= int(caller.level / 20) + 1:
                    college_output += "     |g%d. %s|n\n" % (index, (college[0].upper() + college[1:]))
                else:
                    college_output += "     %d. %s\n" % (index, (college[0].upper() + college[1:]))
                index += 1

        if not caller.db.skills:
            caller.msg("You have not yet learned skills in any college yet.")
        else:
            caller.msg(college_output)


class CmdCSkills(MuxCommand):
    """
    Provides the skills that can be learned in each college, and
    at what level

    Usage:
      cskills <college>

    Provides a list of the levels at which skills can be learned
    in the given college. Cannot be used without an argument.

    """

    key = "cskills"
    aliases = ["csk"]
    locks = "cmd:all()"

    def func(self):
        """Implements the command."""

        caller = self.caller

        if not self.args:
            caller.msg("You must provide a college for which you want to see the skills.")
            return

        college = self.args.lower()

        skill_dictionary = rules_skills.get_skill(all=True)
        college_dictionary = {}

        for skill in skill_dictionary:
            if college in skill_dictionary[skill]["classes"]:
                level = skill_dictionary[skill]["classes"][college]
                if level in college_dictionary:
                    college_dictionary[level] += ", %s" % skill
                else:
                    college_dictionary[level] = skill

        if not college_dictionary:
            caller.msg("There is no %s college. Please try a real college." % college.capitalize())
        else:
            level_output_list = []
            skills_output_list = []
            for level in range(1, 102):
                if level in college_dictionary:
                    level_output_list.append(level)
                    skills_output_list.append(college_dictionary[level])

            table = evtable.EvTable("Level", "Skill(s)", table=[level_output_list, skills_output_list], border=None, width=80)
            table.reformat_column(0, width=7)

            caller.msg("The following skills are available in the %s college:\n%s" % (college.capitalize(), table))


class CmdDestroy(MuxCommand):
    """
    permanently delete objects
    Usage:
       destroy[/switches] [obj, obj2, obj3, [dbref-dbref], ...]
    Switches:
       override - The destroy command will usually avoid accidentally
                  destroying account objects. This switch overrides this safety.
       force - destroy without confirmation.
    Examples:
       destroy house, roof, door, 44-78
       destroy 5-10, flower, 45
       destroy/force north
    Destroys one or many objects. If dbrefs are used, a range to delete can be
    given, e.g. 4-10. Also the end points will be deleted. This command
    displays a confirmation before destroying, to make sure of your choice.
    You can specify the /force switch to bypass this confirmation.
    """

    key = "destroy"
    aliases = ["delete", "del"]
    switch_options = ("override", "force")
    locks = "cmd:perm(destroy) or perm(Builder)"
    help_category = "Building"

    confirm = True  # set to False to always bypass confirmation
    default_confirm = "yes"  # what to assume if just pressing enter (yes/no)

    def func(self):
        """Implements the command."""

        caller = self.caller
        delete = True

        if not self.args or not self.lhslist:
            caller.msg("Usage: destroy[/switches] [obj, obj2, obj3, [dbref-dbref],...]")
            delete = False

        def delobj(obj):
            # helper function for deleting a single object
            string = ""
            if not obj.pk:
                string = "\nObject %s was already deleted." % obj.db_key
            else:
                objname = obj.name
                if not (obj.access(caller, "control") or obj.access(caller, "delete")):
                    return "\nYou don't have permission to delete %s." % objname
                if obj.account and "override" not in self.switches:
                    return (
                        "\nObject %s is controlled by an active account. Use /override to delete anyway."
                        % objname
                    )
                if obj.dbid == int(settings.DEFAULT_HOME.lstrip("#")):
                    return (
                        "\nYou are trying to delete |c%s|n, which is set as DEFAULT_HOME. "
                        "Re-point settings.DEFAULT_HOME to another "
                        "object before continuing." % objname
                    )

                had_exits = hasattr(obj, "exits") and obj.exits
                had_objs = hasattr(obj, "contents") and any(
                    obj
                    for obj in obj.contents
                    if not (hasattr(obj, "exits") and obj not in obj.exits)
                )
                # do the deletion
                okay = obj.delete()
                if not okay:
                    string += (
                        "\nERROR: %s not deleted, probably because delete() returned False."
                        % objname
                    )
                else:
                    string += "\n%s was destroyed." % objname
                    if had_exits:
                        string += " Exits to and from %s were destroyed as well." % objname
                    if had_objs:
                        string += " Objects inside %s were moved to their homes." % objname
            return string

        objs = []
        for objname in self.lhslist:
            if not delete:
                continue

            if "-" in objname:
                # might be a range of dbrefs
                dmin, dmax = [utils.dbref(part, reqhash=False) for part in objname.split("-", 1)]
                if dmin and dmax:
                    for dbref in range(int(dmin), int(dmax + 1)):
                        obj = caller.search("#" + str(dbref))
                        if obj:
                            objs.append(obj)
                    continue
                else:
                    obj = caller.search(objname)
            else:
                obj = caller.search(objname)

            if obj is None:
                self.caller.msg(
                    " (Objects to destroy must either be local or specified with a unique #dbref.)"
                )
            elif obj not in objs:
                objs.append(obj)

        if objs and ("force" not in self.switches and type(self).confirm):
            confirm = "Are you sure you want to destroy "
            if len(objs) == 1:
                confirm += objs[0].get_display_name(caller)
            elif len(objs) < 5:
                confirm += ", ".join([obj.get_display_name(caller) for obj in objs])
            else:
                confirm += ", ".join(["#{}".format(obj.id) for obj in objs])
            confirm += " [yes]/no?" if self.default_confirm == "yes" else " yes/[no]"
            answer = ""
            answer = yield (confirm)
            answer = self.default_confirm if answer == "" else answer

            if answer and answer not in ("yes", "y", "no", "n"):
                caller.msg(
                    "Canceled: Either accept the default by pressing return or specify yes/no."
                )
                delete = False
            elif answer.strip().lower() in ("n", "no"):
                caller.msg("Canceled: No object was destroyed.")
                delete = False

        if delete:
            results = []
            for obj in objs:
                # All code under the if statement below added to 1) clean up equipped status on
                # equipment on mobiles being deleted, and 2) clean up equipment slots on
                # equipment being deleted.
                if obj.db.character_type == "mobile":
                    if not all(wear_location == "" for wear_location in obj.db.eq_slots.values()):
                        for wear_location in obj.db.eq_slots:
                            if obj.db.eq_slots[wear_location]:
                                equipment = obj.db.eq_slots[wear_location]
                                equipment.db.equipped = False
                #elif obj.db.equipped:
                #    wearer = obj.location
                #    if hasattr(wearer, eq_slots):
                #        for wear_location in wearer.db.eq_slots:
                #            if wearer.db.eq_slots[wear_location] == obj:
                #               wearer.db.eq_slots[wear_location] = ""
                results.append(delobj(obj))

            if results:
                caller.msg("".join(results).strip())


class CmdDrop(MuxCommand):
    """
    drop something
    Usage:
        drop <obj>
    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = "drop"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement command"""

        caller = self.caller
        if not self.args:
            caller.msg("Drop what?")
            return

        # First, find items on the caller, and filter out items
        # that are equipped.
        inventory = search.search_object(False, attribute_name="equipped", candidates=caller.contents)
        inventory = list(inventory)
        for item in caller.contents:
            if not item.attributes.has("equipped"):
                inventory.append(item)
        # Then search those for the item to be dropped.
        obj = caller.search(
            self.args,
            candidates=inventory,
            nofound_string="You aren't carrying %s." % self.args,
            multimatch_string="You carry more than one %s:" % self.args,
        )
        if not obj:
            return
        elif not rules.is_visible(obj, caller):
            caller.msg("You aren't carrying %s." % self.args)
            return

        # Check for the object being cursed to be undroppable.

        if not obj.access(caller, "drop") and caller.level < 104:
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("This object is cursed, and cannot be dropped.")
            return

        # Call the object script's at_before_drop() method.
        if not obj.at_before_drop(caller):
            return

        success = obj.move_to(caller.location, quiet=True)
        if not success:
            caller.msg("This couldn't be dropped.")
        else:
            if caller.db.level < 103:
                rules.set_disintegrate_timer(obj)
            caller.msg("You drop %s." % (obj.name,))
            caller.location.msg_contents("%s drops %s."
                                         % (caller.name, obj.name),
                                         exclude=caller)
            # Call the object script's at_drop() method.
            obj.at_drop(caller)


class CmdGet(MuxCommand):
    """
    Pick up something, or get something from a container.
    Usage:
      get <object>
      get <object> from <container>
    Picks up an object from your location or a container and puts it in
    your inventory.
    """

    key = "get"
    delimiter = " from "
    aliases = "grab"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        if not self.args:
            caller.msg("Get what?")
            return

        # Process getting from a container.
        if self.rhs:
            if not self.lhs:
                caller.msg("Get what from %s?" % self.rhs)
                return

            container = caller.search(self.rhs, location=[caller, caller.location])

            if not container:
                caller.msg("There is no %s here to get items from." % self.rhs)
                return
            elif not rules.is_visible(container, caller):
                caller.msg("There is no %s here to get items from." % self.args)
                return
            elif container.db.item_type != "container":
                caller.msg("%s is not a container." % (container.key[0].upper() + container.key[1:]))
                return
            elif not container.access(caller, "put"):
                if "open" not in container.db.state:
                    caller.msg("You can neither see in nor access %s while it is closed."
                               % container.key
                               )
                return

            get_list = []

            if self.lhs == "all":
                for object in container.contents:
                    if "object" in object.tags.all() and rules.is_visible(object, caller):
                        get_list.append(object)
                if not get_list:
                    caller.msg("There is nothing in %s to get." % container.key)
                    return
            else:
                get_list = []
                objects = []
                for object in container.contents:
                    if "object" in object.tags.all() and rules.is_visible(object, caller):
                        objects.append(object)
                object = caller.search(self.lhs, candidates=objects)
                get_list.append(object)
                if not object:
                    caller.msg("There is no %s in %s to get." % (self.lhs, container.key))
                    return

            for obj in get_list:

                get_output = ""
                get_output_room = ""

                if caller == obj:
                    get_output += "You can't get yourself.\n"
                elif not obj.access(caller, "get"):
                    if obj.db.get_err_msg:
                        get_output += "%s\n" % obj.db.get_err_msg
                    else:
                        get_output += "You can't get %s.\n" % obj.key

                if rules.carry_permitted(caller, obj) == "weight_fail":
                    caller.msg("You cannot carry that much weight!")
                    return
                elif rules.carry_permitted(caller, obj) == "number_fail":
                    caller.msg("Your hands are already full!")
                    return

                # calling at_before_get hook method
                elif not obj.at_before_get(caller):
                    pass

                else:
                    success = obj.move_to(caller, quiet=True)
                    if not success:
                        get_output += "%s can't be picked up.\n" % (obj.key[0].upper() + obj.key[1:])
                    else:
                        rules.remove_disintegrate_timer(obj)
                        get_output += "You take %s from %s.\n" % (obj.name, container.key)
                        get_output_room = "%s takes %s from %s.\n" % (caller.name, obj.name, container.key)
                        # calling at_get hook method
                        obj.at_get(caller)
                        
                        # Check if the object resets in the room. If so, add the room to objects to reset
                        # if not there already. Use caller.location since the object has already been gotten
                        # at this point.
                        if obj.db.vnum in caller.location.db.reset_objects:
                            reset_script = search.script_search("reset_script")
                            area = rules.get_area_name(caller.location)

                            if caller.location not in reset_script.db.area_list[area]["resets"]:
                                reset_script.db.area_list[area]["resets"].append(caller.location)   

                caller.msg(get_output)
                caller.location.msg_contents(
                    get_output_room, exclude=caller
                )

        # If just a regular get command.
        else:
            get_list = []
            if self.args == "all":
                for object in caller.location.contents:
                    if "object" in object.tags.all() and rules.is_visible(object, caller):
                        get_list.append(object)
                if not get_list:
                    caller.msg("There is nothing here to get.")
                    return

            else:
                get_list = []
                objects = []
                for object in caller.location.contents:
                    if "object" in object.tags.all() and rules.is_visible(object, caller):
                        objects.append(object)
                object = caller.search(self.args, candidates=objects)
                get_list.append(object)
                if not object:
                    caller.msg("There is no %s here to get." % self.args)
                    return

            for obj in get_list:

                get_output = ""
                get_output_room = ""

                if caller == obj:
                    get_output += "You can't get yourself.\n"
                elif not obj.access(caller, "get"):
                    if obj.db.get_err_msg:
                        get_output += "%s\n" % obj.db.get_err_msg
                    else:
                        get_output += "You can't get %s.\n" % obj.key

                if rules.carry_permitted(caller, obj) == "weight_fail":
                    caller.msg("You cannot carry that much weight!")
                    return
                elif rules.carry_permitted(caller, obj) == "number_fail":
                    caller.msg("Your hands are already full!")
                    return

                # calling at_before_get hook method
                elif not obj.at_before_get(caller):
                    pass

                else:
                    success = obj.move_to(caller, quiet=True)
                    if not success:
                        get_output += "%s can't be picked up.\n" % (obj.key[0].upper() + obj.key[1:])
                    else:
                        rules.remove_disintegrate_timer(obj)
                        get_output += "You pick up %s.\n" % obj.name
                        get_output_room = "%s picks up %s.\n" % (caller.name, obj.name)
                        # calling at_get hook method
                        obj.at_get(caller)
                        
                        # Check if the object resets in the room. If so, add the room to objects to reset
                        # if not there already. Use caller.location since the object has already been gotten
                        # at this point.
                        if obj.db.vnum in caller.location.db.reset_objects:
                            reset_script = search.script_search("reset_script")
                            area = rules.get_area_name(caller.location)

                            if caller.location not in reset_script.db.area_list[area]["resets"]:
                                reset_script.db.area_list[area]["resets"].append(caller.location)   

                caller.msg(get_output)
                caller.location.msg_contents(
                    get_output_room, exclude=caller
                )


class CmdGive(MuxCommand):
    """
    Give away something to someone.
    Usage:
      give <inventory obj> to <target>
    Gives an items from your inventory to another character,
    placing it in their inventory.
    """

    key = "give"
    delimiter = " to "
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement give"""

        caller = self.caller
        if not self.args or not self.rhs:
            caller.msg("Usage: give <inventory object> to <target>")
            return
        to_give = caller.search(
            self.lhs,
            location=caller,
            nofound_string="You aren't carrying %s." % self.lhs,
            multimatch_string="You carry more than one %s:" % self.lhs,
        )
        target = caller.search(self.rhs)
        if not (to_give and target):
            return
        elif not rules.is_visible(to_give, caller):
            caller.msg("You aren't carrying %s." % self.lhs)
            return
        elif not rules.is_visible(to_give, target):
            caller.msg("%s must be able to see %s to receive it." % ((target.key[0].upper() + target.key[1:]), object.key))
            return
        if target == caller:
            caller.msg("You keep %s to yourself." % to_give.key)
            return
        if not to_give.location == caller:
            caller.msg("You are not holding %s." % to_give.key)
            return

        if rules.carry_permitted(target, to_give) == "weight_fail":
            caller.msg("You cannot carry that much weight!")
            return
        elif rules.carry_permitted(target, to_give) == "number_fail":
            caller.msg("Your hands are already full!")
            return

        # calling at_before_give hook method
        if not to_give.at_before_give(caller, target):
            return

        # give object
        success = to_give.move_to(target, quiet=True)
        if not success:
            caller.msg("This could not be given.")
        else:
            caller.msg("You give %s to %s." % (to_give.key, target.key))
            if "player" in target.tags.all():
                target.msg("%s gives you %s." % (caller.key, to_give.key))
            # Call the target's at_give() method.
            target.at_give(caller, to_give)
            # Call the object's at_give() method.
            to_give.at_give(caller, target)

class CmdHome(MuxCommand):
    """
    Return to the room you have set to recall.
    Usage:
      recall
    If you are not in battle or otherwise in a cursed location, recall will
    allow you to swiftly jump to where you are currently set to recall, at
    the cost of a significant chunk of movement points. At present recall is
    only available to the Town Square in Eden's Grove.
    """

    key = "home"
    aliases = ["recall"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement the command"""
        caller = self.caller
        location = caller.location
        home = caller.home
        if not home:
            caller.msg("You do not currently have a recall location set!")
            return
        elif home == caller.location:
            caller.msg("You are already at your recall location!")
            return
        elif "no recall" in location.db.room_flags:
            caller.msg("This location is cursed! You cannot recall!")
            return
        elif "curse" in caller.db.spell_affects:
            caller.msg("You are cursed! You cannot recall!")
            return
        elif "combat_handler" in caller.ndb.all:
            caller.msg("You cannot focus enough to recall in combat!")
            return
        else:
            caller.msg("You close your eyes, cross your fingers and utter your word of recall ...")
            cost = int(caller.moves_current / 4)
            caller.moves_spent += cost
            caller.move_to(home)


class CmdInspect(MuxCommand):
    """
    Look more closely at an aspect of a room or object.
    Usage:
      inspect <room aspect>
      inspect <object aspect> on <object>
    Looks at extra descriptions that are on rooms or objects. Remember
    that this is not a replacement for using "look" at the objects
    themselves.
    """

    key = "inspect"
    aliases = ["read"]
    delimiter = " on "
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement inspect"""

        caller = self.caller
        if not self.args:
            caller.msg("Usage: inspect <room aspect> OR inspect <object aspect> on <object>")
            return

        if not self.rhs:
            room = caller.location
            for extra_keywords_string in room.db.extra_description:
                extra_keywords_list = extra_keywords_string.split()
                if self.args in extra_keywords_list:
                    caller.msg(
                        "You inspect the %s:\n%s" % (self.args, room.db.extra_description[extra_keywords_string]))
                    return

            caller.msg("You see nothing special about the %s." % self.args)
            return
        else:
            object = caller.search(self.rhs, location=(caller, caller.location))
            aspect = self.lhs

            if not object:
                caller.msg("There is no %s here." % self.lhs)
                return
            elif not rules.is_visible(object, caller):
                caller.msg("There is no %s here." % self.lhs)
                return
            else:
                for extra_keywords_string in object.db.extra_descriptions:
                    extra_keywords_list = extra_keywords_string.split()
                    if aspect in extra_keywords_list:
                        caller.msg("You closely inspect the %s on %s:\n%s" % (
                        self.lhs, object.key, object.db.extra_descriptions[extra_keywords_string]))
                        return
                caller.msg("You see nothing special about the %s on the %s." % (self.rhs, self.lhs))
                return


class CmdInventory(MuxCommand):
    """
    view inventory
    Usage:
      inventory
      inv
    Shows your inventory.
    """

    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        items = self.caller.contents
        if not items:
            string = "You are not carrying anything."
        else:
            table = self.styled_table(border="header")
            for item in items:
                if not item.db.equipped and rules.is_visible(item, self.caller):  # So equipped items don't show up.
                    table.add_row(
                        f"|C{item.name}|n",
                        "{}|n".format(utils.crop(raw_ansi(item.db.desc), width=50) or ""),
                    )
            string = f"|wYou are carrying:\n{table}"
        self.caller.msg(string)


class CmdLock(MuxCommand):
    """
    assign a lock definition to an object
    Usage:
      objectlock <object or *account>[ = <lockstring>]
      or
      objectlock[/switch] <object or *account>/<access_type>
    Switch:
      del - delete given access type
      view - view lock associated with given access type (default)
    If no lockstring is given, shows all locks on
    object.
    Lockstring is of the form
       access_type:[NOT] func1(args)[ AND|OR][ NOT] func2(args) ...]
    Where func1, func2 ... valid lockfuncs with or without arguments.
    Separator expressions need not be capitalized.
    For example:
       'get: id(25) or perm(Admin)'
    The 'get' lock access_type is checked e.g. by the 'get' command.
    An object locked with this example lock will only be possible to pick up
    by Admins or by an object with id=25.
    You can add several access_types after one another by separating
    them by ';', i.e:
       'get:id(25); delete:perm(Builder)'
    """

    key = "objectlock"
    aliases = ["olock"]
    locks = "cmd: perm(locks) or perm(Builder)"
    help_category = "Building"

    def func(self):
        """Sets up the command"""

        caller = self.caller
        if not self.args:
            string = (
                "Usage: lock <object>[ = <lockstring>] or lock[/switch] " "<object>/<access_type>"
            )
            caller.msg(string)
            return

        if "/" in self.lhs:
            # call of the form lock obj/access_type
            objname, access_type = [p.strip() for p in self.lhs.split("/", 1)]
            obj = None
            if objname.startswith("*"):
                obj = caller.search_account(objname.lstrip("*"))
            if not obj:
                obj = caller.search(objname)
                if not obj:
                    return
            has_control_access = obj.access(caller, "control")
            if access_type == "control" and not has_control_access:
                # only allow to change 'control' access if you have 'control' access already
                caller.msg("You need 'control' access to change this type of lock.")
                return

            if not (has_control_access or obj.access(caller, "edit")):
                caller.msg("You are not allowed to do that.")
                return

            lockdef = obj.locks.get(access_type)

            if lockdef:
                if "del" in self.switches:
                    obj.locks.delete(access_type)
                    string = "deleted lock %s" % lockdef
                else:
                    string = lockdef
            else:
                string = "%s has no lock of access type '%s'." % (obj, access_type)
            caller.msg(string)
            return

        if self.rhs:
            # we have a = separator, so we are assigning a new lock
            if self.switches:
                swi = ", ".join(self.switches)
                caller.msg(
                    "Switch(es) |w%s|n can not be used with a "
                    "lock assignment. Use e.g. "
                    "|wlock/del objname/locktype|n instead." % swi
                )
                return

            objname, lockdef = self.lhs, self.rhs
            obj = None
            if objname.startswith("*"):
                obj = caller.search_account(objname.lstrip("*"))
            if not obj:
                obj = caller.search(objname)
                if not obj:
                    return
            if not (obj.access(caller, "control") or obj.access(caller, "edit")):
                caller.msg("You are not allowed to do that.")
                return
            ok = False
            lockdef = re.sub(r"\'|\"", "", lockdef)
            try:
                ok = obj.locks.add(lockdef)
            except LockException as e:
                caller.msg(str(e))
            if "cmd" in lockdef.lower() and inherits_from(
                obj, "evennia.objects.objects.DefaultExit"
            ):
                # special fix to update Exits since "cmd"-type locks won't
                # update on them unless their cmdsets are rebuilt.
                obj.at_init()
            if ok:
                caller.msg("Added lock '%s' to %s." % (lockdef, obj))
            return

        # if we get here, we are just viewing all locks on obj
        obj = None
        if self.lhs.startswith("*"):
            obj = caller.search_account(self.lhs.lstrip("*"))
        if not obj:
            obj = caller.search(self.lhs)
        if not obj:
            return
        if not (obj.access(caller, "control") or obj.access(caller, "edit")):
            caller.msg("You are not allowed to do that.")
            return
        caller.msg("\n".join(obj.locks.all()))


class CmdLook(MuxCommand):
    """
    look at location or object
    Usage:
        look
        look <obj>
        look *<account>
    Observes your location or objects in your vicinity.
    """

    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        if caller.db.position == "sleeping":
            caller.msg("Look at what? Your eyelids? You are sleeping!")
            return
        elif not self.args:
            target = caller.location
            if not target:
                caller.msg("You have no location to look at!")
                return
        else:
            target = caller.search(self.args)
            if not target:
                return
            elif not rules.is_visible(target, caller):
                return
        self.msg((caller.at_look(target), {"type": "look"}), options=None)

        # Check to see if the target is a character (or mobile), and if so
        # get and show their equipment.


class CmdPut(MuxCommand):
    """
    Put something in a container.
    Usage:
      put <inventory obj> in <target>
    Puts an item from your inventory in a container,
    placing it in its inventory.
    """

    key = "put"
    delimiter = " in "
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement put"""

        caller = self.caller
        if not self.args or not self.rhs:
            caller.msg("Usage: put <inventory object> in <target>")
            return
        to_put = caller.search(
            self.lhs,
            location=caller,
            nofound_string="You aren't carrying %s." % self.lhs,
            multimatch_string="You carry more than one %s:" % self.lhs,
        )

        if not to_put:
            return
        elif not rules.is_visible(to_put, caller):
            caller.msg("You aren't carrying %s." % self.lhs)
            return
        
        # For ease of programming reasons, you cannot put a container in
        # another container.
        if to_put.db.item_type == "container" and to_put.contents:
            caller.msg("You cannot put a container with items in it in another container.")
            return

        target = caller.search(self.rhs, 
                               location=[caller, caller.location],
                               nofound_string="There is no %s here." % self.rhs,
                               multimatch_string="There is more than one %s here:" % self.rhs
                               )

        if not target:
            return
        elif not rules.is_visible(target, caller):
            caller.msg("There is no %s here." % self.rhs)
            return

        if not (to_put and target):
            return
        if "object" not in target.tags.all() or target.db.item_type != "container":
            caller.msg("%s is not a container." % (target.key[0].upper() + target.key[1:]))
            return

        # Check to see if the locks for put are met, and give corrective
        # output if not.
        if not target.access(caller, "put"):
            if "locked" in target.db.state:
                caller.msg("%s is locked." % (target.key[0].upper() + target.key[1:]))
            elif "open" not in target.db.state:
                caller.msg("%s is closed." % (target.key[0].upper() + target.key[1:]))
            return

        if rules.carry_permitted(target, to_put) == "weight_fail":
            caller.msg("%s cannot contain that much weight." % (target.key[0].upper() + target.key[1:]))
            return

        # Put object in the container.
        success = to_put.move_to(target, quiet=True)
        if not success:
            caller.msg("This could not be put there.")
        else:
            caller.msg("You put %s in %s." % (to_put.key, target.key))


class CmdRepop(MuxCommand):
    """
    Repopulate an area in the MUD, or all areas in the MUD.

    Usage:
      repop <area>

    Returns the area argument to its initial configuration. With no argument,
    it will repopulate all areas.
    """

    key = "repop"
    locks = "cmd:perm(Admin)"
    arg_regex = r"\s|$"

    def func(self):
        """
        The main body of the area repopulating function.
        """

        caller = self.caller

        # If an area is given, get all objects that are tagged with the area
        # name.
        if self.args:

            objects_to_reset = search.search_tag(self.args,
                                                 category="area name")

            if not objects_to_reset:
                caller.msg("There are no objects in %s."
                           % self.args)
                return

        # Otherwise, get all objects.
        else:
            objects_to_reset = search.search_tag(category="area name")

        # iterate through and reset all objects
        for object in objects_to_reset:
            object.at_reset()

        if self.args:
            caller.msg("The %s area has been reset." % self.args)
        else:
            caller.msg("All areas have been reset.")


class CmdRest(MuxCommand):
    """
    Cause your character to sit down and rest.

    Usage:
      rest

    Causes your character to sit down and rest. Resting causes less of an
    increase in hit point, mana and move regeneration than sleeping, with
    the trade-off of no increased risk of damage.
    """

    key = "rest"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        if caller.ndb.combat_handler:
            caller.msg("You cannot rest while you are fighting!")
            return
        if caller.position == "resting":
            caller.msg("If you want to rest more, try sleeping.")
            return

        if caller.position == "standing":
            caller.msg("You sit down and rest your tired bones.")
            caller.location.msg_contents("%s sits down and rests." % (caller.name), exclude=caller)
        elif caller.position == "sitting":
            caller.msg("You convert from a seated position into a more comfortable rest.")
            caller.location.msg_contents("%s readjusts and rests." % (caller.name), exclude=caller)
        else:
            caller.msg("You wake, sit up and rest.")
            caller.location.msg_contents("%s awakens and sits up to rest." % (caller.name), exclude=caller)
        caller.position = "resting"


class CmdSacrifice(MuxCommand):
    """
    Offer up an object as a sacrifice to the gods.
    Usage:
        sacrifice <obj>
    Allows you to destroy an object on the ground in exchange for the
    possibility of a gift of hitpoints, mana, moves or gold from the
    gods. The gods do like a clean MUD, after all.
    """

    key = "sacrifice"
    aliases = ["sac"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement command"""

        caller = self.caller
        if not self.args:
            caller.msg("What would you like to sacrifice?")
            return

        obj = caller.search(
            self.args,
            location=caller.location,
            nofound_string="There is no %s here to sacrifice." % self.args,
            multimatch_string="There is more than one %s here:" % self.args,
        )
        if not obj:
            return
        elif not rules.is_visible(obj, caller):
            caller.msg("There is no %s here to sacrifice." % self.args)
            return

        # Check for the object not being get-able, which can't be sacrificed.

        if not obj.access(caller, "get"):
            caller.msg("That is not available for sacrifice.")
            return

        if obj.contents and "npc corpse" not in obj.tags.all():
            caller.msg("You cannot sacrifice a container with objects inside.")
            return

        if obj.db.item_type == "food":
            caller.msg("The gods appreciate your addition to their feast table.")
            obj.location = None
            rules.remove_disintegrate_timer(obj)
            caller.location.msg_contents("%s sacrifices %s to the gods."
                                         % (caller.name, obj.name),
                                         exclude=caller)
            return



        award = random.randint(1, 3)

        # Once we implement gold, go back for gold awards. Code
        # is in act_obj

        if award == 1:
            if caller.hitpoints_damaged > 20:
                hitpoint_award_max = 20
            else:
                hitpoint_award_max = caller.hitpoints_damaged
            award_amount = random.randint(0, hitpoint_award_max)
            if award_amount == 1:
                award = "hitpoint"
            else:
                award = "hitpoints"
            if award_amount != 0:
                caller.hitpoints_damaged -= award_amount
        elif award == 2:
            if caller.mana_spent > 20:
                mana_award_max = 20
            else:
                mana_award_max = caller.mana_spent
            award_amount = random.randint(0, mana_award_max)
            award = "mana"
            if award_amount != 0:
                caller.mana_spent -= award_amount
        else:
            if caller.moves_spent > 20:
                moves_award_max = 20
            else:
                moves_award_max = caller.moves_spent
            award_amount = random.randint(0, moves_award_max)
            if award_amount == 1:
                award = "move"
            else:
                award = "moves"
            if award_amount != 0:
                caller.moves_spent -= award_amount

        if award_amount > 0:
            caller.msg("You build a small pyre and sacrifice %s to the gods.\n"
                       "The gods award you %d %s for your sacrifice." % (obj.name, award_amount, award))
        else:
            caller.msg("You build a small pyre and sacrifice %s to the gods.\n"
                       "The gods are pleased with your sacrifice." % obj.name)

        if obj.contents:
            for item in obj.contents:
                item.location = None
        
        # Check if the object resets in the room. If so, add the room to objects to reset
        # if not there already. Use caller.location since the object has already been gotten
        # at this point.
        if obj.db.vnum in obj.location.db.reset_objects:
            reset_script = search.script_search("reset_script")
            area = rules.get_area_name(obj.location)

            if caller.location not in reset_script.db.area_list[area]["resets"]:
                reset_script.db.area_list[area]["resets"].append(obj.location)   
        
        obj.location = None
        
        
        
        rules.remove_disintegrate_timer(obj)
        caller.location.msg_contents("%s builds a small pyre, and sacrifices %s to the gods."
                                         % (caller.name, obj.name),
                                         exclude=caller)


class CmdSay(MuxCommand):
    """
    speak as your character
    Usage:
      say <message>
    Talk to those in your current location.
    """

    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"

    def func(self):
        """Run the say command"""

        caller = self.caller

        if not self.args:
            caller.msg("Say what?")
            return

        speech = self.args

        # Calling the at_before_say hook on the character
        speech = caller.at_before_say(speech)

        # If speech is empty, stop here
        if not speech:
            return

        # Call the at_after_say hook on the character
        caller.at_say(speech, msg_self=True)

        # Call the at_after_say hook on the location and its contents.
        # Primarily for scripts.
        caller.location.at_after_say(caller, speech)
        for object in caller.location.contents:
            if "mobile" in object.tags.all() or "object" in object.tags.all():
                object.at_after_say(caller, speech)

                
class CmdScan(MuxCommand):
    """
    Scan your surroundings to look for threats.
    Usage:
      scan
    Scan will look up to three rooms away in each of the cardinal directions,
    and let you know any of the mobiles that you would be able to see if you
    were in that room.
    """

    key = "scan"
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement the command"""
        caller = self.caller
        room = caller.location

        def get_mobiles(player, room):

            mobile_list = []
            for object in room.contents:
                if "mobile" in object.tags.all():
                    if rules.is_visible(object, player):
                        mobile_list.append(object)
            return mobile_list

        def scan_direction(caller, exit, direction):
            scan_string = ""

            mobiles = get_mobiles(caller, exit.destination)
            if mobiles:
                for mobile in mobiles:
                    if direction != "up" and direction != "down":
                        scan_string += "%s is immediately to the %s.\n" % ((mobile.key[0].upper() + mobile.key[1:]), direction)
                    else:
                        scan_string += "%s is immediately %s.\n" % ((mobile.key[0].upper() + mobile.key[1:]), direction)
            room = exit.destination
            next_exit = ""
            for new_exit in room.exits:
                if new_exit.key == direction and "open" in new_exit.db.door_attributes:
                    next_exit = new_exit
                    mobiles = get_mobiles(caller, new_exit.destination)
                    if mobiles:
                        for mobile in mobiles:
                            if direction != "up" and direction != "down":
                                scan_string += "%s is a short distance to the %s.\n" % ((mobile.key[0].upper() + mobile.key[1:]), direction)
                            else:
                                scan_string += "%s is a short distance %s.\n" % ((mobile.key[0].upper() + mobile.key[1:]), direction)
                    room = new_exit.destination
            if next_exit:
                for new_exit in room.exits:
                    if new_exit.key == direction and "open" in new_exit.db.door_attributes:
                        mobiles = get_mobiles(caller, exit.destination)
                        if mobiles:
                            for mobile in mobiles:
                                if direction != "up" and direction != "down":
                                    scan_string += "%s is some distance to the %s.\n" % ((mobile.key[0].upper() + mobile.key[1:]), direction)
                                else:
                                    scan_string += "%s is some distance %s.\n" % ((mobile.key[0].upper() + mobile.key[1:]), direction)
            return scan_string
        
        output_string = ""
        
        for exit in room.exits:
            if exit.key == "north" and "open" in exit.db.door_attributes:
                output_string += scan_direction(caller, exit, "north")
            elif exit.key == "east" and "open" in exit.db.door_attributes:
                output_string += scan_direction(caller, exit, "east")
            elif exit.key == "south" and "open" in exit.db.door_attributes:
                output_string += scan_direction(caller, exit, "south")
            elif exit.key == "west" and "open" in exit.db.door_attributes:
                output_string += scan_direction(caller, exit, "west")
            elif exit.key == "up" and "open" in exit.db.door_attributes:
                output_string += scan_direction(caller, exit, "up")
            elif exit.key == "down" and "open" in exit.db.door_attributes:
                output_string += scan_direction(caller, exit, "down")

        if not output_string:
            output_string = "There are no mobiles within your view."

        caller.msg(output_string)
        
        
class CmdScore(MuxCommand):
    """
    List abilities

    Usage:
       score

    Displays a formatted chart showing all of your relevant statistics.
    """
    key = "score"
    aliases = ["sc"]
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        """implements the actual functionality"""

        caller = self.caller

        strength, dexterity, intelligence, wisdom, constitution, \
            hitpoints_current, hitpoints_maximum, mana_current, mana_maximum, \
            moves_current, moves_maximum, sex, race, died, kills, \
            maximum_damage, maximum_kill_experience, hitroll, \
            experience_total, experience_spent, damroll, gold, bank_balance, \
            armor_class, alignment, saving_throw, staff_position, \
            immortal_invisible, immortal_cloak, immortal_ghost, holy_light, \
            level, age, wimpy, items, weight, maximum_damage_mobile, maximum_kill_experience_mobile = self.caller.get_score_info()

        unspent_experience = experience_total - experience_spent
        experience_to_level = experience_total
        experience_in_level = experience_total

        modified_strength = caller.get_modified_attribute("strength")
        modified_intelligence = caller.get_modified_attribute("intelligence")
        modified_wisdom = caller.get_modified_attribute("wisdom")
        modified_dexterity = caller.get_modified_attribute("dexterity")
        modified_constitution = caller.get_modified_attribute("constitution")

        hit_points_string = ("%s/%s" % (hitpoints_current, hitpoints_maximum))
        mana_string = ("%s/%s" % (mana_current, mana_maximum))
        moves_string = ("%s/%s" % (moves_current, moves_maximum))
        name_and_title = self.caller

        score = ""
        buffer = ("|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-"
                  "|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w="
                  "|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-"
                  "|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|x\n|w| "
                  "|cName: |W%-40s                        |w|\n|w| |cLevel: "
                  "|W%-12d          |cRace: |W%-12s         |cAge: |W%-3d    "
                  "  |w|\n" % (name_and_title, level, race, age))
        score = score + buffer

        if level > 101:
            buffer = ("|w| |cStaff Position: |w%-15s                      "
                      "|w|\n" % staff_position)
            score = score + buffer

        buffer = ("|C======================================================"
                  "===================|W\n|w| |cStr: |w%-2d(|G%-2d|c)       "
                  "|c     Hit Points: |w%-14s     |cWimpy: |w%-4d     |w|\n"
                  % (strength, modified_strength, hit_points_string, wimpy))
        score = score + buffer

        buffer = ("|w| |cInt: |w%-2d|c(|G%-2d|c)                  |cMana:"
                  " |w%-15s     |cDied: |r%-6d   |w|\n"
                  % (intelligence, modified_intelligence, mana_string, died))
        score = score + buffer

        buffer = ("|w| |cWis: |w%-2d|c(|G%-2d|c)                 |cMoves:"
                  " |w%-15s    |cKills: |w%-9d|w|\n"
                  % (wisdom, modified_wisdom, moves_string, kills))
        score = score + buffer

        buffer = ("|w| |cDex: |w%-2d|c(|G%-2d|c)         |cItems carried: "
                  "|w%-5d     |cWeight carried: |w%-9d|w|\n"
                  % (dexterity, modified_dexterity, items, weight))
        score = score + buffer

        buffer = ("|w| |cCon: |w%-2d|c(|G%-2d|c)               |cHitroll: |w%-8d         |cDamroll: |w%-5d    |w|\n"
                  % (
                      constitution,
                      modified_constitution,
                      hitroll, damroll
                     ))
        score = score + buffer

        buffer = ("|w| |cExperience: |w%-12d|c     |cGold: |y%-10d  "
                  "|cBank Balance: |y%-6d   |w|\n"
                  % (
                      unspent_experience,
                      gold, bank_balance
                     ))
        score = score + buffer

        buffer = ("|w| |C---------------------------------------------------"
                  "------------------ |w|\n")
        score = score + buffer

        buffer = ("|w| |cArmor Class: |w%-5d              |cAlignment: |w%-5d"
                  "                      |w|\n" % (armor_class, alignment))
        score = score + buffer

        buffer = ("|w| |cSaving throw: |w%-4d                           "
                  "                         |w|\n" % saving_throw)
        score = score + buffer

        buffer = ("|w| |C---------------------------------------------------"
                  "------------------ |w|\n")
        score = score + buffer

        if maximum_damage:

            buffer = ("|w| |cMax Damage: |w%-13d   |cAgainst: |w%-33s|w|\n"
                      % (maximum_damage, (maximum_damage_mobile[0].upper() + maximum_damage_mobile[1:])))
            score = score + buffer
        else:
            buffer = ("|w| |cMax Damage: |w%-13d   |cAgainst: |w%-33s|w|\n"
                      % (0, "None"))
            score = score + buffer

        if maximum_kill_experience:
            buffer = ("|w| |cMax Experience: |w%-9d   |cAgainst: |w%-33s|w|\n"
                      % (maximum_kill_experience, (maximum_kill_experience_mobile[0].upper() + maximum_kill_experience_mobile[1:])))
            score = score + buffer
        else:
            buffer = ("|w| |cMax Experience: |w%-9d   |cAgainst: |w%-33s|w|\n"
                      % (0, "None"))
            score = score + buffer

        if level > 101:
            buffer = ("|w| |cHoly Light: |w%-3d       |cInvis: |w%-3d     |c"
                      "Cloak: |w%-3d    |cGhost: |w%-3d |w|\n"
                      % (
                          holy_light,
                          immortal_invisible,
                          immortal_cloak,
                          immortal_ghost
                         ))
            score = score + buffer

        score = score + ("|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-"
                         "|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w="
                         "|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-"
                         "|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w=|c-|w="
                         "|c-|w=|c-|w=|c-|x")

        self.caller.msg(score)


class CmdSetHome(MuxCommand):
    """
    set an object's home location
    Usage:
      sethome <obj> [= <home_location>]
      sethom <obj>
    Switches:
      global - attempts to set home on an object not in the room.
    The "home" location is a "safety" location for objects; they
    will be moved there if their current location ceases to exist. All
    objects should always have a home location for this reason.
    It is also a convenient target of the "home" command.
    If no location is given, just view the object's home location.
    """

    key = "sethome"
    locks = "cmd:perm(sethome) or perm(Builder)"
    help_category = "Building"

    def func(self):
        """implement the command"""
        if not self.args:
            string = "Usage: sethome <obj> [= <home_location>]"
            self.caller.msg(string)
            return

        if "global" in self.switches:
            obj = self.caller.search(self.lhs, global_search=True)
        else:
            obj = self.caller.search(self.lhs, global_search=False)
        if not obj:
            return
        if not self.rhs:
            # just view
            home = obj.home
            if not home:
                string = "This object has no home location set!"
            else:
                string = "%s's current home is %s(%s)." % (obj, home, home.dbref)
        else:
            # set a home location
            if "global" in self.switches:
                new_home = self.caller.search(self.rhs, global_search=True)
            else:
                new_home = self.caller.search(self.rhs, global_search=False)
            if not new_home:
                return
            old_home = obj.home
            obj.home = new_home
            if old_home:
                string = "Home location of %s was changed from %s(%s) to %s(%s)." % (
                    obj,
                    old_home,
                    old_home.dbref,
                    new_home,
                    new_home.dbref,
                )
            else:
                string = "Home location of %s was set to %s(%s)." % (obj, new_home, new_home.dbref)
        self.caller.msg(string)


class CmdSleep(MuxCommand):
    """
    Cause your character to go to sleep.

    Usage:
      sleep

    Causes your character to go to sleep. Sleeping causes an increase in
    hit point, mana and move regeneration, but leaves you vulnerable to
    attack.
    """

    key = "sleep"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        if caller.ndb.combat_handler:
            caller.msg("You cannot sleep while you are fighting!")
            return
        elif caller.db.position == "sleeping":
            caller.msg("You are sleeping as well as you can already.")
            return

        if caller.db.position == "standing":
            caller.msg("You find a comfortable spot, lay your head down, and drift off to sleep.")
            caller.location.msg_contents("%s lays down and falls asleep." % (caller.name), exclude=caller)
        else:
            caller.msg("More tired than you thought, you lay your head down, and drift off to sleep.")
            caller.location.msg_contents("%s lays down and falls asleep." % (caller.name), exclude=caller)

        caller.position = "sleeping"


class CmdStand(MuxCommand):
    """
    Cause your character to stand up, and stop sleeping or resting.

    Usage:
      rest

    Causes your character to stand up and stop sleeping or resting. Has no
    effect on a character that is fighting.
    """

    key = "stand"
    aliases = ['wake']
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        if caller.position == "fighting":
            caller.msg("You are already standing and fighting!")
            return
        if caller.position == "standing":
            caller.msg("You can't stand any more than you are already.")
            return

        if caller.position == "sleeping":
            caller.msg("You wake up and stand up, ready for more.")
            caller.location.msg_contents("%s wakes up and stands up." % (caller.name), exclude=caller)
        elif caller.position == "resting":
            caller.msg("You stop resting and stand up, ready for action.")
            caller.location.msg_contents("%s stands up." % (caller.name), exclude=caller)
        else:
            caller.msg("You stand up, ready for action.")
            caller.location.msg_contents("%s leaps back to %s feet." % (caller.name, rules.pronoun_possessive(caller)), exclude=caller)

        caller.position = "standing"


class CmdTag(MuxCommand):
    """
    handles the tags of an object, defaults to objects in the room.
    Usage:
      tag[/del] <obj> [= <tag>[:<category>]]
      tag/search <tag>[:<category]
    Switches:
      global - attempts to set a tag on an object not in the room.
      search - return all objects with a given Tag
      del - remove the given tag. If no tag is specified,
            clear all tags on object.
    Manipulates and lists tags on objects. Tags allow for quick
    grouping of and searching for objects.  If only <obj> is given,
    list all tags on the object.  If /search is used, list objects
    with the given tag.
    The category can be used for grouping tags themselves, but it
    should be used with restrain - tags on their own are usually
    enough to for most grouping schemes.
    """

    key = "tag"
    aliases = ["tags"]
    options = ("search", "del", "global")
    locks = "cmd:perm(tag) or perm(Builder)"
    help_category = "Building"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        """Implement the tag functionality"""

        if not self.args:
            self.caller.msg("Usage: tag[/switches] <obj> [= <tag>[:<category>]]")
            return
        if "search" in self.switches:
            # search by tag
            tag = self.args
            category = None
            if ":" in tag:
                tag, category = [part.strip() for part in tag.split(":", 1)]
            objs = search.search_tag(tag, category=category)
            nobjs = len(objs)
            if nobjs > 0:
                catstr = (
                    " (category: '|w%s|n')" % category
                    if category
                    else ("" if nobjs == 1 else " (may have different tag categories)")
                )
                matchstr = ", ".join(o.get_display_name(self.caller) for o in objs)

                string = "Found |w%i|n object%s with tag '|w%s|n'%s:\n %s" % (
                    nobjs,
                    "s" if nobjs > 1 else "",
                    tag,
                    catstr,
                    matchstr,
                )
            else:
                string = "No objects found with tag '%s%s'." % (
                    tag,
                    " (category: %s)" % category if category else "",
                )
            self.caller.msg(string)
            return
        if "del" in self.switches:
            # remove one or all tags
            obj = self.caller.search(self.lhs, global_search=True)
            if not obj:
                return
            if self.rhs:
                # remove individual tag
                tag = self.rhs
                category = None
                if ":" in tag:
                    tag, category = [part.strip() for part in tag.split(":", 1)]
                if obj.tags.get(tag, category=category):
                    obj.tags.remove(tag, category=category)
                    string = "Removed tag '%s'%s from %s." % (
                        tag,
                        " (category: %s)" % category if category else "",
                        obj,
                    )
                else:
                    string = "No tag '%s'%s to delete on %s." % (
                        tag,
                        " (category: %s)" % category if category else "",
                        obj,
                    )
            else:
                # no tag specified, clear all tags
                old_tags = [
                    "%s%s" % (tag, " (category: %s)" % category if category else "")
                    for tag, category in obj.tags.all(return_key_and_category=True)
                ]
                if old_tags:
                    obj.tags.clear()
                    string = "Cleared all tags from %s: %s" % (obj, ", ".join(sorted(old_tags)))
                else:
                    string = "No Tags to clear on %s." % obj
            self.caller.msg(string)
            return
        # no search/deletion, global search
        if "global" in self.switches:
            if self.rhs:
                # = is found; command args are of the form obj = tag
                obj = self.caller.search(self.lhs, global_search=True)
                if not obj:
                    return
                tag = self.rhs
                category = None
                if ":" in tag:
                    tag, category = [part.strip() for part in tag.split(":", 1)]
                # create the tag
                obj.tags.add(tag, category=category)
                string = "Added tag '%s'%s to %s." % (
                    tag,
                    " (category: %s)" % category if category else "",
                    obj,
                )
                self.caller.msg(string)
            else:
                # no = found - list tags on object
                obj = self.caller.search(self.args, global_search=True)
                if not obj:
                    return
                tagtuples = obj.tags.all(return_key_and_category=True)
                ntags = len(tagtuples)
                tags = [tup[0] for tup in tagtuples]
                categories = [" (category: %s)" % tup[1] if tup[1] else "" for tup in tagtuples]
                if ntags:
                    string = "Tag%s on %s: %s" % (
                        "s" if ntags > 1 else "",
                        obj,
                        ", ".join(sorted("'%s'%s" % (tags[i], categories[i]) for i in range(ntags))),
                    )
                else:
                    string = "No tags attached to %s." % obj
                self.caller.msg(string)
        else:
            # Standard default tagging in room.
            if self.rhs:
                # = is found; command args are of the form obj = tag
                obj = self.caller.search(self.lhs, global_search=False)
                if not obj:
                    return
                tag = self.rhs
                category = None
                if ":" in tag:
                    tag, category = [part.strip() for part in tag.split(":", 1)]
                # create the tag
                obj.tags.add(tag, category=category)
                string = "Added tag '%s'%s to %s." % (
                    tag,
                    " (category: %s)" % category if category else "",
                    obj,
                )
                self.caller.msg(string)
            else:
                # no = found - list tags on object
                obj = self.caller.search(self.args, global_search=False)
                if not obj:
                    return
                tagtuples = obj.tags.all(return_key_and_category=True)
                ntags = len(tagtuples)
                tags = [tup[0] for tup in tagtuples]
                categories = [" (category: %s)" % tup[1] if tup[1] else "" for tup in tagtuples]
                if ntags:
                    string = "Tag%s on %s: %s" % (
                        "s" if ntags > 1 else "",
                        obj,
                        ", ".join(sorted("'%s'%s" % (tags[i], categories[i]) for i in range(ntags))),
                    )
                else:
                    string = "No tags attached to %s." % obj
                self.caller.msg(string)


class CmdTalk(MuxCommand):
    """
    Talk to a mobile to see what they have to say.
    Usage:
      talk <mobile>
    Talks to a mobile.
    """

    key = "talk"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement talk"""

        caller = self.caller
        if not self.args:
            caller.msg("Who do you want to talk to?")
            return

        to_talk = caller.search(
            self.args,
            location=caller.location,
            nofound_string="There is no %s here." % self.args,
            multimatch_string="There is more than one %s here:" % self.args,
        )

        if not to_talk:
            return
        elif not rules.is_visible(to_talk, caller):
            caller.msg("There is no %s here." % self.args)
            return

        if to_talk == caller:
            caller.msg("You mutter away to yourself quietly.")
            return
        if "mobile" not in to_talk.tags.all():
            caller.msg("Try talking to a mobile.")
            return
        else:
            if to_talk.db.character_type != "mobile":
                caller.msg("Talk cannot be used on other players. Try say or tell.")
                return
            else:
                quest_status = "done"
                # Talk to the mobile.
                if to_talk.db.quests:
                    if not caller.db.quests:
                        caller.db.quests = {}

                    for quest in to_talk.db.quests:
                        if quest not in caller.db.quests:
                            quest_status = "not done"
                            break
                        else:
                            if caller.db.quests[quest] != "done":
                                quest_status = "not done"
                                break

                if quest_status == "done":
                    if to_talk.db.talk:
                        caller.msg('You strike up a conversation with %s.\n%s says, "%s"' % (to_talk.key, (to_talk.key[0].upper() + to_talk.key[1:]), to_talk.db.talk))
                    else:
                        caller.msg("%s chatters along about nothing for a while." % to_talk.key)
                else:
                    for quest in to_talk.db.quests:
                        if quest not in caller.db.quests:
                            if "talk" in to_talk.db.quests[quest]:
                                quest_script = create_script(to_talk.db.quests[quest]["talk"], obj=to_talk)
                                quest_script.db.player = caller
                                quest_script.quest_talk()
                        elif caller.db.quests[quest] != "done":
                            if "talk" in to_talk.db.quests[quest]:
                                quest_script = create_script(to_talk.db.quests[quest]["talk"], obj=to_talk)
                                quest_script.db.player = caller
                                quest_script.quest_talk()


class CmdTest(MuxCommand):
    """
    Talk to a mobile to see what they have to say.
    Usage:
      talk <mobile>
    Talks to a mobile.
    """

    key = "test"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement talk"""

        caller = self.caller

        if not rules.player_in_area(self.args):
            caller.msg("no %s here" % self.args)

        caller.msg("Done.")
