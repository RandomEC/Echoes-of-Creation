from commands.command import MuxCommand
from evennia.utils import evtable

class CmdQuestList(MuxCommand):
    """
    Lists all active, uncompleted quests that a player is on, with a short description
    of the status of each.
    Usage:
      questlist
      qlist
    Lists all active, uncompleted quests that a player is on, with a short description
    of the status of each.
    """

    key = "questlist"
    aliases = ["qlist"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    quest_status = {
        "daycare": {
            "name": "Protecting the Kids (and Moms)",
            1: "Get an assignment at Dwarven Daycare in Eden's Grove and complete it.",
            2: "Get an assignment at Dwarven Daycare and complete it.",
            3: "Return to Sabrina in Eden's Grove and talk to her.",
        }, 
        "graveyard": {
            "name": "Cleanse the Graveyard",
            1: "Find Henry the Gardener in the Eden's Grove Graveyard and talk to him.",
            2: "Kill five skeletons in the Eden's Grove Graveyard.",
            3: "Kill four more skeletons in the Eden's Grove Graveyard.",
            4: "Kill three more skeletons in the Eden's Grove Graveyard.",
            5: "Kill two more skeletons in the Eden's Grove Graveyard.",
            6: "Kill one more skeleton in the Eden's Grove Graveyard.",
            7: "Return to Henry the Gardener in the Eden's Grove Graveyard and talk to him.",
            8: "When you are ready to face the ghastly ghoul, return to Henry the Gardener in the Eden's Grove Graveyard and talk to him.",
            9: "Kill the ghastly ghoul in the Eden's Grove Graveyard.",
            10: "Return to Henry the Gardener in the Eden's Grove Graveyard and talk to him."
        }, 
        "smurfs": {
            "name": "Put Everything Back Where It Belongs",
            1: "Find the blue man through the portal in the Eden's Grove park and talk to him.",
            2: "Put Papa Smurf's children's toys away in his house. Don't forget to close the lid.",
            3: "Figure out where the girdle goes, and return it."
        }
    }
        
    
    def func(self):
        """Implement questlist"""

        caller = self.caller
        
        player_quests = caller.db.quests
        
        output_string = ""
        quest_names_list = []
        quest_status_list = []
        if not player_quests:
            output_string += "You are not currently on any quests."
        else:            
            for quest in player_quests:                
                if player_quests[quest] != "done":
                    quest_names_list.append(quest_status[quest]["name"])
                    quest_status_list.append(quest_status[quest][player_quests[quest]])
                                                                    
            table = evtable.EvTable("Quest", "Status", table=[quest_names_list, quest_status_list], border=None, width=80)                                                                             
            output_string += ("%s" % table)
        
        caller.msg(output_string)
        
