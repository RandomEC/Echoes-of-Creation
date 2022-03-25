import math
import random
import time
from server.conf import settings
from world import rules_race
from evennia import TICKER_HANDLER as tickerhandler
from evennia.utils import search

def affect_remove(character, affect_name, target_message, room_message):
    """
    This function removes the spell a character is affected by
    from their affects dictionary.
    """
    
    del character.db.spell_affects[affect_name]
    character.msg(target_message)
    character.location.msg_contents(room_message, exclude=character)

def attributes_cost(character):
    """
    This function determines the experience cost of getting an
    additional attribute (e.g. strength, dexterity, etc.) bonus.
    The formula for this has to be calculated from the next four
    xp steps.
    """
    
    cost = current_experience_step(character, 0)
    cost += current_experience_step(character, 1)
    cost += current_experience_step(character, 2)
    cost += current_experience_step(character, 3)    

    return cost


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

def can_see(target, looker):
    """
    This function checks to see (heh) if a target is visible to
    a looker, and returns a boolean of True if the looker can
    see the target, and False if not.
    """
    
    if looker.get_affect_status("blind"):
        return False
    elif target.get_affect_status("hide") and not looker.get_affect_status("detect hidden"):
        return False
    elif target.get_affect_status("invisible") and not looker.get_affect_status("detect invis"):
        return False


def check_ready_to_level(character):
    """
    This function checks if a character has grown sufficiently
    to level up. Characters may level, at fastest, on every
    sixth train. Attribute gains count as four.
    """
    
    step = (character.level +
            character.db.hitpoints["trains spent"] +
            character.db.mana["trains spent"] +
            character.db.moves["trains spent"] +
            (character.db.attribute_trains["strength"] * 4) +
            (character.db.attribute_trains["intelligence"] * 4) +
            (character.db.attribute_trains["wisdom"] * 4) +
            (character.db.attribute_trains["dexterity"] * 4) +
            (character.db.attribute_trains["constitution"] * 4) +
            int(character.db.practices_spent))
    
    if step >= ((character.level - 1) * 6) + 5:
        return True
    else:
        return False
    

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
    
    
def current_experience_step(character, extra_step):
    """
    This function uses a character's current total trains and
    practices spent to determine the experience step that the
    character is currently at.
    """

    step = (character.level +
            character.db.hitpoints["trains spent"] +
            character.db.mana["trains spent"] +
            character.db.moves["trains spent"] +
            (character.db.attribute_trains["strength"] * 4) +
            (character.db.attribute_trains["intelligence"] * 4) +
            (character.db.attribute_trains["wisdom"] * 4) +
            (character.db.attribute_trains["dexterity"] * 4) +
            (character.db.attribute_trains["constitution"] * 4) +
            int(character.db.practices_spent) +
            extra_step)
    
    experience_cost = int(((1 + (step/8.303)) ** 3) * 176.889)
    
    return experience_cost


def experience_loss_base(character):
    """
    This function calculates the experience that fleeing, death,
    and the like use to calculate proportional loss from.
    """
    
    loss = (current_experience_step(character, -1) +
            current_experience_step(character, -2) +
            current_experience_step(character, -3) +
            current_experience_step(character, -4) +
            current_experience_step(character, -5)
            )
    
    return loss


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

    hp_gain = math.ceil(hp_gain)

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

    mana_gain = math.ceil(mana_gain)

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

    moves_gain = math.ceil(moves_gain)

    if moves_gain > character.db.moves["spent"]:
        return character.db.moves["spent"]
    else:
        return moves_gain


def hitpoints_cost(character):
    """
    This function determines the experience cost of getting an
    additional amount of hitpoints.
    """
    return current_experience_step(character, 0)


def intelligence_learn_rating(character):
    """
    This function returns the learn rating of a character
    based on their intelligence.
    """
    int = character.intelligence
    
    if int == 0:
        return 3
    elif int == 1:
        return 5
    elif int == 2:
        return 7
    elif int == 3:
        return 8
    elif int == 4:
        return 9
    elif int == 5:
        return 10
    elif int == 6:
        return 11
    elif int == 7:
        return 12
    elif int == 8:
        return 13
    elif int == 9:
        return 15
    elif int == 10:
        return 17
    elif int == 11:
        return 19
    elif int == 12:
        return 22
    elif int == 13:
        return 25
    elif int == 14:
        return 28
    elif int == 15:
        return 31
    elif int == 16:
        return 34
    elif int == 17:
        return 37
    elif int == 18:
        return 40
    elif int == 19:
        return 44
    elif int == 20:
        return 49
    elif int == 21:
        return 55
    elif int == 22:
        return 60
    elif int == 23:
        return 70
    elif int == 24:
        return 85
    else:
        return 90

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

def is_visible_character(target, looker):
    """
    This function returns a boolean as to whether one character
    is visible to another currently.
    """
    if looker.get_affect_status("blind"):
        return False
    if target.get_affect_status("hide") and not looker.get_affect_status("detect hidden"):
        return False
    if target.get_affect_status("invisible") and not looker.get_affect_status("detect invis"):
        return False
    if "act_flags" in target.db.all:
        if "total invis" in target.db.act_flags:
            return False
    
    return True
    
def level_cost(character):
    """
    This function determines the experience cost of increasing a
    character one level.
    """
    
    return current_experience_step(character, 0)


def make_object(location, equipped, reset_object):
    new_object = ""

    # First, search for all objects of that type and pull out
    # any that are at "None".
    object_candidates = search.search_object(reset_object)

    for object in object_candidates:
        if not object.location:
            new_object = object

    # If it is not in "None", find the existing object in the world
    # and copy it.
    if not new_object:

        object_to_copy = object_candidates[0]
        new_object = object_to_copy.copy()
        new_object.key = object_to_copy.key
        new_object.alias = object_to_copy.aliases
        if new_object.db.equipped:
            new_object.db.equipped = False
        new_object.home = location

    # Either way, put it where it should be.
    new_object.location = location

    # Clear any enchantment/poison/other affects.
    new_object.db.spell_affects = {}

    # Set level, other values, and/or fuzz numbers as necessary
    new_object.db.level = 1
    if new_object.db.item_type == "armor":
        new_object.db.armor = set_armor(new_object.db.level)
    elif new_object.db.item_type == "weapon":
        new_object.db.damage_low, new_object.db.damage_high = set_weapon_low_high(new_object.db.level)
    elif new_object.db.item_type == "scroll":
        new_object.db.spell_level = fuzz_number(new_object.db.spell_level_base)
    elif new_object.db.item_type == "wand" or new_object.db.item_type == "staff":
        new_object.db.spell_level = fuzz_number(new_object.db.spell_level_base)
        new_object.db.charges_maximum = fuzz_number(new_object.db.charges_maximum_base)
        new_object.db.charges_current = new_object.db.charges_maximum
    elif new_object.db.item_type == "potion" or new_object.db.item_type == "pill":
        new_object.db.spell_level = fuzz_number(fuzz_number(new_object.db.spell_level_base))

    # If it should be equipped, equip it.
    if equipped:
        if not new_object.db.equipped:
            if new_object.db.item_type == "weapon":
                new_object.wield_to(location)
            else:
                new_object.wear_to(location)

    return new_object


def mana_cost(character):
    """
    This function determines the experience cost of getting an
    additional amount of mana.
    """
    return current_experience_step(character, 0)


def moves_cost(character):
    """
    This function determines the experience cost of getting an
    additional amount of moves.
    """
    return current_experience_step(character, 0)


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


def set_armor(level):
    """
    This function sets the armor value of a piece of armor.
    """

    return round(fuzz_number((level/4) + 2))


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


def set_weapon_low_high(level):
    """
    This function sets the damage range of a weapon.
    """

    low = round(fuzz_number(fuzz_number(level/4 + 2)))
    high = round(fuzz_number(fuzz_number(3*level/4 + 6)))
    return low, high


def wait_state_apply(character, wait_state):
    """
    This function takes a character and applies an ndb attribute
    of wait_state, which is a Unix-type time that can be used
    to determine how much longer the wait state will last, if
    needed. The function also creates a delay to call the
    function to eliminate the wait state once it has run.
    """
    
    wait_state_time = int(time.time() + wait_state)
    
    character.ndb.wait_state = wait_state_time
    
    def wait_state_remove():
        """
        This gets called to remove the wait state after it has run.
        """
        character.ndb.wait_state = 0
        prompt_wait = "|gReady!|n"
        prompt = "<|r%d|n/|R%d hp |b%d|n/|B%d mana |y%d|n/|Y%d moves|n %s>\n" % (caller.hitpoints_current,
                                                                                  caller.hitpoints_maximum,
                                                                                  caller.mana_current,
                                                                                  caller.mana_maximum,
                                                                                  caller.moves_current,
                                                                                  caller.moves_maximum,
                                                                                  prompt_wait)
        character.msg(prompt = prompt)
    
    wait_state_return = utils.delay(wait_state, wait_state_remove)

    character.ndb.wait_state_return = wait_state_return


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
        
def wisdom_practices(character):
    """
    This function returns the amount of practice sessions
    that a character receives per experience step based
    on wisdom.
    """
    wis = character.wisdom
    
    if wis < 5:
        return 0
    elif wis < 9:
        return 1
    elif wis < 15:
        return 2
    elif wis < 17:
        return 3
    elif wis < 19:
        return 4
    elif wis < 21:
        return 5
    elif wis < 22:
        return 6
    elif wis < 25:
        return 7
    else:
        return 8
        
