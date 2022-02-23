from random import randint

def fuzz_number(number):
    random_number = randint(1, 4)
    if random_number < 2:
        return number - 1
    elif random_number >3:
        return number + 1
    else:
        return number

def set_armor(level):
    return round(fuzz_number((level/4) + 2))

def set_weapon_low_high(level):
    low = round(fuzz_number(fuzz_number(level/4 + 2)))
    high = round(fuzz_number(fuzz_number(3*level/4 + 6)))
    return low, high

def calculate_experience(mobile):
    level_xp = mobile.db.level * mobile.db.level * mobile.db.level * 5
    hp_xp = mobile.hitpoints_maximum
    ac_xp = (mobile.armor_class - 50) * 2
    if mobile.db.eq_slots["wielded, primary"]:
        weapon_mod = 1.5
    else:
        weapon_mod = 1
    damage_xp = ((weapon_mod * 3 * mobile.db.level / 4) + mobile.damroll) * 50
    hitroll_xp = mobile.hitroll * mobile.db.level * 10

    experience = level_xp + hp_xp - ac_xp + damage_xp + hitroll_xp

    if mobile.get_affect_status("sanctuary"):

        experience += experience*1.5

    if mobile.get_affect_status("flameshield"):

        experience += experience*1.2

    return experience