"""
Spell Commands

This file handles most of the commands that deal with casting spells,
and other magic-related commands. IMPORTANTLY, please note that the
processing of the command input is handled here, but the actual "meat"
of the spell itself is handled in a function entitled "do_ ..." in
rules_magic. This is for two purposes - 1) to accommodate mobile
casting, which does not need the command structure, and 2) to prepare
for the implementation of wands, staves and scrolls, all of which
will need the functional parts of the spell, but will have their own
command-handling part.
"""
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
       
class CmdCreateWater(MuxCommand):
    """
    Create water in a drink container in your possession.
    Usage:
      cast create water <drink container>
      create water <drink container>
    Creates water in a drink container in your possession.
    """

    key = "create water"
    aliases = ["cast create water"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    spell = rules_skills.get_skill(key)
    wait_state = spell["wait state"]

    def func(self):
        """Implement create water"""

        caster = self.caller

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(check_cast(caster))
            return

        if not self.args:
            caster.msg("Create water where?")
            return
        
        target_container = caster.search(self.args, location=caster)
        
        if not target_container:
            caster.msg("You have no %s." self.args)
            return
        
        if target_container.db.item_type != "drink container":
            caster.msg("%s is not able to hold water." % (target_container.key[0].upper() + target_container.key[1:]))
            return
        
        if target_container.db.liquid_type != "water":
            caster.msg("%s already contains some of another liquid." % (target_container.key[0].upper() + target_container.key[1:]))
            return
                
        cost = rules_magic.mana_cost(spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast create water!")
            return

        rules_magic.do_create_water(caster, cost, target_container)
