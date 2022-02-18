from evennia import create_object
from evennia import TICKER_HANDLER as tickerhandler
from commands.command import MuxCommand
from typeclasses.objects import Object
from world import rules_combat


class Combat(Object):
    """
    
    This is the class for instances of combat in rooms of the MUD.
    
    """

    def at_object_creation(self):
        self.db.combatants = {}
        self.db.rounds = 0
        self.x = 1
        tickerhandler.add(2, self.at_repeat)

    def at_stop(self):
        # Called just before the script is stopped/destroyed.
        for dbref in list(self.db.combatants.values()):
            # note: the list() call above disconnects list from database
            combatant = dbref["combatant"]
            self._cleanup_combatant(combatant)

    def msg_all(self, message):
        "Send message to all combatants"
        for combatant in self.db.combatants:
            self.db.combatants[combatant]["combatant"].msg(message)

    def at_repeat(self):
        self.msg_all("This is pass number %s." % self.x)
        self.clear_messages()
        for combatant in self.db.combatants:
            attacker = self.db.combatants[combatant]["combatant"]
            victim = self.db.combatants[combatant]["target"]
            attacker_string, victim_string, room_string = rules_combat.do_attack_round(attacker, victim, "wielded, primary")
            attacker.msg("Past do_attack_round.")
            self.db.combatants[attacker]["combat message"] += (attacker_string + "\n")
            self.db.combatants[victim]["combat message"] += (victim_string + "\n")
            for combatant in self.db.combatants:
                if combatant != attacker and combatant != victim:
                    self.db.combatants[combatant]["combat message"] += (room_string + "\n")

        for combatant in self.db.combatants:
            if "player" in combatant.tags.all():
                combatant.msg(self.db.combatants[combatant]["combat message"])

        self.x += 1
        if self.x > 4:
            self.at_stop()
            self.delete()

    def clear_messages(self):
        for combatant in self.db.combatants:
            self.db.combatants[combatant]["combat message"] = ""

    def _init_combatant(self, combatant):
        """
        This initializes handler back-reference.        
        """
        combatant.ndb.combat_handler = self
    
    # Note: Another way to implement a combat handler would be to use a normal
    # Python object and handle time-keeping with the TickerHandler. This would
    # require either adding custom hook methods on the character or to implement
    # a custom child of the TickerHandler class to track turns. Whereas the
    # TickerHandler is easy to use, a Script offers more power in this case.
    
    # Combat-handler methods

    def add_combatant(self, combatant, combatant_target):
        # Add combatant to handler
        self.db.combatants[combatant] = {"combatant": combatant, "target": combatant_target, "combat message": ""}

        # set up back-reference
        self._init_combatant(combatant)

    def _cleanup_combatant(self, combatant):
        """
        Remove combatant from handler and clean
        it of the back-reference.
        """
        dbref = combatant.id
        del self.db.combatants[dbref]
        del combatant.ndb.combat_handler
        
    def remove_combatant(self, combatant):
        "Remove combatant from handler"
        if combatant.id in self.db.combatants:
            self._cleanup_combatant(combatant)
        if not self.db.combatants:
            # if no more combatants in battle, kill this handler
            self.stop()

class CmdAttack(MuxCommand):
    """
    Start combat against a mobile target.
    Usage:
      attack <mobile>
    Starts the default attacks rounds that occur in combat.
    """

    key = "attack"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def create_combat(self, attacker, victim):
        """Create a combat, if needed"""
        combat = create_object("commands.combat_commands.Combat", key=("combat_handler_%s" % attacker.location.db.vnum))
        combat.add_combatant(attacker, victim)
        combat.add_combatant(victim, attacker)
        combat.location = attacker.location
        combat.desc = "This is a combat instance."

    def func(self):
        """Implement attack"""

        attacker = self.caller
        if not self.args:
            attacker.msg("Usage: attack <mobile>")
            return

        victim = attacker.search(self.args, location=attacker.location)
        if not victim:
            attacker.msg("There is no %s here to attack." % self.args)
            return
        elif "player" in victim.tags.all():
            attacker.msg("You cannot attack another player!")
            return

        if attacker.db.combat_handler or victim.db.combat_handler:
            pass
        else:
            self.create_combat(attacker, victim)
