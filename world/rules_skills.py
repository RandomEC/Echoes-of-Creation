"""
This rules file is to handle anything related to skills and/or spells
"""

import random
from evennia import TICKER_HANDLER as tickerhandler
from world import rules

def check_skill_improve(character, skill_name, success):
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
            learn_chance = 100 - character.db.skills[skill_name]
            if learn_chance < 5:
                learn_chance = 5
            elif learn_chance > 95:
                learn_chance = 95
            
            if random.randint(1,100) < learn_chance:
                character.msg("You have become better at %s!" % skill_name)
                character.db.skills[skill_name] += 1
        else:
            learn_chance = character.db.skills[skill_name] / 2
            if learn_chance < 5:
                learn_chance = 5
            elif learn_chance > 30:
                learn_chance = 30
                
            if random.randint(1, 100) < learn_chance:
                character.msg("You learn from your mistakes, and your %s skill improves!" % skill_name)
                skill_increase = random.randint(1, 2)
                character.db.skills[skill_name] += skill_increase

def do_dowse(character):
    """
    This is the function that does the actual mechanics of the
    dowse skill.
    """
    # create the spring
    spring = rules.make_object(character.location, False, "o22")

    # put a timer on the spring equal to skill level
    timer = character.db.skills["dowse"]
    tickerhandler.add(timer, spring.at_disintegrate)

def do_forage(character):
    """
    This is the function that does the actual mechanics of the
    forage skill.
    """
    # create the magic mushroom
    mushroom = rules.make_object(character.location, False, "o20")

    rules.set_disintegrate_timer(mushroom)

def get_skill(skill_name):
    skills = {
        "enhanced damage": {
            "classes" : {
                "warrior": 3,
                "ranger": 13,
                "paladin": 11
                }
            }
        }