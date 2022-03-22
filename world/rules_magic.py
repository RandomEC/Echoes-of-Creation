import random
from evennia.utils import search
from world import rules, rules_skills

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
    
def do_create_food(caster, mana_cost):
    """ Function implementing create food spell"""
    
    spell = rules_skills.get_skill(skill_name="create food")

    level = caster.level - rules_skills.lowest_learned_level(spell)

    if random.randint(1, 100) > caster.db.skills["create food"]:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        caster.msg("You chant 'create food'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "create food")
    else:
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
        caster.msg("You chant 'create food'.\n%s suddenly appears." % (food.key[0].upper() + food.key[1:]))
        player_output_magic_chant(caster, "create food")
        caster.location.msg_contents("%s suddenly appears."
                                     % (food.key[0].upper() + food.key[1:]),
                                     exclude=caster)


def do_create_sound(caster, mana_cost, target, sound):
    """ Function implementing create sound spell"""

    spell = rules_skills.get_skill(skill_name="create sound")
    level = caster.level - rules_skills.lowest_learned_level(spell)

    if random.randint(1, 100) > caster.db.skills["create sound"]:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        caster.msg("You chant 'create sound'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "create sound")
    else:
        if "player" in caster.tags.all():
            caster.mana_spent += mana_cost
        caster.msg(
            "You chant 'create sound'.\n%s says '%s'." % ((target.key[0].upper() + target.key[1:]), sound))
        player_output_magic_chant(caster, "create sound")
        for object in caster.location.contents:
            if object == target and object.db.position != "sleeping":
                object.msg("A sound seemingly emanates from you saying '%s'" % sound)
            elif ("player" in object.tags.all() or "mobile" in object.tags.all()) and object != caster and object.db.position != "sleeping":
                if save_spell(level, target):
                    object.msg("%s makes %s say '%s'" % ((caster.key[0].upper() + caster.key[1:]), target, sound))
                else:
                    object.msg("%s says '%s'" % ((target.key[0].upper() + target.key[1:]), sound))

def do_create_water(caster, mana_cost, target_container):
    """ Function implementing create water spell"""
    
    spell = rules_skills.get_skill(skill_name="create water")
    level = caster.level - rules_skills.lowest_learned_level(spell)

    if random.randint(1, 100) > caster.db.skills["create water"]:
        if "player" in caster.tags.all():
            caster.mana_spent += int(mana_cost / 2)
        caster.msg("You chant 'create water'.\nYou lost your concentration.\n")
        player_output_magic_chant(caster, "create water")            
    else:
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
        caster.msg("You chant 'create water'.\n%s is filled." % (target_container.key[0].upper() + target_container.key[1:]))
        player_output_magic_chant(caster, "create water")
    
            
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
