import random
import math
from server.conf import settings
from world import rules_race
from evennia import TICKER_HANDLER as tickerhandler

def classes_current(character):
    """
    This function will eventually evaluate all the skills that
    a character has learned and compare them to the character's
    level to determine what their most-used class (or classes,
    at higher levels) is. For now just returns default.
    """
    
    return ["default"]

def constitution_hitpoint_bonus(character):
    """
    This function returns the amount of bonus hitpoints that a
    character receives on gaining another set of hitpoints.
    """
    con = character.constitution
    
    if con == 0:
        return -4
    elif con == 1:
        return -3
    elif con < 4:
        return -2
    elif con < 7:
        return -1
    elif con < 15:
        return 0
    elif con < 16:
        return 1
    elif con < 18:
        return 2
    elif con < 20:
        return 3
    elif con < 22:
        return 4
    elif con < 23:
        return 5
    elif con < 24:
        return 6
    elif con < 25:
        return 7
    else:
        return 8 
    
    
def intelligence_mana_bonus(character):
    """
    This function returns the amount of bonus mana that a
    character receives on gaining another set of mana based
    on intelligence.
    """
    int = character.intelligence
    
    if int < 16:
        return 0
    elif int < 20:
        return 1
    elif int < 22:
        return 2
    elif int < 24:
        return 3
    elif int < 25:
        return 4
    else:
        return 5 
    
def wisdom_mana_bonus(character):
    """
    This function returns the amount of bonus mana that a
    character receives on gaining another set of mana based
    on wisdom.
    """
    wis = character.wisdom
    
    if wis < 10:
        return 0
    elif wis < 22:
        return 1
    elif wis < 23:
        return 2
    elif wis < 24:
        return 3
    elif wis < 25:
        return 4
    else:
        return 5
        

def remove_disintegrate_timer(obj):
    """
    This function removes the timer that comes from dropping an
    object.
    """

    if "pc corpse" in obj.tags.all() and "disintegrating" in obj.tags.all():
        tickerhandler.remove(settings.PC_CORPSE_DISINTEGRATE_TIME, obj.at_disintegrate)
        obj.tags.remove("disintegrating")
    elif "disintegrating" in obj.tags.all():
        tickerhandler.remove(settings.DEFAULT_DISINTEGRATE_TIME, obj.at_disintegrate)
        obj.tags.remove("disintegrating")


def set_disintegrate_timer(obj):
    """
    This function sets the timer that comes from dropping an
    object.
    """

    if "pc corpse" in obj.tags.all():
        tickerhandler.set(settings.PC_CORPSE_DISINTEGRATE_TIME, obj.at_disintegrate)
        obj.tags.add("disintegrating")
    else:
        tickerhandler.add(settings.DEFAULT_DISINTEGRATE_TIME, obj.at_disintegrate)
        obj.tags.add("disintegrating")


def experience_cost_base(step):
    """
    This function determines the base experience cost for a step
    of experience, which is then split by other functions to get
    the cost of a level, hitpoint gain, etc.
    """
    
    if step == 2:
        return settings.EXPERIENCE_STEP_TWO
    else:
        return ((step ** settings.EXPERIENCE_STEP_EXPONENT) * settings.EXPERIENCE_STEP_MULTIPLIER)

def current_experience_step(character):
    """
    This function uses a character's current total experience to
    determine the experience step that the character is currently
    at.
    """

    step = 1
    step_experience_total = 0
    while character.db.experience_total <= step_experience_total:
        step += 1
        if step == 2:
            step_experience_total += 2700
        else:
            step_experience_total += experience_cost_base(step)

    # Since the above calculated one step past, reduce step by one.
    step -= 1

    return step


def level_cost(level):
    """
    This function determines the experience cost of increasing a
    character one level.
    """
    
    return int(settings.ECHOES_COST_LEVEL * experience_cost_base(level))


def hitpoints_cost(character):
    """
    This function determines the experience cost of getting an
    additional amount of hitpoints.
    """
    hitpoints_step = character.db.hitpoints["trains spent"] + 2
    return int(settings.ECHOES_COST_HITPOINTS * experience_cost_base(hitpoints_step))


def mana_cost(character):
    """
    This function determines the experience cost of getting an
    additional amount of mana.
    """
    mana_step = character.db.mana["trains spent"] + 2
    return int(settings.ECHOES_COST_MANA * experience_cost_base(mana_step))


def moves_cost(character):
    """
    This function determines the experience cost of getting an
    additional amount of moves.
    """
    moves_step = character.db.moves["trains spent"] + 2
    return int(settings.ECHOES_COST_MOVES * experience_cost_base(moves_step))


def attributes_cost(character):
    """
    This function determines the experience cost of getting an
    additional attribute (e.g. strength, dexterity, etc.) bonus.
    The formula for this has to be calculated from the total xp
    available for attributes, which may change.
    """
    
    attributes_step = 1
    for attribute in character.db.attribute_trains:
        attributes_step += character.db.attribute_trains[attribute]
    
    # Calculate the amount of xp allocated to getting attributes.
    attribute_total_xp = 0
    for step in range(2, 102):
        attribute_total_xp += int((experience_cost_base(step) * settings.ECHOES_COST_ATTRIBUTES))

    denominator = 0

    for upgrade in range(1, settings.ATTRIBUTES_TOTAL_UPGRADES + 1):
        denominator += (upgrade ** settings.ATTRIBUTES_EXPONENT)

    attribute_factor = int(attribute_total_xp / denominator)
    
    return int(attributes_step ** settings.ATTRIBUTES_EXPONENT * attribute_factor)


def practices_cost(character):
    """
    This function determines current cost of practicing a skill,
    based on the character's wisdom, and the amount of experience
    already spent on practicing skills.
    """
    
    # The cost of practicing is going to be divided by a factor,
    # based on character wisdom.
    if character.wisdom <= 4:
        practice_factor = 0
    elif character.wisdom <= 8:
        practice_factor = 1
    elif character.wisdom <= 14:
        practice_factor = 2
    elif character.wisdom <= 16:
        practice_factor = 3
    elif character.wisdom <= 18:
        practice_factor = 4
    elif character.wisdom <= 20:
        practice_factor = 5
    elif character.wisdom <= 21:
        practice_factor = 6
    elif character.wisdom <= 24:
        practice_factor = 7
    else:
        practice_factor = 8
    
    # Calculate the first step that costs more accumulated experience
    # spent practicing than the character has.
    
    step = 1
    step_experience_total = 0
    while character.db.experience_spent_practices <= step_experience_total:
        step += 1
        if step == 2:
            step_experience_total += 2700 * settings.ECHOES_COST_PRACTICES
        else:
            step_experience_total += experience_cost_base(step) * settings.ECHOES_COST_PRACTICES
            
    # Since the above calculated one step past, reduce step by one.
    step -= 1
    
    return experience_cost_base(step) * settings.ECHOES_COST_PRACTICES / practice_factor
    
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

    percent_hp_recovered = hp_gain / mobile.db.hitpoints["damaged"]
    experience_awarded = math.ceil(mobile.db.experience_total -
                                   mobile.db.experience_current)

    experience_gain = int(percent_hp_recovered * experience_awarded)

    return experience_gain
