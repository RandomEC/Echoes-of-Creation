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
from world import rules_skills, rules_magic, rules_combat


class CmdChillTouch(MuxCommand):
    """
    Cast a spell to cause chilling damage to an enemy.

    Usage:
      cast chill touch <target>
      chill touch <target>

    Chill touch does damage to your enemy, and also inflicts
    a chill on them that causes their strength to weaken for
    a short time.

    Colleges that can teach (level):
    Druid (4)
    """

    key = "chill touch"
    aliases = ["cast chill touch"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement chill touch"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "chill touch" not in caster.db.skills:
            caster.msg("You do not know the spell 'chill touch' yet!")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        caster.msg("Casting cost is %d" % cost)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast chill touch!")
            return

        if not self.args:

            if not caster.ndb.combat_handler:
                caster.msg("You are not in combat, so you must choose a target for your spell.")
                return
            else:
                combat = caster.ndb.combat_handler
                target = combat.get_target(caster)

        else:
            mobiles = []
            for object in caster.location.contents:
                if "mobile" in object.tags.all():
                    mobiles.append(object)
            target = caster.search(self.args, candidates=mobiles)
            if not target:
                caster.msg("There is no %s here to chill with your touch." % self.args)
                return

        if rules_combat.is_safe(target):
            caster.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
            return

        if not caster.ndb.combat_handler:
            combat = rules_combat.create_combat(caster, target)
            rules_magic.do_chill_touch(caster, target, cost)
            combat.at_repeat()
        else:
            rules_magic.do_chill_touch(caster, target, cost)


class CmdContinualLight(MuxCommand):
    """
    Create a continuous light source.

    Usage:
      cast continual light
      continual light

    Summons a ball of light with eternal duration, but no statistics
    bonuses.

    Colleges that can teach (level):
    Mage (4)
    """

    key = "continual light"
    aliases = ["cast continual light"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement continual light"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "continual light" not in caster.db.skills:
            caster.msg("You do not know the spell 'continual light' yet!")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast create food!")
            return

        rules_magic.do_continual_light(caster, cost)


class CmdCreateFood(MuxCommand):
    """
    Create some food of a random type.

    Usage:
      cast create food
      create food

    Summons some food from among eight different types.
    
    Colleges that can teach (level):
    Cleric (3)
    """

    key = "create food"
    aliases = ["cast create food"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement create food"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "create food" not in caster.db.skills:
            caster.msg("You do not know the spell 'create food' yet!")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast create food!")
            return

        rules_magic.do_create_food(caster, cost)

class CmdCreateSound(MuxCommand):
    """
    A spell that puts words in the mouths of other players and
    mobiles.

    Usage:
      cast create sound <target> says <speech string>
      create sound <target> says <speech string>

    A spell that attempts to make it seem as though a mobile or player
    has said a word or sentence. A player that saves against the spell
    will know that you forced the player or mobile to say the words.

    Colleges that can teach (level):
    Psionicist (3), Bard (3)
    """

    key = "create sound"
    aliases = ["cast create sound"]
    delimiter = " says "
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement create sound"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "create sound" not in caster.db.skills:
            caster.msg("You do not know the spell 'create sound' yet!")
            return

        if not self.args or not self.lhs or not self.rhs:
            caster.msg("Usage: create sound <target> says <speech string>")
            return

        speakers = []
        for object in caster.location.contents:
            if "player" in object.tags.all() or "mobile" in object.tags.all():
                speakers.append(object)

        target = caster.search(self.lhs, location=[caster.location], candidates=speakers)

        if not target:
            caster.msg("There is no %s here to create sounds on." % self.lhs)
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast create sound!")
            return

        rules_magic.do_create_sound(caster, cost, target, self.rhs)


class CmdCreateWater(MuxCommand):
    """
    Create water in a drink container in your possession.

    Usage:
      cast create water <drink container>
      create water <drink container>

    Creates water in a drink container in your possession.
    
    Colleges that can teach (level):
    Cleric (3), Paladin (13)
    """

    key = "create water"
    aliases = ["cast create water"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    spell = rules_skills.get_skill(skill_name=key)
    wait_state = spell["wait state"]

    def func(self):
        """Implement create water"""

        caster = self.caller

        if "create water" not in caster.db.skills:
            caster.msg("You do not know the spell 'create water' yet!")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        if not self.args:
            caster.msg("Create water where?")
            return
        
        target_container = caster.search(self.args, location=caster)
        
        if not target_container:
            caster.msg("You have no %s." % self.args)
            return
        
        if target_container.db.item_type != "drink_container":
            caster.msg("%s is not able to hold water." % (target_container.key[0].upper() + target_container.key[1:]))
            return
        
        if target_container.db.liquid_type != "water" and target_container.db.liquid_type != None and target_container.db.liquid_type != "":
            caster.msg("%s already contains some of another liquid." % (target_container.key[0].upper() + target_container.key[1:]))
            return
                
        cost = rules_magic.mana_cost(caster, self.spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast create water!")
            return

        rules_magic.do_create_water(caster, cost, target_container)


class CmdDetectEvil(MuxCommand):
    """
    Allow yourself or a target to detect evil.

    Usage:
      cast detect evil <target>
      cast detect evil
      detect evil

    Detect evil will show a (|RRed Aura|n) on any
    object or monster that is evilly aligned. Cast
    with no target, it targets the caster.

    Colleges that can teach (level):
    Cleric (4), Paladin (4)
    """

    key = "detect evil"
    aliases = ["cast detect evil"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement detect evil"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "detect evil" not in caster.db.skills:
            caster.msg("You do not know the spell 'detect evil' yet!")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast detect evil!")
            return

        if not self.args:
            target = caster

        else:
            targets = []
            for object in caster.location.contents:
                if "mobile" in object.tags.all() or "player" in object.tags.all():
                    targets.append(object)
            target = caster.search(self.args, candidates=targets)
            if not target:
                caster.msg("There is no %s here on whom to cast detect evil on." % self.args)
                return

        if target.get_affect_status("detect magic"):
            if target == caster:
                subject = "You"
            else:
                subject = (target.key[0].upper() + target.key[1:])

            caster.msg("%s is already affected by detect magic.\n")
            return

        rules_magic.do_detect_evil(caster, target, cost)

