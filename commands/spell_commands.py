import random
from commands.command import MuxCommand
from world import rules_skills, rules_magic

class SpellCommand(MuxCommand):
    """
    Base class for spell commands.
    """

    def mana_cost(caster, spell):
        """Calculate mana cost for a spell"""

        minimum_cost = spell["minimum cost"]

        minimum_level = 101
        for class_name in spell["classes"]:
            if spell["classes"][class_name] < minimum_level:
                minimum_level = spell["classes"][class_name]

        level_cost = 120 / (2 + (caster.level - minimum_level) / 2)

        if level_cost > minimum_cost:
            return level_cost
        else:
            return minimum_cost

    def check_cast(self, caster):
        if "cone of silence" in caster.location.db.room_flags:
            return "You can't ... You are in a Cone of Silence!"
        elif "no magic" in caster.location.db.room_flags:
            return "You feel a strong dampening field blocking your spell."
        elif caster.get_affect_status("mute"):
            return False

        return


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

        def mana_cost(spell):
            super().mana_cost(spell)

        def check_cast(caster):
            super().check_cast(caster)

        if check_cast(caster):
            caster.msg(check_cast(caster))
            return

        cost = mana_cost(self.spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast create food!")
            return

        rules_magic.do_create_food(caster, cost)