import random
from evennia.utils import search
from commands.command import MuxCommand
from world import rules_skills, rules_combat, rules

class CmdDowse(MuxCommand):
    """
    Attempt to find a water source.
    Usage:
      dowse
    Tries to find a water source, if you have the skill. Not possible
    when indoors, or in a city.
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
            caller.location.msg_contents("%s digs a bit, and water flows from the ground."
                                         % caller.name, exclude=caller)

class CmdForage(MuxCommand):
    """
    Attempt to find some food.
    Usage:
      forage
    Tries to find some food, if you have the skill. Not possible
    when indoors, or in a city.
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
            caller.location.msg_contents("%s roots around a bit, and finds some food."
                                         % caller.name, exclude=caller)

class CmdPickLock(MuxCommand):
    """
    Pick a lock to unlock a door or container.
    
    Usage:
      pick lock <direction of door>
      pick lock <container>
      
    Makes an attempt to pick a lock on a door in a given direction,
    or the lock on a container.
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
                if self.args == "exit.key":
                    target = exit
        
        if target:
        
            if "locked" not in target.db.door_attributes:
                caller.msg("That door is not locked.")
                return                          
        
            rules_skills.do_pick_lock(caller, target, "door")
        
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

        if target.db.item_type != "container":
            caller.msg("%s is not a container." % (target.key[0].upper() + target.key[1:]))
            return
        
        if "locked" not in target.db.state:
            caller.msg("%s is not locked." % (target.key[0].upper() + target.key[1:]))
            return
        
        rules_skills.do_pick_lock(caller, target, to_steal)

            
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

        mobiles = search.search_object_by_tag("mobile")
        target = caller.search(self.rhs, location=caller.location, candidates=mobiles)
        
        if not target:
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
        else:
            to_steal = "gold"
            
        rules_skills.do_steal(caller, target, to_steal)
