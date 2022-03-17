"""
This file handles character growth, through levels, counting
categories, attributes, skills and similar.
"""

import random
from commands.command import MuxCommand
from world import rules

def hitpoint_gain_minimum(character):
    classes = rules.classes_current(character)
    
    if "default" in classes and len(classes) == 1:
        return 9
    elif "ranger" in classes:
        return 13
    elif "warrior" in classes or "paladin" in classes:
        return 11
    elif "bard" in classses:
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
    elif "bard" in classses or "thief" in classes:
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
    elif "cleric" in classses:
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
    
class CmdTrain(MuxCommand):
    """
    drop something
    Usage:
        drop <obj>
    Lets you drop an object from your inventory into the
    location you are currently in.
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

            if rules.check_ready_to_level(character):
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

            if needed_to_level <= 0 and rules.check_ready_to_level(character):
                caller.db.experience_spent += rules.level_cost(caller)
                caller.db.level += 1
                caller.msg("Congratulations! You have reached level %d!!!!" % caller.db.level)
            else:
                if rules.check_ready_to_level(character):
                    ready = "You have grown sufficiently to reach level %d.\n" % (caller.level + 1)
                else:
                    ready = "You must train in other ways to be ready for level %d.\n" % (caller.level + 1)
                
                if (rules.level_cost(caller) - caller.experience_available) > 0:
                    needed_to_level = ("You need %d" % (rules.level_cost(caller) - caller.experience_available))
                else:
                    needed_to_level = "You have enough"
                    
                experience = ("%s experience to go up to level %d." % (needed_to_level, (caller.level + 1)))
                
                caller.msg("%s%s" % (ready, experience)
                
        
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
