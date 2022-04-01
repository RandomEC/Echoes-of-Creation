"""
This rules file is to handle anything related to non-combat skills.
"""

import math
import random
from evennia import TICKER_HANDLER as tickerhandler
from server.conf import settings
from world import rules, rules_combat

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
    tickerhandler.add(timer, spring.at_disintegrate)



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
        return

    character.msg("*Click*")

    if target_type == "container":
        character.location.msg_contents("%s picks %s." % ((character.key[0].upper() + character.key[1:]), target.key), exclude=(character))
        target.db.state.remove("locked")
    else:
        character.location.msg_contents("%s picks the %s." % ((character.key[0].upper() + character.key[1:]), target_string),
                                        exclude=(character))
        target.db.door_attributes.remove("locked")


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
    """
    
    skills = {
        "agitation": {
            "classes": {
                "psionicist": 5
                },
            "minimum cost": 10,
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
        "create water": {
            "classes": {
                "cleric": 3,
                "paladin": 13
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
        "forage": {
            "classes": {
                "ranger": 3,
                "druid": 6,
                "bard": 9
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
        "magic missile": {
            "classes": {
                "mage": 4,
                "bard": 8
                },
            "minimum cost": 15,
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
        
