import random
from evennia import create_object
from evennia import TICKER_HANDLER as tickerhandler
from evennia.utils import search
from commands.command import MuxCommand
from server.conf import settings
from typeclasses.objects import Object
from world import rules_combat, rules_skills, rules


class Combat(Object):
    """
    
    This is the class for instances of combat in rooms of the MUD.
    
    """

    def at_object_creation(self):
        self.db.combatants = {}
        self.db.rounds = 0
        self.x = 1
        tickerhandler.add(2, self.at_repeat)

    def at_stop(self):
        # Called just before the script is stopped/destroyed.
        for combatant in list(self.db.combatants.keys()):
            # note: the list() call above disconnects list from database,
            # needed because you are going to be removing things from the
            # combatants dictionary.
            self._cleanup_combatant(combatant)

    def msg_all(self, message):
        "Send message to all combatants"
        for combatant in self.db.combatants:
            self.db.combatants[combatant]["combatant"].msg(message)

    def allow_attacks(self, combatant, target):
        """
        Checks whether the combatant and target for this round are still alive, returns
        True if so, False if not.

        """
        if "mobile" in combatant.tags.all():
            if combatant.hitpoints_current <= 0:
                return False
        elif "mobile" in target.tags.all():
            if target.hitpoints_current <= 0:
                return False
        if "player" in combatant.tags.all():
            if combatant.hitpoints_current <= 0:
                return False
        elif "player" in target.tags.all():
            if target.hitpoints_current <= 0:
                return False

        if combatant.location != target.location:
            return False

        return True

    def combat_end_check(self):
        """
        Checks to see whether the combat should end.
        """

        # Check to see whether everyone in the combat is on the "same side" (player or mobile), and
        # end the combat.
        combatant_list = list(self.db.combatants.keys())

        # Check to see what type of combatant the first one is.
        if "mobile" in combatant_list[0].tags.all():
            first_combatant_type = "mobile"
        else:
            first_combatant_type = "player"
        # Default is to end the combat.
        combat_end = True

        # Cycle through combatants, and check their type.
        for combatant in combatant_list:
            if "mobile" in combatant.tags.all():
                combatant_type = "mobile"
            else:
                combatant_type = "player"

            # Check against first one. If any are different, set combat_end to False, and stop looking.
            if combatant_type != first_combatant_type:
                combat_end = False
                break;

        if combat_end == True:
            self.at_stop()
            self.delete()

    def at_repeat(self):

        self.clear_messages()

        # Copy the dictionary, in case changes are made to it during the round.
        # combat_dict = dict(self.db.combatants)
        round_output = {}
        round_combatants_list = []
        for combatant in self.db.combatants:
            round_combatants_list.append(combatant)

        # Iterate through combatants to do a round of attacks.
        for combatant in round_combatants_list:
            if combatant in self.db.combatants:

                # First, check to see if the combatant is below their wimpy.
                if combatant.hitpoints_current > 0 and (("player" in combatant.tags.all() and
                    combatant.hitpoints_current <= combatant.db.wimpy) or \
                        ("mobile" in combatant.tags.all() and
                         "wimpy" in combatant.db.act_flags and
                         combatant.hitpoints_current <= (0.15 * combatant.hitpoints_maximum
                         ))):

                    # Make a free attempt to flee.
                    rules_combat.do_flee(combatant)

                # Make sure this combatant and target are alive and both still in the same room.
                if combatant.location == self.location and self.allow_attacks(combatant, self.db.combatants[combatant]["target"]):
                    attacker = self.db.combatants[combatant]["combatant"]
                    victim = self.db.combatants[combatant]["target"]

                    # Do the attacks for this attacker, and get output.
                    attacker_string, victim_string, room_string = rules_combat.do_one_character_attacks(attacker, victim)

                    # Add output to the rest of the output generated this round

                    for output_receiver in round_combatants_list:
                        if output_receiver == attacker:
                            if output_receiver not in round_output:
                                round_output[output_receiver] = attacker_string
                            else:
                                round_output[output_receiver] += attacker_string
                        elif output_receiver == victim:
                            if output_receiver not in round_output:
                                round_output[output_receiver] = victim_string
                            else:
                                round_output[output_receiver] += victim_string
                        else:
                            if output_receiver not in round_output:
                                round_output[output_receiver] = room_string
                            else:
                                round_output[output_receiver] += room_string

        for combatant in round_combatants_list:
            combatant.msg(round_output[combatant])

            # If the player and their target are still alive, tell them the status of their target.
            if combatant.ndb.combat_handler and "player" in combatant.tags.all():
                if self.db.combatants[combatant]["target"].location == combatant.location:
                    target = self.db.combatants[combatant]["target"]
                    combat_message = ("%s %s\n" % ((target.key[0].upper() + target.key[1:]), rules_combat.get_health_string(target)))
                    combatant.msg(combat_message)

                    if "wait_state" not in combatant.ndb.all:
                        prompt_wait = "|gReady!|n"
                    elif combatant.ndb.wait_state >= 12:
                        prompt_wait = "|rCompleting action!"
                    elif combatant.ndb.wait_state > 0:
                        prompt_wait = "|yRecovering.|n"
                    else:
                        prompt_wait = "|gReady!|n"
                    prompt = "<|r%d|n/|R%d hp |b%d|n/|B%d mana |y%d|n/|Y%d moves|n %s>\n" % (combatant.hitpoints_current,
                                                                                             combatant.hitpoints_maximum,
                                                                                             combatant.mana_current,
                                                                                             combatant.mana_maximum,
                                                                                             combatant.moves_current,
                                                                                             combatant.moves_maximum,
                                                                                             prompt_wait)
                    combatant.msg(prompt=prompt)

        if combatant.hitpoints_current <= 0 and "player" in combatant.tags.all():

            # Reset dead players to one hitpoint, and move to home. Mobile hitpoints will get reset by reset
            # function.
            combatant.db.hitpoints["damaged"] = (combatant.hitpoints_maximum - 1)
            combatant.move_to(combatant.home, quiet=True)

        if self.db.combatants:
            self.db.rounds += 1

            self.combat_end_check()

        if self.db.combatants:
            # Check to see if any other mobiles in the room jump in.

            # Get all possible assisting mobiles.
            possible_assists = []
            for object in self.location.contents:
                if "mobile" in object.tags.all():
                    if not object.ndb.combat_handler:
                        possible_assists.append(object)

            # Get players that are in combat.
            possible_targets = []
            for combatant in self.db.combatants:
                if "player" in combatant.tags.all():
                    possible_targets.append(combatant)

            # Run through possible assisting mobiles.
            for candidate in possible_assists:

                # Get a random seen player from those found.
                seen_targets = []
                for target in possible_targets:
                    if rules.can_see(target, candidate):
                        seen_targets.append(target)
                if seen_targets:
                    random_player = seen_targets[random.randint(0, (len(seen_targets) - 1))]
                    if (candidate.level - 7) < random_player.level < (candidate.level + 7) and not (
                            random_player.alignment > 333 and candidate.alignment > 333):
                        to_be_assisted = self.db.combatants[random_player]["target"]
                        if candidate.db.vnum == to_be_assisted.db.vnum:
                            self.add_combatant(candidate, random_player)
                            break
                        elif random.randint(1, 8) == 1:
                            self.add_combatant(candidate, random_player)
                            break

    def clear_messages(self):
        for combatant in self.db.combatants:
            self.db.combatants[combatant]["combat message"] = ""

    def _init_combatant(self, combatant):
        """
        This initializes handler back-reference.        
        """
        combatant.ndb.combat_handler = self

    # Combat-handler methods

    def find_other_attackers(self, seeking_target):
        """
        This method is called when the target of a
        combatant dies, to see if there is anyone else
        attacking that combatant. If so, it will automatically
        make that its new target, and return the target. If
        not, returns False
        """

        for combatant in self.db.combatants:
            if self.db.combatants[combatant]["target"] == seeking_target:
                self.db.combatants[seeking_target]["target"] = combatant
                return combatant

        return False


    def add_combatant(self, combatant, combatant_target):

        # Add combatant to handler
        self.db.combatants[combatant] = {"combatant": combatant, "target": combatant_target, "combat message": "", "special attack": {}, "wait state": 0}

        # set up back-reference
        self._init_combatant(combatant)

    def change_target(self, attacker, victim):
        self.db.combatants[attacker]["target"] = victim

    def get_target(self, attacker):
        return self.db.combatants[attacker]["target"]

    def _cleanup_combatant(self, combatant):
        """
        Remove combatant from handler and clean
        it of the back-reference.
        """
        del self.db.combatants[combatant]
        del combatant.ndb.combat_handler
        
    def remove_combatant(self, combatant):
        "Remove combatant from handler"

        if combatant in self.db.combatants:
            self._cleanup_combatant(combatant)

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
            if "mobile" in object.tags.all():
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
            if "mobile" in object.tags.all():
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
                if "mobile" in object.tags.all():
                    mobiles.append(object)
            target = caller.search(self.args, candidates=mobiles)
            if not target:
                caller.msg("There is no %s here to kick." % self.args)
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
                if "mobile" in object.tags.all():
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
            target = caller.search(self.args, location=caller.location, candidates=players)
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
                if "mobile" in object.tags.all():
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
            wait_state = skill["wait state"]
            rules.affect_apply(caller,
                               "sitting",
                               (wait_state * 2),
                               "You slowly get to your feet, embarrassed at having tripped yourself.",
                               "%s gets up after tripping %s, likely hoping no one notices." % (caller, rules.pronoun_reflexive(caller)),
                               apply_1=["position", "sitting"]
                               )
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
