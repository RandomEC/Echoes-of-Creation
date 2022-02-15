from commands.command import MuxCommand
from typeclasses.objects import Object
from world import rules_combat

class Combat(Object):
    """
    
    This is the class for instances of combat in rooms of the MUD.
    
    """
    from evennia import TICKER_HANDLER as tickerhandler
    
    def at_object_creation(self):
        self.db.combatants = {}
        self.db.rounds = 0
        tickerhandler.add(2, self.at_repeat)
    
    def at_repeat(self):
        pass
    
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
    
    def at_repeat(self):
        """
        This is called every self.interval seconds (turn timeout) or
        when force_repeat is called (because everyone has entered their
        commands). We know this by checking the existence of the
        `normal_turn_end` NAttribute, set just before calling
        force_repeat.

        """
        if self.ndb.normal_turn_end:
            # we get here because the turn ended normally
            # (force_repeat was called) - no msg output
            del self.ndb.normal_turn_end
        else:
            # turn timeout
            self.msg_all("Turn timer timed out. Continuing.")
        self.end_turn()

    # Combat-handler methods

    def add_combatant(self, combatant, combatant_target):
        "Add combatant to handler"
        dbref = combatant.id
        self.db.combatants[dbref] = {"combatant":combatant, "target":combatant_target}
        
        # set up back-reference
        self._init_combatant(combatant)

    def _cleanup_combatant(self, combatant):
        """
        Remove combatant from handler and clean
        it of the back-reference.
        """
        dbref = character.id
        del self.db.combatants[dbref]
        del combatant.ndb.combat_handler
        
    def remove_combatant(self, combatant):
        "Remove combatant from handler"
        if combatant.id in self.db.combatants:
            self._cleanup_combatant(combatant)
        if not self.db.combatants:
            # if no more combatants in battle, kill this handler
            self.stop()

    def msg_all(self, message):
        "Send message to all combatants"
        for character in self.db.characters.values():
            character.msg(message)



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

    def create_combat(attacker, victim):
        """Create a combat, if needed"""
        combat = Combat()
        combat.add_combatant(attacker, victim)
        combat.add.combatant(victim, attacker)
        combat.db.location = attacker.location
        combat.key = ("combat_handler_%s" % attacker.location.vnum)

    def func(self):
        """Implement attack"""

        attacker = self.caller
        if not self.args:
            attacker.msg("Usage: attack <mobile>")
            return

        victim = attacker.search(self.args, location=caller.location)
        if not victim:
            attacker.msg("There is no %s here to attack. % self.args)
            return
        elif "player" in victim.tags.all():
            attacker.msg("You cannot attack another player!")
            return

        if attacker.db.combat_handler or victim.db.combat_handler:
            pass
        else:
            create_combat(attacker, victim)
