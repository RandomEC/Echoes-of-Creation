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

        if not player.db.frank:
            player.msg("in the test.")
            player.db.frank = {}

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

class Mobile101Script(Script):
    """
    This is the script for Marshal Marshall to lead you to the 
    Graveyard quest.
    """

    def at_script_creation(self):
        self.key = "m101_script"
        self.desc = "Script for Marshal to handle Graveyard."
        self.persistent = True
        self.db.player = ""

    def quest_talk(self):
        player = self.db.player

        if not player.db.quests:
            player.db.quests = {}

        if "graveyard" not in player.db.quests:
            def callback(caller, prompt, user_input):
                if user_input == "yes":
                    caller.msg("Marshal Marshall says to you, 'Thanks a lot, friend!'")
                    caller.db.quests["graveyard"] = 1
                    return False
                elif user_input == "no":
                    caller.msg("Marshal Marshall says to you, 'Yeah, I'm sure it's not a big deal. I'll look into it later.'")
                    caller.msg("Marshal Marshall says to you, 'Come back if you change your mind.'")
                    return False
                else:
                    caller.msg("Marshal Marshall says, 'Try just typing yes or no.'")                    
                    return True

            player.msg("Marshal Marshall smiles at your approach.")            
            player.msg("Marshal Marshall says to you, 'Well, Seeker, do you think you can take some time from diving into portals to help me out?'")
            player.msg("Marshal Marshall says to you, 'My friend Henry is the gardener and caretaker over at the graveyard at the south end of town.'")
            player.msg("Marshal Marshall says to you, 'He didn't come by for our regular card game the other night, and I'm a mite worried about him.'")
            player.msg("Marshal Marshall says to you, 'I would go myself, but I'm afraid I'm a bit tied up, what with all the ... er ....'")
            player.msg("Marshal Marshall trails off into mumbling.")
            
            get_input(player, "Marshal Marshall says to you, 'Anyways, will you go take a look?'", callback)            
  
        self.stop()


class Mobile103Script(Script):
    """
    This is the script for Sabrina to lead you to the Dwarven
    Daycare quest.
    """

    def at_script_creation(self):
        self.key = "m104_script"
        self.desc = "Script for Sabrina to handle Dwarven Daycare."
        self.persistent = True
        self.db.player = ""

    def quest_talk(self):
        player = self.db.player

        if not player.db.quests:
            player.db.quests = {}

        if "daycare" not in player.db.quests:
            def callback(caller, prompt, user_input):
                if user_input == "yes":
                    caller.msg("Sabrina, clearly holding her breath, releases it in a 'Whoosh!'")
                    caller.msg("Sabrina says to you, 'Thanks so much.'")
                    caller.msg("Sabrina says to you, 'Just go and see if you can get them to give you an assignment, then check it out.'")
                    caller.msg("Sabrina says to you, 'Come back and talk to me afterwards, and thanks again.'")
                    caller.db.quests["daycare"] = 1
                    return False
                elif user_input == "no":
                    caller.msg("Sabrina sighs and says to you, 'I understand, we're all busy.'")
                    caller.msg("Sabrina says to you, 'Come back if you change your mind.'")
                    return False
                else:
                    caller.msg("Sabrina says, 'Try just typing yes or no.'")                    
                    return True

            player.msg("Sabrina whirls on you quickly, seeming on the verge of yelling, or breaking down.")            
            player.msg("Sabrina says to you, 'Oh, you're not Tabitha.'")
            player.msg("Sabrina says to you, 'I love that girl, but my gods, she is a handful.'")
            player.msg("Sabrina sighs.")
            player.msg("Sabrina says to you, 'I used to send her to the Dwarven Daycare in town, which was great for her.'")
            player.msg("Sabrina says to you, 'But recently, some things that Tabitha told me made me question their ... curriculum.'")
            
            get_input(player, "Sabrina says to you, 'I'd like to send her back, but I'm nervous. Could you look into it for me?'", callback)            
            
        elif player.db.quests["daycare"] < 3:
            player.msg("Sabrina says to you, 'I hope you can find something out!'")
            
        elif player.db.quests["daycare"] == 3:
            player.msg("Sabrina says to you, 'Exploring scary tunnels and beating up naughty kids for fingerpaint, huh?'")
            player.msg("Sabrina sighs again. It's a wonder the woman has any air left in her.")
            player.msg("Sabrina says to you, 'Well, it's non-traditional, but for a girl with Tabitha's ... energy, it's probably perfect for her.'")
            player.msg("Sabrina says to you, 'Thanks again!'")
            player.experience_total += 2000
            player.msg("You gain 2,000 experience points!")
            player.db.quests["daycare"] = "done"

        self.stop()

       
class Mobile104Script(Script):
    """
    This is the script for Tabitha to lead you to the Smurf
    Village quest.
    """

    def at_script_creation(self):
        self.key = "m104_script"
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

class Mobile3600Script(Script):
    """
    This is the script for Henry the Gardener in the 
    Graveyard quest.
    """

    def at_script_creation(self):
        self.key = "m3600_script"
        self.desc = "Script for Henry the Gardener to handle Graveyard."
        self.persistent = True
        self.db.player = ""

    def quest_talk(self):
        player = self.db.player

        if not player.db.quests:
            player.db.quests = {}

        if "graveyard" not in player.db.quests:
            player.msg("Henry the Gardener says to you, 'Say, friend, I don't suppose you've noticed the dead being a little, uh, lively out there, have you?'")
            player.db.quests["graveyard"] = 1
        elif player.db.quests["graveyard"] == 1:
            player.msg("You explain to Henry the Gardener that the Marshal sent you.")
            player.msg("Henry the Gardener says to you, 'Ah, the Marshal, a good friend.'")
            player.msg("You gain 100 experience points!")
            player.experience_total += 100
            player.msg("Henry the Gardener chuckles nervously, though it is not at all clear what is funny about that.")
            player.msg("Henry the Gardener says to you, 'The truth is, I've not been out of this hut in days.'")
            player.msg("Henry the Gardener says to you, 'The dead have been a little ... uh ... active lately.'")
        
        if player.db.quests["graveyard"] == 1:
            player.msg("Henry the Gardener says to you, 'I'm not sure what's come over them, but they don't seem that sanguine about staying in the ground.'")
            player.msg("Henry the Gardener says to you, 'Though I guess, once you're as dried up as some of them, it's hard to be sanguine about much!'")
            player.msg("Henry the Gardener laughs exremely nervously, almost manically, at this.")
            player.msg("Henry the Gardener collects himself briefly.")
            player.msg("Henry the Gardener says to you, 'Anyways, I think that if you could kill five of the skeletons around these parts, I could probably get out safely.'")
            player.msg("Henry the Gardener says to you, 'Once you do, come back and talk to me again.'")
            player.msg("Henry the Gardener sits back, takes a long draw off a dark bottle, and shakes his head.")
            player.msg("Henry the Gardener says to you, 'Just steer clear of that ghastly ghoul, if you see it.'")
            player.msg("Henry the Gardener shudders violently.")
            player.db.quests["graveyard"] = 2

        elif 1 < player.db.quests["graveyard"] < 7:
            skeletons = 7 - player.db.quests["graveyard"]
            if skeletons == 1:
                skeleton_string = "one skeleton"
            else:
                skeleton_string = "%d skeletons" % skeletons
            player.msg("Henry the Gardener says to you, 'Looks as though you've made some progress, fella. Just %s to go.'" % skeleton_string)

        elif player.db.quests["graveyard"] == 7:
            player.msg("Henry the Gardener says to you, 'Well, done, fella! I suspect I can get out to see the Marshal now.'")
            player.msg("You gain 800 experience points!")
            player.experience_total += 800
            player.msg("Henry the Gardener says to you, 'You know, I busted up my good snow shovel to use in defense against those things if I had to.'")
            player.msg("Henry the Gardener says to you, 'Guess I won't need it now, but I suppose you might.'")
            
            # Load the shovel shield.
            shield = rules.make_object(player, False, "o3614")

            shield.db.level = 5
            shield.db.armor = rules.set_armor(shield.db.level)
            
            player.msg("Henry the Gardener hands you the shovel shield.")
            player.msg("Henry the Gardener says to you, 'Use it in good health, and if you take it in mind to go after that ghastly ghoul, come see me first.'")
            player.db.quests["graveyard"] = 8

        elif player.db.quests["graveyard"] == 8:
            player.msg("Henry the Gardener says to you, 'Back for more, eh? Well, that ghastly ghoul is pretty tough.'")
            player.msg("Henry the Gardener says to you, 'It seems to be sort of the boss of the undead in the graveyard.'")
            player.msg("Henry the Gardener says to you, 'My worry is that there is more beyond the graveyard, but let's worry about that another day.'")
            player.msg("Henry the Gardener says to you, 'If you can polish it off, I'll have some more gear for you.'")
            player.msg("Henry the Gardener says to you, 'Good luck, I guess?'")
            if player.sex == "male":
                mutter = "That boy is crazy."
            elif player.sex == "female":
                mutter = "That girl is crazy."
            else:
                mutter = "They are crazy."
            player.msg("As you turn to walk away, you hear Henry the Gardener mutter '%s'" % mutter)
            player.db.quests["graveyard"] = 9

        elif player.db.quests["graveyard"] == 10:
            player.msg("Henry the Gardener says to you, 'You are amazing! Polished off that ghastly ghoul, huh?'")
            player.msg("Henry the Gardener says to you, 'I watched you right out my window here.'")
            player.msg("Henry the Gardener says to you, 'Well, fair is fair, here's your reward.'")
            player.msg("Henry the Gardener says to you, 'I've crafted these out of the enchanted bones of the undead you've killed.'")
            player.msg("Henry the Gardener hands you a pair of bone leg guards.")

            # Load a pair of bone leg guards.
            guards = rules.make_object(player, False, "o3615")

            guards.db.level = 10
            guards.db.armor = rules.set_armor(guards.db.level)

            player.msg("Henry the Gardener says to you, 'I managed to reverse the magic on them, soooo, I hope you're not evil!'")
            player.msg("Henry the Gardener says to you, 'As I was afraid, there still seems to be undead out there.'")
            player.msg("Henry the Gardener says to you, 'Ah, well, come back when you want to take a shot at the Chapel Catacombs.'")
            player.msg("Henry the Gardener says to you, 'I have a feeling that's where the ultimate evil here is.'")
            player.db.quests["graveyard"] == "done"

        self.stop()


class Mobile3602Script(Script):
    """
    This is the death script for the ghastly ghoul in the
    Graveyard quest.
    """

    def at_script_creation(self):
        self.key = "m3602_script"
        self.desc = "Death script for ghastly ghoul in Graveyard."
        self.persistent = True
        self.db.player = ""

    def quest_death(self):
        player = self.db.player

        if not player.db.quests:
            player.db.quests = {}

        if "graveyard" in player.db.quests:
            if player.db.quests["graveyard"] == 9:
                player.db.quests["graveyard"] += 1

        self.stop()


class Mobile3603Script(Script):
    """
    This is the death script for a skeleton type 1 in the 
    Graveyard quest.
    """

    def at_script_creation(self):
        self.key = "m3603_script"
        self.desc = "Death script for skeleton type 1 in Graveyard."
        self.persistent = True
        self.db.player = ""

    def quest_death(self):
        player = self.db.player

        if not player.db.quests:
            player.db.quests = {}

        if "graveyard" in player.db.quests:
            if 1 < player.db.quests["graveyard"] < 7:
                player.db.quests["graveyard"] += 1
                
        self.stop()


class Mobile3604Script(Script):
    """
    This is the death script for a skeleton type 2 in the
    Graveyard quest.
    """

    def at_script_creation(self):
        self.key = "m3603_script"
        self.desc = "Death script for skeleton type 2 in Graveyard."
        self.persistent = True
        self.db.player = ""

    def quest_death(self):
        player = self.db.player

        if not player.db.quests:
            player.db.quests = {}

        if "graveyard" in player.db.quests:
            if 1 < player.db.quests["graveyard"] < 7:
                player.db.quests["graveyard"] += 1

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
                    caller.msg("Papa Smurf says to you, 'Finally, someone else responsible.'")
                    caller.msg("Papa Smurf says to you, 'As I say, just gather them up and put them away in my house.'")
                    caller.msg("Papa Smurf says to you, 'Hrm, you may need the key as well. I'm sure it's around somewhere.'")
                    caller.msg("Papa Smurf says to you, 'Don't forget to close the lid when you are done.'")
                    player.msg("Papa Smurf says to you, 'Don't worry, I'll know when you are done.'")
                    caller.db.quests["smurfs"] = 2

                elif "no" in user_input:
                    caller.msg("You decline to help Papa Smurf at the present time.")
                    caller.msg("Papa Smurf says to you, 'Perhaps another time.'")

            player.msg("Papa Smurf sighs, exhausted.")
            player.msg("Papa Smurf says to you, 'These kids these days.'")
            player.msg("Papa Smurf says to you, 'All I ask is that they put their toys away in my house when they are done.'")
            player.msg("Papa Smurf says to you, 'But can they do that? No.'")

            get_input(player, "Papa Smurf says to you, 'Can you gather up my children's toys and put them away?'", callback)

        elif player.db.quests["smurfs"] == 1:
            player.msg("You talk to Papa Smurf, and explain that Tabitha sent you.")
            player.msg("Papa Smurf says to you, 'Ah, wonderful!'")
            player.experience_total += 50
            player.msg("You gain 50 experience points!")
            player.msg("Papa Smurf sighs, exhausted.")
            player.msg("Papa Smurf says to you, 'I need you to help me by gathering up my children's toys and putting them away.'")
            player.msg("Papa Smurf says to you, 'Just gather them up and put them away in my house.'")
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

        
class Mobile6612Script(Script):
    """
    This is the script for the teacher in the Dwarven
    Daycare quest.
    """

    def at_script_creation(self):
        self.key = "m6612_script"
        self.desc = "Script for teacher to handle Dwarven Daycare."
        self.persistent = True
        self.db.player = ""

    def quest_talk(self):
        player = self.db.player

        if not player.db.quests:
            player.db.quests = {}

        if "daycare" in player.db.quests:
            if player.db.quests["daycare"] == 1:
                player.msg("The teacher begins writing tomorrow's lesson on the board for you.")
                player.msg("The teacher says to you, 'Butterflies are such beautiful creatures. For your homework get some paint. Then we can fingerpaint.'")
                player.msg("The teacher says to you, 'There should be some around the daycare somewhere.'")
                player.msg("You got your assignment, and 1000 experience points!")
                player.experience_total += 1000
                player.db.quests["daycare"] = 2
                
            elif player.db.quests["daycare"] == 2:
                player.msg("The teacher says to you, 'Well, where's your fingerpaint? Give it to me when you have some.'")

        self.stop()

    def quest_give(self):

        player = self.db.player
        receiver = self.obj
        given_object = self.db.given_object

        if "daycare" in player.db.quests:
            if player.db.quests["daycare"] > 2 or player.db.quests["daycare"] == "done":
                player.msg("The teacher says to you, 'One painting per student.'")
                player.msg("The teacher gives you a pot of fingerpaint.")                       
                given_object.location = player
            elif player.db.quests["daycare"] == 2:
                if given_object.db.vnum == "o6657":
                    player.msg("The teacher beams at you.")
                    player.msg("The teacher says to you, 'Good job, %s! You get an A!'" % player.key)
                    given_object.location = None
                    player.msg("The teacher sets you up with a blank sheet and some fingerpaint.")
                    player.msg("A whirl of fingerpaint, and a bunch of hand-washing later, and you have a fingerpainting of a butterfly!")
                    
                    # Load the fingerpainting.
                    fingerpainting = rules.make_object(player, False, "o6656")

                    fingerpainting.db.level = 7
                    
                    player.msg("The teacher says to you, 'Well done. Remember, the world is full of miracles. Butterflies are but one of them.")
                    player.msg("The teacher says to you, 'Enjoy your painting.'")
                    player.msg("You had probably better head back to Sabrina.")
                    player.db.quests["daycare"] = 3

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

