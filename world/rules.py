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
