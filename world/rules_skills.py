"""
This rules file is to handle anything related to skills and/or spells
"""

import math
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
    # create the spring
    spring = rules.make_object(character.location, False, "o22")

    # put a timer on the spring equal to skill level
    timer = (character.level - lowest_learned_level("dowse")) * 60
    tickerhandler.add(timer, spring.at_disintegrate)

def do_forage(character):
    """
    This is the function that does the actual mechanics of the
    forage skill.
    """
    # create the magic mushroom
    mushroom = rules.make_object(character.location, False, "o20")

    rules.set_disintegrate_timer(mushroom)

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
        "enhanced damage": {
            "classes": {
                "warrior": 3,
                "ranger": 13,
                "paladin": 11
                }
            },
        "kick": {
            "classes": {
                "warrior": 3,
                "ranger": 10,
                "paladin": 12
                }
            },
        "rescue": {
            "classes": {
                "warrior": 4,
                "ranger": 11,
                "paladin": 3
                }
            }
        }

    if "skill_name" in kwargs:
    
        for skill in skills:
            if skill == skill_name:
                return skills[skill]
            
    elif "eligible_character" in kwargs:
        
        level = eligible_character.level
        eligible_skills = {}
        for skill in skills:
            for class_name in skills[skill][classes]:
                if skills[skill][classes][class_name] <= level:
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
        
