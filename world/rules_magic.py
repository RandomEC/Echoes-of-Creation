import random
from evennia.utils import search

def check_cast(caster):
    """
    This function is used to check for any player or room-based
    state effects that would prevent casting.
    """
    
    if "cone of silence" in caster.location.db.room_flags:
        return "You can't ... You are in a Cone of Silence!"
    
    elif "no magic" in caster.location.db.room_flags:
        return "You feel a strong dampening field blocking your spell."
    
    elif caster.get_affect_status("mute"):
        return False

    return
    
def do_create_food(caster, mana_cost):
    cast_name = say_spell("create food")

    if caster.ndb.combat_handler:
        pass
    else:
        if random.randint(1, 100) > caster.db.skills["create food"]:
            caster.msg("You chant 'create food'.\nYou fail to cast create food.")

            # Make a method that iterates through players in the room and dictates
            # whether they get the gibberish or the actual name based on whether
            # they have the skill.
            caster.location.msg_contents("%s chants %s."
                                         % (caster.name, cast_name),
                                         exclude=caster)

            caster.mana_spent += mana_cost / 2
            return

def mana_cost(caster, spell):
    """Calculate mana cost for a spell"""

    minimum_cost = spell["minimum cost"]

    minimum_level = 101
    for class_name in spell["classes"]:
        if spell["classes"][class_name] < minimum_level:
            minimum_level = spell["classes"][class_name]

    level_cost = 120 / (2 + (caster.level - minimum_level) / 2)

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
    
    players = search.search_object_by_tag("player")
    in_room_players = caster.search(candidates=players, location=caster.location)
    
    can_understand = []
    cannot_understand = []
    
    for player in in_room_players:
        if player.db.skills[spell_name] and player != caster:
            can_understand.append(player)
        else:
            cannot_understand.append(player)
    
    if can_understand:
        for player in can_understand:
            player.msg("%s chants '%s'.\n" % (caster.key, spell_name))
            
    if cannot_understand
        for player in cannot_understand:
            player.msg("%s chants '%s'.\n" % (caster.key, magic_name))
        
    
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
            if spell_name[index + 1] == "u":
                magic_name += "judi"
                index += 2
            else:
                magic_name += "q"
                index += 1
        elif spell_name[index] == "d":
            if spell_name[index + 1] == "e":
                magic_name += "oculo"
                index += 2
            else:
                magic_name += "e"
                index += 1
        elif spell_name[index] == "e":
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
            if spell_name[index + 1:index + 3] == "on":
                magic_name += "sabru"
                index += 3
            else:
                magic_name += "g"
                index += 1
        elif spell_name[index] == "t":
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

    return magic_name
