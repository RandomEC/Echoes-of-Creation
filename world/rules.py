import random

def fuzz_number(number):
    """
    This function simply adds slight variation to a number.
    """
    
    random_number = random.randint(1, 4)
    if random_number < 2:
        return number - 1
    elif random_number >3:
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
        if ("breath_any" or "cast_psionicist" or "cast_undead" or "breath_gas" or "cast_mage") in mobile.db.special_function:
            experience *= 1.33

        elif ("breath_fire" or "breath_frost" or "breath_acid" or "breath_lightning" or "cast_cleric" or "cast_judge" or "cast_ghost") in mobile.db.special_function:
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
    This method handles the passive regaining of hitpoints when
    injured.
    """

    if "mobile" in self.tags.all():
        hp_gain = character.db.level * 3 / 2
    else:
        if self.db.level < 5:
            hp_gain = character.db.level
        else:
            hp_gain = 5

        if character.db.position == "sleeping":
            hp_gain += self.constitution * 2
        elif character.db.position == "resting":
            hp_gain += self.constitution

        # Hitpoint gain is impacted by thirst and hunger. If you are full,
        # you get a bonus to gain. If you are starving and parched, you
        # get no benefit. Sliding scale between.

        # hunger_modifier = character.db.hunger/20
        # thirst_modifier = character.db.thirst/20
        # total_food_modifier = 1 + hunger_modifier + thirst_modifier

        # hp_gain *= total_food_modifier

        # Need to accommodate furniture, poisoning, and
        # enhanced healing in here once coded.

    if rules_race.get_race(character)["heal modifier"]:
        hp_gain += rules_race.get_race(character)["heal modifier"]

    hp_gain = int(hp_gain)

    if hp_gain > character.db.hitpoints["damaged"]:
        character.db.hitpoints["damaged"] = 0
    else:
        character.db.hitpoints["damaged"] -= hp_gain
