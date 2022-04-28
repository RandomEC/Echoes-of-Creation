import random
from evennia.utils import search
from commands.command import MuxCommand
from world import rules_skills, rules_combat, rules

class CmdBashDoor(MuxCommand):
    """
    Bash in a door to allow progress through.
    
    Usage:
      bash door <direction of door>      
      
    Makes an attempt to bash in a door in a given direction.
    Be aware that some doors are bash proof!

    Colleges that can teach (level):
    Warrior (8)
    """

    key = "bash door"
    aliases = ["bash"]    
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement bash door"""

        caller = self.caller
        
        if "bash door" not in caller.db.skills:
            caller.msg("You're not enough of a warrior to bash doors!")
            return

        if not self.args:
            caller.msg("Bash a door in what direction?")
            return
        
        if caller.position != "standing":
            caller.msg("You aren't bashing anything from the ground, stand up first.")
            return

        if caller.nattributes.has("combat_handler"):
            caller.msg("You can't do that in the middle of a fight.")
            return
        
        target = ""
        if caller.location.exits:
            for exit in caller.location.exits:
                if self.args == exit.key:
                    target = exit
        
        if target:
        
            if "closed" not in target.db.door_attributes:
                caller.msg("That door is not closed.")
                return
            
        else:
            caller.msg("There is no door to bash called '%s'." % self.args)
            return
        
        rules_skills.do_bash_door(caller, target)

            
class CmdChameleonPower(MuxCommand):
    """
    Attempt to blend into your surroundings.

    Usage:
      chameleon power

    Tries to blend into the surroundings. Approximates the hide
    skill.

    Colleges that can teach (level):
    Psionicist (10)
    """

    key = "chameleon power"
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement chameleon power"""

        caller = self.caller

        if self.args:
            caller.msg("Usage: chameleon power")
            return

        if "chameleon power" not in caller.db.skills:
            caller.msg("You do not have the power to blend in.")
            return

        if caller.position != "standing":
            caller.msg("You can't blend in on the ground, try standing.")
            return

        if caller.get_affect_status("hide"):
            caller.msg("You are already hidden.")
            return

        rules_skills.do_chameleon_power(caller)


class CmdDowse(MuxCommand):
    """
    Attempt to find a water source.

    Usage:
      dowse

    Tries to find a water source, if you have the skill. Not possible
    when indoors, or in a city.

    Colleges that can teach (level):
    Ranger (3)
    """

    key = "dowse"
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement dowse"""

        caller = self.caller
        location = caller.location

        if self.args:
            caller.msg("Usage: dowse")
            return

        if "dowse" not in caller.db.skills:
            caller.msg("You do not know how to dowse!")
            return

        if caller.position != "standing":
            caller.msg("You have to wander a bit to dowse, try standing.")
            return

        if location.db.terrain == "inside" or location.db.terrain == "city" or "indoors" in location.db.room_flags:
            caller.msg("You cannot dowse in these surroundings.")
            return

        if caller.moves_current < 50:
            caller.msg("You are too tired to dowse at present.")
            return

        if random.randint(1, 100) > caller.db.skills["dowse"]:
            caller.msg("You did not find any water.")
            rules_skills.check_skill_improve(caller, "dowse", False, 1)
            caller.moves_spent += 50
            return
        else:
            rules_skills.do_dowse(caller)
            rules_skills.check_skill_improve(caller, "dowse", True, 1)

            if caller.db.skills["dowse"] > 80:
                moves_cost = 20
            else:
                moves_cost = 100 - caller.db.skills["dowse"]

            caller.moves_spent += moves_cost

            # if character ends up with less moves than 0, set to 0
            if caller.moves_spent > caller.moves_maximum:
                caller.moves_spent = caller.moves_maximum

            caller.msg("You dig a bit, and water flows from the ground.")

            # Deal with invisible objects/characters for output.
            # Assemble a list of all possible lookers.
            lookers = list(cont for cont in caller.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
            for looker in lookers:
                # Exclude the caller, who got their output above.
                if looker != caller:
                    # Address visibility of character wearing.
                    if rules.is_visible(caller, looker):
                        looker.msg("%s digs a bit, and water flows from the ground." % caller.name)
                    else:
                        looker.msg("Water suddenly begins to flow from the ground.")

class CmdForage(MuxCommand):
    """
    Attempt to find some food.

    Usage:
      forage

    Tries to find some food, if you have the skill. Not possible
    when indoors, or in a city.

    Colleges that can teach (level):
    Ranger (3), Druid (6), Bard (9)
    """

    key = "forage"
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement forage"""

        caller = self.caller
        location = caller.location

        if self.args:
            caller.msg("Usage: forage")
            return

        if "forage" not in caller.db.skills:
            caller.msg("You do not know how to forage!")
            return

        if caller.position != "standing":
            caller.msg("You have to wander a bit to forage, try standing.")
            return

        if location.db.terrain == "inside" or location.db.terrain == "city" or "indoors" in location.db.room_flags:
            caller.msg("You cannot forage in these surroundings.")
            return

        if caller.moves_current < 50:
            caller.msg("You are too tired to forage at present.")
            return

        if random.randint(1, 100) > caller.db.skills["forage"]:
            caller.msg("You failed to find any food.")
            rules_skills.check_skill_improve(caller, "forage", False, 1)
            caller.moves_spent += 50
            return
        else:
            rules_skills.do_forage(caller)
            rules_skills.check_skill_improve(caller, "forage", True, 1)

            if caller.db.skills["forage"] > 80:
                moves_cost = 20
            else:
                moves_cost = 100 - caller.db.skills["forage"]

            caller.moves_spent += moves_cost

            # if character ends up with less moves than 0, set to 0
            if caller.moves_spent > caller.moves_maximum:
                caller.moves_spent = caller.moves_maximum

            caller.msg("You root around a bit, and find some food.")
            
            # Deal with invisible objects/characters for output.
            # Assemble a list of all possible lookers.
            lookers = list(cont for cont in caller.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
            for looker in lookers:
                # Exclude the caller, who got their output above.
                if looker != caller:
                    # Address visibility of character wearing.
                    if rules.is_visible(caller, looker):
                        looker.msg("%s roots around a bit, and finds some food." % caller.name)

                        
class CmdHide(MuxCommand):
    """
    Attempt to hide.

    Usage:
      hide

    Tries to hide among various terrain elements and objects to be
    unseen in a room.

    Colleges that can teach (level):
    Thief (8), Ranger (9), Bard (10), Druid (16)
    """

    key = "hide"
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement hide"""

        caller = self.caller

        if self.args:
            caller.msg("Usage: hide")
            return

        if "hide" not in caller.db.skills:
            caller.msg("You do not know how to hide!")
            return

        if caller.position != "standing":
            caller.msg("You can't hide while on the ground, try standing.")
            return

        if caller.get_affect_status("hide"):
            caller.msg("You are already hidden.")
            return

        rules_skills.do_hide(caller)


class CmdPickLock(MuxCommand):
    """
    Pick a lock to unlock a door or container.
    
    Usage:
      pick lock <direction of door>
      pick lock <container>
      
    Makes an attempt to pick a lock on a door in a given direction,
    or the lock on a container.

    Colleges that can teach (level):
    Thief (5), Bard (14)
    """

    key = "pick lock"
    aliases = ["pick"]    
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement pick lock"""

        caller = self.caller
        
        if "pick lock" not in caller.db.skills:
            caller.msg("You do not know how to pick locks!")
            return

        if not self.args:
            caller.msg("Pick a lock in what direction or on what container?")
            return
        
        if caller.position != "standing":
            caller.msg("You aren't picking any locks on the ground, stand up first.")
            return

        target = ""
        if caller.location.exits:
            for exit in caller.location.exits:
                if self.args == exit.key:
                    target = exit
        
        if target:
        
            if "locked" not in target.db.door_attributes:
                caller.msg("That door is not locked.")
                return

            rules_skills.do_pick_lock(caller, target, "door")
            return
        
        objects = []
        for object in caller.location.contents:
            if "object" in object.tags.all():
                objects.append(object)
        for object in caller.contents:
            if "object" in object.tags.all():
                objects.append(object)
                
        target = caller.search(self.args, candidates=objects)
        
        if not target:
            caller.msg("There is no %s here pick the lock of." % self.args)
            return
        
        if not rules.is_visible(target, caller):
            caller.msg("There is no %s here pick the lock of." % self.args)
            return
        
        if target.db.item_type != "container":
            caller.msg("%s is not a container." % (target.key[0].upper() + target.key[1:]))
            return
        
        if "locked" not in target.db.state:
            caller.msg("%s is not locked." % (target.key[0].upper() + target.key[1:]))
            return

        if not target.access(caller, "pick"):
            caller.msg("The lock on %s cannot be picked." % target.key)
            return

        rules_skills.do_pick_lock(caller, target, "container")

            
class CmdShadowForm(MuxCommand):
    """
    Attempt to take a shadowy form.

    Usage:
      shadow form

    Tries to take the form of the shadows. Approximates the sneak
    skill, allowing you to move silently.

    Colleges that can teach (level):
    Psionicist (8)
    """

    key = "shadow form"
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement shadow form"""

        caller = self.caller

        if self.args:
            caller.msg("Usage: shadow form")
            return

        if "shadow form" not in caller.db.skills:
            caller.msg("You do not have the power to take the form of the shadows.")
            return

        if caller.position != "standing":
            caller.msg("You can't take shadow form on the ground, try standing.")
            return

        if caller.get_affect_status("sneak"):
            caller.msg("You are already sneaking.")
            return

        rules_skills.do_shadow_form(caller)


class CmdSkills(MuxCommand):
    """
    List the skills you know, and the percentage you have learned of each.
    Usage:
      skills
    List the skills you know, and the percentage you have learned of each.
    """

    key = "skills"
    aliases = ["sk"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement skills"""

        caller = self.caller 
        skills = caller.db.skills
        
        # Turn the skills from the dictionary into a list, so
        # they can be alphabetized.
        skills_list = []
        for skill in skills:
            skills_list.append(skill)

        # Alphabetize the list
        skills_list.sort()
        total_skills = len(skills_list)
        leftover = total_skills % 3

        index = 0
        output_string = "You know the following skills, to the following percentages:\n"
        
        # Run through the list indices to format a table of skills, at three per
        # column.
        if total_skills > 2:
            while index + 1 <= (total_skills - leftover):
                output_string += "%-20s%d%%   %-20s%-d%%   %-20s%d%%\n" % (skills_list[index],
                                                                 skills[skills_list[index]],
                                                                 skills_list[index + 1],
                                                                 skills[skills_list[index + 1]],
                                                                 skills_list[index + 2],
                                                                 skills[skills_list[index + 2]])
                index += 3
            
        # Handle the remnant after the even three per column.
        if leftover == 1:
            output_string += "%-20s%d%%\n" % (skills_list[index],
                                           skills[skills_list[index]])
        elif leftover == 2:
            output_string += "%-20s%d%%   %-20s%d%%\n" % (skills_list[index],
                                                    skills[skills_list[index]],
                                                    skills_list[index + 1],
                                                    skills[skills_list[index + 1]])
        
        caller.msg(output_string)

class CmdSneak(MuxCommand):
    """
    Attempt to sneak.

    Usage:
      sneak

    Tries to sneak, which allows you to move silently between rooms.

    Colleges that can teach (level):
    Thief (6), Ranger (7), Bard (8)
    """

    key = "sneak"
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement sneak"""

        caller = self.caller

        if self.args:
            caller.msg("Usage: sneak")
            return

        if "sneak" not in caller.db.skills:
            caller.msg("You do not know how to sneak!")
            return

        if caller.position != "standing":
            caller.msg("You can't sneak while on the ground, try standing.")
            return

        if caller.get_affect_status("sneak"):
            caller.msg("You are already sneaking.")
            return

        rules_skills.do_sneak(caller)

class CmdSteal(MuxCommand):
    """
    Steal gold or an item from a mobile.

    Usage:
      steal gold from <mobile>
      steal <item name> from <mobile>

    Makes an attempt to steal either gold or an item from a mobile.
    Stealing is NOT permitted (and not possible) from other players.
    It is also not possible to steal items that cannot be dropped,
    and worn equipment that cannot be removed.

    Colleges that can teach (level):
    Thief (3), Bard (3)
    """

    key = "steal"
    delimiter = " from "
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement steal"""

        caller = self.caller
        
        if "steal" not in caller.db.skills:
            caller.msg("You do not know how to steal!")
            return

        if not self.args or not self.rhs:
            caller.msg("Steal what from which mobile?")
            return
        
        if caller.position != "standing":
            caller.msg("You aren't stealing anything on the ground, stand up first.")
            return


        mobiles = []
        for object in caller.location.contents:
            if "mobile" in object.tags.all():
                mobiles.append(object)
        target = caller.search(self.args, candidates=mobiles)

        if not target:
            caller.msg("There is no %s here to steal from." % self.args)
            return
        if not rules.is_visible(target, caller):
            caller.msg("There is no %s here to steal from." % self.args)
            return        
        elif caller == target:
            caller.msg("That seems pointless.")
            return
        elif "player" in target.tags.all():
            caller.msg("You cannot steal from another player.")
            return
        elif rules_combat.is_safe(target):

            pronoun = rules.pronoun_subject(target)
            if pronoun == "they":
                phrase = "they are"
            else:
                phrase = "%s is" % pronoun

            caller.msg("You cannot steal from %s, %s under the protection of the gods." % (target.key, phrase))
            return
        elif caller.level - target.level > 5:
            caller.msg("Honestly, pick on someone your own size.")
            return
        
        if self.lhs != "gold":
            to_steal = caller.search(
                self.lhs,
                location=target,
                nofound_string="%s is not carrying %s." % ((target.key[0].upper() + target.key[1:]), self.lhs),
                multimatch_string="%s carries more than one %s:" % ((target.key[0].upper() + target.key[1:]), self.lhs),
            )
            
            if not to_steal:
                return
            if not rules.is_visible(to_steal, caller):
                caller.msg("%s is not carrying %s." % ((target.key[0].upper() + target.key[1:]), self.lhs))
                return
        else:
            to_steal = "gold"
            
        rules_skills.do_steal(caller, target, to_steal)
