"""
This rules file is to handle anything related to non-combat skills.
"""

import math
import random
import time
from evennia import TICKER_HANDLER as tickerhandler
from server.conf import settings
from world import rules, rules_combat

def do_bash_door(character, target):
    """
    This is the function that does the actual mechanics of
    bashing a door.
    """
    skill = get_skill(skill_name="bash door")

    if target.key == "up" or target.key == "down":
        target_string = "door %s" % target.key
    else:
        target_string = "%s door" % target.key

    if not target.access(character, "bash"):
        character.msg("WHAAAAM!!!  You bash against the %s, but it doesn't budge. That HURT!" % target_string)
        
        # Deal with invisible characters for output.
        # Assemble a list of all possible lookers.
        lookers = list(cont for cont in character.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
        for looker in lookers:
            # Exclude the caller, who got their output above.
            if looker != character:
                basher_string = rules.get_visible_output(character, looker)
                looker.msg("WHAAAAM!!! %s bashes against the %s, but it holds strong." % ((basher_string[0].upper() + basher_string[1:]), target_string))
        return
    
        rules.do_damage_noncombat(character,
                                  "Your",
                                  (character.key + "'s"),
                                  (character.hitpoints_maximum / 5),
                                  "powerful bash"
                                  )                                  
                                  
        check_skill_improve(character, "bash door", False, 3)
    else:

        if "player" in character.tags.all():
            chance = character.db.skills["bash door"] / 2
        # As of right now, mobiles can't bash doors.
        else:
            chance = 0

        if "locked" in target.db.door_attributes:
            chance /= 2

        # Successful door bash.
        if character.strength >= 20 and random.randint(1, 100) < (chance + 4 * (character.strength - 20)):

            # Modify door attributes as needed to be open, not locked and not closeable.
            if "locked" in target.db.door_attributes:
                target.db.door_attributes.remove("locked")
            if "closeable" in target.db.door_attributes:
                target.db.door_attributes.remove("closeable")
            if "open" not in target.db.door_attributes:
                target.db.door_attributes.append("open")

            rules.do_damage_noncombat(character,
                                      "Your",
                                      (character.key + "'s"),
                                      (character.hitpoints_maximum / 20),
                                      "powerful bash"
                                      )                                  

            check_skill_improve(character, "bash door", True, 3)

            rules.wait_state_apply(character, skill["wait state"])
            
            # Handle output in the character's room.
            character.msg("Crash! You bashed open the the %s!" % target_string)

            # Deal with invisible characters for output.
            # Assemble a list of all possible lookers.
            lookers = list(cont for cont in character.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
            for looker in lookers:
                # Exclude the caller, who got their output above.
                if looker != character:
                    basher_string = rules.get_visible_output(character, looker)
                    looker.msg("%s bashes open the %s." % ((character_string[0].upper() + character_string[1:]), target_string))

            # Fetch the exit in the opposite direction from the destination room.
            if target.key == "north":
                opposite_direction = "south"
            elif target.key == "east":
                opposite_direction = "west"
            elif target.key == "south":
                opposite_direction = "north"
            elif target.key == "west":
                opposite_direction = "east"
            elif target.key == "up":
                opposite_direction = "down"
            elif target.key == "down":
                opposite_direction = "up"
            else:
                opposite_direction = door.key

            opposite_door = character.search(opposite_direction,
                                             location=target.destination)

            # Build output string for opposite door.
            if opposite_door.key == "north" or opposite_door.key == "east" or opposite_door.key == "south" \
                    or opposite_door.key == "west":
                opposite_door_string = ("door to the %s" % opposite_door.key)
            elif opposite_door.key == "up" or opposite_door.key == "down":
                opposite_door_string = ("door %s" % opposite_door.key)
            else:
                opposite_door_string = ("%s" % opposite_door.key)

            # Modify opposite door attributes as above.
            if "locked" in opposite_door.db.door_attributes:
                target.db.door_attributes.remove("locked")
            if "closeable" in opposite_door.db.door_attributes:
                target.db.door_attributes.remove("closeable")
            if "open" not in opposite_door.db.door_attributes:
                target.db.door_attributes.append("open")

            # Handle output in the opposite room.
            target.destination.contents.msg("The %s crashes open!" % opposite_door_string)

        # Unsuccessful door bash.
        else:

            rules.do_damage_noncombat(character,
                                      "Your",
                                      (character.key + "'s"),
                                      (character.hitpoints_maximum / 10),
                                      "powerful bash"
                                      )                                  

            check_skill_improve(character, "bash door", False, 3)

            # Handle output in the character's room.
            character.msg("OW! You bash against the %s, but it doesn't budge." % target_string)

            # Deal with invisible characters for output.
            # Assemble a list of all possible lookers.
            lookers = list(cont for cont in character.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
            for looker in lookers:
                # Exclude the caller, who got their output above.
                if looker != character:
                    basher_string = rules.get_visible_output(character, looker)
                    looker.msg("%s bashes against the %s, but it holds strong." % ((character_string[0].upper() + character_string[1:]), target_string))

    # If the character didn't die, check for whether any of the mobiles in the
    # room worry about the character's show of aggression. 25% chance a mobile
    # will attack.
    if character.location == target.location and character.hitpoints_current > 1:
        mobiles = list(cont for cont in character.location.contents if "mobile" in cont.tags.all())
        for mobile in mobiles:
            if (mobile.position != "sleeping"
                    and not mobile.nattributes.has("combat_handler")
                    and rules.is_visible(character, mobile)
                    and character.level - mobile.level <= 4
                    and random.randint(1, 4) > 3):
                if character.nattributes.has("combat_handler"):
                    combat = character.ndb.combat_handler
                    combat.combatant_add(mobile, character)
                else:
                    combat = rules_combat.create_combat(mobile, character)
                    combat.at_repeat()

def check_skill_improve(character, skill_name, success, learn_factor):
    if "mobile" in character.tags.all():
        return False
    elif skill_name not in character.db.skills:
        return False
    elif character.db.skills[skill_name] >= 96:
        return False
    # Should also check for whether high enough level to learn.
    else:
        # Calculate the chance that the player could potentially
        # learn more about the skill.
        chance = 10 * rules.intelligence_learn_rating(character)
        chance += character.db.skills[skill_name]
        
        if random.randint(1, 1000) > chance:
            return False
        
        if success:
            learn_chance = (100 - character.db.skills[skill_name]) / learn_factor
            if learn_chance < 5:
                learn_chance = 5
            elif learn_chance > 95:
                learn_chance = 95
            
            if random.randint(1,100) < learn_chance and character.db.skills[skill_name] < 96:
                character.msg("You have become better at %s!" % skill_name)
                character.db.skills[skill_name] += 1
        else:
            learn_chance = character.db.skills[skill_name] / 2
            if learn_chance < 5:
                learn_chance = 5
            elif learn_chance > 30:
                learn_chance = 30
                
            if random.randint(1, 100) < learn_chance and character.db.skills[skill_name] < 96:
                character.msg("You learn from your mistakes, and your %s skill improves!" % skill_name)
                skill_increase = random.randint(1, 2)
                character.db.skills[skill_name] += skill_increase

def do_chameleon_power(character):
    """
    This is the function that does the actual mechanics of the
    chameleon power skill.
    """
    skill = get_skill(skill_name="chameleon power")

    character.msg("You attempt to blend in with your surroundings.")
    if random.randint(1, 100) <= character.db.skills["chameleon power"] or "mobile" in character.tags.all():
        if "player" in character.tags.all():
            check_skill_improve(character, "chameleon power", True, 2)

        rules.affect_apply(character,
                           "hide",
                           character.level,
                           "You no longer blend in with your surroundings.",
                           "%s appears from nowhere." % (character.key[0].upper() + character.key[1:])
                           )

        rules.wait_state_apply(character, skill["wait state"])

        # Deal with invisible objects/characters for output.
        # Assemble a list of all possible lookers.
        lookers = list(cont for cont in character.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
        for looker in lookers:
            # Exclude the character, who got their output above.
            if looker != character:

                # Give output to those who can no longer see the character.
                if not rules.is_visible(character, looker):
                    looker.msg("%s blends into %s surroundings and disappears!" % (character.key, rules.pronoun_possessive(character)))
        
    else:
        if "player" in character.tags.all():
            check_skill_improve(character, "chameleon power", False, 2)


def do_dowse(character):
    """
    This is the function that does the actual mechanics of the
    dowse skill.
    """
    skill = get_skill(skill_name="dowse")

    # create the spring
    spring = rules.make_object(character.location, False, "o22")
    rules.wait_state_apply(character, skill["wait state"])

    # put a timer on the spring equal to skill level
    timer = character.level * settings.TICK_OBJECT_TIMER
    timestamp = spring.key + str(time.time())
    tickerhandler.add(timer, spring.at_disintegrate, timestamp)
    spring.db.disintegrate_ticker = timestamp
    spring.tags.add("disintegrating")
    

def do_forage(character):
    """
    This is the function that does the actual mechanics of the
    forage skill.
    """
    skill = get_skill(skill_name="forage")

    # create the magic mushroom
    mushroom = rules.make_object(character.location, False, "o20")
    rules.wait_state_apply(character, skill["wait state"])

    mushroom.db.hours_fed = 5 + character.level
    rules.set_disintegrate_timer(mushroom)


def do_hide(character):
    """
    This is the function that does the actual mechanics of the
    hide skill.
    """
    skill = get_skill(skill_name="hide")

    character.msg("You attempt to hide.")
    if random.randint(1, 100) <= character.db.skills["hide"] or "mobile" in character.tags.all():
        if "player" in character.tags.all():
            check_skill_improve(character, "hide", True, 2)

        rules.affect_apply(character,
                           "hide",
                           character.level,
                           "You are no longer hidden.",
                           "%s appears from hiding." % (character.key[0].upper() + character.key[1:])
                           )

        rules.wait_state_apply(character, skill["wait state"])
        
        # Deal with invisible objects/characters for output.
        # Assemble a list of all possible lookers.
        lookers = list(cont for cont in character.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
        for looker in lookers:
            # Exclude the character, who got their output above.
            if looker != character:

                # Give output to those who can no longer see the character.
                if not rules.is_visible(character, looker):
                    looker.msg("%s hides and disappears!" % character.key)
        
    else:
        if "player" in character.tags.all():
            check_skill_improve(character, "hide", False, 2)


def do_pick_lock(character, target, target_type):
    """
    This is the function that does the actual mechanics of
    picking a lock.
    """
    skill = get_skill(skill_name="pick lock")

    if target.key == "up" or target.key == "down":
        target_string = "door %s" % target.key
    else:
        target_string = "%s door" % target.key

    if not target.access(character, "pick"):
        if target_type == "object":
            character.msg("The lock on %s cannot be picked." % target.key)
            return

        character.msg("The lock on the %s cannot be picked." % target_string)
        return

    if random.randint(1, 100) > character.db.skills["pick lock"]:
        character.msg("You failed.")
        check_skill_improve(character, "pick lock", False, 3)
        return

    character.msg("*Click*")

    if target_type == "container":
        
        # Deal with invisible objects/characters for output.
        # Assemble a list of all possible lookers.
        lookers = list(cont for cont in character.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
        for looker in lookers:
            # Exclude the caller, who got their output above.
            if looker != character:
                # Address visibility of character picking.
                if rules.is_visible(character, looker):
                    picker = (character.key[0].upper() + character.key[1:])
                else:
                    picker = "Someone"

                # Address visibility of object picked.
                if rules.is_visible(target, looker):
                    picked = target.key
                else:
                    picked = "something"

                # As long as something was visible, give output.
                if picker != "Someone" or picked != "something":
                    looker.msg("%s picks %s" % (picker, target.key))

        target.db.state.remove("locked")
        
    else:
        
        # Deal with invisible objects/characters for output.
        # Assemble a list of all possible lookers.
        lookers = list(cont for cont in character.location.contents if "mobile" in cont.tags.all() or "player" in cont.tags.all())
        for looker in lookers:
            # Exclude the caller, who got their output above.
            if looker != character:
                # Address visibility of character picking.
                if rules.is_visible(character, looker):
                    picker = (character.key[0].upper() + character.key[1:])
                else:
                    picker = "Someone"

                looker.msg("%s picks the %s" % (picker, target_string))
        
        # Unlock the exit in the character's room.
        target.db.door_attributes.remove("locked")
        
        # Unlock the exit in the destination room.
        # Fetch the exit in the opposite direction from the destination room.
        if target.key == "north":
            opposite_direction = "south"
        elif target.key == "east":
            opposite_direction = "west"
        elif target.key == "south":
            opposite_direction = "north"
        elif target.key == "west":
            opposite_direction = "east"
        elif target.key == "up":
            opposite_direction = "down"
        elif target.key == "down":
            opposite_direction = "up"
        else:
            opposite_direction = door.key

        opposite_door = character.search(opposite_direction,
                                         location=target.destination)

        # Modify opposite door attributes as above.
        if "locked" in opposite_door.db.door_attributes:
            target.db.door_attributes.remove("locked")

    rules.wait_state_apply(character, skill["wait state"])
    check_skill_improve(character, "pick lock", True, 3)
        
def do_shadow_form(character):
    """
    This is the function that does the actual mechanics of the
    shadow form skill.
    """
    skill = get_skill(skill_name="shadow form")

    character.msg("You attempt to move in the shadows.")
    if random.randint(1, 100) <= character.db.skills["shadow form"] or "mobile" in character.tags.all():
        if "player" in character.tags.all():
            check_skill_improve(character, "shadow form", True, 2)

        rules.affect_apply(character,
                           "sneak",
                           character.level,
                           "You are no longer moving in the shadows.",
                           ""
                           )

        rules.wait_state_apply(character, skill["wait state"])

    else:
        if "player" in character.tags.all():
            check_skill_improve(character, "shadow form", False, 2)


def do_sneak(character):
    """
    This is the function that does the actual mechanics of the
    sneak skill.
    """
    skill = get_skill(skill_name="sneak")

    character.msg("You attempt to move silently.")
    if random.randint(1, 100) <= character.db.skills["sneak"] or "mobile" in character.tags.all():
        if "player" in character.tags.all():
            check_skill_improve(character, "sneak", True, 2)

        rules.affect_apply(character,
                           "sneak",
                           character.level,
                           "You are no longer moving silently.",
                           ""
                           )

        rules.wait_state_apply(character, skill["wait state"])

    else:
        if "player" in character.tags.all():
            check_skill_improve(character, "sneak", False, 2)


def do_steal(thief, target, to_steal):
    """
    This is the function that does the actual theft of gold or an
    item (to_steal) by a character (thief) from a target.
    """
    skill = get_skill(skill_name="steal")
    minimum_moves = skill["minimum cost"]
    wait_state = skill["wait state"]
    
    # Build chance of a successful steal.
    percent = thief.db.skills["steal"]
    percent += thief.level - target.level   # modify with level difference
    percent += random.randint(0, 20) - 10   # luck factor
    
    if target.position == "sleeping":
        percent += 25
        
    if thief.get_affect_status("sneak"):
        percent += 5
        
    if not rules.can_see(thief, target):
        percent += 10
        
    if to_steal == "gold":                   # gold is easier to steal
        percent *= 1.2
    elif to_steal.db.equipped:
        percent *= 0.8                       # equipped items are harder
    else:
        percent *= 0.4                       # stuff packed away in inventory is hardest to steal

    if percent < random.randint(1, 100):
        thief.msg("Oops! That was NOT a success!\n")
        check_skill_improve(thief, "steal", False, 4)
        if rules.is_visible(thief, target):
            if not thief.ndb.combat_handler and not target.ndb.combat_handler:
                thief.msg("%s is not pleased with your attempt to steal, and jumps forward and ATTACKS you!" % (target.key[0].upper() + target.key[1:]))
                rules_combat.create_combat(target, thief)
            if not thief.ndb.combat_handler:
                combat = thief.ndb.combat_handler
                combat.add_combatant(target, thief)
    else:
        if to_steal == "gold":
            amount = math.ceil(target.db.gold * random.randint(1, 10) / 100)
            if amount <= 0:
                thief.msg("You check the pockets of %s, but come up empty." % target.key)
                return
            else:
                thief.db.gold += amount
                target.db.gold -= amount
                thief.msg("|gBingo!|n You got %d gold coins." % amount)
                check_skill_improve(thief, "steal", True, 4)
                if "combat_handler" in thief.ndb.all:
                    combat = thief.ndb.combat_handler
                    rules.wait_state_apply(thief, wait_state)
        else:
            if "no drop" in to_steal.db.extra_flags:
                thief.msg("A magical force prevents you from prying %s away." % to_steal.key)
                check_skill_improve(thief, "steal", True, 4)
                return
            elif "no remove" in to_steal.db.extra_flags and not to_steal.db.equipped:
                thief.msg("A magical force prevents you from removing %s from %s." % (to_steal.key, target.key))
                check_skill_improve(thief, "steal", True, 4)
                return
            # In the future, do weight and object number checks here.
            elif not to_steal.db.equipped:
                thief.msg("You daringly swipe %s from %s's inventory. Sneaky!" % (to_steal.key, target.key))
                check_skill_improve(thief, "steal", True, 4)
                rules.wait_state_apply(thief, wait_state)
            else:
                thief.msg("While %s is distracted, you swipe %s right off them!" % (target.key, to_steal.key))
                check_skill_improve(thief, "steal", True, 4)
                to_steal.db.equipped = False
                rules.wait_state_apply(thief, wait_state)

            to_steal.location = thief
                
def get_skill(**kwargs):
    """
    This function holds the skill database, and has multiple kwargs
    that will return different data.
    skill_name - returns the dictionary of that skill, including
                 classes that learn it and at what level,
                 minimum mana cost and wait state.
    eligible_character - returns a dictionary of skills that
                         character is eligible to practice, and
                         the cost for that practice.
    all - returns the entire skills dictionary.
    """
    
    skills = {
        "adrenaline control": {
            "classes": {
                "psionicist": 10,
                "bard": 30
                },
            "minimum cost": 6,
            "wait state": 12
            },
        "agitation": {
            "classes": {
                "psionicist": 5
                },
            "minimum cost": 10,
            "wait state": 12
            },
        "armor": {
            "classes": {
                "cleric": 6,
                "druid": 9,
                "paladin": 14
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "bamf": {
            "classes": {
                "mage": 6,
                "bard": 15
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "bash door": {
            "classes": {
                "warrior": 8
                },
            "minimum cost": 5,
            "wait state": 24
            },
        "bless": {
            "classes": {
                "cleric": 6,
                "paladin": 12
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "burning hands": {
            "classes": {
                "mage": 6
                },
            "minimum cost": 15,
            "wait state": 12
            },
        "cause light": {
            "classes": {
                "cleric": 5,
                "paladin": 15
                },
            "minimum cost": 15,
            "wait state": 12
            },
        "chameleon power": {
            "classes": {
                "psionicist": 10
                },
            "wait state": 12
            },
        "chill touch": {
            "classes": {
                "druid": 4
                },
            "minimum cost": 15,
            "wait state": 12
            },
        "continual light": {
            "classes": {
                "mage": 4
                },
            "minimum cost": 7,
            "wait state": 12
            },
        "create food": {
            "classes": {
                "cleric": 3
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "create sound": {
            "classes": {
                "psionicist": 3,
                "bard": 3
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "create spring": {
            "classes": {
                "druid": 10
                },
            "minimum cost": 20,
            "wait state": 12
            },
        "create water": {
            "classes": {
                "cleric": 3,
                "paladin": 13
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "cure blindness": {
            "classes": {
                "cleric": 8,
                "paladin": 25,
                "ranger": 30
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "cure light": {
            "classes": {
                "cleric": 5,
                "druid": 7,                
                "paladin": 15,
                "bard": 18
                },
            "minimum cost": 10,
            "wait state": 12
            },
        "detect evil": {
            "classes": {
                "cleric": 4,
                "paladin": 4
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "detect hidden": {
            "classes": {
                "mage": 5,
                "cleric": 8,
                "druid": 10,
                "ranger": 18,
                "thief": 25
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "detect invis": {
            "classes": {
                "mage": 6,
                "cleric": 13,
                "thief": 33
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "detect magic": {
            "classes": {
                "mage": 5,
                "cleric": 8,
                "bard": 12
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "dirt kicking": {
            "classes": {
                "ranger": 4,
                "thief": 22,
                "bard": 27
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "dodge": {
            "classes": {
                "thief": 6,
                "ranger": 6,
                "bard": 7,
                "warrior": 25,
                "paladin": 25
                },
            },
        "dowse": {
            "classes": {
                "ranger": 3
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "enhanced damage": {
            "classes": {
                "warrior": 3,
                "ranger": 13,
                "paladin": 11
                }
            },
        "faerie fog": {
            "classes": {
                "druid": 6
                },
            "minimum cost": 12,
            "wait state": 12
            },
        "firebolt": {
            "classes": {
                "mage": 10
                },
            "minimum cost": 15,
            "wait state": 12
            },
        "fly": {
            "classes": {
                "mage": 9
                },
            "minimum cost": 10,
            "wait state": 18
            },
        "forage": {
            "classes": {
                "ranger": 3,
                "druid": 6,
                "bard": 9
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "giant strength": {
            "classes": {
                "mage": 9,
                "warrior": 66
                },
            "minimum cost": 20,
            "wait state": 12
            },
        "hide": {
            "classes": {
                "thief": 8,
                "ranger": 9,
                "bard": 10,
                "druid": 16
                },
            "wait state": 12
            },
        "infravision": {
            "classes": {
                "druid": 9,
                "ranger": 22
                },
            "minimum cost": 5,
            "wait state": 18
            },
        "invisible": {
            "classes": {
                "mage": 10,
                "druid": 35,
                "thief": 60
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "kick": {
            "classes": {
                "warrior": 3,
                "ranger": 10,
                "paladin": 12
                },
            "wait state": 6
            },
        "know alignment": {
            "classes": {
                "cleric": 9,
                "paladin": 15
                },
            "minimum cost": 9,
            "wait state": 12
            },
        "levitation": {
            "classes": {
                "psionicist": 7
                },
            "minimum cost": 10,
            "wait state": 18
            },
        "magic missile": {
            "classes": {
                "mage": 4,
                "bard": 8
                },
            "minimum cost": 15,
            "wait state": 12
            },
        "mental barrier": {
            "classes": {
                "psionicist": 6
                },
            "minimum cost": 8,
            "wait state": 12
            },
        "mind thrust": {
            "classes": {
                "psionicist": 7
                },
            "minimum cost": 8,
            "wait state": 12
            },
        "parry": {
            "classes": {
                "warrior": 5,
                "paladin": 7,
                "ranger": 9,
                "bard": 15,
                "thief": 16
                },
            },
        "pick lock": {
            "classes": {
                "thief": 5
                },
            },
        "protection": {
            "classes": {
                "cleric": 7,
                "druid": 8,
                "paladin": 16
                },
            "minimum cost": 12,
            "wait state": 18
            },
        "psychic heal": {
            "classes": {
                "psionicist": 6
                },
            "minimum cost": 20,
            "wait state": 12
            },
        "refresh": {
            "classes": {
                "druid": 4,
                "ranger": 16
                },
            "minimum cost": 12,
            "wait state": 18
            },
        "rescue": {
            "classes": {
                "warrior": 4,
                "ranger": 11,
                "paladin": 3
                },
            "wait state": 12
            },
        "shadow form": {
            "classes": {
                "psionicist": 8
                },
            "wait state": 12
            },
        "shield": {
            "classes": {
                "mage": 7
                },
            "minimum cost": 12,
            "wait state": 18
            },
        "shocking grasp": {
            "classes": {
                "mage": 8
                },
            "minimum cost": 15,
            "wait state": 12
            },
        "slumber": {
            "classes": {
                "bard": 8
                },
            "minimum cost": 15,
            "wait state": 12
            },
        "snare":
            "classes": {
                "thief": 8,
                "ranger": 8,
                },
            "wait state": 12
            },
        "sneak": {
            "classes": {
                "thief": 6,
                "ranger": 7,
                "bard": 8
                },
            "wait state": 12
            },
        "steal": {
            "classes": {
                "thief": 3,
                "bard": 13
                },
            "minimum cost": 5,
            "wait state": 24
            },
        "summon weapon": {
            "classes": {
                "paladin": 4
                },
            "minimum cost": 7,
            "wait state": 12
            },
        "trip": {
            "classes": {
                "thief": 4,
                "bard": 5,
                "ranger": 14,
                "warrior": 15
                },
            "minimum cost": 5,
            "wait state": 24
            },
        "thought shield": {
            "classes": {
                "psionicist": 10
                },
            "minimum cost": 5,
            "wait state": 12
            },
        "ventriloquate": {
            "classes": {
                "bard": 5
                },
            "minimum cost": 5,
            "wait state": 12
            }

        }

    if "skill_name" in kwargs:
        skill_name = kwargs["skill_name"]

        for skill in skills:
            if skill == skill_name:
                return skills[skill]

    elif "all" in kwargs:
        return skills

    elif "eligible_character" in kwargs:
        eligible_character = kwargs["eligible_character"]

        level = eligible_character.level
        eligible_skills = {}
        for skill in skills:
            for class_name in skills[skill]["classes"]:
                if skills[skill]["classes"][class_name] <= level:
                    if skill not in eligible_skills:
                        cost_to_practice = rules.current_experience_step(eligible_character, 0)
                        cost_to_practice = math.ceil(cost_to_practice / rules.wisdom_practices(eligible_character))
                                                
                        eligible_skills[skill] = cost_to_practice
        
        return eligible_skills

def lowest_learned_level(skill):
    """Calculate the earliest that a player could have learned a skill"""
    
    minimum_level = 101
    for class_name in skill["classes"]:
        if skill["classes"][class_name] < minimum_level:
            minimum_level = skill["classes"][class_name]
    
    return minimum_level
        
