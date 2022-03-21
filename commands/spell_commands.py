import random
from commands.command import MuxCommand
from world import rules_skills, rules_magic

class CmdCreateFood(MuxCommand):
    """
    Create some food of a random type.
    Usage:
      cast create food
      create food
    Summons some food from among eight different types.
    """

    key = "create food"
    aliases = ["cast create food"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    spell = rules_skills.get_skill(key)
    wait_state = spell["wait state"]

    def func(self):
        """Implement create food"""

        caster = self.caller

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(check_cast(caster))
            return

        cost = rules_magic.mana_cost(spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast create food!")
            return

        rules_magic.do_create_food(caster, cost)
