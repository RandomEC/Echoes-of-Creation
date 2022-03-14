import random
from commands.command import MuxCommand
from world import rules_skills

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
    arg_regex = r"\s|$"

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

        if location.db.terrain == "inside" or location.db.terrain == "city" or "indoors" in location.db.room_flags:
            caller.msg("You cannot dowse in these surroundings.")
            return

        if caller.moves_current < 50:
            caller.msg("You are too tired to dowse at present.")
            return

        if random.randint(1, 100) > caller.db.skills["dowse"]:
            caller.msg("You did not find any water.")
            rules_skills.check_skill_improve(caller, "dowse", False)
            caller.moves_spent += 50
            return
        else:
            rules_skills.do_dowse(caller)
            rules_skills.check_skill_improve(caller, "dowse", True)

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
    arg_regex = r"\s|$"

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

        if location.db.terrain == "inside" or location.db.terrain == "city" or "indoors" in location.db.room_flags:
            caller.msg("You cannot forage in these surroundings.")
            return

        if caller.moves_current < 50:
            caller.msg("You are too tired to forage at present.")
            return

        if random.randint(1, 100) > caller.db.skills["forage"]:
            caller.msg("You failed to find any food.")
            rules_skills.check_skill_improve(caller, "forage", False)
            caller.moves_spent += 50
            return
        else:
            rules_skills.do_forage(caller)
            rules_skills.check_skill_improve(caller, "forage", True)

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
