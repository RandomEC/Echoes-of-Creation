import math
import random
from evennia.utils import search
from world import rules, rules_combat, rules_skills

def check_cast(caster):
    """
    This function is used to check for any player or room-based
    state effects that would prevent casting.
    """

    if "cone of silence" in caster.location.db.room_flags:
        return "You can't ... You are in a Cone of Silence!\n"
    
    elif "no magic" in caster.location.db.room_flags:
        return "You feel a strong dampening field blocking your spell.\n"
    
    elif caster.get_affect_status("mute"):
        return "You can't ... You're mute!\n"
    
    elif caster.db.position != "standing":
        return "You can't concentrate enough - stand up!\n"

    return False


def do_agitation(caster, target, mana_cost):
    """ Function implementing agitation spell"""

    spell = rules_skills.get_skill(skill_name="agitation")

    level = caster.level

    # This list creates a seed for how high damage will be,
    # with the caster's level corresponding to the list
    # index.
    damage_seed = [0,
                   0, 0, 0, 0, 0, 12, 15, 18, 21, 24,
                   24, 24, 25, 25, 26, 26, 26, 27, 27, 27,
                   28, 28, 28, 29, 29, 29, 30, 30, 30, 31,
                   31, 31, 32, 32, 32, 33, 33, 33, 34, 34,
                   34, 35, 35, 35, 36, 36, 36, 37, 37, 37
                   ]

    # Make sure you do not exceed the list boundaries.
    if level > len(damage_seed):
        level = len(damage_seed)
    elif level < 0:
        level = 0

    # Use the seed to create a damage range from seed/2 up to
    # seed*2, then get a value randomly in that range.
    damage = random.randint(int(damage_seed[level] / 2), int(damage_seed[level] * 2))

    if save_spell(caster.level, target):
        damage = int(damage / 2)

    if random.randint(1, 100) <= caster.db.skills["agitation"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "agitation", True, 4)

        caster.msg("You chant 'agitation'.\n")
        player_output_magic_chant(caster, "agitation")

        attacker_output = ("You |g%s|n %s with your molecular agitation.\n" % (rules_combat.get_damagestring("attacker", damage),
                                                                          target.key
                                                                          ))
        victim_output = ("%s |r%s|n you with %s molecular agitation.\n" % ((caster.key[0].upper() + caster.key[1:]),
                                                                      rules_combat.get_damagestring("victim", damage),
                                                                      rules.pronoun_possessive(caster)
                                                                      ))
        room_output = ("%s |r%s|n %s with %s molecular agitation.\n" % ((caster.key[0].upper() + caster.key[1:]),
                                                                   rules_combat.get_damagestring("victim", damage),
                                                                   target.key,
                                                                   rules.pronoun_possessive(caster)
                                                                   ))

        output = [attacker_output, victim_output, room_output]

        rules_combat.do_attack(caster, target, None, hit=True, damage=damage, output=output, type="molecular agitation")

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "agitation", False, 4)
        caster.msg("You chant 'agitation'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "agitation")

        
def do_armor(caster, target, mana_cost):
    """Implements the armor spell."""

    spell = rules_skills.get_skill(skill_name="armor")
    level = caster.level
    wait_state = spell["wait state"]

    if random.randint(1, 100) <= caster.db.skills["armor"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "armor", True, 2)

        caster.msg("You chant 'armor'.\n")
        player_output_magic_chant(caster, "armor")

        if caster != target:
            caster.msg("You temporarily enhance %s's armor." % (target.key[0].upper() + target.key[1:]))
        target.msg("Your armor has been temporarily enhanced.")

        rules.affect_apply(target,
                           "armor",
                           24,
                           "You feel less armored.",
                           "",
                           armor_class=-20
                           )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "armor", False, 2)
        caster.msg("You chant 'armor'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "armor")


def do_bless(caster, target, mana_cost):
    """Implements the bless spell."""

    spell = rules_skills.get_skill(skill_name="bless")
    level = caster.level
    wait_state = spell["wait state"]

    if random.randint(1, 100) <= caster.db.skills["bless"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "bless", True, 2)

        caster.msg("You chant 'bless'.\n")
        player_output_magic_chant(caster, "bless")

        if caster != target:
            caster.msg("You bless %s." % (target.key[0].upper() + target.key[1:]))
        target.msg("You feel righteous.")

        rules.affect_apply(target,
                           "bless",
                           (6 + caster.level),
                           "You feel less righteous.",
                           "",
                           hitroll=math.ceil((caster.level + 2) / 8),
                           saving_throw=math.ceil((caster.level + 2) / 8)
                           )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "bless", False, 2)
        caster.msg("You chant 'bless'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "bless")


def do_cause_light(caster, target, mana_cost):
    """ Function implementing cause light wounds spell"""

    spell = rules_skills.get_skill(skill_name="cause light")

    level = caster.level

    damage = random.randint(1, 8) + int(caster.level / 3)

    if random.randint(1, 100) <= caster.db.skills["cause light"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "cause light", True, 4)

        caster.msg("You chant 'cause light'.\n")
        player_output_magic_chant(caster, "cause light")

        attacker_output = ("You |g%s|n %s with your invocation.\n" % (rules_combat.get_damagestring("attacker", damage),
                                                                          target.key
                                                                          ))
        victim_output = ("%s |r%s|n you with %s invocation.\n" % ((caster.key[0].upper() + caster.key[1:]),
                                                                      rules_combat.get_damagestring("victim", damage),
                                                                      rules.pronoun_possessive(caster)
                                                                      ))
        room_output = ("%s |r%s|n %s with %s invocation.\n" % ((caster.key[0].upper() + caster.key[1:]),
                                                                   rules_combat.get_damagestring("victim", damage),
                                                                   target.key,
                                                                   rules.pronoun_possessive(caster)
                                                                   ))

        output = [attacker_output, victim_output, room_output]

        rules_combat.do_attack(caster, target, None, hit=True, damage=damage, output=output, type="invocation")

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "cause light", False, 4)
        caster.msg("You chant 'cause light'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "cause light")


def do_chill_touch(caster, target, mana_cost):
    """ Function implementing chill touch spell"""

    spell = rules_skills.get_skill(skill_name="chill touch")

    level = caster.level

    # This list creates a seed for how high damage will be,
    # with the caster's level corresponding to the list
    # index.
    damage_seed = [0,
                   0, 0, 6, 7, 8, 9, 12, 13, 13, 13,
                   14, 14, 14, 15, 15, 15, 16, 16, 16, 17,
                   17, 17, 18, 18, 18, 19, 19, 19, 20, 20,
                   20, 21, 21, 21, 22, 22, 22, 23, 23, 23,
                   24, 24, 24, 25, 25, 25, 26, 26, 26, 27
                   ]

    # Make sure you do not exceed the list boundaries.
    if level > len(damage_seed):
        level = len(damage_seed)
    elif level < 0:
        level = 0

    # Use the seed to create a damage range from seed/2 up to
    # seed*2, then get a value randomly in that range.
    damage = random.randint(int(damage_seed[level] / 2), int(damage_seed[level] * 2))

    if save_spell(caster.level, target):
        damage = int(damage / 2)

    if random.randint(1, 100) <= caster.db.skills["chill touch"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "chill touch", True, 4)

        caster.msg("You chant 'chill touch'.\n")
        player_output_magic_chant(caster, "chill touch")

        attacker_output = ("You |g%s|n %s with your chilling touch.\n" % (rules_combat.get_damagestring("attacker", damage),
                                                                          target.key
                                                                          ))
        victim_output = ("%s |r%s|n you with %s chilling touch.\n" % ((caster.key[0].upper() + caster.key[1:]),
                                                                      rules_combat.get_damagestring("victim", damage),
                                                                      rules.pronoun_possessive(caster)
                                                                      ))
        room_output = ("%s |r%s|n %s with %s chilling touch.\n" % ((caster.key[0].upper() + caster.key[1:]),
                                                                   rules_combat.get_damagestring("victim", damage),
                                                                   target.key,
                                                                   rules.pronoun_possessive(caster)
                                                                   ))

        output = [attacker_output, victim_output, room_output]

        rules_combat.do_attack(caster, target, None, hit=True, damage=damage, output=output, type="chilling touch")

        if not target.get_affect_status("chill touch"):
            rules.affect_apply(target,
                               "chill touch",
                               6,
                               "You feel less cold.",
                               "%s appears to warm significantly." % (target.key[0].upper() + target.key[1:]),
                               apply_1=["strength", -1]
                               )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "chill touch", False, 4)
        caster.msg("You chant 'chill touch'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "chill touch")


def do_continual_light(caster, mana_cost):
    """ Function implementing continual light spell"""

    spell = rules_skills.get_skill(skill_name="continual light")

    level = caster.level

    if random.randint(1, 100) <= caster.db.skills["continual light"] or "mobile" in caster.tags.all():
        light = rules.make_object(caster.location, False, "o21")

        light.db.cost = 0
        rules.set_disintegrate_timer(light)

        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "continual light", True, 1)

        caster.msg("You chant 'continual light'.\nYou twiddle your thumbs and %s appears." % light.key)
        player_output_magic_chant(caster, "continual light")
        caster.location.msg_contents("%s twiddles %s thumbs and %s appears."
                                     % ((caster.key[0].upper() + caster.key[1:]),
                                        rules.pronoun_possessive(caster),
                                        light.key),
                                     exclude=caster)

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "continual light", False, 1)
        caster.msg("You chant 'continual light'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "continual light")


def do_create_food(caster, mana_cost):
    """ Function implementing create food spell"""
    
    spell = rules_skills.get_skill(skill_name="create food")

    level = caster.level

    if random.randint(1, 100) <= caster.db.skills["create food"] or "mobile" in caster.tags.all():
        food = random.randint(1, 8)
        if food == 1:
            food = rules.make_object(caster.location, False, "o20")
        elif food == 2:
            food = rules.make_object(caster.location, False, "o4434")
        elif food == 3:
            food = rules.make_object(caster.location, False, "o4432")
        elif food == 4:
            food = rules.make_object(caster.location, False, "o4436")
        elif food == 5:
            food = rules.make_object(caster.location, False, "o4443")
        elif food == 6:
            food = rules.make_object(caster.location, False, "o4445")
        elif food == 7:
            food = rules.make_object(caster.location, False, "o4433")
        else:
            food = rules.make_object(caster.location, False, "o4444")

        food.db.hours_fed = 5 + level
        rules.set_disintegrate_timer(food)

        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "create food", True, 1)
        caster.msg("You chant 'create food'.\n%s suddenly appears." % (food.key[0].upper() + food.key[1:]))
        player_output_magic_chant(caster, "create food")
        caster.location.msg_contents("%s suddenly appears."
                                     % (food.key[0].upper() + food.key[1:]),
                                     exclude=caster)
        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "create food", False, 1)
        caster.msg("You chant 'create food'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "create food")


def do_create_sound(caster, mana_cost, target, sound):
    """ Function implementing create sound spell"""

    spell = rules_skills.get_skill(skill_name="create sound")
    level = caster.level

    if random.randint(1, 100) <= caster.db.skills["create sound"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
            rules_skills.check_skill_improve(caster, "create sound", True, 1)
        caster.msg(
            "You chant 'create sound'.\nYou make it appear that %s says '%s'." % ((target.key[0].upper() + target.key[1:]), sound))
        player_output_magic_chant(caster, "create sound")
        for object in caster.location.contents:
            if object == target and object.db.position != "sleeping":
                object.msg("A sound seemingly emanates from you saying '%s'" % sound)
            elif ("player" in object.tags.all() or "mobile" in object.tags.all()) and object != caster and object.db.position != "sleeping":
                if save_spell(level, target):
                    object.msg("%s makes %s say '%s'" % ((caster.key[0].upper() + caster.key[1:]), target, sound))
                else:
                    object.msg("%s says '%s'" % ((target.key[0].upper() + target.key[1:]), sound))
        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
            rules_skills.check_skill_improve(caster, "create sound", False, 1)
        caster.msg("You chant 'create sound'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "create sound")


def do_create_water(caster, mana_cost, target_container):
    """ Function implementing create water spell"""
    
    spell = rules_skills.get_skill(skill_name="create water")
    level = caster.level

    if random.randint(1, 100) <= caster.db.skills["create water"] or "mobile" in caster.tags.all():
        # If we implement weather at some point, the below 2 gets boosted to 4
        # if it is raining.
        # Just a quick reminder here, we treat capacity as amount of liquid in the
        # container, not amount remaining unfilled.
        if level * 2 < (target_container.db.capacity_maximum - target_container.db.capacity_current):
            water = level * 2
        else:
            water = target_container.db.capacity_maximum - target_container.db.capacity_current

        target_container.db.liquid_type = "water"
        target_container.db.capacity_current += water
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "create water", True, 1)
        caster.msg(
            "You chant 'create water'.\n%s is filled." % (target_container.key[0].upper() + target_container.key[1:]))
        player_output_magic_chant(caster, "create water")
        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "create water", False, 1)
        caster.msg("You chant 'create water'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "create water")            

        
def do_cure_light(caster, target, mana_cost):
    """ Function implementing cure light wounds spell"""

    spell = rules_skills.get_skill(skill_name="cure light")

    level = caster.level

    heal = random.randint(1, 8) + (caster.level / 3)

    if random.randint(1, 100) <= caster.db.skills["cure light"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "cure light", True, 1)

        caster.msg("You chant 'cure light'.\n")
        player_output_magic_chant(caster, "cure light")

        if target == caster:
            target_string = "your"
        else:
            target_string = "%s's" % target.key
        
        caster.msg("You cure some of %s light wounds.\n" % target_string)
                
        if target != caster:
            target.msg("You feel better!\n")
        
        if heal >= target.hitpoints_damaged:
            heal = target.hitooints_damaged
        target.hitpoints_damaged -= heal
        
        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "cure light", False, 1)
        caster.msg("You chant 'cure light'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "cure light")

        
def do_detect_evil(caster, target, mana_cost):
    """Implements the detect evil spell."""

    spell = rules_skills.get_skill(skill_name="detect evil")
    level = caster.level
    wait_state = spell["wait state"]

    if random.randint(1, 100) <= caster.db.skills["detect evil"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "detect evil", True, 2)

        caster.msg("You chant 'detect evil'.\n")
        player_output_magic_chant(caster, "detect evil")

        if caster != target:
            caster.msg("%s can now detect evil." % (target.key[0].upper() + target.key[1:]))
        target.msg("Your eyes tingle.")

        rules.affect_apply(target,
                           "detect evil",
                           caster.level,
                           "The red in your vision disappears.",
                           ""
                           )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "detect evil", False, 2)
        caster.msg("You chant 'detect evil'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "detect evil")


def do_detect_hidden(caster, target, mana_cost):
    """Implements the detect hidden spell."""

    spell = rules_skills.get_skill(skill_name="detect hidden")
    level = caster.level
    wait_state = spell["wait state"]

    if random.randint(1, 100) <= caster.db.skills["detect hidden"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "detect hidden", True, 2)

        caster.msg("You chant 'detect hidden'.\n")
        player_output_magic_chant(caster, "detect hidden")

        if caster != target:
            caster.msg("%s can now detect hidden." % (target.key[0].upper() + target.key[1:]))
        target.msg("Your awareness improves.")

        rules.affect_apply(target,
                           "detect hidden",
                           caster.level,
                           "You feel less aware of your surroundings.",
                           ""
                           )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "detect hidden", False, 2)
        caster.msg("You chant 'detect hidden'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "detect hidden")


def do_detect_invis(caster, target, mana_cost):
    """Implements the detect invis spell."""

    spell = rules_skills.get_skill(skill_name="detect invis")
    level = caster.level
    wait_state = spell["wait state"]

    if random.randint(1, 100) <= caster.db.skills["detect invis"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "detect invis", True, 2)

        caster.msg("You chant 'detect invis'.\n")
        player_output_magic_chant(caster, "detect invis")

        if caster != target:
            caster.msg("%s can now detect invisible." % (target.key[0].upper() + target.key[1:]))
        target.msg("Your eyes tingle.")

        rules.affect_apply(target,
                           "detect invis",
                           caster.level,
                           "You no longer see invisible things.",
                           ""
                           )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "detect invis", False, 2)
        caster.msg("You chant 'detect invis'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "detect invis")


def do_detect_magic(caster, target, mana_cost):
    """Implements the detect magic spell."""

    spell = rules_skills.get_skill(skill_name="detect magic")
    level = caster.level
    wait_state = spell["wait state"]

    if random.randint(1, 100) <= caster.db.skills["detect magic"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "detect magic", True, 2)

        caster.msg("You chant 'detect magic'.\n")
        player_output_magic_chant(caster, "detect magic")

        if caster != target:
            caster.msg("%s can now detect magic." % (target.key[0].upper() + target.key[1:]))
        target.msg("Your eyes tingle.")

        rules.affect_apply(target,
                           "detect magic",
                           caster.level,
                           "The detect magic wears off.",
                           ""
                           )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "detect magic", False, 2)
        caster.msg("You chant 'detect magic'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "detect magic")


def do_fly(caster, target, mana_cost):
    """Implements the fly spell."""

    spell = rules_skills.get_skill(skill_name="fly")
    level = caster.level
    wait_state = spell["wait state"]

    if random.randint(1, 100) <= caster.db.skills["fly"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "fly", True, 2)

        caster.msg("You chant 'fly'.\n")
        player_output_magic_chant(caster, "fly")

        if caster != target:
            caster.msg("%s's feet rise off the ground." % (target.key[0].upper() + target.key[1:]))
        target.msg("Your feet rise off the ground.")

        rules.affect_apply(target,
                           "fly",
                           (caster.level + 3),
                           "You slowly float to the ground.",
                           "%s slowly floats to the ground." % (target.key[0].upper() + target.key[1:])
                           )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "fly", False, 2)
        caster.msg("You chant 'fly'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "fly")


def do_levitation(caster, target, mana_cost):
    """Implements the levitation spell."""

    spell = rules_skills.get_skill(skill_name="levitation")
    level = caster.level
    wait_state = spell["wait state"]

    if random.randint(1, 100) <= caster.db.skills["levitation"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "levitation", True, 2)

        caster.msg("You chant 'levitation'.\n")
        player_output_magic_chant(caster, "levitation")

        if caster != target:
            caster.msg("%s's feet rise off the ground." % (target.key[0].upper() + target.key[1:]))
        target.msg("Your feet rise off the ground.")

        rules.affect_apply(target,
                           "fly",
                           (caster.level + 3),
                           "You slowly float to the ground.",
                           "%s slowly floats to the ground." % (target.key[0].upper() + target.key[1:])
                           )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "levitation", False, 2)
        caster.msg("You chant 'levitation'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "levitation")


def do_magic_missile(caster, target, mana_cost):
    """ Function implementing magic missile spell"""

    spell = rules_skills.get_skill(skill_name="magic missile")

    level = caster.level

    # This list creates a seed for how high damage will be,
    # with the caster's level corresponding to the list
    # index.
    damage_seed = [0,
                   3, 3, 4, 4, 5, 6, 6, 6, 6, 6,
                   7, 7, 7, 7, 7, 8, 8, 8, 8, 8,
                   9, 9, 9, 9, 9, 10, 10, 10, 10, 10,
                   11, 11, 11, 11, 11, 12, 12, 12, 12, 12,
                   13, 13, 13, 13, 13, 14, 14, 14, 14, 14
                   ]

    # Make sure you do not exceed the list boundaries.
    if level > len(damage_seed):
        level = len(damage_seed)
    elif level < 0:
        level = 0

    # Use the seed to create a damage range from seed/2 up to
    # seed*2, then get a value randomly in that range.
    damage = random.randint(int(damage_seed[level] / 2), int(damage_seed[level] * 2))

    if save_spell(caster.level, target):
        damage = int(damage / 2)

    if random.randint(1, 100) <= caster.db.skills["magic missile"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "magic missile", True, 4)

        caster.msg("You chant 'magic missile'.\n")
        player_output_magic_chant(caster, "magic missile")

        attacker_output = ("You |g%s|n %s with your magic missile.\n" % (rules_combat.get_damagestring("attacker", damage),
                                                                          target.key
                                                                          ))
        victim_output = ("%s |r%s|n you with %s magic missile.\n" % ((caster.key[0].upper() + caster.key[1:]),
                                                                      rules_combat.get_damagestring("victim", damage),
                                                                      rules.pronoun_possessive(caster)
                                                                      ))
        room_output = ("%s |r%s|n %s with %s magic missile.\n" % ((caster.key[0].upper() + caster.key[1:]),
                                                                   rules_combat.get_damagestring("victim", damage),
                                                                   target.key,
                                                                   rules.pronoun_possessive(caster)
                                                                   ))

        output = [attacker_output, victim_output, room_output]

        rules_combat.do_attack(caster, target, None, hit=True, damage=damage, output=output, type="magic missile")

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "magic missile", False, 4)
        caster.msg("You chant 'magic missile'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "magic missile")


def do_mental_barrier(caster, target, mana_cost):
    """Implements the mental barrier spell."""

    spell = rules_skills.get_skill(skill_name="mental barrier")
    level = caster.level
    wait_state = spell["wait state"]

    if random.randint(1, 100) <= caster.db.skills["mental barrier"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "mental barrier", True, 2)

        caster.msg("You chant 'mental barrier'.\n")
        player_output_magic_chant(caster, "mental barrier")

        caster.msg("You erect a mental barrier around yourself.")

        rules.affect_apply(target,
                           "mental barrier",
                           24,
                           "Your mental barrier breaks down.",
                           "",
                           armor_class=-20
                           )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "mental barrier", False, 2)
        caster.msg("You chant 'mental barrier'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "mental barrier")


def do_protection(caster, target, mana_cost):
    """Implements the protection spell."""

    spell = rules_skills.get_skill(skill_name="protection")
    level = caster.level
    wait_state = spell["wait state"]

    if random.randint(1, 100) <= caster.db.skills["protection"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "protection", True, 2)

        caster.msg("You chant 'protection'.\n")
        player_output_magic_chant(caster, "protection")

        if caster != target:
            caster.msg("You protection %s." % (target.key[0].upper() + target.key[1:]))
        target.msg("You feel righteous.")

        rules.affect_apply(target,
                           "protection",
                           24,
                           "You feel less protected.",
                           ""
                           )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "protection", False, 2)
        caster.msg("You chant 'protection'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "protection")


def do_refresh(caster, target, mana_cost):
    """ Function implementing refresh spell"""

    spell = rules_skills.get_skill(skill_name="refresh")

    level = caster.level

    refresh = random.randint(1, 8) + caster.level - 4
    
    if refresh < 1:
        refresh = 1

    if random.randint(1, 100) <= caster.db.skills["refresh"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "refresh", True, 1)

        caster.msg("You chant 'refresh'.\n")
        player_output_magic_chant(caster, "refresh")

        if target == caster:
            target_string = "yourself"
        else:
            target_string = target.key
        
        caster.msg("You cast refresh on %s.\n" % target_string)
                
        if target != caster:
            target.msg("You feel less tired.\n")
        
        if refresh >= target.moves_spent:
            refresh = target.moves_spent
        target.moves_spent -= refresh
        
        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "refresh", False, 1)
        caster.msg("You chant 'refresh'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "refresh")


def do_shield(caster, target, mana_cost):
    """Implements the shield spell."""

    spell = rules_skills.get_skill(skill_name="shield")
    level = caster.level
    wait_state = spell["wait state"]

    if random.randint(1, 100) <= caster.db.skills["shield"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "shield", True, 2)

        caster.msg("You chant 'shield'.\n")
        player_output_magic_chant(caster, "shield")

        if caster != target:
            caster.msg("%s is surrounded by a force shield." % (target.key[0].upper() + target.key[1:]))
        target.msg("You are surrounded by a force shield.")

        rules.affect_apply(target,
                           "shield",
                           (8 + caster.level),
                           "Your force shield shimmers then fades away.",
                           "",
                           armor_class=-20
                           )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "shield", False, 2)
        caster.msg("You chant 'shield'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "shield")


def do_sleep(caster, target, mana_cost):
    """ Function implementing sleep spell"""

    spell = rules_skills.get_skill(skill_name="sleep")
    level = caster.level

    if target.level > caster.level or save_spell(caster.level, target):
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
            rules_skills.check_skill_improve(caster, "sleep", False, 1)
        caster.msg("You chant 'sleep'.\nYou failed.\n")
        player_output_magic_chant(caster, "sleep")

    if random.randint(1, 100) <= caster.db.skills["sleep"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
            rules_skills.check_skill_improve(caster, "sleep", True, 1)
        caster.msg("You chant 'sleep'.\nYou put %s to sleep." % (target.key[0].upper() + target.key[1:]))
        player_output_magic_chant(caster, "sleep")
        target.msg("You feel very sleepy ... zzzzzz.")
        if target.sex == "neuter":
            verb = "drift"
        else:
            verb = "drifts"
        caster.location.msg_contents("%s's eyes close and %s slowly %s off to sleep."
                                     % ((caster.key[0].upper() + caster.key[1:]),
                                        rules.pronoun_subject(target),
                                        verb),
                                     exclude=(caster, target))

        rules.affect_apply(target,
                           "sleep",
                           (4 + caster.level),
                           "You feel less tired and wake up.",
                           "",
                           position="sleeping"
                           )

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
            rules_skills.check_skill_improve(caster, "create sound", False, 1)
        caster.msg("You chant 'create sound'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "create sound")


def do_summon_weapon(caster, mana_cost):
    """ Function implementing summon weapon spell"""

    spell = rules_skills.get_skill(skill_name="summon weapon")

    level = caster.level

    if random.randint(1, 100) <= caster.db.skills["summon weapon"] or "mobile" in caster.tags.all():
        weapon = rules.make_object(caster.location, False, "o36")

        weapon.db.cost = 0
        weapon.db.level = level
        weapon.db.damage_low, weapon.db.damage_high = rules.set_weapon_low_high(weapon.db.level)
        
        rules.set_disintegrate_timer(weapon)

        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        rules_skills.check_skill_improve(caster, "summon weapon", True, 1)

        caster.msg("You chant 'summon weapon'.\nYou pray to the Paladin gods and %s appears." % weapon.key)
        player_output_magic_chant(caster, "summon weapon")
        caster.location.msg_contents("%s prays to the Paladin gods and %s appears."
                                     % ((caster.key[0].upper() + caster.key[1:]),
                                        weapon.key),
                                     exclude=caster)

        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        rules_skills.check_skill_improve(caster, "summon weapon", False, 1)
        caster.msg("You chant 'summon weapon'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "summon weapon")


def do_ventriloquate(caster, mana_cost, target, sound):
    """ Function implementing ventriloquate spell"""

    spell = rules_skills.get_skill(skill_name="ventriloquate")
    level = caster.level

    if random.randint(1, 100) <= caster.db.skills["ventriloquate"] or "mobile" in caster.tags.all():
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
            rules_skills.check_skill_improve(caster, "ventriloquate", True, 1)
        caster.msg(
            "You chant 'ventriloquate'.\nYou make it appear that %s says '%s'." % ((target.key[0].upper() + target.key[1:]), sound))
        player_output_magic_chant(caster, "ventriloquate")
        for object in caster.location.contents:
            if object == target and object.db.position != "sleeping":
                object.msg("A sound seemingly emanates from you saying '%s'" % sound)
            elif ("player" in object.tags.all() or "mobile" in object.tags.all()) and object != caster and object.db.position != "sleeping":
                if save_spell(level, target):
                    object.msg("%s makes %s say '%s'" % ((caster.key[0].upper() + caster.key[1:]), target, sound))
                else:
                    object.msg("%s says '%s'" % ((target.key[0].upper() + target.key[1:]), sound))
        rules.wait_state_apply(caster, spell["wait state"])

    else:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
            rules_skills.check_skill_improve(caster, "ventriloquate", False, 1)
        caster.msg("You chant 'ventriloquate'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "ventriloquate")


def mana_cost(caster, spell):
    """Calculate mana cost for a spell"""

    minimum_cost = spell["minimum cost"]

    minimum_level = rules_skills.lowest_learned_level(spell)

    level_cost = int(120 / (2 + (caster.level - minimum_level) / 2))
    if level_cost > minimum_cost:
        return level_cost
    else:
        return minimum_cost


def player_output_magic_chant(caster, spell_name):
    """
    Sorts through players in a room where a spell is cast to determine
    which players can understand the casting, and which cannot. Gives
    output to players depending on which category they fall into.
    """

    in_room_players = []

    for object in caster.location.contents:
        if "player" in object.tags.all():
            in_room_players.append(object)

    magic_name = say_spell(spell_name)

    can_understand = []
    cannot_understand = []
    
    if in_room_players:
        for player in in_room_players:
            if player.db.skills[spell_name] and player != caster:
                can_understand.append(player)
            elif player != caster:
                cannot_understand.append(player)
    
    if can_understand:
        for player in can_understand:
            player.msg("%s chants '%s'.\n" % (caster.key, spell_name))
            
    if cannot_understand:
        for player in cannot_understand:
            player.msg("%s chants '%s'.\n" % (caster.key, magic_name))


def save_spell(cast_level, victim):
    """
    This function returns a boolean based on whether a spell is
    resisted/saved by a victim (True) or not (False)
    """
    
    base_save = 50
    if "mobile" in victim.tags.all():
        base_save += 25
    save = base_save + (victim.level - cast_level) * 2 - victim.saving_throw
    if save < 5:
        save = 5
    elif save > 95:
        save = 95
    
    if random.randint(1, 100) < save:
        return True
    else:
        return False


def say_spell(spell_name):
    """
    This function creates the magical gibberish that replaces the
    name of the spell when the listening player does not know the
    spell
    """
    
    magic_name = ""

    max_index = len(spell_name) - 1
    index = 0

    while index <= max_index:
        if spell_name[index] == "a":
            if index + 1 > max_index:
                magic_name += "a"
                index += 1
            else:
                if spell_name[index + 1] == "r":
                    magic_name += "abra"
                    index += 2
                elif spell_name[index + 1] == "u":
                    magic_name += "kada"
                    index += 2
                else:
                    magic_name += "a"
                    index += 1
        elif spell_name[index] == "b":
            if index + 3 > max_index:
                magic_name += "b"
                index += 1
            elif index + 5 > max_index:
                if spell_name[index + 1:index + 3] == "ur":
                    magic_name += "mosa"
                    index += 3
                else:
                    magic_name += "b"
                    index += 1
            else:
                if spell_name[index + 1:index + 5] == "less":
                    magic_name += "ylem"
                    index += 5
                elif spell_name[index + 1:index + 5] == "lind":
                    magic_name += "quas"
                    index += 5
                elif spell_name[index + 1:index + 3] == "ur":
                    magic_name += "mosa"
                    index += 3
                else:
                    magic_name += "b"
                    index += 1
        elif spell_name[index] == "c":
            if index + 1 > max_index:
                magic_name += "q"
                index += 1
            else:
                if spell_name[index + 1] == "u":
                    magic_name += "judi"
                    index += 2
                else:
                    magic_name += "q"
                    index += 1
        elif spell_name[index] == "d":
            if index + 1 > max_index:
                magic_name += "e"
                index += 1
            else:
                if spell_name[index + 1] == "e":
                    magic_name += "oculo"
                    index += 2
                else:
                    magic_name += "e"
                    index += 1
        elif spell_name[index] == "e":
            if index + 1 > max_index:
                magic_name += "z"
                index += 1
            else:
                if spell_name[index + 1] == "n":
                    magic_name += "unso"
                    index += 2
                else:
                    magic_name += "z"
                    index += 1
        elif spell_name[index] == "f":
            magic_name += "y"
            index += 1
        elif spell_name[index] == "g":
            magic_name += "o"
            index += 1
        elif spell_name[index] == "h":
            magic_name += "p"
            index += 1
        elif spell_name[index] == "i":
            magic_name += "u"
            index += 1
        elif spell_name[index] == "j":
            magic_name += "y"
            index += 1
        elif spell_name[index] == "k":
            magic_name += "t"
            index += 1
        elif spell_name[index] == "l":
            if index + 1 > max_index:
                magic_name += "r"
                index += 1
            elif index + 5 > max_index:
                if spell_name[index + 1] == "o":
                    magic_name += "hi"
                    index += 2
                else:
                    magic_name += "r"
                    index += 1
            else:
                if spell_name[index + 1:index + 5] == "ight":
                    magic_name += "dies"
                    index += 5
                elif spell_name[index + 1] == "o":
                    magic_name += "hi"
                    index += 2
                else:
                    magic_name += "r"
                    index += 1
        elif spell_name[index] == "m":
            if index + 1 > max_index:
                magic_name += "w"
                index += 1
            elif index + 4 > max_index:
                if spell_name[index + 1:index + 3] == "or":
                    magic_name += "zak"
                    index += 3
                else:
                    magic_name += "w"
                    index += 1
            else:
                if spell_name[index + 1:index + 3] == "or":
                    magic_name += "zak"
                    index += 3
                elif spell_name[index + 1:index + 4] == "ove":
                    magic_name += "sido"
                    index += 4
                else:
                    magic_name += "w"
                    index += 1
        elif spell_name[index] == "n":
            if index + 4 > max_index:
                magic_name += "i"
                index += 1
            else:
                if spell_name[index + 1:index + 4] == "ess":
                    magic_name += "lacri"
                    index += 4
                elif spell_name[index + 1:index + 4] == "ing":
                    magic_name += "illa"
                    index += 4
                else:
                    magic_name += "i"
                    index += 1
        elif spell_name[index] == "o":
            magic_name += "a"
            index += 1
        elif spell_name[index] == "p":
            if index + 3 > max_index:
                magic_name += "s"
                index += 1
            else:
                if spell_name[index + 1:index + 3] == "er":
                    magic_name += "duda"
                    index += 3
                else:
                    magic_name += "s"
                    index += 1
        elif spell_name[index] == "q":
            magic_name += "d"
            index += 1
        elif spell_name[index] == "r":
            if index + 1 > max_index:
                magic_name += "f"
                index += 1
            else:
                if spell_name[index + 1] == "a":
                    magic_name += "gru"
                    index += 2
                elif spell_name[index + 1] == "e":
                    magic_name += "candus"
                    index += 2
                else:
                    magic_name += "f"
                    index += 1
        elif spell_name[index] == "s":
            if index + 3 > max_index:
                magic_name += "g"
                index += 1
            else:
                if spell_name[index + 1:index + 3] == "on":
                    magic_name += "sabru"
                    index += 3
                else:
                    magic_name += "g"
                    index += 1
        elif spell_name[index] == "t":
            if index + 4 > max_index:
                magic_name += "f"
                index += 1
            elif index + 5 > max_index:
                if spell_name[index + 1:index + 4] == "ect":
                    magic_name += "infra"
                    index += 4
                else:
                    magic_name += "f"
                    index += 1
            else:
                if spell_name[index + 1:index + 4] == "ect":
                    magic_name += "infra"
                    index += 4
                elif spell_name[index + 1:index + 5] == "ri":
                    magic_name += "cula"
                    index += 3
                else:
                    magic_name += "f"
                    index += 1
        elif spell_name[index] == "u":
            magic_name += "j"
            index += 1
        elif spell_name[index] == "v":
            if index + 3 > max_index:
                magic_name += "z"
                index += 1
            else:
                if spell_name[index + 1:index + 3] == "en":
                    magic_name += "nofo"
                    index += 3
                else:
                    magic_name += "z"
                    index += 1
        elif spell_name[index] == "w":
            magic_name += "x"
            index += 1
        elif spell_name[index] == "x":
            magic_name += "n"
            index += 1
        elif spell_name[index] == "y":
            magic_name += "l"
            index += 1
        elif spell_name[index] == "z":
            magic_name += "k"
            index += 1
        elif spell_name[index] == " ":
            magic_name += " "
            index += 1
        else:
            magic_name += "fred"
            index += 1

    return magic_name
