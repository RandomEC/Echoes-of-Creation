"""
This file handles character growth, through levels, counting
categories, attributes, skills and similar.
"""

import random
from commands.command import MuxCommand
from world import rules, rules_skills

def hitpoint_gain_minimum(character):
    classes = rules.classes_current(character)
    
    if "default" in classes and len(classes) == 1:
        return 9
    elif "ranger" in classes:
        return 13
    elif "warrior" in classes or "paladin" in classes:
        return 11
    elif "bard" in classes:
        return 9
    elif "thief" in classes or "druid" in classes:
        return 8
    else:
        return 7
    
def hitpoint_gain_maximum(character):
    classes = rules.classes_current(character)
    
    if "default" in classes and len(classes) == 1:
        return 13
    elif "ranger" in classes:
        return 19
    elif "paladin" in classes:
        return 18
    elif "warrior" in classes:
        return 17
    elif "bard" in classes or "thief" in classes:
        return 13
    elif "druid" in classes:
        return 11
    elif "cleric" in classes or "psionist" in classes:
        return 10
    else:
        return 9

def mana_gain_minimum(character):
    classes = rules.classes_current(character)
    
    if "default" in classes and len(classes) == 1:
        return 8
    elif "psionist" in classes:
        return 13
    elif "mage" in classes:
        return 11
    elif "cleric" in classes:
        return 9
    elif "bard" in classes or "druid" in classes:
        return 8
    else:
        return 7
    
def mana_gain_maximum(character):
    classes = rules.classes_current(character)
    
    if "default" in classes and len(classes) == 1:
        return 12
    elif "psionist" in classes:
        return 19
    elif "mage" in classes:
        return 17
    elif "cleric" in classes or "druid" in classes:
        return 13
    elif "bard" in classes:
        return 11
    elif "thief" in classes or "ranger" in classes or "paladin" in classes:
        return 10
    else:
        return 9

class CmdPractice(MuxCommand):
    """
    Practice to gain addtional skills or spells for your character, or to gain
    additional ability at those skills or spells.
    Usage:
        practice
        practice <skill or spell>
    Practice without argument will tell you the skills that you are currently
    eligible to practice, and the experience cost of that practice session. This
    excludes skills that are too high level for you to practice, and those that
    you are already at or above 70% learned on, which can only be practiced
    through use. Practice with an argument will spend experience and practice
    the skill in question. Unlike train, this practice session may not
    automatically bump you to a higher experience bracket for your next practice
    or train. Depending on your wisdom, you may get several practices at one
    level of experience.
    
    See help level, help practice and help skills for more.
    """
        
    key = "practice"
    aliases = ["prac"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement command"""

        caller = self.caller

        if not self.args:
            output_string = "You can currently practice the following:\n"
            eligible_skills = rules_skills.get_skill(eligible_character=caller)
            for skill in eligible_skills:
                output_string += "%-20s%d\n" % (skill, eligible_skills[skill])
            
            caller.msg(output_string)
        
        else:
            eligible_skills = rules_skills.get_skill(eligible_character=caller)
            skill = self.args
            if skill not in eligible_skills:
                caller.msg("Please use the full name of a skill that you are eligible to practice.")
                return
            else:
                cost = eligible_skills[skill]
                amount_learned = rules.intelligence_learn_rating(caller)
                
                if skill not in caller.db.skills:
                    caller.db.skills[skill] = amount_learned
                    caller.experience_spent += eligible_skills[skill]
                    caller.msg("You have learned the %s skill at %d percent learned!" % (skill, amount_learned))
                else:
                    if caller.db.skills[skill] + amount_learned > 70:
                        caller.db.skills[skill] = 70
                        caller.experience_spent += eligible_skills[skill]
                        caller.msg("Your skill at %s has increased to %d percent!\nYou can only learn more through using your skill." % (skill, amount_learned))
                    else:
                        caller.db.skills[skill] += amount_learned
                        caller.experience_spent += eligible_skills[skill]
                        caller.msg("Your skill at %s has increased to %d percent!" % (skill, amount_learned))
                                    
class CmdTrain(MuxCommand):
    """
    Train to gain addtional attributes for your character.
    Usage:
        train
        train <level, hitpoints, mana, moves, strength, dexterity, etc.>
    Train without argument will tell you the amount of experience needed to increase
    in any trainable category. In the case of levels, it will also tell you whether
    you have trained enough in other categories to be ready to level. Train with an
    argument will attempt to gain an additional level or attribute, in those cases,
    or an additional amount of hitpoints, mana or moves depending on your attributes
    and skills you have learned.
    
    See help level, help practice and help skills for more.
    """

    key = "train"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement command"""

        caller = self.caller

        if not self.args:
            if (rules.level_cost(caller) - caller.experience_available) > 0:
                needed_to_level = rules.level_cost(caller) - caller.experience_available
            else:
                needed_to_level = "You have enough"

            if (rules.hitpoints_cost(caller) - caller.experience_available) > 0:
                needed_for_hitpoints = rules.hitpoints_cost(caller) - caller.experience_available
            else:
                needed_for_hitpoints = "You have enough"

            if (rules.mana_cost(caller) - caller.experience_available) > 0:
                needed_for_mana = rules.mana_cost(caller) - caller.experience_available
            else:
                needed_for_mana = "You have enough"

            if (rules.moves_cost(caller) - caller.experience_available) > 0:
                needed_for_moves = rules.moves_cost(caller) - caller.experience_available
            else:
                needed_for_moves = "You have enough"

            if (rules.attributes_cost(caller) - caller.experience_available) > 0:
                needed_for_attribute = rules.attributes_cost(caller) - caller.experience_available
            else:
                needed_for_attribute = "You have enough"

            if rules.check_ready_to_level(caller):
                check_level = "and you have grown sufficiently to level"
            else:
                check_level = "but you have not yet grown sufficiently to level"
                
            caller.msg("In order to train yourself further, you require:\n"
                       "%s experience to go up a level, %s.\n"
                       "%s experience to acquire more hitpoints.\n"
                       "%s experience to acquire more mana.\n"
                       "%s experience to acquire more moves.\n"
                       "%s experience to increase an attribute.\n"
                       % (needed_to_level,
                          check_level,
                          needed_for_hitpoints,
                          needed_for_mana,
                          needed_for_moves,
                          needed_for_attribute
                          ))
        elif self.args == "level":

            needed_to_level = (rules.level_cost(caller) - caller.experience_available)

            if needed_to_level <= 0 and rules.check_ready_to_level(caller):
                caller.db.experience_spent += rules.level_cost(caller)
                caller.db.level += 1
                caller.msg("Congratulations! You have reached level %d!!!!" % caller.db.level)
            else:
                if rules.check_ready_to_level(caller):
                    ready = "You have grown sufficiently to reach level %d.\n" % (caller.level + 1)
                else:
                    ready = "You must train in other ways to be ready for level %d.\n" % (caller.level + 1)
                
                if (rules.level_cost(caller) - caller.experience_available) > 0:
                    needed_to_level = ("You need %d" % (rules.level_cost(caller) - caller.experience_available))
                else:
                    needed_to_level = "You have enough"
                    
                experience = ("%s experience to go up to level %d." % (needed_to_level, (caller.level + 1)))
                
                caller.msg("%s%s" % (ready, experience))
                
        
        elif self.args == "hitpoints":
            
            needed_for_hitpoints = rules.hitpoints_cost(caller) - caller.experience_available
            
            if needed_for_hitpoints <= 0:
                caller.db.experience_spent += rules.hitpoints_cost(caller)
                caller.db.hitpoints["trains spent"] += 1
                hit_gain = random.randint(hitpoint_gain_minimum(caller), hitpoint_gain_maximum(caller)) + rules.constitution_hitpoint_bonus(caller)
                new_hitpoints_maximum = caller.hitpoints_maximum + hit_gain
                
                caller.hitpoints_maximum = new_hitpoints_maximum
                caller.msg("Congratulations! Your maximum hitpoints have increased by %d to %d!" % (hit_gain, caller.hitpoints_maximum))
            else:
                caller.msg("You are %d experience short of being able to gain more hitpoints." % needed_for_hitpoints)
        
        elif self.args == "mana":
            
            needed_for_mana = rules.mana_cost(caller) - caller.experience_available
            
            if needed_for_mana <= 0:
                caller.db.experience_spent += rules.mana_cost(caller)
                caller.db.mana["trains spent"] += 1
                mana_gain = (random.randint(mana_gain_minimum(caller), mana_gain_maximum(caller)) + 
                             rules.intelligence_mana_bonus(caller) +
                             rules.wisdom_mana_bonus(caller)
                             )
                new_mana_maximum = caller.mana_maximum + mana_gain
                
                caller.mana_maximum = new_mana_maximum
                caller.msg("Congratulations! Your maximum mana has increased by %d to %d!" % (mana_gain, caller.mana_maximum))
            else:
                caller.msg("You are %d experience short of being able to gain more mana." % needed_for_mana)
       
        elif self.args == "moves":
            
            needed_for_moves = rules.moves_cost(caller) - caller.experience_available
            
            if needed_for_moves <= 0:
                caller.db.experience_spent += rules.moves_cost(caller)
                caller.db.moves["trains spent"] += 1
                moves_gain_maximum = int((caller.dexterity + caller.constitution)/4)
                if moves_gain_maximum < 5:
                    moves_gain_maximum = 5
                moves_gain = random.randint(5, moves_gain_maximum)
                
                new_moves_maximum = caller.moves_maximum + moves_gain
                
                caller.moves_maximum = new_moves_maximum
                caller.msg("Congratulations! Your maximum moves have increased by %d to %d!" % (moves_gain, caller.moves_maximum))
            else:
                caller.msg("You are %d experience short of being able to gain more moves." % needed_for_moves)        

        elif self.args == "strength" or self.args == "dexterity" or self.args == "intelligence" or self.args == "wisdom" or self.args == "constitution":
            
            attribute = self.args
            needed_for_attribute = rules.attributes_cost(caller) - caller.experience_available
            
            if caller.db.attribute_trains[attribute] > 4:
                caller.msg("You cannot train %s any further. Any additional gains must come from equipment or spells." % attribute)
                return
            elif needed_for_attribute <= 0:
                caller.db.experience_spent += rules.attributes_cost(caller)
                caller.db.attribute_trains[attribute] += 1
                caller.msg("Congratulations! Your base %s has increased by one to %d!" % (attribute, caller.get_base_attribute(attribute)))
            else:
                caller.msg("You are %d experience short of being able to increase an attribute." % needed_for_attribute)
        else:
            caller.msg("%s is not a trainable statistic. Choose from level, hitpoints, mana, moves or any attribute." % (self.args[0].upper() + self.args[1:]))
