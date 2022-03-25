import math
import random
import evennia
from evennia import create_object
from evennia import TICKER_HANDLER as tickerhandler
from world import rules_race, rules, rules_skills
from server.conf import settings


def create_combat(attacker, victim):
    """Create a combat, if needed, returns the combat object."""

    # Check if the attacker is in a safe room.
    if "safe" in attacker.location.db.room_flags:
        attacker.msg("You cannot attack in a safe room!")
        return
    # Check if the victim cannot be killed.
    elif "mobile" in victim.tags.all():
        if "no kill" in victim.db.act_flags:
            attacker.msg("The forces of commerce and justice stop you from attacking %s." % victim.key)
            return

    if not attacker.ndb.combat_handler and not victim.ndb.combat_handler:

        combat = create_object("commands.combat_commands.Combat", key=("combat_handler_%s" % attacker.location.db.vnum))
        combat.add_combatant(attacker, victim)
        combat.add_combatant(victim, attacker)
        combat.location = attacker.location
        combat.db.desc = "This is a combat instance."
        return combat

    elif not attacker.ndb.combat_handler:
        combat = victim.ndb.combat_handler
        combat.add_combatant(attacker, victim)

    elif not victim.ndb.combat_handler:
        combat = attacker.ndb.combat_handler
        combat.add_combatant(victim, attacker)
        combat.change_target(attacker, victim)

    return False

def do_attack(attacker, victim, eq_slot, **kwargs):
    """
    This function implements the effects of a single hit. It
    is used in two different modes. It is called with no
    kwargs when a standard attack-round attack, which both
    calls the take_damage method on the victim, doing the
    damage, and returns a tuple of strings of output for the
    attacker, the victim, and those watching in the room for
    that single hit attempt. The second mode allows special
    attacks (kick, fireball, damage on dirt kicking) to do
    the work on determining whether they hit, the amount of
    damage and output, and provide that to do_attack to
    handle the dealing of the damage, awarding of xp, and
    actually sending out output, rather than building into
    a string.    
    """

    # Don't beat a dead horse.
    if victim.hitpoints_current <= 0:
        return
    
    # Special attack.
    if "hit" in kwargs:
        hit = kwargs["hit"]
    # Base combat round attacks.
    else:
        hit = hit_check(attacker, victim)
        
    damage_type = get_damagetype(attacker)
    experience_modified = 0

    if hit:

        # Special attack
        if "damage" in kwargs:
            damage = kwargs["damage"]
        # Base combat round attacks.
        else:
            damage = do_damage(attacker, victim, eq_slot)
        
        if "player" in attacker.tags.all():
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

            combat = victim.ndb.combat_handler
            round = combat.db.rounds
            round_fraction = (1 / (1 + round / 10))

            experience_raw = int(round_fraction *
                                 percent_damage *
                                 victim.db.experience_total
                                 )

            # Reduce the mobile's current experience based on the pre-
            # modification award.
            victim.db.experience_current -= experience_raw

            # Attacker experience is modified by alignment and race.
            experience_modified = int(modify_experience(attacker,
                                                        victim,
                                                        experience_raw
                                                        ))

            attacker.db.experience_total += experience_modified

        victim.take_damage(damage)
        
        if "output" in kwargs:
            attacker.msg("%s" % kwargs["output"][0])
            victim.msg("%s" % kwargs["output"][1])
            attacker.location.msg_contents("%s" % kwargs["output"][2], exclude=(attacker, victim))
        else:
            attacker_string = ("You |g%s|n %s with your %s.\n"
                               % (get_damagestring("attacker", damage),
                                  victim.key,
                                  damage_type
                                  )
                               )
            victim_string = ("%s |r%s|n you with its %s.\n"
                             % (attacker.key,
                                get_damagestring("victim", damage),
                                damage_type
                                )
                             )
            room_string = ("%s %s %s with its %s.\n"
                           % (attacker.key,
                              get_damagestring("victim", damage),
                              victim.key,
                              damage_type
                              )
                           )

        if "player" in attacker.tags.all():
            if damage > attacker.db.damage_maximum:
                attacker.db.damage_maximum = damage
                attacker.db.damage_maximum_mobile = victim.key
                attacker_string += ("Your %s for %d damage is your record for damage in one hit!!!\n"
                                    % (damage_type, damage))
    else:
        if "output" in kwargs:
            attacker.msg("%s" % kwargs["output"][0])
            victim.msg("%s" % kwargs["output"][1])
            attacker.location.msg_contents("%s" % kwargs["output"][2], exclude=(attacker, victim))
        else:
            attacker_string = ("You miss %s with your %s.\n" % (victim.key,
                                                                damage_type
                                                                ))
            victim_string = ("%s misses you with its %s.\n" % (attacker.key,
                                                               damage_type
                                                               ))
            room_string = ("%s misses %s with its %s.\n" % (attacker.key,
                                                            victim.key,
                                                            damage_type
                                                            ))
    if not kwargs:
        return (attacker_string, victim_string, room_string)


def do_damage(attacker, victim, eq_slot):
    """
    This is called on a successful hit, and returns the total
    damage for that hit.
    """

    if "mobile" in attacker.tags.all():
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

    else:
        if attacker.db.eq_slots[eq_slot]:
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

        else:
            damage = random.randint(1, 2) * attacker.size

            # Get a bonus to damage from damroll. Since we got here, there is
            # no weapon to worry about.
            dam_bonus = attacker.damroll

            damage += dam_bonus

    # Check if player has enhanced damage.
    if "player" in attacker.tags.all():
        if "enhanced damage" in attacker.db.skills:
            damage += int(damage * attacker.db.skills["enhanced damage"] / 150)
            rules_skills.check_skill_improve(attacker, "enhanced damage", True, 5)
            
    if victim.db.position == "sleeping":
        damage *= 2

    return damage


def do_death(attacker, victim):
    """
    This handles the death and returns some output.
    """

    # Build a string for reporting death to characters, and add to output
    # strings.
    attacker_string = ("With your final %s, %s falls to the ground, DEAD!!!\n"
                       % (get_damagetype(attacker), victim.key))
    victim_string = ("You have been |rKILLED|n!!!\n You awaken again at your "
                     "home location.\n")
    room_string = ("%s has been KILLED by %s!!!\n"
                   % ((victim.key[0].upper() + victim.key[1:0]), attacker.key))

    if "mobile" in victim.tags.all():

        # Check none to see if there is a handy corpse, already made.

        object_candidates = evennia.search_tag("npc corpse")

        corpse = False

        for object in object_candidates:
            if not object.location:
                corpse = object
                corpse.key = "the corpse of %s" % victim.key
                break

        if not corpse:

            # Create corpse.
            corpse = create_object("objects.NPC_Corpse", key=("the corpse of %s"
                                                              % victim.key))

        corpse.db.desc = ("The corpse of %s lies here." % victim.key)
        corpse.location = attacker.location
        # Set the corpse to disintegrate.
        tickerhandler.add(settings.DEFAULT_DISINTEGRATE_TIME, corpse.at_disintegrate)

        # Move all victim items to corpse.
        for item in victim.contents:
            if item.db.equipped:
                item.remove_from(victim)
            # Eventually, will want the below to have , quiet = True after
            # done testing.
            item.move_to(corpse)

        # Move victim to None location to be reset later.
        victim.location = None

        # Award xp.
        if "player" in attacker.tags.all():
            experience_modified = \
                modify_experience(attacker,
                                  victim,
                                  victim.db.experience_current
                                  )
            attacker.db.experience_total += experience_modified
            attacker_string += ("You receive %s experience as a result of "
                                "your kill!\n" % experience_modified)
        # Check if experience was more than previous best kill.
        if victim.db.experience_total > attacker.db.kill_experience_maximum:
            attacker.db.kill_experience_maximum = victim.db.experience_total
            attacker.db.kill_experience_maximum_mobile = victim.key
            attacker_string += ("That kill is your new record for most "
                                "experience obtained for a kill!\n"
                                "You received a total of %d experience "
                                "from %s.\n" % (victim.db.experience_total, victim.key))

        # Trying to give the attacker a look at the corpse after it dies
        corpse_look = attacker.at_look(corpse)
        attacker_string += ("%s\n" % corpse_look)
            
        # Increment kills.
        attacker.db.kills += 1

        # Update alignment.
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
                                               )/50000000
                                              )

        # Figure out how to calculate gold on mobile and award.

        # attacker_string += ("You receive |y%s gold|n as a result of your
        # kill!" % victim.)

    else:

        corpse = False

        object_candidates = evennia.search_tag("pc corpse")

        for object in object_candidates:
            if not object.location:
                corpse = object
                corpse.key = "the corpse of %s" % victim.key
                break

        if not corpse:

            # Create corpse.
            corpse = create_object("objects.PC_Corpse", key=("the corpse of %s"
                                                              % victim.key))

        corpse.db.desc = ("The corpse of %s lies here." % victim.key)
        corpse.location = attacker.location
        tickerhandler.add(settings.PC_CORPSE_DISINTEGRATE_TIME, corpse.at_disintegrate)

        # Increment hero deaths.
        victim.db.died += 1

        # Heroes keep their items.

        # Clear spell affects.
        victim.db.spell_affects = {}

        # Do xp penalty.
        if victim.level > 5:
            experience_loss = int(settings.EXPERIENCE_LOSS_DEATH * rules.experience_loss_base(victim))
            victim.db.experience_total -= experience_loss

            victim_string += ("You lose %s experience as a result of your death!" % experience_loss)

            # Do gold penalty, after figuring out how much it should be.

    return (attacker_string, victim_string, room_string)


def do_dirt_kicking(attacker, victim):
    """
    This does the dirty (heh) work of the dirt kick command.
    """
    
    skill = rules_skills.get_skill(skill_name="dirt kicking")
    wait_state = skill["wait state"]
    
    # Build basic chance of success.
    chance = (attacker.db.skills["dirt kicking"] - victim.level) * 2
    chance += attacker.dexterity
    chance -= victim.dexterity
    
    # Correct for terrain.
    
    if "desert" in attacker.location.db.room_flags:
        chance += 10
    elif "field" in attacker.location.db.room_flags:
        chance += 5
    elif "city" in attacker.location.db.room_flags or "mountain" in attacker.location.db.room_flags:
        chance -= 10
    elif "inside" in attacker.location.db.room_flags:
        chance -= 20
    elif "forest" in attacker.location.db.room_flags or "hills" in attacker.location.db.room_flags:
        pass
    else:
        chance = 0
        
    if chance == 0:
        attacker.msg("There is no dirt to kick here!")
        return
    
    if random.randint(1, 100) > chance:
        
        if "player" in attacker.tags.all():
            rules_skills.check_skill_improve(attacker, "dirt kicking", False, 1)
            attacker.moves_spent += 5

        attacker_output = ("Your attempt to kick dirt in the eyes of %s fails.\n" % victim.key)
        victim_output = ("%s kicks dirt over your shoulder.\n" % (attacker.key[0].upper() + attacker.key[1:]))
        room_output = ("%s kicks dirt past %s.\n" % ((attacker.key[0].upper() + attacker.key[1:]), victim.name))

        combat.db.combatants[attacker]["special attack"]["output"] = [attacker_output, victim_output, room_output]
        
    else:

        if "player" in attacker.tags.all():
            rules_skills.check_skill_improve(attacker, "dirt kicking", True, 1)
            attacker.moves_spent += 10

        damage = random.randint(2, 5)
        attacker_output = ("%s is blinded by the dirt in its eyes!\n" % (victim.key[0].upper() + victim.key[1:]))
        victim_output = ("%s kicks dirt in your eyes!.\nYou can't see a thing!\n" % (attacker.key[0].upper() + attacker.key[1:]))
        room_output = ("%s kicks dirt in %s's eyes, blinding them.\n" % ((attacker.key[0].upper() + attacker.key[1:]), victim.key))

        combat.db.combatants[attacker]["special attack"]["output"] = [attacker_output, victim_output, room_output]
        combat.db.combatants[attacker]["special attack"]["hit"] = True
        combat.db.combatants[attacker]["special attack"]["damage"] = damage
        # Need to figure out how to pass info on duration, and put affect in as a kwarg in do_attack, with callback function for removing affect.
        combat.db.combatants[attacker]["special attack"]["affect"] = {"name": "blind", "apply": "hitroll", "modifier": -4}
        combat.db.combatants[attacker]["special attack"]["affect duration"] = attacker.level
       
        rules.wait_state_apply(attacker, wait_state)
        
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
        # Remove character from combat.
        combat = character.ndb.combat_handler
        combat.remove_combatant(character)

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
        combat.combat_end_check()

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

def do_kick(attacker, victim):
    combat = attacker.ndb.combat_handler
    
    if random.randint(1, 100) > attacker.db.skills["kick"]:
        if "player" in attacker.tags.all():
            rules_skills.check_skill_improve(attacker, "kick", False, 4)
            attacker.moves_spent += 5

        attacker_output = ("You kick wildly at %s and miss.\n" % victim.key)
        victim_output = ("%s kicks wildly at you and misses.\n" % (attacker.key[0].upper() + attacker.key[1:]))
        room_output = ("%s kicks at %s and misses.\n" % ((attacker.key[0].upper() + attacker.key[1:]), victim.name))

        combat.db.combatants[attacker]["special attack"]["output"] = [attacker_output, victim_output, room_output]
        combat.db.combatants[attacker]["special attack"]["hit"] = False
        combat.db.combatants[attacker]["special attack"]["damage"] = 0
        
    else:

        if "player" in attacker.tags.all():
            rules_skills.check_skill_improve(attacker, "kick", True, 4)
            attacker.moves_spent += 10

        damage = random.randint(1, attacker.level)
        attacker_output = ("You |g%s|n %s with your vicious kick.\n" % (get_damagestring("attacker", damage), victim.key))
        victim_output = ("%s |r%s|n you with its vicious kick.\n" % ((attacker.key[0].upper() + attacker.key[1:]), get_damagestring("victim", damage)))
        room_output = ("%s |r%s|n %s with its vicious kick.\n" % ((attacker.key[0].upper() + attacker.key[1:]), get_damagestring("victim", damage), victim.key))

        combat.db.combatants[attacker]["special attack"]["output"] = [attacker_output, victim_output, room_output]
        combat.db.combatants[attacker]["special attack"]["hit"] = True
        combat.db.combatants[attacker]["special attack"]["damage"] = damage
        

def do_one_character_attacks(attacker, victim):
    """
    This calls do_one_weapon_attacks for all relevant weapon slots for one
    attacker on one victim, which should be ALL attacks for that
    attacker.
    """

    attacker_string = ""
    victim_string = ""
    room_string = ""
    
    # Check if special attack is necessary.
    combat = attacker.ndb.combat_handler
    if combat.db.combatants[attacker]["special attack"] and victim.hitpoints_current > 0 and victim.location == attacker.location:
        if "hit" in combat.db.combatants[attacker]["special attack"]:
            special_hit = combat.db.combatants[attacker]["special attack"]["hit"]
            special_damage = combat.db.combatants[attacker]["special attack"]["damage"]
            special_output = combat.db.combatants[attacker]["special attack"]["output"]

            new_attacker_string, new_victim_string, new_room_string = do_attack(attacker, victim, None, hit=special_hit, damage=special_damage, output=special_output)
        else:
            special_output = combat.db.combatants[attacker]["special attack"]["output"]
            new_attacker_string = special_output[0]
            new_victim_string = special_output[1]
            new_room_string = special_output[2]

            if "extra" in combat.db.combatants[attacker]["special attack"]:
                extra = combat.db.combatants[attacker]["special attack"]["extra"]
                extra_string = special_output[3]
                combat.db.combatants[extra]["combat message"] += extra_string

        attacker_string += new_attacker_string
        victim_string += new_victim_string
        room_string += new_room_string
    
    # Do base attacks.
    if victim.hitpoints_current > 0 and victim.location == attacker.location:
        new_attacker_string, new_victim_string, new_room_string = \
            do_one_weapon_attacks(attacker, victim, "wielded, primary")
        attacker_string += new_attacker_string
        victim_string += new_victim_string
        room_string += new_room_string
    
    # Check for dual wield.
    if victim.hitpoints_current > 0 and victim.location == attacker.location:
        if attacker.db.eq_slots["wielded, primary"] and \
                attacker.db.eq_slots["wielded, secondary"]:
            new_attacker_string, new_victim_string, new_room_string = \
                do_one_weapon_attacks(attacker, victim, "wielded, secondary")
            attacker_string += new_attacker_string
            victim_string += new_victim_string
            room_string += new_room_string

    if victim.hitpoints_current <= 0:
        new_attacker_string, new_victim_string, new_room_string = \
            do_death(attacker, victim)
        attacker_string += new_attacker_string
        victim_string += new_victim_string
        room_string += new_room_string

    # In combat handler, need to use these strings to create the full output
    # block reporting the results of everyone's attacks to all players only.
    return (attacker_string, victim_string, room_string)


def do_one_weapon_attacks(attacker, victim, eq_slot):
    """
    This determines how many hit attempts will occur for one attacker
    against one victim, with one weapon slot, and then calls do_attack
    for each. It assembles the output for each hit attempt for the
    attacker, victim and those in the room, and returns a tuple of
    those values.
    """
    attacker_string = ""
    victim_string = ""
    room_string = ""

    # If primary weapon, first hit is free.
    if victim.hitpoints_current > 0 and victim.location == attacker.location:
        if eq_slot == "wielded, primary":
            attacker_string, victim_string, room_string = do_attack(attacker,
                                                                    victim,
                                                                    eq_slot
                                                                    )
        else:
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    attacker_string, victim_string, room_string = \
                        do_attack(attacker, victim, eq_slot)
            else:
                # Save hero for dual skill implementation.
                pass

    # Check for second attack.
    if victim.hitpoints_current > 0 and victim.location == attacker.location:
        if eq_slot == "wielded, primary":
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    new_attacker_string, new_victim_string, new_room_string = \
                        do_attack(attacker, victim, eq_slot)
                    attacker_string += new_attacker_string
                    victim_string += new_victim_string
                    room_string += new_room_string
            else:
                # Wait to build out hero until skills built
                pass
        else:
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    new_attacker_string, new_victim_string, new_room_string = \
                        do_attack(attacker, victim, eq_slot)
                    attacker_string += new_attacker_string
                    victim_string += new_victim_string
                    room_string += new_room_string
            else:
                # Wait to build out hero until skills built
                pass

    # Check for third attack.
    if victim.hitpoints_current > 0 and victim.location == attacker.location:
        if eq_slot == "wielded, primary":
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    new_attacker_string, new_victim_string, new_room_string = \
                        do_attack(attacker, victim, eq_slot)
                    attacker_string += new_attacker_string
                    victim_string += new_victim_string
                    room_string += new_room_string
            else:
                # Wait to build out hero until skills built
                pass
        else:
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    new_attacker_string, new_victim_string, new_room_string = \
                        do_attack(attacker, victim, eq_slot)
                    attacker_string += new_attacker_string
                    victim_string += new_victim_string
                    room_string += new_room_string
            else:
                # Wait to build out hero until skills built
                pass

    # Check for fourth attack, for mobiles only.
    if victim.hitpoints_current > 0 and victim.location == attacker.location:
        if "mobile" in attacker.tags.all():
            if random.randint(1, 100) < (attacker.db.level / 2):
                new_attacker_string, new_victim_string, new_room_string = \
                    do_attack(attacker, victim, eq_slot)
                attacker_string += new_attacker_string
                victim_string += new_victim_string
                room_string += new_room_string

    return (attacker_string, victim_string, room_string)


def do_rescue(attacker, extra, victim):
    combat = attacker.ndb.combat_handler

    if random.randint(1, 100) > attacker.db.skills["rescue"]:
        if "player" in attacker.tags.all():
            rules_skills.check_skill_improve(attacker, "rescue", False)
            attacker.moves_spent += 5

        attacker_output = ("You fail to rescue %s!\n" % extra.key)
        victim_output = ("%s tries to get between you and %s and fails.\n" % ((attacker.key[0].upper() + attacker.key[1:]), extra.key))
        room_output = ("%s tries to get between %s and %s and fails.\n" % ((attacker.key[0].upper() + attacker.key[1:]), victim.key, extra.key))
        extra_output = ("%s tries to get get between you and your attacker and fails!" % (attacker.key[0].upper() + attacker.key[1:]))

        combat.db.combatants[attacker]["special attack"]["output"] = [attacker_output, victim_output, room_output, extra_output]
        combat.db.combatants[attacker]["special attack"]["extra"] = extra

    else:

        if "player" in attacker.tags.all():
            rules_skills.check_skill_improve(attacker, "rescue", True)

        combat.db.combatants[victim]["target"] = attacker
        attacker_output = ("You rescue %s!\n" % extra.key)
        victim_output = ("%s rescues %s from you.\n" % ((attacker.key[0].upper() + attacker.key[1:]), extra.key))
        room_output = ("%s rescues %s from %s.\n" % ((attacker.key[0].upper() + attacker.key[1:]), extra.key, victim.key))
        extra_output = ("%s rescues you from %s!" % (attacker.key[0].upper() + attacker.key[1:]), victim.key)

        combat.db.combatants[attacker]["special attack"]["output"] = [attacker_output, victim_output, room_output, extra_output]
        combat.db.combatants[attacker]["special attack"]["extra"] = extra


def hit_check(attacker, victim):
    """
    This function simply evaluates whether the attempted hit actually
    hits.
    """

    hit_chance = get_hit_chance(attacker, victim)
    if random.randint(1, 100) <= hit_chance:
        return True
    else:
        return False


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
    if attacker.db.eq_slots["wielded, primary"]:
        weapon = attacker.db.eq_slots["wielded, primary"]
        damagetype = weapon.db.weapon_type
    else:
        if "damage message" in rules_race.get_race(attacker.race):
            damagetype = rules_race.get_race(attacker.race)["damage message"]
        else:
            damagetype = "punch"

    return damagetype


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



def get_hitskill(attacker, victim):
    # Make sure that hitroll does not include hitroll from weapon if can't
    # wield it.
    hitskill = get_warskill(attacker) + attacker.hitroll + \
        get_race_hitbonus(attacker, victim) + 10*(attacker.dexterity - 10)
    if hitskill > 1:
        return hitskill
    else:
        return 1


def get_race_hitbonus(attacker, victim):
    hitbonus = victim.size - attacker.size
    return hitbonus


def get_warskill(combatant):
    if "mobile" in combatant.tags.all():
        warskill_factor = combatant.db.level/101
        warskill = int(120*warskill_factor)
        return warskill
    else:
        # Will eventually deal with variable player warskill based on
        # class-type skills learned.
        warskill_factor = combatant.db.level/101
        warskill = int(120*warskill_factor)
        return warskill


def is_safe(character):
    """
    This function tests whether combat is possible with this character
    in its location, and returns a boolean of True if combat is not
    possible (they ARE safe) or False if it is possible (they are NOT
    safe).
    """
    
    if "act_flags" in character.db.all:
        if "no kill" in target.db.act_flags:
            return True
    elif "safe" in character.location.db.room_flags:
        return True
    
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
