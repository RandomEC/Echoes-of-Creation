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
        tickerhandler.add(2, self.at_repeat)
        self.x = 1

    def at_stop(self):
        # Called just before the script is stopped/destroyed.
        for combatant in list(self.db.combatants.values()):
            # note: the list() call above disconnects list from database
            self._cleanup_combatant(combatant)

    def msg_all(self, message):
        "Send message to all combatants"
        for combatant in self.db.combatants:
            self.db.combatants[combatant]["combatant"].msg(message)

    def at_repeat(self):
        self.msg_all("This is pass number %s." % self.x)
        for combatant in self.db.combatants:
            attacker = self.db.combatants[combatant]["combatant"]
            victim = self.db.combatants[combatant]["target"]
            attack_output_string = rules_combat.do_attack(attacker, victim)
            print(attack_output_string)
            print("%s's current hitpoints are %d" % (victim, victim.hitpoints_current))
        
        self.x += 1
        if self.x > 4:
            self.at_stop()
            self.delete()

    
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
        dbref = combatant.id
        self.db.combatants[dbref] = {"combatant": combatant, "target": combatant_target}
        
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
        attacker.msg("And here.")
        combat = create_object("commands.combat_commands.Combat", key=("combat_handler_%s" % attacker.location.db.vnum))
        attacker.msg(combat.key)
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
