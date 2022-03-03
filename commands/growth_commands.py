"""
This file handles character growth, through levels, counting
categories, attributes, skills and similar.
"""

from commands.command import MuxCommand
from world import rules

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
            if (rules.level_cost(caller.db.level + 1) - caller.experience_available) > 0:
                needed_to_level = rules.level_cost(caller.db.level + 1) - caller.experience_available
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

            caller.msg("In order to train yourself further, you require:\n"
                       "%s experience to go up a level.\n"
                       "%s experience to acquire more hitpoints.\n"
                       "%s experience to acquire more mana.\n"
                       "%s experience to acquire more moves.\n"
                       "%s experience to increase an attribute.\n"
                       % (needed_to_level,
                          needed_for_hitpoints,
                          needed_for_mana,
                          needed_for_moves,
                          needed_for_attribute
                          ))
