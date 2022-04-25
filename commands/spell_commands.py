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
from world import rules, rules_skills, rules_magic, rules_combat


class CmdAdrenalineControl(MuxCommand):
    """
    Use your mental control over yourself to increase your adrenaline.

    Usage:
      cast adrenaline control
      adrenaline control

   Adrenaline control will allow you to increase both your dexterity and
    constitution.

    Colleges that can teach (level):
    Psionicist (10), Bard (30)
    """

    key = "adrenaline control"
    aliases = ["cast adrenaline control"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement adrenaline control"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)

        if "adrenaline control" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
            return

        target = caster

        if target.get_affect_status(self.key):
            if target == caster:
                subject = "You"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s is already affected by %s.\n" % (subject, self.key))
            return

        rules_magic.do_adrenaline_control(caster, target, cost)


class CmdAgitation(MuxCommand):
    """
    Cast a spell to cause magical damage to an enemy.

    Usage:
      cast agitation <target>
      agitation <target>

    Agitation causes the cells in your victim to become
    agitated, moving so fast as to cause burn damage.

    Colleges that can teach (level):
    Psionicist (5)
    """

    key = "agitation"
    aliases = ["cast agitation"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement agitation"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "agitation" not in caster.db.skills:
            caster.msg("You do not know the spell 'agitation' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
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
            caster.msg("You do not have sufficient mana to cast agitation!")
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
                caster.msg("There is no %s here to inflict agitation on." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to inflict agitation on." % self.args)
                return

        if rules_combat.is_safe(target):
            caster.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
            return

        if not caster.ndb.combat_handler:
            combat = rules_combat.create_combat(caster, target)
            rules_magic.do_agitation(caster, target, cost)
            if combat in caster.location.contents:
                combat.at_repeat()
        else:
            rules_magic.do_agitation(caster, target, cost)

            
class CmdArmor(MuxCommand):
   """
   Provide additional armor for yourself or a target.

   Usage:
     cast armor <target>
     cast armor
     armor

   Armor will provide extra defense for you or a
   target. Cast with no target, it targets the caster.

   Colleges that can teach (level):
   Cleric (6), Druid (9), Paladin (14)
   """

   key = "armor"
   aliases = ["cast armor"]
   locks = "cmd:all()"
   arg_regex = r"\s|$"

   def func(self):
       """Implement armor"""

       spell = rules_skills.get_skill(skill_name=self.key)
       caster = self.caller
       cost = rules_magic.mana_cost(caster, spell)


       if "armor" not in caster.db.skills:
           caster.msg("You do not know the spell '%s' yet!" % self.key)
           return

       if caster.position != "standing":
           caster.msg("You have to stand to concentrate enough to cast.")
           return

       # Check whether anything about the room or affects on the caster
       # would prevent casting. Check_cast returns output for the state
       # if true, False if not.

       if rules_magic.check_cast(caster):
           caster.msg(rules_magic.check_cast(caster))
           return
       if caster.mana_current < cost:
           caster.msg("You do not have sufficient mana to cast %s!" % self.key)
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
               caster.msg("There is no %s here on whom to cast %s." % (self.args, self.key))
               return
           if not rules.is_visible(target, caster):
               caster.msg("There is no %s here on whom to cast %s." % (self.args, self.key))
               return

       if target.get_affect_status(self.key):
           if target == caster:
               subject = "You are"
           else:
               subject = "%s is" % (target.key[0].upper() + target.key[1:])

           caster.msg("%s already affected by %s.\n" % (subject, self.key))
           return

       rules_magic.do_armor(caster, target, cost)


class CmdBamf(MuxCommand):
    """
    Cast a spell to banish a mobile from the room.

    Usage:
      cast bamf <target>
      bamf <target>

    Bamf banishes a mobile from the room to another
    room in the same area.

    Colleges that can teach (level):
    Mage (6), Bard (15)
    """

    key = "bamf"
    aliases = ["cast bamf"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement bamf"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "bamf" not in caster.db.skills:
            caster.msg("You do not know the spell 'bamf' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
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
            caster.msg("You do not have sufficient mana to cast bamf!")
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
                caster.msg("There is no %s here to bamf." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to bamf." % self.args)
                return

        if rules_combat.is_safe(target):
            caster.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
            return

        rules_magic.do_bamf(caster, target, cost)


class CmdBless(MuxCommand):
    """
    Bless yourself or a target.

    Usage:
      cast bless <target>
      cast bless
      bless

    Bless will provide extra spell and breath defense for you or a
    target, as well as additional hitroll. Cast with no target, it
    targets the caster.

    Colleges that can teach (level):
    Cleric (6), Paladin (12)
    """

    key = "bless"
    aliases = ["cast bless"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement bless"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)


        if "bless" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
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
                caster.msg("There is no %s here to bless." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to bless." % self.args)
                return

        if target.get_affect_status(self.key):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already affected by %s.\n" % (subject, self.key))
            return

        rules_magic.do_bless(caster, target, cost)


class CmdBurningHands(MuxCommand):
    """
    Cast a spell to cause magical damage to an enemy.

    Usage:
      cast burning hands <target>
      burning hands <target>

    Burning hands simply does damage to your enemy.

    Colleges that can teach (level):
    Mage (6)
    """

    key = "burning hands"
    aliases = ["cast burning hands"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement burning hands"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "burning hands" not in caster.db.skills:
            caster.msg("You do not know the spell 'burning hands' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast burning hands!")
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
                caster.msg("There is no %s here to hit with your burning hands." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to hit with your burning hands." % self.args)
                return

        if rules_combat.is_safe(target):
            caster.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
            return

        if not caster.ndb.combat_handler:
            combat = rules_combat.create_combat(caster, target)
            rules_magic.do_burning_hands(caster, target, cost)
            if combat in caster.location.contents:
                combat.at_repeat()
        else:
            rules_magic.do_burning_hands(caster, target, cost)


class CmdCauseLight(MuxCommand):
    """
    Cast a spell to inflict damage on an enemy.

    Usage:
      cast cause light <target>
      cause light <target>

    Cause light wounds is one of a family of healing-type
    spells that essentially reverse healing.

    Colleges that can teach (level):
    Cleric (5), Paladin (15)
    """

    key = "cause light"
    aliases = ["cast cause light"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement cause light"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "cause light" not in caster.db.skills:
            caster.msg("You do not know the spell 'cause light' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
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
            caster.msg("You do not have sufficient mana to cast cause light!")
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
                caster.msg("There is no %s here to cause light wounds to." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to cause light wounds to." % self.args, self.key)
                return

        if rules_combat.is_safe(target):
            caster.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
            return

        if not caster.ndb.combat_handler:
            combat = rules_combat.create_combat(caster, target)
            rules_magic.do_cause_light(caster, target, cost)
            if combat in caster.location.contents:
                combat.at_repeat()
        else:
            rules_magic.do_cause_light(caster, target, cost)


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

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
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
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to chill with your touch." % self.args)
                return

        if rules_combat.is_safe(target):
            caster.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
            return

        if not caster.ndb.combat_handler:
            combat = rules_combat.create_combat(caster, target)
            rules_magic.do_chill_touch(caster, target, cost)
            if combat in caster.location.contents:
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

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast continual light!")
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

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
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

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
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
        if not rules.is_visible(target, caster):
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

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
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
        if not rules.is_visible(target_container, caster):
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

        
class CmdCureLight(MuxCommand):
    """
    Cast a spell to restore hitpoints to a target.

    Usage:
      cast cure light <target>
      cure light <target>

    Cure light wounds restores a small amount of hitpoints to a wounded
    target.

    Colleges that can teach (level):
    Cleric (5), Druid (7), Paladin (15), Bard (18)
    """

    key = "cure light"
    aliases = ["cast cure light"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement cure light"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "cure light" not in caster.db.skills:
            caster.msg("You do not know the spell 'cure light' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast cure light!")
            return

        if not self.args:

            target = caster

        else:
            mobiles = []
            for object in caster.location.contents:
                if "mobile" in object.tags.all() or "player" in object.tags.all():
                    mobiles.append(object)
            target = caster.search(self.args, candidates=mobiles)
            if not target:
                caster.msg("There is no %s here to cure light wounds on." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to cure light wounds on." % self.args)
                return

        if target:
            rules_magic.do_cure_light(caster, target, cost)

            
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
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
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
                caster.msg("There is no %s here on whom to cast %s." % (self.args, self.key))
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here on whom to cast %s." % (self.args, self.key))
                return

        if target.get_affect_status(self.key):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already affected by %s.\n" % (subject, self.key))
            return

        rules_magic.do_detect_evil(caster, target, cost)


class CmdDetectHidden(MuxCommand):
    """
    Allow yourself or a target to detect hidden characters.

    Usage:
      cast detect hidden <target>
      cast detect hidden
      detect hidden

    Detect hidden will cause any hidden characters to become
    visible for a time. Cast with no target, it targets the
    caster.

    Colleges that can teach (level):
    Mage (5), Cleric (8), Druid (10), Ranger (18), Thief (25)
    """

    key = "detect hidden"
    aliases = ["cast detect hidden"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement detect hidden"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "detect hidden" not in caster.db.skills:
            caster.msg("You do not know the spell 'detect hidden' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast detect hidden!")
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
                caster.msg("There is no %s here on whom to cast detect hidden." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here on whom to cast detect hidden." % self.args)
                return

        if target.get_affect_status("detect hidden"):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already affected by detect hidden.\n" % subject)
            return

        rules_magic.do_detect_hidden(caster, target, cost)


class CmdDetectInvis(MuxCommand):
    """
    Enable yourself or a target to detect invisible objects and
    characters.

    Usage:
      cast detect invis <target>
      cast detect invis
      detect invis

    Detect invis will allow you or a target, to detect invisible objects
    and characters for a time. Cast with no target, it targets the caster.

    Colleges that can teach (level):
    Mage (6), Cleric (13), Thief (33)
    """

    key = "detect invis"
    aliases = ["cast detect invis"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement detect invis"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)

        if "detect invis" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
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
                caster.msg("There is no %s here on whom to cast %s." % (self.args, self.key))
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here on whom to cast %s." % (self.args, self.key))
                return

        if target.get_affect_status(self.key):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already affected by %s.\n" % (subject, self.key))
            return

        rules_magic.do_detect_invis(caster, target, cost)


class CmdDetectMagic(MuxCommand):
    """
    Allow yourself or a target to detect magic in items.

    Usage:
      cast detect magic <target>
      cast detect magic
      detect magic

    Detect magic will cause any magical items to show up with
    a (Magical) aura for a time. Cast with no target, it
    targets the caster.

    Colleges that can teach (level):
    Mage (5), Cleric (8), Bard (12)
    """

    key = "detect magic"
    aliases = ["cast detect magic"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement detect magic"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "detect magic" not in caster.db.skills:
            caster.msg("You do not know the spell 'detect magic' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast detect magic!")
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
                caster.msg("There is no %s here on whom to cast detect magic." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here on whom to cast detect magic." % self.args)
                return

        if target.get_affect_status("detect magic"):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already affected by detect magic.\n" % subject)
            return

        rules_magic.do_detect_magic(caster, target, cost)

        
class CmdFaerieFog(MuxCommand):
    """
    Create a magical fog to reveal hidden characters.

    Usage:
      cast faerie fog
      faerie fog

    Create a magical fog that will cause hidden, sneaking and invisible
    characters to become visible to all in the room.

    Colleges that can teach (level):
    Druid (6)
    """

    key = "faerie fog"
    aliases = ["cast faerie fog"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement faerie fog"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "faerie fog" not in caster.db.skills:
            caster.msg("You do not know the spell 'faerie fog' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast faerie fog!")
            return

        rules_magic.do_faerie_fog(caster, cost)


class CmdFirebolt(MuxCommand):
    """
    Cast a spell to cause magical damage to an enemy.

    Usage:
      cast firebolt <target>
      firebolt <target>

    Firebolt simply does damage to your enemy. At level
    20, firebolt will flare for an additional hit (albeit at lower
    damage), and again each 10 levels after that up to level
    50.

    Colleges that can teach (level):
    Mage (10)
    """

    key = "firebolt"
    aliases = ["cast firebolt"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement firebolt"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "firebolt" not in caster.db.skills:
            caster.msg("You do not know the spell 'firebolt' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
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
            caster.msg("You do not have sufficient mana to cast firebolt!")
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
                caster.msg("There is no %s here to hit with your firebolt." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to hit with your firebolt." % self.args)
                return

        if rules_combat.is_safe(target):
            caster.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
            return

        if not caster.ndb.combat_handler:
            combat = rules_combat.create_combat(caster, target)
            rules_magic.do_burning_hands(caster, target, cost)
            if combat in caster.location.contents:
                combat.at_repeat()
        else:
            rules_magic.do_firebolt(caster, target, cost)


class CmdFly(MuxCommand):
    """
    Enable yourself or a target to fly.

    Usage:
      cast fly <target>
      cast fly
      fly

    Fly allows you or a target to avoid some of the
    effects of terrain, and renders you invulnerable to
    tripping, but also leaves you unable to trip others.

    Colleges that can teach (level):
    Mage (9)
    """

    key = "fly"
    aliases = ["cast fly"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement fly"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)


        if "fly" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
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
                caster.msg("There is no %s here to cast fly on." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to cast fly on." % self.args)
                return

        if target.get_affect_status("fly"):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already flying.\n" % subject)
            return

        rules_magic.do_fly(caster, target, cost)


class CmdGiantStrength(MuxCommand):
    """
    Lend the strength of a giant to yourself or a target.
    Usage:
      cast giant strength <target>
      cast giant strength
      giant strength
    Giant strength will provide extra strength for you or a
    target. Cast with no target, it targets the caster.

    Colleges that can teach (level):
    Mage (9), Warrior (66)
    """

    key = "giant strength"
    aliases = ["cast giant strength"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement giant strength"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)

        if "giant strength" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
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
                caster.msg("There is no %s here on whom to cast %s." % (self.args, self.key))
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here on whom to cast %s." % (self.args, self.key))
                return

        if target.get_affect_status(self.key):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s is already affected by %s.\n" % (subject, self.key))
            return

        rules_magic.do_giant_strength(caster, target, cost)


class CmdInfravision(MuxCommand):
    """
    Give the ability to see in the dark to yourself or a target.
    Usage:
      cast infravision <target>
      cast infravision
      infravision
    Infravision will provide the ability for you or a target to see in
    the dark, if you cannot already do so due to a racial ability.
    Cast with no target, it targets the caster.

    Colleges that can teach (level):
    Druid (9), Ranger (22)
    """

    key = "infravision"
    aliases = ["cast infravision"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement infravision"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)

        if "infravision" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
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
                caster.msg("There is no %s here on whom to cast %s." % (self.args, self.key))
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here on whom to cast %s." % (self.args, self.key))
                return

        if target.get_affect_status(self.key):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already affected by %s.\n" % (subject, self.key))
            return

        rules_magic.do_infravision(caster, target, cost)


class CmdInvis(MuxCommand):
    """
    Make yourself or a target become invisible.

    Usage:
      cast invis <target>
      cast invis
      invis

    Invis will allow either you or a target to become invisible.
    Cast without a target, it targets the caster.

    Colleges that can teach (level):
    Mage (10), Druid (35), Thief (60)
    """

    key = "invis"
    aliases = ["cast invis"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement invis"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)

        if "invis" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
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
                caster.msg("There is no %s here on whom to cast %s." % (self.args, self.key))
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here on whom to cast %s." % (self.args, self.key))
                return

        if target.get_affect_status(self.key):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already affected by %s.\n" % (subject, self.key))
            return

        rules_magic.do_invis(caster, target, cost)


class CmdLevitation(MuxCommand):
    """
    Enable yourself or a target to levitate above the ground.

    Usage:
      cast levitation <target>
      cast levitation
      levitation

    Levitation allows you or a target to avoid some of the
    effects of terrain, and renders you invulnerable to
    tripping, but also leaves you unable to trip others.

    Colleges that can teach (level):
    Psionicist (7)
    """

    key = "levitation"
    aliases = ["cast levitation"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement levitation"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)


        if "levitation" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
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
                caster.msg("There is no %s here to levitate." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to levitate." % self.args)
                return

        if target.get_affect_status("fly"):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already flying.\n" % subject)
            return

        rules_magic.do_levitation(caster, target, cost)


class CmdMagicMissile(MuxCommand):
    """
    Cast a spell to cause magical damage to an enemy.

    Usage:
      cast magic missile <target>
      magic missile <target>

    Magic missile simply does damage to your enemy.

    Colleges that can teach (level):
    Mage (4), Bard (8)
    """

    key = "magic missile"
    aliases = ["cast magic missile"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement magic missile"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "magic missile" not in caster.db.skills:
            caster.msg("You do not know the spell 'magic missile' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
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
            caster.msg("You do not have sufficient mana to cast magic missile!")
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
                caster.msg("There is no %s here to hit with your magic missile." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to hit with your magic missile." % self.args)
                return

        if rules_combat.is_safe(target):
            caster.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
            return

        if not caster.ndb.combat_handler:
            combat = rules_combat.create_combat(caster, target)
            rules_magic.do_magic_missile(caster, target, cost)
            if combat in caster.location.contents:
                combat.at_repeat()
        else:
            rules_magic.do_magic_missile(caster, target, cost)


class CmdMentalBarrier(MuxCommand):
    """
    Create a mental barrier around yourself.

    Usage:
      cast mental barrier
      mental barrier

    This spell uses your mental energy to create a barrier
    around you that will provide extra armor.

    Colleges that can teach (level):
    Psionicist (6)
    """

    key = "mental barrier"
    aliases = ["cast mental barrier"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement mental barrier"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)

        if "mental barrier" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
            return
        target = caster

        if target.get_affect_status(self.key):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already affected by %s.\n" % (subject, self.key))
            return

        rules_magic.do_mental_barrier(caster, target, cost)


class CmdMindThrust(MuxCommand):
    """
    Cast a spell to cause magical damage to an enemy.

    Usage:
      cast mind thrust <target>
      mind thrust <target>

    Mind thrust does damage to your enemy that avoids
    a saving throw.

    Colleges that can teach (level):
    Psionicist (7)
    """

    key = "mind thrust"
    aliases = ["cast mind thrust"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement mind thrust"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "mind thrust" not in caster.db.skills:
            caster.msg("You do not know the spell 'mind thrust' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
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
            caster.msg("You do not have sufficient mana to cast mind thrust!")
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
                caster.msg("There is no %s here to hit with your mind thrust." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to hit with your mind thrust." % self.args)
                return

        if rules_combat.is_safe(target):
            caster.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
            return

        if not caster.ndb.combat_handler:
            combat = rules_combat.create_combat(caster, target)
            rules_magic.do_burning_hands(caster, target, cost)
            if combat in caster.location.contents:
                combat.at_repeat()
        else:
            rules_magic.do_mind_thrust(caster, target, cost)


class CmdProtection(MuxCommand):
    """
    Create magical protection for yourself or a target.

    Usage:
      cast protection <target>
      cast protection
      protection

    Protection reduces the damage of all attacks by 1/4. Cast with
    no target, it targets the caster.

    Colleges that can teach (level):
    Cleric (7), Druid (8), Paladin (16)
    """

    key = "protection"
    aliases = ["cast protection"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement protection"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)


        if "protection" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
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
                caster.msg("There is no %s here on whom to bestow your protection." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here on whom to bestow your protection." % self.args)
                return

        if target.get_affect_status(self.key):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already affected by %s.\n" % (subject, self.key))
            return

        rules_magic.do_protection(caster, target, cost)


class CmdRefresh(MuxCommand):
    """
    Cast a spell to restore movement points to a target.

    Usage:
      cast refresh <target>
      refresh <target>

    Refresh restores some amount of the lost movement points
    of a target.

    Colleges that can teach (level):
    Druid (4), Ranger (16)
    """

    key = "refresh"
    aliases = ["cast refresh"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement refresh"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "refresh" not in caster.db.skills:
            caster.msg("You do not know the spell 'refresh' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast refresh!")
            return

        if not self.args:

            target = caster

        else:
            mobiles = []
            for object in caster.location.contents:
                if "mobile" in object.tags.all() or "player" in object.tags.all():
                    mobiles.append(object)
            target = caster.search(self.args, candidates=mobiles)
            if not target:
                caster.msg("There is no %s here to refresh." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to refresh." % self.args)
                return

        if target:
            rules_magic.do_refresh(caster, target, cost)


class CmdShield(MuxCommand):
    """
    Shield yourself or a target with magical force.

    Usage:
      cast shield <target>
      cast shield
      shield

    Shield will provide extra defense for you or a target. Cast
    with no target, it targets the caster.

    Colleges that can teach (level):
    Mage (7)
    """

    key = "shield"
    aliases = ["cast shield"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement shield"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)


        if "shield" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
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
                caster.msg("There is no %s here to shield." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to shield." % self.args)
                return

        if target.get_affect_status(self.key):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already affected by %s.\n" % (subject, self.key))
            return

        rules_magic.do_shield(caster, target, cost)


class CmdShockingGrasp(MuxCommand):
    """
    Cast a spell to cause magical damage to an enemy.

    Usage:
      cast shocking grasp <target>
      shocking grasp <target>

    Shocking grasp simply does damage to your enemy.
    Colleges that can teach (level):
    Mage (8)
    """

    key = "shocking grasp"
    aliases = ["cast shocking grasp"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement shocking grasp"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "shocking grasp" not in caster.db.skills:
            caster.msg("You do not know the spell 'shocking grasp' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
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
            caster.msg("You do not have sufficient mana to cast shocking grasp!")
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
                caster.msg("There is no %s here to hit with your shocking grasp." % self.args)
                return
            if not rules.is_visible(target, caster):
                caster.msg("There is no %s here to hit with your shocking grasp." % self.args)
                return

        if rules_combat.is_safe(target):
            caster.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
            return

        if not caster.ndb.combat_handler:
            combat = rules_combat.create_combat(caster, target)
            rules_magic.do_burning_hands(caster, target, cost)
            if combat in caster.location.contents:
                combat.at_repeat()
        else:
            rules_magic.do_shocking_grasp(caster, target, cost)


class CmdSlumber(MuxCommand):
    """
    Induce a magical slumber in a target.

    Usage:
      cast slumber <target>
      slumber <target>

    Magically induce slumber in your target. Will automatically
    fail against targets of a higher leve.

    Colleges that can teach (level):
    Bard (8)
    """

    key = "slumber"
    aliases = ["cast slumber"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement sleep"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)


        if "sleep" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
            return

        targets = []
        for object in caster.location.contents:
            if "mobile" in object.tags.all():
                targets.append(object)

        target = caster.search(self.args, candidates=targets)

        if not target:
            caster.msg("There is no %s here to put into a slumber." % self.args)
            return
        if not rules.is_visible(target, caster):
            caster.msg("There is no %s here to put into a slumber." % self.args)
            return

        if target.get_affect_status(self.key):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already asleep.\n" % subject)
            return

        rules_magic.do_slumber(caster, target, cost)


class CmdSummonWeapon(MuxCommand):
    """
    Summon a Paladin's holy weapon.

    Usage:
      cast summon weapon
      summon weapon

    Summons a Paladin's holy weapon, equal to caster's level.

    Colleges that can teach (level):
    Paladin (4)
    """

    key = "summon weapon"
    aliases = ["cast summon weapon"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """Implement summon weapon"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "summon weapon" not in caster.db.skills:
            caster.msg("You do not know the spell 'summon weapon' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast summon weapon!")
            return

        rules_magic.do_summon_weapon(caster, cost)


class CmdThoughtShield(MuxCommand):
    """
    Use your mental powers to create a shield around yourself.

    Usage:
      cast thought shield
      thought shield

    Thought shield will improve your armor class for a time.

    Colleges that can teach (level):
    Psionicist (10)
    """

    key = "thought shield"
    aliases = ["cast thought shield"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement thought shield"""

        spell = rules_skills.get_skill(skill_name=self.key)
        caster = self.caller
        cost = rules_magic.mana_cost(caster, spell)

        if "thought shield" not in caster.db.skills:
            caster.msg("You do not know the spell '%s' yet!" % self.key)
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.

        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return
        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast %s!" % self.key)
            return

        target = caster

        if target.get_affect_status(self.key):
            if target == caster:
                subject = "You are"
            else:
                subject = "%s is" % (target.key[0].upper() + target.key[1:])

            caster.msg("%s already affected by %s.\n" % (subject, self.key))
            return

        rules_magic.do_thought_shield(caster, target, cost)


class CmdVentriloquate(MuxCommand):
    """
    A spell that puts words in the mouths of other players and
    mobiles.

    Usage:
      cast ventriloquate <target> says <speech string>
      ventriloquate <target> says <speech string>

    A spell that attempts to make it seem as though a mobile or player
    has said a word or sentence. A player that saves against the spell
    will know that you forced the player or mobile to say the words.

    Colleges that can teach (level):
    Bard (5)
    """

    key = "ventriloquate"
    aliases = ["cast ventriloquate", "vent"]
    delimiter = " says "
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement ventriloquate"""

        spell = rules_skills.get_skill(skill_name=self.key)

        caster = self.caller

        if "ventriloquate" not in caster.db.skills:
            caster.msg("You do not know the spell 'ventriloquate' yet!")
            return

        if caster.position != "standing":
            caster.msg("You have to stand to concentrate enough to cast.")
            return

        if not self.args or not self.lhs or not self.rhs:
            caster.msg("Usage: ventriloquate <target> says <speech string>")
            return

        speakers = []
        for object in caster.location.contents:
            if "player" in object.tags.all() or "mobile" in object.tags.all():
                speakers.append(object)

        target = caster.search(self.lhs, location=[caster.location], candidates=speakers)

        if not target:
            caster.msg("There is no %s here to ventriloquate on." % self.lhs)
            return
        if not rules.is_visible(target, caster):
            caster.msg("There is no %s here to ventriloquate on." % self.lhs)
            return

        # Check whether anything about the room or affects on the caster
        # would prevent casting. Check_cast returns output for the state
        # if true, False if not.
        if rules_magic.check_cast(caster):
            caster.msg(rules_magic.check_cast(caster))
            return

        cost = rules_magic.mana_cost(caster, spell)

        if caster.mana_current < cost:
            caster.msg("You do not have sufficient mana to cast ventriloquate!")
            return

        rules_magic.do_ventriloquate(caster, cost, target, self.rhs)


