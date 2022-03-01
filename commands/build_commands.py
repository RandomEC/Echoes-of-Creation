"""
Build Commands

Build commands are those used to build the world of the game.

"""
from commands.command import MuxCommand
from server.conf import settings
from evennia.utils import create

class ObjManipCommand(MuxCommand):
    """
    This is a parent class for some of the defining objmanip commands
    since they tend to have some more variables to define new objects.
    Each object definition can have several components. First is
    always a name, followed by an optional alias list and finally an
    some optional data, such as a typeclass or a location. A comma ','
    separates different objects. Like this:
        name1;alias;alias;alias:option, name2;alias;alias ...
    Spaces between all components are stripped.
    A second situation is attribute manipulation. Such commands
    are simpler and offer combinations
        objname/attr/attr/attr, objname/attr, ...
    """

    # OBS - this is just a parent - it's not intended to actually be
    # included in a commandset on its own!

    def parse(self):
        """
        We need to expand the default parsing to get all
        the cases, see the module doc.
        """
        # get all the normal parsing done (switches etc)
        super().parse()

        obj_defs = ([], [])  # stores left- and right-hand side of '='
        obj_attrs = ([], [])  # "

        for iside, arglist in enumerate((self.lhslist, self.rhslist)):
            # lhslist/rhslist is already split by ',' at this point
            for objdef in arglist:
                aliases, option, attrs = [], None, []
                if ":" in objdef:
                    objdef, option = [part.strip() for part in objdef.rsplit(":", 1)]
                if ";" in objdef:
                    objdef, aliases = [part.strip() for part in objdef.split(";", 1)]
                    aliases = [alias.strip() for alias in aliases.split(";") if alias.strip()]
                if "/" in objdef:
                    objdef, attrs = [part.strip() for part in objdef.split("/", 1)]
                    attrs = [part.strip().lower() for part in attrs.split("/") if part.strip()]
                # store data
                obj_defs[iside].append({"name": objdef, "option": option, "aliases": aliases})
                obj_attrs[iside].append({"name": objdef, "attrs": attrs})

        # store for future access
        self.lhs_objs = obj_defs[0]
        self.rhs_objs = obj_defs[1]
        self.lhs_objattr = obj_attrs[0]
        self.rhs_objattr = obj_attrs[1]

class CmdSetObjAlias(MuxCommand):
    """
    Adding permanent aliases for object
    Usage:
      alias <obj> [= [alias[^alias^alias^...]]]
      alias <obj> =
      alias/category <obj> = [alias[^alias^...]:<category>
    Switches:
      category - requires ending input with :category, to store the
        given aliases with the given category.
    Assigns aliases to an object so it can be referenced by more
    than one name. Assign empty to remove all aliases from object. If
    assigning a category, all aliases given will be using this category.
    Observe that this is not the same thing as personal aliases
    created with the 'nick' command! Aliases set with alias are
    changing the object in question, making those aliases usable
    by everyone.
    """

    key = "alias"
    aliases = "setobjalias"
    switch_options = ("category",)
    locks = "cmd:perm(setobjalias) or perm(Builder)"
    help_category = "Building"

    def func(self):
        """Set the aliases."""

        caller = self.caller

        if not self.lhs:
            string = "Usage: alias <obj> [= [alias[,alias ...]]]"
            self.caller.msg(string)
            return
        objname = self.lhs

        # Find the object to receive aliases
        obj = caller.search(objname)
        if not obj:
            return
        if self.rhs is None:
            # no =, so we just list aliases on object.
            aliases = obj.aliases.all(return_key_and_category=True)
            if aliases:
                caller.msg(
                    "Aliases for %s: %s"
                    % (
                        obj.get_display_name(caller),
                        ", ".join(
                            "'%s'%s"
                            % (alias, "" if category is None else "[category:'%s']" % category)
                            for (alias, category) in aliases
                        ),
                    )
                )
            else:
                caller.msg("No aliases exist for '%s'." % obj.get_display_name(caller))
            return

        if not (obj.access(caller, "control") or obj.access(caller, "edit")):
            caller.msg("You don't have permission to do that.")
            return

        if not self.rhs:
            # we have given an empty =, so delete aliases
            old_aliases = obj.aliases.all()
            if old_aliases:
                caller.msg(
                    "Cleared aliases from %s: %s"
                    % (obj.get_display_name(caller), ", ".join(old_aliases))
                )
                obj.aliases.clear()
            else:
                caller.msg("No aliases to clear.")
            return

        category = None
        if "category" in self.switches:
            if ":" in self.rhs:
                rhs, category = self.rhs.rsplit(":", 1)
                category = category.strip()
            else:
                caller.msg(
                    "If specifying the /category switch, the category must be given "
                    "as :category at the end."
                )
        else:
            rhs = self.rhs

        # merge the old and new aliases (if any)
        old_aliases = obj.aliases.get(category=category, return_list=True)
        new_aliases = [alias.strip().lower() for alias in rhs.split("^") if alias.strip()]

        # make the aliases only appear once
        old_aliases.extend(new_aliases)
        aliases = list(set(old_aliases))

        # save back to object.
        obj.aliases.add(aliases, category=category)

        # we need to trigger this here, since this will force
        # (default) Exits to rebuild their Exit commands with the new
        # aliases
        obj.at_cmdset_get(force_init=True)

        # report all aliases on the object
        caller.msg(
            "Alias(es) for '%s' set to '%s'%s."
            % (
                obj.get_display_name(caller),
                str(obj.aliases),
                " (category: '%s')" % category if category else "",
            )
        )

class CmdDig(ObjManipCommand):
    """
    build new rooms and connect them to the current location
    Usage:
      dig[/switches] <roomname>[;alias;alias...][:typeclass]
            [= <exit_to_there>[;alias][:typeclass]]
               [^ <exit_to_here>[;alias][:typeclass]]
    Switches:
       tel or teleport - move yourself to the new room
    Examples:
       dig kitchen = north;n, south;s
       dig house:myrooms.MyHouseTypeclass
       dig sheer cliff;cliff;sheer = climb up, climb down
    This command is a convenient way to build rooms quickly; it creates the
    new room and you can optionally set up exits back and forth between your
    current room and the new one. You can add as many aliases as you
    like to the name of the room and the exits in question; an example
    would be 'north;no;n'.
    """

    key = "dig"
    switch_options = ("teleport",)
    locks = "cmd:perm(dig) or perm(Builder)"
    help_category = "Building"

    # lockstring of newly created rooms, for easy overloading.
    # Will be formatted with the {id} of the creating object.
    new_room_lockstring = (
        "control:id({id}) or perm(Admin); "
        "delete:id({id}) or perm(Admin); "
        "edit:id({id}) or perm(Admin)"
    )

    def func(self):
        """Do the digging. Inherits variables from ObjManipCommand.parse()"""

        caller = self.caller

        if not self.lhs:
            string = "Usage: dig[/teleport] <roomname>[;alias;alias...]" "[:parent] [= <exit_there>"
            string += "[;alias;alias..][:parent]] "
            string += "[, <exit_back_here>[;alias;alias..][:parent]]"
            caller.msg(string)
            return

        room = self.lhs_objs[0]

        if not room["name"]:
            caller.msg("You must supply a new room name.")
            return
        location = caller.location

        # Create the new room
        typeclass = room["option"]
        if not typeclass:
            typeclass = settings.BASE_ROOM_TYPECLASS

        # create room
        new_room = create.create_object(
            typeclass, room["name"], aliases=room["aliases"], report_to=caller
        )
        lockstring = self.new_room_lockstring.format(id=caller.id)
        new_room.locks.add(lockstring)
        alias_string = ""
        if new_room.aliases.all():
            alias_string = " (%s)" % ", ".join(new_room.aliases.all())
        room_string = "Created room %s(%s)%s of type %s." % (
            new_room,
            new_room.dbref,
            alias_string,
            typeclass,
        )

        # create exit to room

        exit_to_string = ""
        exit_back_string = ""

        if self.rhs_objs:
            to_exit = self.rhs_objs[0]
            if not to_exit["name"]:
                exit_to_string = "\nNo exit created to new room."
            elif not location:
                exit_to_string = "\nYou cannot create an exit from a None-location."
            else:
                # Build the exit to the new room from the current one
                typeclass = to_exit["option"]
                if not typeclass:
                    typeclass = settings.BASE_EXIT_TYPECLASS

                new_to_exit = create.create_object(
                    typeclass,
                    to_exit["name"],
                    location,
                    aliases=to_exit["aliases"],
                    locks=lockstring,
                    destination=new_room,
                    report_to=caller,
                )
                alias_string = ""
                if new_to_exit.aliases.all():
                    alias_string = " (%s)" % ", ".join(new_to_exit.aliases.all())
                exit_to_string = "\nCreated Exit from %s to %s: %s(%s)%s."
                exit_to_string = exit_to_string % (
                    location.name,
                    new_room.name,
                    new_to_exit,
                    new_to_exit.dbref,
                    alias_string,
                )

        # Create exit back from new room

        if len(self.rhs_objs) > 1:
            # Building the exit back to the current room
            back_exit = self.rhs_objs[1]
            if not back_exit["name"]:
                exit_back_string = "\nNo back exit created."
            elif not location:
                exit_back_string = "\nYou cannot create an exit back to a None-location."
            else:
                typeclass = back_exit["option"]
                if not typeclass:
                    typeclass = settings.BASE_EXIT_TYPECLASS
                new_back_exit = create.create_object(
                    typeclass,
                    back_exit["name"],
                    new_room,
                    aliases=back_exit["aliases"],
                    locks=lockstring,
                    destination=location,
                    report_to=caller,
                )
                alias_string = ""
                if new_back_exit.aliases.all():
                    alias_string = " (%s)" % ", ".join(new_back_exit.aliases.all())
                exit_back_string = "\nCreated Exit back from %s to %s: %s(%s)%s."
                exit_back_string = exit_back_string % (
                    new_room.name,
                    location.name,
                    new_back_exit,
                    new_back_exit.dbref,
                    alias_string,
                )
        caller.msg("%s%s%s" % (room_string, exit_to_string, exit_back_string))
        if new_room and ("teleport" in self.switches or "tel" in self.switches):
            caller.move_to(new_room)

class CmdCreate(ObjManipCommand):
    """
    create new objects
    Usage:
      create[/drop] <objname>[;alias;alias...][:typeclass]^ <objname>...
    switch:
       drop - automatically drop the new object into your current
              location (this is not echoed). This also sets the new
              object's home to the current location rather than to you.
    Creates one or more new objects. If typeclass is given, the object
    is created as a child of this typeclass. The typeclass script is
    assumed to be located under types/ and any further
    directory structure is given in Python notation. So if you have a
    correct typeclass 'RedButton' defined in
    types/examples/red_button.py, you could create a new
    object of this type like this:
       create/drop button;red : examples.red_button.RedButton
    """

    key = "create"
    switch_options = ("drop",)
    locks = "cmd:perm(create) or perm(Builder)"
    help_category = "Building"

    # lockstring of newly created objects, for easy overloading.
    # Will be formatted with the {id} of the creating object.
    new_obj_lockstring = "control:id({id}) or perm(Admin);delete:id({id}) or perm(Admin)"

    def func(self):
        """
        Creates the object.
        """

        caller = self.caller

        if not self.args:
            string = "Usage: create[/drop] <newname>[;alias;alias...] [:typeclass.path]"
            caller.msg(string)
            return

        # create the objects
        for objdef in self.lhs_objs:
            string = ""
            name = objdef["name"]
            aliases = objdef["aliases"]
            typeclass = objdef["option"]

            # create object (if not a valid typeclass, the default
            # object typeclass will automatically be used)
            lockstring = self.new_obj_lockstring.format(id=caller.id)
            obj = create.create_object(
                typeclass,
                name,
                caller,
                home=caller,
                aliases=aliases,
                locks=lockstring,
                report_to=caller,
            )
            if not obj:
                continue
            if aliases:
                string = "You create a new %s: %s (aliases: %s)."
                string = string % (obj.typename, obj.name, ", ".join(aliases))
            else:
                string = "You create a new %s: %s."
                string = string % (obj.typename, obj.name)
            # set a default desc
            if not obj.db.desc:
                obj.db.desc = "You see nothing special."
            if "drop" in self.switches:
                if caller.location:
                    obj.home = caller.location
                    obj.move_to(caller.location, quiet=True)
        if string:
            caller.msg(string)

class CmdName(ObjManipCommand):
    """
    change the name and/or aliases of an object
    Usage:
      name <obj> = <newname>;alias1;alias2
    Rename an object to something new. Use *obj to
    rename an account.
    """

    key = "name"
    aliases = ["rename"]
    locks = "cmd:perm(rename) or perm(Builder)"
    help_category = "Building"

    def func(self):
        """change the name"""

        caller = self.caller
        if not self.args:
            caller.msg("Usage: name <obj> = <newname>[;alias;alias;...]")
            return

        obj = None
        if self.lhs_objs:
            objname = self.lhs_objs[0]["name"]
            if objname.startswith("*"):
                # account mode
                obj = caller.account.search(objname.lstrip("*"))
                if obj:
                    if self.rhs_objs[0]["aliases"]:
                        caller.msg("Accounts can't have aliases.")
                        return
                    newname = self.rhs
                    if not newname:
                        caller.msg("No name defined!")
                        return
                    if not (obj.access(caller, "control") or obj.access(caller, "edit")):
                        caller.msg("You don't have right to edit this account %s." % obj)
                        return
                    obj.username = newname
                    obj.save()
                    caller.msg("Account's name changed to '%s'." % newname)
                    return
            # object search, also with *
            obj = caller.search(objname)
            if not obj:
                return
        if self.rhs_objs:
            newname = self.rhs_objs[0]["name"]
            aliases = self.rhs_objs[0]["aliases"]
        else:
            newname = self.rhs
            aliases = None
        if not newname and not aliases:
            caller.msg("No names or aliases defined!")
            return
        if not (obj.access(caller, "control") or obj.access(caller, "edit")):
            caller.msg("You don't have the right to edit %s." % obj)
            return
        # change the name and set aliases:
        if newname:
            obj.name = newname
        astring = ""
        if aliases:
            [obj.aliases.add(alias) for alias in aliases]
            astring = " (%s)" % (", ".join(aliases))
        # fix for exits - we need their exit-command to change name too
        if obj.destination:
            obj.flush_from_cache(force=True)
        caller.msg("Object's name changed to '%s'%s." % (newname, astring))


class CmdOpen(ObjManipCommand):
    """
    open a new exit from the current room
    Usage:
      openexit <new exit>[;alias;alias..][:typeclass] [,<return exit>[;alias;..][:typeclass]]] = <destination>
    Handles the creation of exits. If a destination is given, the exit
    will point there. The <return exit> argument sets up an exit at the
    destination leading back to the current room. Destination name
    can be given both as a #dbref and a name, if that name is globally
    unique.
    """

    key = "openexit"
    locks = "cmd:perm(open) or perm(Builder)"
    help_category = "Building"

    new_obj_lockstring = "control:id({id}) or perm(Admin);delete:id({id}) or perm(Admin)"
    # a custom member method to chug out exits and do checks

    def create_exit(
                    self,
                    exit_name,
                    location,
                    destination,
                    exit_aliases=None,
                    typeclass=None
                    ):
        """
        Helper function to avoid code duplication.
        At this point we know destination is a valid location
        """
        caller = self.caller
        string = ""
        # check if this exit object already exists at the location.
        # we need to ignore errors (so no automatic feedback)since we
        # have to know the result of the search to decide what to do.
        exit_obj = caller.search(
                                 exit_name,
                                 location=location,
                                 quiet=True,
                                 exact=True
                                )
        if len(exit_obj) > 1:
            # give error message and return
            caller.search(exit_name, location=location, exact=True)
            return None
        if exit_obj:
            exit_obj = exit_obj[0]
            if not exit_obj.destination:
                # we are trying to link a non-exit
                string = "'%s' already exists and is not an exit!\nIf you want to convert it "
                string += (
                    "to an exit, you must assign an object to the 'destination' property first."
                )
                caller.msg(string % exit_name)
                return None
            # we are re-linking an old exit.
            old_destination = exit_obj.destination
            if old_destination:
                string = "Exit %s already exists." % exit_name
                if old_destination.id != destination.id:
                    # reroute the old exit.
                    exit_obj.destination = destination
                    if exit_aliases:
                        [exit_obj.aliases.add(alias) for alias in exit_aliases]
                    string += " Rerouted its old destination '%s' to '%s' and changed aliases." % (
                        old_destination.name,
                        destination.name,
                    )
                else:
                    string += " It already points to the correct place."

        else:
            # exit does not exist before. Create a new one.
            lockstring = self.new_obj_lockstring.format(id=caller.id)
            if not typeclass:
                typeclass = settings.BASE_EXIT_TYPECLASS
            exit_obj = create.create_object(
                typeclass,
                key=exit_name,
                location=location,
                aliases=exit_aliases,
                locks=lockstring,
                report_to=caller,
            )
            if exit_obj:
                # storing a destination is what makes it an exit!
                exit_obj.destination = destination
                string = (
                    ""
                    if not exit_aliases
                    else " (aliases: %s)" % (", ".join([str(e) for e in exit_aliases]))
                )
                string = "Created new Exit '%s' from %s to %s%s." % (
                    exit_name,
                    location.name,
                    destination.name,
                    string,
                )
            else:
                string = "Error: Exit '%s' not created." % exit_name
        # emit results
        caller.msg(string)
        return exit_obj

    def func(self):
        """
        This is where the processing starts.
        Uses the ObjManipCommand.parser() for pre-processing
        as well as the self.create_exit() method.
        """
        caller = self.caller

        if not self.args or not self.rhs:
            string = "Usage: open <new exit>[;alias...][:typeclass][,<return exit>[;alias..][:typeclass]]] "
            string += "= <destination>"
            caller.msg(string)
            return

        # We must have a location to open an exit
        location = caller.location
        if not location:
            caller.msg("You cannot create an exit from a None-location.")
            return

        # obtain needed info from cmdline

        exit_name = self.lhs_objs[0]["name"]
        exit_aliases = self.lhs_objs[0]["aliases"]
        exit_typeclass = self.lhs_objs[0]["option"]
        dest_name = self.rhs

        # first, check so the destination exists.
        destination = caller.search(dest_name, global_search=True)
        if not destination:
            return

        # Create exit
        ok = self.create_exit(exit_name, location, destination, exit_aliases, exit_typeclass)
        if not ok:
            # an error; the exit was not created, so we quit.
            return
        # Create back exit, if any
        if len(self.lhs_objs) > 1:
            back_exit_name = self.lhs_objs[1]["name"]
            back_exit_aliases = self.lhs_objs[1]["aliases"]
            back_exit_typeclass = self.lhs_objs[1]["option"]
            self.create_exit(
                back_exit_name, destination, location, back_exit_aliases, back_exit_typeclass
            )
