import math
import random
import time
from objects import Object
from evennia import create_object
from evennia import logger
from evennia import TICKER_HANDLER as tickerhandler
from evennia.utils import search
from server.conf import settings
from world import rules, rules_race, rules_skills

class Combat_2(Object):
    """
    
    This is the new class for instances of combat in rooms of the MUD.
    
    """

    def at_object_creation(self):
        # This will be a dictionary with key of combatant and value of target.
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

    def change_target(self, attacker, victim):
        self.db.combatants[attacker] = victim

    def combat_end_check(self):
        """
        Checks to see whether the combat should end.
        """

        try:
            # Default is to end the combat.
            combat_end = True

            # Compile a list of all combatants.
            combatant_list = list(combatant for combatant in self.db.combatants)

            # Check to see what type of combatant the first one is, to check the remainder against
            if "mobile" in combatant_list[0].tags.all():
                first_combatant_type = "mobile"
            else:
                first_combatant_type = "player"

            # Cycle through combatants.
            for combatant in combatant_list:

                # Get the combatant type.
                if "mobile" in combatant.tags.all():
                    combatant_type = "mobile"
                else:
                    combatant_type = "player"

                # Check type against first one. If any awake combatants are different, set 
                # combat_end to False, and stop looking.
                if combatant_type != first_combatant_type and combatant.position != "sleeping":
                    combat_end = False
                    break;

            # If it should end after all that, stop the combat and delete the combat object.
            if combat_end == True:
                self.at_stop()
                self.delete()

        except Exception:
            logger.log_file("Error in combat end check.", filename="combat.log")
            logger.log_trace("Error in combat end check.")
                
    def combatant_add(self, combatant, combatant_target):

        # Add combatant to handler
        self.db.combatants[combatant] = combatant_target

        # set up back-reference
        self._combatant_init(combatant)

        # Wake up the target if they are asleep.
        if combatant_target.position != "standing":
            combatant_target.position = "standing"
            combatant_target.msg("An attack! You stand up to face your foe!")
            combatant_target.location.msg_contents("%s stands up to face %s foe!" % ((combatant_target.key[0].upper() + combatant_target.key[1:]),
                                                                                     rules.pronoun_possessive(combatant_target)
                                                                                     ), exclude=combatant_target)

    def _combatant_cleanup(self, combatant):
        """
        Remove combatant from handler and clean
        it of the back-reference.
        """
        del self.db.combatants[combatant]
        del combatant.ndb.combat_handler
    
    def _combatant_init(self, combatant):
        """
        This initializes handler back-reference.        
        """
        combatant.ndb.combat_handler = self
        
    def combatant_remove(self, combatant):
        "Remove combatant from handler"
        try:
            if combatant in self.db.combatants:
                self._combatant_cleanup(combatant)
        except Exception:
            logger.log_file("Error in removing combatant from combat." % combatant.key, filename="combat.log")
            logger.log_trace("Error in removing combatant from combat.")
            
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

    def get_target(self, attacker):
        return self.db.combatants[attacker]
        
    def at_repeat(self):

        # Copy the dictionary, in case changes are made to it during the round.
        # combat_dict = dict(self.db.combatants)
        round_combatants_list = list(combatant for combatant in self.db.combatants)

        # All at_repeat handles is whose turn it is in this round of combat. Everything
        # else is handled in rules_combat.
        for combatant in round_combatants_list:
            
            # First, check to make sure that combatant is still in the combat at this point.
            if combatant in self.db.combatants:

                try:
                    do_one_character_combat_turn(combatant, self.db.combatants[combatant], self)
                except Exception:
                    logger.log_file("Error in trying to do_one_character_combat_turn", filename="combat.log")

        # At the end of the round, if the player and their target are still alive, and in combat,
        # tell them the status of their target.
        try:
            for combatant in round_combatants_list:

                # Combatant is in the combat, and a player (no point in output to mobiles).
                if combatant in self.db.combatants and "player" in combatant.tags.all():

                    # Target's location is the same as combat.
                    if self.db.combatants[combatant].location == self.location:
                        target = self.db.combatants[combatant]
                        combat_message = ("%s %s\n" % ((target.key[0].upper() + target.key[1:]), get_health_string(target)))
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
            except Exception:
                logger.log_file("Error in trying to give end of round output.", filename="combat.log")
                logger.log_trace("Error in trying to give end of round output.")

        if self.db.combatants:
            self.db.rounds += 1

            self.combat_end_check()
        try:
            if self.db.combatants:
                # Check to see if any other mobiles in the room jump in before the next round.

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
        except Exception:
            logger.log_file("Error in checking to have mobiles jump in.", filename="combat.log")
            logger.log_trace("Error in checking to have mobiles jump in.")


                            
                            
                            
                            
                            
                            
                            
################# NEW COMBAT RULES ##############################

def allow_attacks(combatant, target, combat):
    """
    Checks whether the combatant and target for this round are still alive, returns
    True if so, False if not.
    """
    try:
        # Are both the attacker and target alive?
        if combatant.hitpoints_current <= 0 or target.hitpoints_current <= 0:
            return False

        # Are both the combatant and target in the same room as the combat?
        if combatant.location != combat.location or target.location != combat.location:
            return False
       
        return True

    except Exception:
        logger.log_file("Error in checking whether attacks are allowed. Combatant = %s, target = %s, combat = %s." % (combatant.key, target.key, combat.key), filename="combat.log")
        logger.log_trace("Error in checking whether attacks are allowed.")
        
def do_attack(attacker, victim, eq_slot, combat, **kwargs):
    """
    This function implements the effects of a single hit. It
    is used in two different modes. It is called with no
    kwargs when a standard attack-round attack, which calls
    the take_damage method on the victim, doing the damage,
    and giving output. The second mode allows special
    attacks (kick, fireball, damage on dirt kicking) to do
    the work on determining whether they hit, the amount
    of damage and output, and provide all of that to
    do_attack to handle the implementation.
    """

    parry = False
    dodge = False

    # Check to make sure that the attack is still appropriate, and
    # return if not.
    if not allow_attacks(attacker, victim, combat):
        return

    # First of all, check to see if the attacks hit.

    # For special attacks, get hit from kwargs.
    if "hit" in kwargs:
        hit = kwargs["hit"]
    # Base combat round attacks.
    else:
        hit = hit_check(attacker, victim)

        try:
            # Do checks for parry and dodge here, as they do not apply
            # to special attacks like kick, fireball, etc. This will
            # potentially turn hit to False from True, and create a
            # True variable of either dodge or parry.
            if hit:
                chance = 0
                # Randomize order of parry and dodge check - this way checks parry
                # first, then dodge.
                if random.randint(1, 2) > 1:
                    if "player" in victim.tags.all():
                        if "parry" in victim.db.skills:
                            if not victim.db.eq_slots["wielded, primary"]:
                                if not victim.db.eq_slots["wielded, secondary"]:
                                    chance = 0
                                else:
                                    chance = victim.db.skills["parry"] / 4
                            else:
                                chance = victim.db.skills["parry"] / 2

                    elif "mobile" in victim.tags.all():
                        chance = 2 * victim.level
                        if chance > 57:
                            chance = 57
                        if not victim.db.eq_slots["wielded, primary"]:
                            if not victim.db.eq_slots["wielded, secondary"]:
                                chance /= 2
                            else:
                                chance = chance * 3 / 4

                    if random.randint(1, 100) <= (chance + victim.level - attacker.level) and chance > 0:
                        hit = False
                        parry = True
                        if "player" in victim.tags.all():
                            rules_skills.check_skill_improve(victim, "parry", True, 5)

                    if "player" in victim.tags.all():
                        if "dodge" in victim.db.skills and parry == False:
                            chance = victim.db.skills["dodge"] / 2

                    elif "mobile" in victim.tags.all() and parry == False:
                        chance = 2 * victim.level
                        if chance > 55:
                            chance = 55

                    if random.randint(1, 100) <= (chance + victim.level - attacker.level) and parry == False and chance > 0:
                        hit = False
                        dodge = True
                        if "player" in victim.tags.all():
                            rules_skills.check_skill_improve(victim, "dodge", True, 5)
                # The other alternative - checking dodge, then parry.
                else:
                    if "player" in victim.tags.all():
                        if "dodge" in victim.db.skills:
                            chance = victim.db.skills["dodge"] / 2

                    elif "mobile" in victim.tags.all():
                        chance = 2 * victim.level
                        if chance > 55:
                            chance = 55

                    if random.randint(1, 100) <= (chance + victim.level - attacker.level) and chance > 0:
                        hit = False
                        dodge = True
                        if "player" in victim.tags.all():
                            rules_skills.check_skill_improve(victim, "dodge", True, 5)
            
                    if "player" in victim.tags.all() and dodge == False:
                        if "parry" in victim.db.skills:
                            if not victim.db.eq_slots["wielded, primary"]:
                                if not victim.db.eq_slots["wielded, secondary"]:
                                    chance = 0
                                else:
                                    chance = victim.db.skills["parry"] / 4
                            else:
                                chance = victim.db.skills["parry"] / 2

                    elif "mobile" in victim.tags.all() and dodge == False:
                        chance = 2 * victim.level
                        if chance > 57:
                            chance = 57
                        if not victim.db.eq_slots["wielded, primary"]:
                            if not victim.db.eq_slots["wielded, secondary"]:
                                chance /= 2
                            else:
                                chance = chance * 3 / 4

                    if random.randint(1, 100) <= (chance + victim.level - attacker.level) and dodge == False and chance > 0:
                        hit = False
                        parry = True
                        if "player" in victim.tags.all():
                            rules_skills.check_skill_improve(victim, "parry", True, 5)
        except Exception:
            logger.log_file("Error in doing parry and dodge tests. Attacker = %s, victim = %s." % (attacker.key, victim.key), filename="combat.log")
            logger.log_trace("Error in doing parry and dodge tests.")

    # Get the damage type next.
    if "type" in kwargs:
        damage_type = kwargs["type"]
    else:
        damage_type = get_damagetype(attacker)

    experience_modified = 0

    # If there is still a hit after the previous checks, continue
    # processing the hit.
    if hit:

        # Step one on a hit, determine damage.
        # Special attack provides damage with it.
        if "damage" in kwargs:
            damage = kwargs["damage"]
        # Base combat round attacks.
        else:
            damage = do_damage(attacker, victim, eq_slot)

        # Step two, translate that damage into experience

        # Step 2(a) is to determine experience from a hit as a factor of
        # the total experience the mobile has to give.

        try:
            # Make sure we aren't giving out experience for more damage than
            # the mobile has hitpoints remaining.
            if damage > victim.hitpoints_current:
                experience_damage = victim.hitpoints_current
            else:
                experience_damage = damage

            # Experience awarded for a hit is dependent on damage done as a
            # percent of total hitpoints.
            percent_damage = experience_damage / victim.hitpoints_maximum

            if percent_damage > 1:
                percent_damage = 1

            # Don't give out all the experience through single hits, to
            # preserve some to be awarded on kill. Amount awarded decreases
            # round by round. Because of this, ALWAYS BE SURE combat is
            # started before calling do_attack on a special attack!!!

            round = combat.db.rounds
            round_fraction = (1 / (1 + round / 10))

            experience_raw = int(round_fraction *
                                 percent_damage *
                                 victim.db.experience_total
                                 )

            # Reduce the mobile's current experience based on the
            # amount calculated.
            victim.db.experience_current -= experience_raw

            # Step 2(b) is to modify the base experience granted by the
            # mobile by the alignment and race of the attacker with
            # regard to the alignment and race of the mobile.

            experience_modified = int(modify_experience(attacker,
                                                        victim,
                                                        experience_raw
                                                        ))

            attacker.db.experience_total += experience_modified
            
        except Exception:
            logger.log_file("Error in doing experience award in do_attack. Attacker = %s, victim = %s" % (attacker.key, victim.key), filename="combat.log")
            logger.log_trace("Error in doing experience award in do_attack.")
            
        # Do damage to the victim.
        try:
            victim.take_damage(damage)
        except Exception:
            logger.log_file("Error in damaging victim in do_attack, victim = %s" % victim.key, filename="combat.log")
            logger.log_trace("Error in damaging victim in do_attack.")

        # Get the victim started healing, if not already.
        try:
            if not victim.attributes.has("heal_ticker"):
                timestamp = victim.key + str(time.time())
                tickerhandler.add(30, victim.at_update, timestamp)
                victim.db.heal_ticker = timestamp
            elif not victim.db.heal_ticker:
                timestamp = victim.key + str(time.time())
                tickerhandler.add(30, victim.at_update, timestamp)
                victim.db.heal_ticker = timestamp
        except Exception:
            logger.log_file("Error in checking if healing needed in do_attack, victim = %s" % victim.key, filename="combat.log")
            logger.log_trace("Error in checking if healing needed in do_attack.")
            
        # Step three - give output.
        try:
            # Special output from special attacks.
            if "output" in kwargs:
                attacker.msg("%s" % kwargs["output"][0])
                victim.msg("%s" % kwargs["output"][1])
                combat.location.msg_contents("%s" % kwargs["output"][2], exclude=(attacker, victim))

            else:
                attacker.msg("You |g%s|n %s with your %s.\n"
                                   % (get_damagestring("attacker", damage),
                                      victim.key,
                                      damage_type
                                      )
                                   )
                victim.msg("%s |r%s|n you with its %s.\n"
                                 % (attacker.key,
                                    get_damagestring("victim", damage),
                                    damage_type
                                    )
                                 )
                combat.location.msg_contents("%s %s %s with its %s.\n"
                               % (attacker.key,
                                  get_damagestring("victim", damage),
                                  victim.key,
                                  damage_type
                                  )
                               )
        except Exception:
            logger.log_file("Error in giving hit output in do_attack. Attacker = %s, victim = %s." % (attacker.key, victim.key), filename="combat.log")
            logger.log_trace("Error in giving hit output in do_attack.")
        
        try:
            if "hit" in kwargs:
                if "player" in attacker.tags.all():
                    if damage > attacker.db.damage_maximum:
                        attacker.db.damage_maximum = damage
                        attacker.db.damage_maximum_mobile = victim.key
                        attacker.msg(
                            "Your %s for %d damage is your record for damage in one hit!!!\n" % (damage_type, damage))
            else:
                if "player" in attacker.tags.all():
                    if damage > attacker.db.damage_maximum:
                        attacker.db.damage_maximum = damage
                        attacker.db.damage_maximum_mobile = victim.key
                        attacker.msg("Your %s for %d damage is your record for damage in one hit!!!\n"
                                            % (damage_type, damage))
        except Exception:
            logger.log_file("Error in checking for single-hit record in do_attack. Attacker = %s" % attacker.key, filename="combat.log")
            logger.log_trace("Error in checking for single-hit record in do_attack.")            

        # Check at the end of processing hit to see if the victim is dead.
        if victim.hitpoints_current <= 0:
            # If dead as a result of a special attack.
            if "hit" in kwargs:
                do_death(attacker, victim, combat, special=True, type=damage_type)
            else:
                do_death(attacker, victim, combat)

    else:
        if "output" in kwargs:
            attacker.msg("%s" % kwargs["output"][0])
            victim.msg("%s" % kwargs["output"][1])
            combat.location.msg_contents("%s" % kwargs["output"][2], exclude=(attacker, victim))
        elif parry == True:
            attacker.msg("%s parries your %s.\n" % ((victim.key[0].upper() + victim.key[1:]),
                                                          damage_type
                                                          ))
            victim.msg("You parry %s's %s.\n" % (attacker.key,
                                                       damage_type
                                                       ))
            combat.location.msg_contents("%s parries %s's %s.\n" % ((victim.key[0].upper() + victim.key[1:]),
                                                      attacker.key,
                                                      damage_type
                                                      ))
        elif dodge == True:
            attacker.msg("%s dodges your %s.\n" % ((victim.key[0].upper() + victim.key[1:]),
                                                         damage_type
                                                         ))
            victim.msg("You dodge %s's %s.\n" % (attacker.key,
                                                       damage_type
                                                       ))
            combat.location.msg_contents("%s dodges %s's %s.\n" % ((victim.key[0].upper() + victim.key[1:]),
                                                     attacker.key,
                                                     damage_type
                                                     ))
        else:
            attacker.msg("You miss %s with your %s.\n" % (victim.key,
                                                                damage_type
                                                                ))
            victim.msg("%s misses you with %s %s.\n" % (attacker.key,
                                                              rules.pronoun_possessive(attacker),
                                                              damage_type
                                                              ))
            combat.location.msg_contents("%s misses %s with %s %s.\n" % (attacker.key,
                                                           victim.key,
                                                           rules.pronoun_possessive(attacker),
                                                           damage_type
                                                           ))


def do_damage(attacker, victim, eq_slot):
    """
    This is called on a successful standard attack hit, and returns the total
    damage for that hit.
    """

    if "mobile" in attacker.tags.all():
        try:
            damage_low = math.ceil(attacker.db.level * 3 / 4)
            damage_high = math.ceil(attacker.db.level * 3 / 2)

            # Damage is a random number between high damage and low damage.
            damage = random.randint(damage_low, damage_high)

            # If mobile is wielding a weapon, they get a 50% bonus.
            if attacker.db.eq_slots["wielded, primary"]:
                damage = int(damage * 1.5)

            # Get a bonus to damage from damroll.
            dam_bonus = int(attacker.damroll)

            damage += dam_bonus
        except Exception:
            logger.log_file("Error in calculating base mobile damage in do_damage. Attacker = %s" % attacker.key, filename="combat.log")
            logger.log_trace("Error in checking for single-hit record in do_attack.")         
    else:
        if attacker.db.eq_slots[eq_slot]:
            try:
                weapon = attacker.db.eq_slots[eq_slot]
                damage = random.randint(weapon.db.damage_low,
                                        weapon.db.damage_high
                                        )

                dam_bonus = int(attacker.damroll)

                # You only get the damroll bonus for the weapon you are using
                # on the attack. As a result, we subtract out the damroll
                # from the weapon not being used in the attack, if there is
                # more than one.

                if eq_slot == "wielded, primary":
                    if attacker.db.eq_slots["wielded, secondary"]:
                        eq = attacker.db.eq_slots["wielded, secondary"]
                        dam_bonus -= eq.db.stat_modifiers["damroll"]
                else:
                    eq = attacker.db.eq_slots["wielded, secondary"]
                    dam_bonus -= eq.db.stat_modifiers["damroll"]

                damage += dam_bonus
            except Exception:
                logger.log_file("Error in calculating armed player damgae in do_damage. Attacker = %s" % attacker.key, filename="combat.log")
                logger.log_trace("Error in calculating armed player damage in do_damage.")         
        else:
            try:
                damage = random.randint(1, 2) * attacker.size

                # Get a bonus to damage from damroll. Since we got here, there is
                # no weapon to worry about.
                dam_bonus = attacker.damroll

                damage += dam_bonus
            except Exception:
                logger.log_file("Error in calculating unarmed player damage in do_damage. Attacker = %s" % attacker.key, filename="combat.log")
                logger.log_trace("Error in calculating unarmed player damage in do_damage.")         
                
    # Check if player has enhanced damage.
    try:
        if "player" in attacker.tags.all():
            if "enhanced damage" in attacker.db.skills:
                damage += int(damage * attacker.db.skills["enhanced damage"] / 150)
                rules_skills.check_skill_improve(attacker, "enhanced damage", True, 5)
    except Exception:
        logger.log_file("Error in calculating enhanced damage for a player in do_damage. Attacker = %s" % attacker.key, filename="combat.log")
        logger.log_trace("Error in calculating enhanced damage for a player in do_damage.")         
        
    if victim.db.position == "sleeping":
        damage *= 2

    if victim.get_affect_status("sanctuary"):
        damage /= 2

    if victim.get_affect_status("protection"):
        damage -= damage / 4

    return math.ceil(damage)


def do_death(attacker, victim, combat, **kwargs):
    """
    This handles death and returns some output.
    """

    # Get damage type for use in output.
    if "type" in kwargs:
        damage_type = kwargs["type"]
    else:
        damage_type = get_damagetype(attacker)

    # Give death output.
    try:
        attacker.msg("With your final %s, %s falls to the ground, DEAD!!!\n"
                     % (damage_type, victim.key))
        victim.msg("You have been |rKILLED|n!!!\n You awaken again at your "
                   "home location.\n")
        attacker.location.msg_contents("%s has been KILLED by %s!!!\n"
                                       % ((victim.key[0].upper() + victim.key[1:0]), attacker.key),
                                       exclude=(attacker, victim))
    except Exception:
        logger.log_file("Error in giving output of death in do_death. Attacker = %s, victim = %s." % (attacker.key, victim.key), filename="combat.log")
        logger.log_trace("Error in giving output of death in do_death.")
        
    if "mobile" in victim.tags.all():

        # Step 1 of mobile death - handle the corpse.
        # 1(a) Check none to see if there is a handy corpse, already made.

        try:
            object_candidates = search.search_tag("npc corpse")

            corpse = False

            for object in object_candidates:
                if not object.location:
                    corpse = object
                    corpse.key = "the corpse of %s" % victim.key
                    break
        except Exception:
            logger.log_file("Error in finding mobile corpse in do_death. Victim = %s." % victim.key, filename="combat.log")
            logger.log_trace("Error in finding mobile corpse in do_death.")        
        # 1(b) If no ready corpse, make one.
        try:
            if not corpse:
                # Create corpse.
                corpse = create_object("objects.NPC_Corpse", key=("the corpse of %s"
                                                                  % victim.key))

            corpse.db.desc = ("The corpse of %s lies here." % victim.key)
            corpse.location = attacker.location
        except Exception:
            logger.log_file("Error in creating mobile corpse in do_death. Victim = %s" % victim.key, filename="combat.log")
            logger.log_trace("Error in creating mobile corpse in do_death.")
            
        # 1(c) Set the corpse to disintegrate.
        try:
            rules.set_disintegrate_timer(corpse)
        except Exception:
            logger.log_file("Error in setting mobile corpse disintegrate in do_death.", filename="combat.log")
            logger.log_trace("Error in setting mobile corpse disintegrate in do_death.")
            
        # 1(d) Move all victim items to corpse, if any.
        try:
            for item in victim.contents:
                if item.db.equipped:
                    item.remove_from(victim)
                item.move_to(corpse, quiet=True)
        except Exception:
            logger.log_file("Error in moving items to mobile corpse. Victim = %s." % victim.key, filename="combat.log")
            logger.log_trace("Error in moving items to mobile corpse.")
        
        # Step 2 - Clean up the mobile.
        try: 
            # Clear spell affects and return calls.
            if victim.db.spell_affects:
                for affect_name in victim.db.spell_affects:
                    rules.affect_remove(victim, affect_name, "", "")

            # Clear wait state.
            if victim.ndb.wait_state:
                rules.wait_state_remove(victim)

            # Reset damage.
            victim.db.hitpoints["damaged"] = 0

            # Return victim to standing.
            victim.db.position = "standing"

            # Move victim to None location to be reset later.
            victim.location = None

        except Exception:
            logger.log_file("Error in cleaning up mobile in do_death. Victim = %s." % victim.key, filename="combat.log")
            logger.log_trace("Error in cleaning up mobile in do_death.")
            
        # Step 3 Add victim to reset list.
        try:
            
            reset_script = search.script_search("reset_script")[0]
            area = rules.get_area_name(victim)

            reset_script.db.area_list[area]["resets"].append(victim)
            
        except Exception:
            logger.log_file("Error in adding dead mobile to reset list in do_death. Victim = %s." % victim.key, filename="combat.log")
            logger.log_trace("Error in adding dead mobile to reset list in do_death.")

        # Step 4 Handle death experience.
        
        try:
            # 4(a) Award death experience.
            if "player" in attacker.tags.all():
                experience_modified = \
                    modify_experience(attacker,
                                      victim,
                                      victim.db.experience_current
                                      )
                attacker.db.experience_total += experience_modified

                attacker.msg("You receive %s experience as a result of "
                                 "your kill!\n" % experience_modified)

        except Exception:
            logger.log_file("Error in awarding death experience in do_death. Attacker = %s." % attacker.key, filename="combat.log")
            logger.log_trace("Error in awarding death experience in do_death.")
                
        # 4(b) Check if experience was more than previous best kill.
        try:
            total_modified_experience = modify_experience(attacker, victim, victim.db.experience_total)

            if total_modified_experience > attacker.db.kill_experience_maximum:
                attacker.db.kill_experience_maximum = total_modified_experience
                attacker.db.kill_experience_maximum_mobile = victim.key

                attacker.msg("That kill is your new record for most "
                                 "experience obtained for a kill!\n"
                                 "You received a total of %d experience "
                                 "from %s.\n" % (victim.db.experience_total, victim.key))
        except Exception:
            logger.log_file("Error in checking if experience exceeded best kill on mobile death. Attacker = %s." % attacker.key, filename="combat.log")
            logger.log_trace("Error in checking if experience exceeded best kill on mobile death.")
            
        # Step 5 Give the attacker a look at the corpse after it dies
        try:
            corpse_look = attacker.at_look(corpse)
            attacker.msg("%s\n" % corpse_look)
        except Exception:
            logger.log_file("Error in giving look at mobile corpse. Attacker = %s, corpse = %s." % (attacker.key, corpse.key), filename="combat.log")
            logger.log_trace("Error in giving look at mobile corpse.")
            
        # Step 6 Increment player kills.
        attacker.db.kills += 1

        # Step 7 Update player alignment.
        try:
            if "player" in attacker.tags.all():
                if victim.db.alignment > 0:
                    directional_modifier = 1
                else:
                    directional_modifier = -1

                attacker.db.alignment = math.ceil(attacker.db.alignment -
                                                  victim.db.alignment *
                                                  (1000 +
                                                   directional_modifier *
                                                   attacker.db.alignment
                                                   ) *
                                                  (1000 +
                                                   abs(attacker.db.alignment)
                                                   ) / 50000000
                                                  )
        except Exception:
            logger.log_file("Error in updating player alignment in do_death. Attacker = %s." % attacker.key, filename="combat.log")
            logger.log_trace("Error in updating player alignment in do_death.")

        # Figure out how to calculate gold on mobile and award.

        # attacker_string += ("You receive |y%s gold|n as a result of your
        # kill!" % victim.)

        # Call the at_death hook for the mobile.
        victim.at_death(attacker)

    # Handle player death.
    else:

        # Step 1 Make a corpse.
        corpse = False

        # 1(a) Check at none to see if there is an existing corpse.
        try:
            object_candidates = search.search_tag("pc corpse")

            for object in object_candidates:
                if not object.location:
                    corpse = object
                    corpse.key = "the corpse of %s" % victim.key
                    break
                    
        except Exception:
            logger.log_file("Error in finding player corpse in do_death.", filename="combat.log")
            logger.log_trace("Error in finding player corpse in do_death.")
                    
        # 1(b) If not a ready corpse, make one.
        try:
            if not corpse:
                # Create corpse.
                corpse = create_object("objects.PC_Corpse", key=("the corpse of %s"
                                                                 % victim.key))
        except Exception:
            logger.log_file("Error in creating player corpse in do_death.", filename="combat.log")
            logger.log_trace("Error in creating player corpse in do_death.")

        corpse.db.desc = ("The corpse of %s lies here." % victim.key)
        corpse.location = attacker.location
        
        try:
            rules.set_disintegrate_timer(corpse)
        except Exception:
            logger.log_file("Error setting disintegrate timer for player corpse in do_death.", filename="combat.log")
            logger.log_trace("Error setting disintegrage timer for player corpse in do_death.")

        # Step 2 Increment hero deaths.
        victim.db.died += 1

        # Heroes keep their items.

        # Step 3 Cleanup the hero.
        try:
            # 3(a) Clear wait state.
            if victim.ndb.wait_state:
                rules.wait_state_remove(victim)

            # 3(b) Clear spell affects and return calls.
            if victim.db.spell_affects:
                for affect_name in victim.db.spell_affects:
                    rules.affect_remove(victim, affect_name, "", "")

        except Exception:
            logger.log_file("Error in cleaning up player in do_death. Player = %s." % victim.key, filename="combat.log")
            logger.log_trace("Error in cleaning up player in do_death.")

        # Step 4 Do xp penalty, if above level 5.
        try:
            if victim.level > 5:
                experience_loss = int(settings.EXPERIENCE_LOSS_DEATH * rules.experience_loss_base(victim))
                victim.db.experience_total -= experience_loss

                victim.msg("You lose %s experience as a result of your death!" % experience_loss)

        except Exception:
            logger.log_file("Error doing xp penalty in do_death. Player = %s." % victim.key, filename="combat.log")
            logger.log_trace("Error in finding player corpse in do_death.")

            # Do gold penalty, after figuring out how much it should be.

        # Step 5 Reset dead players to one hitpoint, and move to home.
        try:
            victim.hitpoints_damaged = victim.hitpoints_maximum - 1
            victim.move_to(victim.home, quiet=True)

            victim.location.msg_contents("A beaten and bedraggled %s rises from the dead."
                                           % victim.key,
                                           exclude=victim)
        except Exception:
            logger.log_file("Error in resetting player to one hp and moving home. Player = %s." % victim.key, filename="combat.log")
            logger.log_trace("Error in resetting player ot one hp and moving home.")


    # Remove dead combatants from combat.
    combat.remove_combatant(victim)

    # Add someone else attacking the attacker as its new
    # target, if any.
    try:
        new_target = combat.find_other_attackers(attacker)
        if new_target:
            attacker.msg("Having dispatched %s, you turn to attack %s!\n" % (victim.key, new_target.key))
    except Exception:
        logger.log_file("Error in finding new target for player in combat after death. Player = %s." % attacker.key, filename="combat.log")
        logger.log_trace("Error in finding new target for player in combat after death.")

    # Check for combat end.
    combat.combat_end_check()


def do_flee(character):
    
    if character.db.position == "sitting":
        character.msg("You had better stand up to try to flee!")
        return

    success = False
    for attempt in range(1, 6):
        direction = random.randint(1, 6)

        if direction == 1:
            direction = "north"
        elif direction == 2:
            direction = "east"
        elif direction == 3:
            direction = "south"
        elif direction == 4:
            direction = "west"
        elif direction == 5:
            direction = "up"
        else:
            direction = "down"

        for exit in character.location.contents:
            if exit.destination and exit.key == direction and exit.access(character, "traverse"):
                success = True
                break

        if success:
            if "mobile" in character.tags.all():
                if random.randint(1, 2) == 2:
                    success = False
            break

    if success:
        # Remove character from combat, and check if combat ends.
        combat = character.ndb.combat_handler
        combat.combatant_remove(character)
        combat.combat_end_check()
        
        # Check to see if this ends combat.

        # Only do experience loss if the character is past level 5.
        if character.level > 5:
            experience_loss = int(settings.EXPERIENCE_LOSS_FLEE * rules.experience_loss_base(character))
        
            character.db.experience_total -= experience_loss

            character.msg("You show a good pair of heels and flee %s out of combat!\nYou lose %d experience for fleeing." % (direction, experience_loss))
            character.location.msg_contents("%s tucks tail and flees %s out of combat!"
                                         % ((character.name[0].upper() + character.name[1:]), direction),
                                         exclude=character)
        else:
            character.msg(
                "You show a good pair of heels and flee %s out of combat!" % direction)
            character.location.msg_contents("%s tucks tail and flees %s out of combat!"
                                            % ((character.name[0].upper() + character.name[1:]), direction),
                                            exclude=character)

        character.move_to(exit.destination, quiet=True)
        
    else:
        # Only do experience loss if the character is past level 5.
        if character.level > 5:
            experience_loss = int(settings.EXPERIENCE_LOSS_FLEE_FAIL * rules.experience_loss_base(character))
            character.db.experience_total -= experience_loss
        
            character.msg("You fail to flee from combat!\nYou lose %d experience for the attempt." % experience_loss)
            character.location.msg_contents("%s looks around frantically for an escape, but can't get away!"
                                         % (character.name[0].upper() + character.name[1:]),
                                         exclude=character)
        else:
            character.msg("You fail to flee from combat!")
            character.location.msg_contents("%s looks around frantically for an escape, but can't get away!"
                                            % (character.name[0].upper() + character.name[1:]),
                                            exclude=character)

def do_one_character_combat_turn(attacker, victim, combat):
    """
    This handles the top level of everything that needs to
    happen in one round of combat for a character.
    """
    
    # First, check to see if the attacker is below their wimpy.
    try:
        if attacker.hitpoints_current > 0 and (("player" in attacker.tags.all() and
            attacker.hitpoints_current <= attacker.db.wimpy) or \
                ("mobile" in attacker.tags.all() and
                 "wimpy" in attacker.db.act_flags and
                 attacker.hitpoints_current <= (0.15 * attacker.hitpoints_maximum
                 ))):

            # If so, make a free attempt to flee.
            do_flee(attacker)
    except Exception:
        logger.log_file("Error in wimpy check and flee attempt in do_one_character_combat_turn. Attacker = %s" % attacker.key, filename="combat.log")
        logger.log_trace("Error in wimpy check and flee attempt in do_one_character_combat_turn.")                 

    # Check to see if the target has been tripped, and, if so, try to stand.
    try:
        if attacker.position == "sitting":

            if "mobile" in attacker.tags.all():
                chance = 50
            else:
                chance = 2 * attacker.dexterity

            chance -= 2 * attacker.size

            if random.randint(1, 100) <= chance:
                attacker.msg("You jump back to your feet.")
                attacker.location.msg_contents("%s jumps back to %s feet." % ((attacker.key[0].upper() + attacker.key[1:]),
                                                                               rules.pronoun_possessive(attacker)
                                                                               ), exclude=(attacker))
            elif random.randint(1, 100) < 30:
                attacker.msg("You struggle to stand up ... and fail.")
                attacker.location.msg_contents("%s tries to stand up, and fails." % (attacker.key[0].upper() + attacker.key[1:]), exclude=(attacker))
    except Exception:
        logger.log_file("Error in trip check and stand attempt in do_one_character_combat_turn. Attacker = %s" % attacker.key, filename="combat.log")
        logger.log_trace("Error in trip check and stand attempt in do_one_character_combat_turn.")                 
        
    # Check on hide and invisible status and remove if attacking.
    if attacker.get_affect_status("hide"):
        pass
    
    # Check on invisibility and hide.
    try:
        rules.check_return_visible(attacker)
    except Exception:
        logger.log_file("Error checking whether to return visible in do_one_character_combat_turn. Attacker = %s" % attacker.key, filename="combat.log")
        logger.log_trace("Error checking whether to return visible in do_one_character_combat_turn.")                 

    # Now, on to actual attacks.

    # Do base attacks.
    do_one_weapon_attacks(attacker, victim, "wielded, primary", combat)
    
    # Check for dual wield, and do attacks if needed.
    try:
        if attacker.db.eq_slots["wielded, primary"] and \
                attacker.db.eq_slots["wielded, secondary"]:
            do_one_weapon_attacks(attacker, victim, "wielded, secondary", combat)
            
    except Exception:
        logger.log_file("Error checking for dual wield in do_one_character_combat_turn. Attacker = %s" % attacker.key, filename="combat.log")
        logger.log_trace("Error checking for dual wield in do_one_character_combat_turn.")                 

def do_one_weapon_attacks(attacker, victim, eq_slot, combat):
    """
    This handles all of the default attacks for one weapon position
    for one attacker for one round of combat.
    """

    # If primary weapon, first hit is free.
    try:
        if eq_slot == "wielded, primary":
            do_attack(attacker, victim, eq_slot, combat)
        else:
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    do_attack(attacker, victim, eq_slot, combat)
            else:
                # Save hero for dual skill implementation.
                pass
    except Exception:
        logger.log_file("Error in checking first attack in do_one_weapon_attacks. Attacker = %s, victim = %s, eq_slot = %s." % (attacker.key, victim.key, eq_slot), filename="combat.log")
        logger.log_trace("Error in checking first attack in do_one_weapon_attacks.")                 

    # Check for second attack.
    try:
        if eq_slot == "wielded, primary":
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    do_attack(attacker, victim, eq_slot, combat)
            else:
                # Wait to build out hero until skills built
                pass
        else:
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    do_attack(attacker, victim, eq_slot, combat)
            else:
                # Wait to build out hero until skills built
                pass
    except Exception:
        logger.log_file("Error in checking second attack in do_one_weapon_attacks. Attacker = %s, victim = %s, eq_slot = %s." % (attacker.key, victim.key, eq_slot), filename="combat.log")
        logger.log_trace("Error in checking second attack in do_one_weapon_attacks.")                 

    # Check for third attack.
    try:
        if eq_slot == "wielded, primary":
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    do_attack(attacker, victim, eq_slot, combat)
            else:
                # Wait to build out hero until skills built
                pass
        else:
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    do_attack(attacker, victim, eq_slot, combat)
            else:
                # Wait to build out hero until skills built
                pass
    except Exception:
        logger.log_file("Error in checking third attack in do_one_weapon_attacks. Attacker = %s, victim = %s, eq_slot = %s." % (attacker.key, victim.key, eq_slot), filename="combat.log")
        logger.log_trace("Error in checking third attack in do_one_weapon_attacks.")                 

    # Check for fourth attack, for mobiles only.
    try:
        if "mobile" in attacker.tags.all():
            if random.randint(1, 100) < (attacker.db.level / 2):
                do_attack(attacker, victim, eq_slot, combat)
    except Exception:
        logger.log_file("Error in checking fourth attack in do_one_weapon_attacks. Attacker = %s, victim = %s, eq_slot = %s." % (attacker.key, victim.key, eq_slot), filename="combat.log")
        logger.log_trace("Error in checking fourth attack in do_one_weapon_attacks.")                 


def get_avoidskill(victim):
    if victim.get_affect_status("blindness"):
        blind_penalty = 60
    else:
        blind_penalty = 0

    ws = get_warskill(victim)
    ac = victim.armor_class
    dex = victim.dexterity

    avoidskill = get_warskill(victim) + (100 - victim.armor_class / 3) - \
        blind_penalty + 10 * (victim.dexterity - 10)
    if avoidskill > 1:
        return avoidskill
    else:
        return 1


def get_damagestring(combatant, damage):
    if combatant == "attacker":
        if damage < 1:
            damagestring = "miss"
        elif damage < 4:
            damagestring = "scratch"
        elif damage < 7:
            damagestring = "graze"
        elif damage < 10:
            damagestring = "bruise"
        elif damage < 13:
            damagestring = "injure"
        elif damage < 16:
            damagestring = "wound"
        elif damage < 22:
            damagestring = "clobber"
        elif damage < 28:
            damagestring = "maul"
        elif damage < 34:
            damagestring = "devastate"
        elif damage < 43:
            damagestring = "MUTILATE"
        elif damage < 52:
            damagestring = "MASSACRE"
        elif damage < 61:
            damagestring = "DISEMBOWEL"
        elif damage < 70:
            damagestring = "EVISCERATE"
        elif damage < 82:
            damagestring = "do EXTRAORDINARY damage to"
        elif damage < 94:
            damagestring = "***OBLITERATE***"
        elif damage < 118:
            damagestring = "***DEMOLISH***"
        elif damage < 142:
            damagestring = "***SLAUGHTER***"
        elif damage < 166:
            damagestring = "do TERRIFIC damage to"
        elif damage < 201:
            damagestring = "***PULVERIZE***"
        elif damage < 236:
            damagestring = "***>PULVERIZE<***"
        elif damage < 271:
            damagestring = "do HORRIFIC damage to"
        elif damage < 323:
            damagestring = "do unspeakable things to"
        elif damage < 375:
            damagestring = "do UNSPEAKABLE things to"
        elif damage < 427:
            damagestring = "do incredible damage to"
        elif damage < 503:
            damagestring = "do INCREDIBLE damage to"
        elif damage < 579:
            damagestring = "do unbelievable damage to"
        elif damage < 664:
            damagestring = "do UNBELIEVABLE damage to"
        elif damage < 749:
            damagestring = "do inconceivable damage to"
        elif damage < 846:
            damagestring = "do INCONCEIVABLE damage to"
        elif damage < 1000:
            damagestring = "do colossal damage to"
        elif damage < 1220:
            damagestring = "do COLOSSAL damage to"
        elif damage < 2105:
            damagestring = "do GHASTLY damage to"
        elif damage < 3007:
            damagestring = "do HORRENDOUS damage to"
        elif damage < 3846:
            damagestring = "do PHENOMENAL damage to"
        elif damage < 7981:
            damagestring = "do MIND-NUMBING damage to"
        elif damage < 16404:
            damagestring = "do OBSCENE damage to"
        elif damage < 32097:
            damagestring = "do EARTH-SHATTERING damage to"
        else:
            damagestring = "**>*>*>*VAPORIZE*<*<*<**"
    if combatant == "victim":
        if damage < 1:
            damagestring = "misses"
        elif damage < 4:
            damagestring = "scratches"
        elif damage < 7:
            damagestring = "grazes"
        elif damage < 10:
            damagestring = "bruises"
        elif damage < 13:
            damagestring = "injures"
        elif damage < 16:
            damagestring = "wounds"
        elif damage < 22:
            damagestring = "clobbers"
        elif damage < 28:
            damagestring = "mauls"
        elif damage < 34:
            damagestring = "devastates"
        elif damage < 43:
            damagestring = "MUTILATES"
        elif damage < 52:
            damagestring = "MASSACRES"
        elif damage < 61:
            damagestring = "DISEMBOWELS"
        elif damage < 70:
            damagestring = "EVISCERATES"
        elif damage < 82:
            damagestring = "does EXTRAORDINARY damage to"
        elif damage < 94:
            damagestring = "***OBLITERATES***"
        elif damage < 118:
            damagestring = "***DEMOLISHES***"
        elif damage < 142:
            damagestring = "***SLAUGHTERS***"
        elif damage < 166:
            damagestring = "does TERRIFIC damage to"
        elif damage < 201:
            damagestring = "***PULVERIZES***"
        elif damage < 236:
            damagestring = "***>PULVERIZES<***"
        elif damage < 271:
            damagestring = "does HORRIFIC damage to"
        elif damage < 323:
            damagestring = "does unspeakable things to"
        elif damage < 375:
            damagestring = "does UNSPEAKABLE things to"
        elif damage < 427:
            damagestring = "does incredible damage to"
        elif damage < 503:
            damagestring = "does INCREDIBLE damage to"
        elif damage < 579:
            damagestring = "does unbelievable damage to"
        elif damage < 664:
            damagestring = "does UNBELIEVABLE damage to"
        elif damage < 749:
            damagestring = "does inconceivable damage to"
        elif damage < 846:
            damagestring = "does INCONCEIVABLE damage to"
        elif damage < 1000:
            damagestring = "does colossal damage to"
        elif damage < 1220:
            damagestring = "does COLOSSAL damage to"
        elif damage < 2105:
            damagestring = "does GHASTLY damage to"
        elif damage < 3007:
            damagestring = "does HORRENDOUS damage to"
        elif damage < 3846:
            damagestring = "does PHENOMENAL damage to"
        elif damage < 7981:
            damagestring = "does MIND-NUMBING damage to"
        elif damage < 16404:
            damagestring = "does OBSCENE damage to"
        elif damage < 32097:
            damagestring = "does EARTH-SHATTERING damage to"
        else:
            damagestring = "**>*>*>*VAPORIZES*<*<*<**"

    return damagestring


def get_damagetype(attacker):
    try:
        if attacker.db.eq_slots["wielded, primary"]:
            weapon = attacker.db.eq_slots["wielded, primary"]
            damagetype = weapon.db.weapon_type
        else:
            if "damage message" in rules_race.get_race(attacker.race):
                damagetype = rules_race.get_race(attacker.race)["damage message"]
            else:
                damagetype = "punch"

        return damagetype
    except Exception:
        logger.log_file("Error in get_damage_type. Attacker = %s." % attacker.key, filename="combat.log")
        logger.log_trace("Error in get_damage_type.")                 


def get_health_string(combatant):
    combatant.msg("here")

    health_percent = int(100 *
                         combatant.hitpoints_current /
                         combatant.hitpoints_maximum
                         )
    if health_percent == 100:
        return "is in |gperfect health|n."
    elif health_percent > 90:
        return "is |gslightly scratched|n."
    elif health_percent > 80:
        return "has |ga few bruises|n."
    elif health_percent > 70:
        return "has |gsome cuts|n."
    elif health_percent > 60:
        return "has |yseveral wounds|n."
    elif health_percent > 50:
        return "has |ymany nasty wounds|n."
    elif health_percent > 40:
        return "is |ybleeding freely|n."
    elif health_percent > 30:
        return "is |ycovered in blood|n."
    elif health_percent > 20:
        return "is |rleaking guts|n."
    elif health_percent > 10:
        return "is |ralmost dead|n."
    elif health_percent > 0:
        return "is |rDYING|n."
    elif health_percent <= 0:
        return "is |rDEAD!!!|n"


def get_hit_chance(attacker, victim):

    try:
        hit_chance = int(100 * (get_hitskill(attacker, victim) +
                                attacker.db.level -
                                victim.db.level) /
                         (get_hitskill(attacker, victim) + get_avoidskill(victim))
                         )

        if hit_chance > 95:
            return 95
        elif hit_chance < 5:
            return 5
        else:
            return hit_chance
    except Exception:
        logger.log_file("Error in get_hit_chance. Attacker = %s, victim = %s." % (attacker.key, victim.key), filename="combat.log")
        logger.log_trace("Error in get_hit_chance.")                 


def get_hitskill(attacker, victim):
    # Make sure that hitroll does not include hitroll from weapon if can't
    # wield it.
    try:
        hitskill = get_warskill(attacker) + attacker.hitroll + \
            get_race_hitbonus(attacker, victim) + 10*(attacker.dexterity - 10)
        if hitskill > 1:
            return hitskill
        else:
            return 1
    except Exception:
        logger.log_file("Error in get_hitskill. Attacker = %s, victim = %s." % (attacker.key, victim.key), filename="combat.log")
        logger.log_trace("Error in get_hitskill.")                 


def get_race_hitbonus(attacker, victim):
    """
    Determines a hit bonus based on comparative race sizes of
    combatants.
    """

    try:
        hitbonus = victim.size - attacker.size
        return hitbonus
    except Exception:
        logger.log_file("Error in get_race_hitbonus. Attacker = %s, victim = %s." % (attacker.key, victim.key), filename="combat.log")
        logger.log_trace("Error in get_race_hitbonus.")                 


def get_warskill(combatant):
    """
    This function returns the innate basic fighting skill
    for the combatant. For players, this is based on what
    colleges they are specializing in.
    """

    try:
        if "mobile" in combatant.tags.all():
            warskill_factor = combatant.db.level / 101
            warskill = int(120 * warskill_factor)
            return warskill
        else:
            colleges = rules.classes_current(combatant)
            max_warskill = 0

            for college in colleges:
                if college == "default" and len(colleges) == 1:
                    max_warskill = 120
                elif college == "mage":
                    if max_warskill < 65:
                        max_warskill = 65
                elif college == "cleric":
                    if max_warskill < 85:
                        max_warskill = 85
                elif college == "thief":
                    if max_warskill < 120:
                        max_warskill = 120
                elif college == "warrior":
                    if max_warskill < 180:
                        max_warskill = 180
                elif college == "psionicist":
                    if max_warskill < 50:
                        max_warskill = 50
                elif college == "druid":
                    if max_warskill < 100:
                        max_warskill = 100
                elif college == "ranger":
                    if max_warskill < 140:
                        max_warskill = 140
                elif college == "paladin":
                    if max_warskill < 160:
                        max_warskill = 160
                elif college == "bard":
                    if max_warskill < 100:
                        max_warskill = 100

            warskill_factor = combatant.db.level / 101
            warskill = int(max_warskill * warskill_factor)
            return warskill
    except Exception:
        logger.log_file("Error in get_warskill. Attacker = %s." % combatant.key, filename="combat.log")
        logger.log_trace("Error in get_warskill.")                 


def hit_check(attacker, victim):
    """
    This function simply evaluates whether the attempted hit actually
    hits.
    """

    try:
        hit_chance = get_hit_chance(attacker, victim)
        if random.randint(1, 100) <= hit_chance:
            return True
        else:
            return False
    except Exception:
        logger.log_file("Error in hit_check. Attacker = %s, victim = %s." % (attacker.key, victim.key), filename="combat.log")
        logger.log_trace("Error in hit_check.")                 


def modify_experience(attacker, victim, experience):
    """
    This function applies the appropriate modifiers to experience
    # based on the player's attributes.
    """

    # Modify experience award based on relative alignment.
    alignment_difference = abs(attacker.db.alignment - victim.db.alignment)
    if alignment_difference >= 1000:
        experience_modified = math.ceil(experience * 1.25)
    elif alignment_difference < 500:
        experience_modified = math.ceil(experience * 0.75)
    else:
        experience_modified = experience

    # Modify experience award based on racial hatreds or affection.

    if "hate list" in rules_race.get_race(attacker.race):
        if victim.race in rules_race.get_race(attacker.race)["hate list"]:
            experience_modified *= 1.1
    elif victim.race == attacker.race:
        experience_modified *= 0.875

    experience_modified = math.ceil(experience_modified)

    return int(experience_modified)
