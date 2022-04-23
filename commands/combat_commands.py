import random
from evennia import create_object
from evennia import TICKER_HANDLER as tickerhandler
from evennia.utils import search
from commands.command import MuxCommand
from server.conf import settings
from typeclasses.objects import Object
from world import rules_combat, rules_skills, rules


class CmdAttack(MuxCommand):
    """
    Start combat against a mobile target.
    Usage:
      attack <mobile>
    Starts the default attacks rounds that occur in combat.
    """

    key = "attack"
    aliases = ["kill"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement attack"""

        attacker = self.caller

        if not self.args:
            attacker.msg("Usage: attack <mobile>")
            return

        if attacker.position != "standing":
            attacker.msg("You might want to try standing before initiating combat.")
            return

        mobiles = []
        for object in attacker.location.contents:
            if "mobile" in object.tags.all() and rules.is_visible(object, attacker):
                mobiles.append(object)
        victim = attacker.search(self.args, candidates=mobiles)
        if not victim:
            attacker.msg("There is no mobile named %s here to attack." % self.args)
            return
        elif "player" in victim.tags.all():
            attacker.msg("You cannot attack another player!")
            return

        combat = rules_combat.create_combat(attacker, victim)

        if combat:
            combat.at_repeat()

        rules.wait_state_apply(attacker, settings.TICK_ATTACK_ROUND)

class CmdConsider(MuxCommand):
    """
    Evaluate whether a mobile should be attacked.
    Usage:
      consider <mobile>
    When used on a mobile, consider will tell you the approximate risk of attacking
    the mobile by comparing levels, and a rough comparison of your current hitpoints.
    """

    key = "consider"
    aliases = ["con"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement consider"""

        caller = self.caller
        if not self.args:
            caller.msg("Usage: consider <mobile>")
            return

        mobiles = []
        for object in caller.location.contents:
            if "mobile" in object.tags.all() and rules.is_visible(object, caller):
                mobiles.append(object)
        mobile = caller.search(self.args, candidates=mobiles)
        if not mobile:
            caller.msg("There is no mobile named %s here to attack." % self.args)
            return
        elif "mobile" not in mobile.tags.all():
            caller.msg("You can only use consider on mobiles.")
            return

        # Create the string for the difference in level.
        level_difference = mobile.db.level - caller.db.level
        
        if level_difference <=-10:
            level_string = "You can kill %s |gnaked and weaponless|n." % mobile.key
        elif level_difference <=-5:
            level_string = "%s is |gno match|n for you." % (mobile.key[0].upper() + mobile.key[1:])
        elif level_difference <=-2:
            level_string = "%s looks like an |geasy kill|n." % (mobile.key[0].upper() + mobile.key[1:])
        elif level_difference <= 1:
            level_string = "The |yperfect match|n!"
        elif level_difference <= 4:
            level_string = "%s says 'Do you |yfeel lucky|n, punk?'." % (mobile.key[0].upper() + mobile.key[1:])
        elif level_difference <= 9:
            level_string = "%s laughs at you |rmercilessly|n." % (mobile.key[0].upper() + mobile.key[1:])
        else:
            level_string = "|rDeath|n will thank you for your gift."
        
        # Create the string for the mobile's overall health.
        health_string = rules_combat.get_health_string(mobile)
        
        # Create the string for the mobile's health relative to the hero's.
        health_difference = mobile.hitpoints_current - caller.hitpoints_current
        health_percent = (100 * health_difference / caller.hitpoints_current)
        
        if health_percent <= -90:
            health_percent_string = "%s is sickly and unwell compared to your health." % (mobile.key[0].upper() + mobile.key[1:])
        elif health_percent <= -50:
            health_percent_string = "You are substantially healthier than %s." % mobile.key
        elif health_percent <= -11:
            health_percent_string = "You are somewhat healthier than %s." % mobile.key
        elif health_percent <= 10:
            health_percent_string = "You are about as healthy as %s." % mobile.key
        elif health_percent <= 50:
            health_percent_string = "%s is somewhat healthier than you." % (mobile.key[0].upper() + mobile.key[1:])
        elif health_percent <= 90:
            health_percent_string = "%s is substantially healthier than you." % (mobile.key[0].upper() + mobile.key[1:])
        else:
            health_percent_string = "Compared to %s, you should maybe consider a long-term hospital stay." % mobile.key
        
        caller.msg("%s\n%s %s\n%s\n" % (level_string, (mobile.key[0].upper() + mobile.key[1:]), health_string, health_percent_string))
    
class CmdDirtKicking(MuxCommand):
    """
    Kick dirt in the eyes of a combatant to blind them.
    Usage:
      dirt kick <mobile>
    Makes an attempt to kick dirt in the eyes of a combatant (or potential combatant),
    blinding them and doing minor damage. The attempt is affected by the terrain
    conditions - a desert dirt kick is more likely to be successful than one
    indoors.
    
    Colleges that can teach (level):
    Warrior (4), Ranger (4), Thief (22), Bard (27)
    """

    key = "dirt kick"
    aliases = ["dirt", "dk"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    wait_state = 12

    def func(self):
        caller = self.caller

        if "dirt kicking" not in caller.db.skills:
            caller.msg("You get your feet dirty, and not much else.")
            return

        if caller.position != "standing":
            caller.msg("You may want to get up out of the dirt before kicking it.")
            return

        if not self.args:

            if not caller.ndb.combat_handler:
                caller.msg("You are not in combat.")
                return
            else:
                combat = caller.ndb.combat_handler
                target = combat.get_target(caller)

        else:
            mobiles = []
            for object in caller.location.contents:
                if "mobile" in object.tags.all() and rules.is_visible(object, caller):
                    mobiles.append(object)
            target = caller.search(self.args, candidates=mobiles)
            if not target:
                caller.msg("There is no %s here to kick dirt at." % self.args)
                return
            else:

                if "player" in target.tags.all():
                    caller.msg("You cannot attack another player.")
                    return

                if target.get_affect_status("blind"):
                    caller.msg("%s has already been blinded." % (target.key[0].upper() + target.key[1:]))
                    return

                if rules_combat.is_safe(target):
                    caller.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
                    return
                
                if not caller.ndb.combat_handler:
                    combat = rules_combat.create_combat(caller, target)
                    rules_combat.do_dirt_kicking(caller, target)
                    combat.db.combatants[caller]["wait state"] = self.wait_state
                    if combat in caller.location.contents:
                        combat.at_repeat()
                    return

                else:
                    combat = caller.ndb.combat_handler

                    if "berserk" in caller.db.spell_affects and target != combat.get_target(caller):
                        caller.msg("You cannot switch targets while you are in the rage of battle!")
                        return

        if target.get_affect_status("blind"):
            caller.msg("%s has already been blinded." % (target.key[0].upper() + target.key[1:]))
            return
        
        if rules_combat.is_safe(target):
            caller.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
            return
                    
        rules_combat.do_dirt_kicking(caller, target)
            
class CmdFlee(MuxCommand):
    """
    Attempt to flee from combat.
    Usage:
      flee
    When you attempt to flee, you will try to exit from the room and combat. Your chance
    of success is decreased the less exits there are from the room, and you cannot flee
    through non-standard (n/e/s/w/u/d) exits. After level 5, you incur a slight
    experience penalty for fleeing from combat, and a decreased penalty for trying and
    failing.
    """

    key = "flee"
    locks = "cmd:all()"
    arg_regex = r"\s|$"
        
    def func(self):
        """Implement flee"""        

        caller = self.caller
        location = caller.location
        success = False
        
        if "combat_handler" not in caller.ndb.all:
            caller.msg("You cannot flee when you are not in combat.")
            return

        rules_combat.do_flee(caller)  

class CmdKick(MuxCommand):
    """
    Make an aggressive kick strike at an enemy
    Usage:
      kick <target>
      kick
    Makes an aggressive kick strike at an enemy, if you have learned the
    ability. Can only be used without a target in combat, where it will
    attack your current target.
    Colleges that can teach (level):
    Warrior (3), Ranger (10), Paladin (12)
    """

    key = "kick"
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    wait_state = 6

    def func(self):
        caller = self.caller

        if "kick" not in caller.db.skills:
            caller.msg("You'd better leave the martial arts to knowledgeable fighters.")
            return

        if caller.position != "standing":
            caller.msg("You can't kick from the ground.")
            return

        if "blind" in caller.db.spell_affects:
            caller.msg("It would help if you could see something to kick!")
            return

        if caller.moves_current < 10:
            caller.msg("You are too tired to kick your enemy currently!")
            return
        
        if not self.args:

            if not caller.ndb.combat_handler:
                caller.msg("You kick at the air, and look foolish doing it.")
                return
            else:
                combat = caller.ndb.combat_handler
                target = combat.get_target(caller)
                rules_combat.do_kick(caller, target)

        else:
            mobiles = []
            for object in caller.location.contents:
                if "mobile" in object.tags.all() and rules.is_visible(object, caller):
                    mobiles.append(object)
            target = caller.search(self.args, candidates=mobiles)
            if not target:
                caller.msg("There is no %s here to kick." % self.args)
                return
            else:

                if "player" in target.tags.all():
                    caller.msg("You cannot attack another player.")
                    return

                if rules_combat.is_safe(target):
                    caller.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
                    return

                if not caller.ndb.combat_handler:
                    combat = rules_combat.create_combat(caller, target)
                    rules_combat.do_kick(caller, target)
                    if combat in caller.location.contents:
                        combat.at_repeat()
                    return

                else:
                    combat = caller.ndb.combat_handler

                    if "berserk" in caller.db.spell_affects and target != combat.get_target(caller):
                        caller.msg("You cannot switch targets while you are in the rage of battle!")
                        return

                    rules_combat.do_kick(caller, target)

class CmdRescue(MuxCommand):
    """
    Rescue a friend currently being attacked by an enemy.
    Usage:
      rescue <target>
    Makes an attempt at stepping between an enemy and a friendly
    player, causing that enemy to begin attacking you, instead.
    Colleges that can teach (level):
    Paladin (3), Warrior (4), Ranger (11)
    """

    key = "rescue"
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    wait_state = 12

    def func(self):
        caller = self.caller

        if "kick" not in caller.db.skills:
            caller.msg("You'd better leave heroic acts to knowledgeable fighters.")
            return

        if caller.position != "standing":
            caller.msg("You can't rescue anyone on the ground.")
            return

        if "berserk" in caller.db.spell_affects:
            caller.msg("You can't rescue anyone while you're BERSERK!")
            return

        if "blind" in caller.db.spell_affects:
            caller.msg("It might be helpful if you could see!")
            return

        if not self.args:
            caller.msg("Rescue whom?")
            return

        else:
            players = search.search_object_by_tag("player")
            visible_candidates = list(player for player in players if player.location == caller.location and rules.is_visible(player, caller))
            target = caller.search(self.args, candidates=visible_candidates)
            if not target:
                caller.msg("There is no player named %s here to rescue." % self.args)
                return
            else:

                if target == caller:
                    caller.msg("You're never going to be able to rescue yourself.")
                    return

                if not target.ndb.combat_handler:
                    subject = rules.pronoun_subject(target)
                    if subject == "they":
                        phrase = "they are"
                    else:
                        phrase = "%s is" % rules.pronoun_subject(target)

                    caller.msg("You cannot rescue %s, as %s not in combat!" % (target.key, phrase))
                    return

                combat = target.ndb.combat_handler
                victim = False

                # We need to iterate through the combat dictionary and make sure
                # that target is being attacked by someone.
                for combatant in combat.db.combatants:
                    if combat.db.combatants[combatant]["target"] == target:
                        victim = combatant

                if not victim:
                    subject = rules.pronoun_subject(target)
                    if subject == "they":
                        phrase = "they are"
                    else:
                        phrase = "%s is" % rules.pronoun_subject(target)

                    caller.msg("You cannot rescue %s, as %s not being attacked!" % (target.key, phrase))
                    return

                if not caller.ndb.combat_handler:
                    attack_target = combat.combatants[target]["target"]
                    combat.add_combatant(caller, attack_target)

                rules_combat.do_rescue(caller, target, victim)
                rules.wait_state_apply(caller, self.wait_state)


class CmdTrip(MuxCommand):
    """
    Make an aggressive tripping strike at an enemy
    Usage:
      trip <target>
      trip
    Makes an aggressive tripping strike at an enemy, if you have
    learned the ability. Can only be used without a target in
    combat, where it will attack your current target.

    Colleges that can teach (level):
    Thief (4), Bard (5), Ranger (14), Warrior (15)
    """

    key = "trip"
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    wait_state = 24

    def func(self):
        caller = self.caller

        if "trip" not in caller.db.skills:
            caller.msg("Tripping? What's that?")
            return

        if caller.position != "standing":
            caller.msg("You might want to try standing before trying to trip.")
            return

        if not self.args:

            if not caller.ndb.combat_handler:
                caller.msg("But you aren't fighting anyone!")
                return
            else:
                combat = caller.ndb.combat_handler
                target = combat.get_target(caller)

        else:
            mobiles = []
            for object in caller.location.contents:
                if "mobile" in object.tags.all() and rules.is_visible(object, caller):
                    mobiles.append(object)
            target = caller.search(self.args, candidates=mobiles)
            if not target:
                caller.msg("There is no %s here to trip." % self.args)
                return

            
        if target.get_affect_status("fly"):
            caller.msg("It is challenging to trip %s when %s feet aren't on the ground." % (target.key, rules.pronoun_possessive(target)))
            return
        elif caller.get_affect_status("fly"):
            caller.msg("%s's feet are on the ground ... but yours aren't." % (target.key[0].upper() + target.key[1:]))
            return
        elif target.get_affect_status("sitting"):
            caller.msg("%s is already down." % (target.key[0].upper() + target.key[1:]))
            return
        elif caller == target:
            caller.msg("You fall flat on your face! What did you expect?")
            skill = rules_skills.get_skill(skill_name="trip")
            wait_state = skill["wait state"] * 2
            caller.position = "sitting"
            return
        elif "player" in target.tags.all():
            caller.msg("You cannot attack another player.")
            return

        elif rules_combat.is_safe(target):
            caller.msg("%s is protected by the gods." % (target.key[0].upper() + target.key[1:]))
            return

        else:

            if not caller.ndb.combat_handler:
                combat = rules_combat.create_combat(caller, target)
                rules_combat.do_trip(caller, target)
                if combat in caller.location.contents:
                    combat.at_repeat()
                return

            else:
                rules_combat.do_trip(caller, target)


class CmdWimpy(MuxCommand):
    """
    Set your wimpy level.
    Usage:
      wimpy
      wimpy <hp amount>
    Wimpy is the amount of hitpoints at which you wish to get an automatic
    attempt to flee from combat each round. Using wimpy without any
    argument automatically sets your wimpy to 15% of your maximum hitpoints.
    """

    key = "wimpy"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement wimpy"""

        caller = self.caller

        if not self.args.isnumeric():
            if not self.args:
                caller.db.wimpy = int(caller.hitpoints_maximum * 0.15)
                caller.msg("Your wimpy has been set to %d." % caller.db.wimpy)
            else:
                caller.msg("Wimpy must be given a number as an argument, or no argument.")
            return
        else:
            caller.db.wimpy = int(self.args)
            caller.msg("Your wimpy has been set to %d." % caller.db.wimpy)
