"""
These are scripts that fire on mobiles, objects or rooms
to support and implement quests. Generally, they are named
for the mobile, object or room that they are on.
"""

from evennia.utils.evmenu import get_input
from typeclasses.scripts import Script
from world import rules

class TestQuestScript(Script):

    def at_script_creation(self):
        self.key = "test_script"
        self.desc = "Test script for quests."
        self.persistent = True
        self.db.player = ""

    def quest_talk(self):
        player = self.db.player

        if not player.db.quests:
            player.db.quests = {}

        if "test" not in player.db.quests:
            def callback(caller, prompt, user_input):
                """
                This is a callback you define yourself.

                Args:
                    caller (Account or Object): The one being asked
                      for input
                    prompt (str): A copy of the current prompt
                    user_input (str): The input from the account.

                Returns:
                    repeat (bool): If not set or False, exit the
                      input prompt and clean up. If returning anything
                      True, stay in the prompt, which means this callback
                      will be called again with the next user input.
                """
                if user_input == "yes":
                    caller.msg("%s says, 'Great, wish I had one.'" % (self.obj.key[0].upper() + self.obj.key[1:]))
                    caller.db.quests["test"] = 1
                    return False
                elif user_input == "no":
                    caller.msg("%s says, 'Whew, I don't have one for you.'" % (self.obj.key[0].upper() + self.obj.key[1:]))
                    return False
                else:
                    caller.msg("%s says, 'Try just typing yes or no.'" % (self.obj.key[0].upper() + self.obj.key[1:]))
                    return True

            get_input(player, "%s says, 'Would you like to do a quest? Just enter yes or no.'" % (self.obj.key[0].upper() + self.obj.key[1:]), callback)
        elif player.db.quests["test"] == 1:
            player.msg("%s says, 'Man, you are killing this quest thing.'" % (self.obj.key[0].upper() + self.obj.key[1:]))
            player.db.quests["test"] = "done"


        self.stop()

class Mobile103Script(Script):
    """
    This is the script for Tabitha to lead you to the Smurf
    Village quest.
    """

    def at_script_creation(self):
        self.key = "m103_script"
        self.desc = "Script for Tabitha to send you to Papa Smurf."
        self.persistent = True
        self.db.player = ""

    def quest_talk(self):
        player = self.db.player

        if not player.db.quests:
            player.db.quests = {}

        if "smurfs" not in player.db.quests:
            def callback(caller, prompt, user_input):
                if user_input == "yes":
                    caller.msg("Tabitha squeals with excitement.")
                    caller.msg("Tabitha says to you, 'How wonderful! I knew you would!")
                    caller.msg("Tabitha says to you, 'Remember, through the portal in the park, and he is the blue man with the red pants and hat!")
                    caller.db.quests["smurfs"] = 1
                    return False
                elif user_input == "no":
                    caller.msg("Tabitha stamps her little foot.")
                    caller.msg("Tabitha says to you, 'Well, fine! Maybe later when you're not such a big meanie!'")
                    caller.msg("Tabitha sticks out her tongue at you. How rude.")
                    return False
                else:
                    caller.msg(
                        "Tabitha says, 'Try just typing yes or no.'")
                    return True

            player.msg("Tabitha giggles cutely")
            player.msg("Tabitha says to you, 'I've been having fun away from daycare! I've been making friends!'")
            player.msg("Tabitha whispers to you, 'I snuck into the portal in the park, and made friends with a tiny blue man with a red hat!")
            player.msg("Tabitha whispers to you, 'He needs help, but I couldn't stay to help him.")

            get_input(player, "Tabitha says to you, 'Will you help my little blue friend?'", callback)
        elif player.db.quests["smurfs"] < 3:
            player.msg("Tabitha says to you, 'I hope you can help my blue friend!'")
        elif player.db.quests["smurfs"] >= 3:
            player.msg("Tabitha says to you, 'Yay, I'm glad I found you to help!'")

        self.stop()

class Mobile6210Script(Script):
    """
    This is the script for Papa Smurf to give you some xp for coming
    from Tabitha, or just point you in the right direction on the
    quest if not.
    """

    def at_script_creation(self):
        self.key = "m6210_script"
        self.desc = "Script for Papa Smurf to give you the smurf quest."
        self.persistent = True
        self.db.player = ""

    def quest_talk(self):
        player = self.db.player

        if not player.db.quests:
            player.db.quests = {}


        if "smurfs" not in player.db.quests:
            def callback(caller, prompt, user_input):
                if "yes" in user_input:
                    caller.msg("You tell Papa Smurf that you would be happy to help.")
                    caller.msg("Papa Smurf says to you, 'Finally, someone else responsible.")
                    caller.msg("Papa Smurf says to you, 'As I say, just gather them up and put them away in my house.")
                    caller.msg("Papa Smurf says to you, 'Hrm, you may need the key as well. I'm sure it's around somewhere.'")
                    caller.msg("Papa Smurf says to you, 'Don't forget to close the lid when you are done.'")
                    player.msg("Papa Smurf says to you, 'Don't worry, I'll know when you are done.'")
                    caller.db.quests["smurfs"] = 2

                elif "no" in user_input:
                    caller.msg("You decline to help Papa Smurf at the present time.")
                    caller.msg("Papa Smurf says to you, 'Perhaps another time.")

            player.msg("Papa Smurf sighs, exhausted.")
            player.msg("Papa Smurf says to you, 'These kids these days.'")
            player.msg("Papa Smurf says to you, 'All I ask is that they put their toys away in my house when they are done.'")
            player.msg("Papa Smurf says to you, 'But can they do that? No.'")

            get_input(player, "Papa Smurf says to you, 'Can you gather up my children's toys and put them away?'", callback)

        elif player.db.quests["smurfs"] == 1:
            player.msg("You talk to Papa Smurf, and explain that Tabitha sent you.")
            player.msg("Papa Smurf says to you, 'Ah, wonderful!")
            player.experience_total += 50
            player.msg("You gain 50 experience points!")
            player.msg("Papa Smurf sighs, exhausted.")
            player.msg("Papa Smurf says to you, 'I need you to help me by gathering up my children's toys and putting them away.'")
            player.msg("Papa Smurf says to you, 'Just gather them up and put them away in my house.")
            player.msg("Papa Smurf says to you, 'Hrm, you may need the key as well. I'm sure it's around somewhere.'")
            player.msg("Papa Smurf says to you, 'Don't forget to close the lid when you are done.'")
            player.msg("Papa Smurf says to you, 'Don't worry, I'll know when you are done.'")
            player.db.quests["smurfs"] = 2

        elif player.db.quests["smurfs"] == 2:
            player.msg("Papa Smurf says to you, 'Thanks for taking this on. It's a great weight off my mind.'")

        elif player.db.quests["smurfs"] > 2:
            player.msg("Papa Smurf says to you, 'Thanks for taking care of that cleanup business!'")
            player.msg("Papa Smurf says to you, 'Why those kids can't be more responsible is beyond me.'")

        self.stop()

class Object6217Script(Script):
    """
    This is the script for Papa Smurf's magic box to give you xp
    when you are done putting the objects away, load Gargamel's
    Girdle in the reward room, if not there, and transfer you
    there.
    """

    def at_script_creation(self):
        self.key = "o6217_script"
        self.desc = "Script for Papa's Magic box in the smurf quest."
        self.persistent = True
        self.db.player = ""

    def quest_open(self):
        player = self.db.player

        if "smurfs" in player.db.quests:
            if player.db.quests["smurfs"] > 2 or player.db.quests["smurfs"] == "done":
                player.msg("Papa's magic box says, 'Thanks for putting everything away! There's nothing more to do!")
                return

        player.msg("Papa's magic box says, 'Now be good boys, and put your toys away neatly.'")

    def quest_close(self):
        player = self.db.player
        box = self.obj
        box_contents = box.contents
        trophy_room = player.search("r6231", global_search=True)

        contents_required = ["o6201", "o6210", "o6212", "o6213", "o6214", "o6216"]
        contents_present = []

        if len(box_contents) == 6:
            for object in box_contents:
                contents_present.append(object.db.vnum)

            contents_present.sort()
            contents_required.sort()

            if contents_present == contents_required:

                for object in box_contents:
                    object.location = None
                trophy_case = player.search("o6218", location=trophy_room)
                girdle = player.search("o6219", location=trophy_case)
                if not girdle:
                    girdle = rules.make_object(trophy_case, False, "o6219")

                girdle.db.level = 5
                girdle.db.armor = rules.set_armor(girdle.db.level)

                player.experience_total += 800
                player.msg("You gain 800 experience points!")
                player.msg("Papa's magic box says to you, 'Good boys! Now enjoy your prize!")
                player.move_to(trophy_room, quiet=True)
                player.db.quests["smurfs"] = 3

        self.stop()

class Mobile6211Script(Script):
    """
    This is the script for Gargamel's girdle being given to
    Gargamel, finishing the smurf quest.
    """

    def at_script_creation(self):
        self.key = "m6211_script"
        self.desc = "Script for Gargamel."
        self.persistent = True
        self.db.player = ""
        self.db.given_object = ""

    def quest_give(self):

        player = self.db.player
        receiver = self.obj
        given_object = self.db.given_object

        if "smurfs" in player.db.quests:
            if player.db.quests["smurfs"] == "done":
                player.msg("Gargamel looks suspiciously at the girdle.")
                player.msg("Gargamel says to you, 'I already rewarded you for this once. Get out of here!")
                player.msg("Gargamel gives you Gargamel's girdle.")
                given_object.location = player
            elif player.db.quests["smurfs"] == 3:
                if given_object.db.vnum == "o6219":
                    player.msg("Gargamel hops up and down excitedly!")
                    player.msg("Gargamel says to you, 'My girdle! You found it! You defeated those pesky smurfs!")
                    player.msg("Gargamel hugs you!")

                    # Clear the girdle.
                    for object in receiver.contents:
                        if object.db.vnum == "o6219":
                            object.location = None

                    # Load the leather belt.
                    belt = rules.make_object(receiver, False, "o6220")

                    belt.db.level = 10
                    belt.db.armor = rules.set_armor(belt.db.level)

                    player.msg("Azreal licks you affectionately.")
                    player.msg("Gargamel removes a leather belt, and sighs with relief.")
                    player.msg("Gargamel says to you, 'This replacement was always a bit tight. Perhaps you'd like it. It's somewhat enchanted.'")
                    player.msg("Gargamel gives you a leather belt.")
                    belt.location = player
                    player.msg("Gargamel says to you, 'Thank you SOOOOO much.'")
                    player.msg("Gargamel enthusiastically shakes your hand.")
                    player.experience_total += 5500
                    player.msg("You gain 5500 experience points!")
                    player.db.quests["smurfs"] = "done"
            else:
                if given_object.db.vnum == "o6219":
                    player.msg("Gargamel says to you, 'You shouldn't have this yet, you need to trick the smurfs out of it honestly.'")
                    player.msg("Gargamel gives you Gargamel's girdle.")
                    given_object.location = player
        else:
            if given_object.db.vnum == "o6219":
                player.msg("Gargamel says to you, 'You shouldn't have this yet, you need to trick the smurfs out of it honestly.'")
                player.msg("Gargamel gives you Gargamel's girdle.")
                given_object.location = player

        self.stop()
