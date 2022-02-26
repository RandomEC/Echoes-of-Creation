import random
import math
from world import rules_race


def fuzz_number(number):
    """
    This function simply adds slight variation to a number.
    """

    random_number = random.randint(1, 4)
    if random_number < 2:
        return number - 1
    elif random_number > 3:
        return number + 1
    else:
        return number


def set_armor(level):
    """
    This function sets the armor value of a piece of armor.
    """

    return round(fuzz_number((level/4) + 2))


def set_weapon_low_high(level):
    """
    This function sets the damage range of a weapon.
    """

    low = round(fuzz_number(fuzz_number(level/4 + 2)))
    high = round(fuzz_number(fuzz_number(3*level/4 + 6)))
    return low, high


def calculate_experience(mobile):
    """
    This function calculates the total experience awarded for
    killing a mobile. This experience is later modified in
    actual combat for bonuses dependent upon the attacker
    (racial hatred, alignment).
    """
    level_xp = mobile.db.level * mobile.db.level * mobile.db.level * 5
    hp_xp = mobile.hitpoints_maximum
    ac_xp = (mobile.armor_class - 50) * 2
    damage_xp = ((3 * mobile.db.level / 4) + mobile.damroll) * 50
    hitroll_xp = mobile.hitroll * mobile.db.level * 10

    experience = level_xp + hp_xp - ac_xp + damage_xp + hitroll_xp

    if mobile.get_affect_status("sanctuary"):
        experience *= 1.5

    if mobile.get_affect_status("flameshield"):
        experience *= 1.4

    if mobile.db.eq_slots["wielded, primary"]:
        experience *= 1.25

    if mobile.db.eq_slots["wielded, secondary"]:
        experience *= 1.2

    if mobile.db.special_function:
        if ("breath_any" or "cast_psionicist" or "cast_undead" or
                "breath_gas" or "cast_mage") in mobile.db.special_function:
            experience *= 1.33

        elif ("breath_fire" or "breath_frost" or "breath_acid" or
                "breath_lightning" or "cast_cleric" or "cast_judge" or
                "cast_ghost") in mobile.db.special_function:
            experience *= 1.2

        elif ("poison" or "thief") in mobile.db.special_function:
            experience *= 1.05

        elif "cast_adept" in mobile.db.special_function:
            experience *= 0.5

    # Finally, randomize slightly, and check for a floor of 50.
    experience = int(random.uniform(0.9, 1.1) * experience)
    if experience < 50:
        experience = 50

    return experience


def gain_hitpoints(character):
    """
    This method calculates the amount of passive hitpoint gain,
    and returns that number.
    """

    if "mobile" in character.tags.all():
        hp_gain = character.db.level * 3 / 2
        character.location.msg_contents("In hp_gain = %d" % hp_gain)
    else:
        if character.db.level < 5:
            hp_gain = character.db.level

        else:
            hp_gain = 5

        if character.db.position == "sleeping":
            hp_gain += character.constitution * 2
        elif character.db.position == "resting":
            hp_gain += character.constitution

        # Hitpoint gain is impacted by thirst and hunger. If you are full,
        # you get a bonus to gain. If you are starving and parched, you
        # get no benefit. Sliding scale between.

        hunger_modifier = character.db.hunger/16000
        thirst_modifier = character.db.thirst/16000
        total_food_modifier = 1 + hunger_modifier + thirst_modifier

        hp_gain *= total_food_modifier

        # Need to accommodate furniture, poisoning, and
        # enhanced healing in here once coded.

    if "heal modifier" in rules_race.get_race(character.race):
        hp_gain += rules_race.get_race(character.race)["heal modifier"]

    hp_gain = int(hp_gain)

    character.location.msg_contents("End hp_gain")

    if hp_gain > character.db.hitpoints["damaged"]:
        return character.db.hitpoints["damaged"]
    else:
        return hp_gain


def gain_mana(character):
    """
    This method calculates the amount of passive mana gain,
    and returns that number.
    """

    if "mobile" in character.tags.all():
        mana_gain = character.db.level
        character.location.msg_contents("In mana_gain")

    else:
        if character.db.level < 5:
            mana_gain = math.ceil(character.db.level / 2)
        else:
            mana_gain = 5

        if character.db.position == "sleeping":
            mana_gain += character.intelligence * 2
        elif character.db.position == "resting":
            mana_gain += character.intelligence

        # Mana gain is impacted by thirst and hunger. If you are full,
        # you get a bonus to gain. If you are starving and parched, you
        # get no benefit. Sliding scale between.

        hunger_modifier = character.db.hunger/16000
        thirst_modifier = character.db.thirst/16000
        total_food_modifier = 1 + hunger_modifier + thirst_modifier

        mana_gain *= total_food_modifier

        # If drunk, you get a further bonus
        if character.db.drunk > 0:
            mana_gain *= 2

        # Need to accommodate furniture, poisoning, and
        # enhanced healing in here once coded.

    if "mana modifier" in rules_race.get_race(character.race):
        mana_gain += character.db.level * \
            rules_race.get_race(character.race)["mana modifier"]

    mana_gain = int(mana_gain)

    character.location.msg_contents("End mana_gain")

    if mana_gain > character.db.mana["spent"]:
        return character.db.mana["spent"]
    else:
        return mana_gain


def gain_moves(character):
    """
    This method calculates the amount of passive moves gain,
    and returns that number.
    """

    if "mobile" in character.tags.all():
        moves_gain = character.db.level
        character.location.msg_contents("In moves_gain")

    else:
        if (character.db.level * 2) > 15:
            moves_gain = character.db.level * 2
        else:
            moves_gain = 15

        if character.db.position == "sleeping":
            moves_gain += character.dexterity * 2
        elif character.db.position == "resting":
            moves_gain += character.dexterity

        # Mana gain is impacted by thirst and hunger. If you are full,
        # you get a bonus to gain. If you are starving and parched, you
        # get no benefit. Sliding scale between.

        hunger_modifier = character.db.hunger/16000
        thirst_modifier = character.db.thirst/16000
        total_food_modifier = 1 + hunger_modifier + thirst_modifier

        moves_gain *= total_food_modifier

        # Need to accommodate furniture, poisoning, and
        # enhanced healing in here once coded.

    if "moves modifier" in rules_race.get_race(character.race):
        moves_gain += character.db.level * \
            rules_race.get_race(character.race)["moves modifier"]

    moves_gain = int(moves_gain)
    character.location.msg_contents("End moves_gain")

    if moves_gain > character.db.moves["spent"]:
        return character.db.moves["spent"]
    else:
        return moves_gain


def gain_experience(mobile, hp_gain):
    """
    This function calculates the amount of experience that
    needs to be regained by a mobile to accommodate its
    hit point gain.
    """

    mobile.location.msg_contents("In xp_gain")

    percent_hp_recovered = hp_gain / mobile.db.hitpoints["damaged"]
    experience_awarded = math.ceil(mobile.db.experience_total -
                                   mobile.db.experience_current)

    experience_gain = int(percent_hp_recovered * experience_awarded)
    mobile.location.msg_contents("End xp_gain")

    return experience_gain
