class Combat_2(Object):
    """
    
    This is the new class for instances of combat in rooms of the MUD.
    
    """

    def at_object_creation(self):
        # This will be a dictionary with key of combatant and value of target.
        self.db.combatants = {}
        self.db.rounds = 0
        self.x = 1
        tickerhandler.add(2, self.at_repeat)

    def at_stop(self):
        # Called just before the script is stopped/destroyed.
        for combatant in list(self.db.combatants.keys()):
            # note: the list() call above disconnects list from database,
            # needed because you are going to be removing things from the
            # combatants dictionary.
            self._cleanup_combatant(combatant)

    def change_target(self, attacker, victim):
        self.db.combatants[attacker] = victim

    def combat_end_check(self):
        """
        Checks to see whether the combat should end.
        """

        # Default is to end the combat.
        combat_end = True
        
        # Compile a list of all combatants.
        combatant_list = list(combatant for combatant in self.db.combatants)

        # Check to see what type of combatant the first one is, to check the remainder against
        if "mobile" in combatant_list[0].tags.all():
            first_combatant_type = "mobile"
        else:
            first_combatant_type = "player"

        # Cycle through combatants.
        for combatant in combatant_list:
            
            # Get the combatant type.
            if "mobile" in combatant.tags.all():
                combatant_type = "mobile"
            else:
                combatant_type = "player"

            # Check type against first one. If any awake combatants are different, set 
            # combat_end to False, and stop looking.
            if combatant_type != first_combatant_type and combatant.position != "sleeping":
                combat_end = False
                break;

        # If it should end after all that, stop the combat and delete the combat object.
        if combat_end == True:
            self.at_stop()
            self.delete()

    def combatant_add(self, combatant, combatant_target):

        # Add combatant to handler
        self.db.combatants[combatant] = combatant_target

        # set up back-reference
        self._combatant_init(combatant)

        # Wake up the target if they are asleep.
        if combatant_target.position != "standing":
            combatant_target.position = "standing"
            combatant_target.msg("An attack! You stand up to face your foe!")
            combatant_target.location.msg_contents("%s stands up to face %s foe!" % ((combatant_target.key[0].upper() + combatant_target.key[1:]),
                                                                                     rules.pronoun_possessive(combatant_target)
                                                                                     ), exclude=combatant_target)

    def _combatant_cleanup(self, combatant):
        """
        Remove combatant from handler and clean
        it of the back-reference.
        """
        del self.db.combatants[combatant]
        del combatant.ndb.combat_handler
    
    def _combatant_init(self, combatant):
        """
        This initializes handler back-reference.        
        """
        combatant.ndb.combat_handler = self
        
    def combatant_remove(self, combatant):
        "Remove combatant from handler"

        if combatant in self.db.combatants:
            self._combatant_cleanup(combatant)
            
    def find_other_attackers(self, seeking_target):
        """
        This method is called when the target of a
        combatant dies, to see if there is anyone else
        attacking that combatant. If so, it will automatically
        make that its new target, and return the target. If
        not, returns False
        """

        for combatant in self.db.combatants:
            if self.db.combatants[combatant]["target"] == seeking_target:
                self.db.combatants[seeking_target]["target"] = combatant
                return combatant

        return False

    def get_target(self, attacker):
        return self.db.combatants[attacker]
        
    def at_repeat(self):

        # Copy the dictionary, in case changes are made to it during the round.
        # combat_dict = dict(self.db.combatants)
        round_combatants_list = list(combatant for combatant in self.db.combatants)

        # All at_repeat handles is whose turn it is in this round of combat. Everything
        # else is handled in rules_combat.
        for combatant in round_combatants_list:
            
            # First, check to make sure that combatant is still in the combat at this point.
            if combatant in self.db.combatants:

                rules_combat.do_one_character_combat_turn(attacker, victim, self)

        # At the end of the round, if the player and their target are still alive, and in combat,
        # tell them the status of their target.
        for combatant in round_combatants_list:
            
            # Combatant is in the combat, and a player (no point in output to mobiles).
            if combatant in self.db.combatants and "player" in combatant.tags.all():
                
                # Target's location is the same as combat.
                if self.db.combatants[combatant].location == self.location:
                    target = self.db.combatants[combatant]
                    combat_message = ("%s %s\n" % ((target.key[0].upper() + target.key[1:]), rules_combat.get_health_string(target)))
                    combatant.msg(combat_message)

                    if "wait_state" not in combatant.ndb.all:
                        prompt_wait = "|gReady!|n"
                    elif combatant.ndb.wait_state >= 12:
                        prompt_wait = "|rCompleting action!"
                    elif combatant.ndb.wait_state > 0:
                        prompt_wait = "|yRecovering.|n"
                    else:
                        prompt_wait = "|gReady!|n"
                    prompt = "<|r%d|n/|R%d hp |b%d|n/|B%d mana |y%d|n/|Y%d moves|n %s>\n" % (combatant.hitpoints_current,
                                                                                             combatant.hitpoints_maximum,
                                                                                             combatant.mana_current,
                                                                                             combatant.mana_maximum,
                                                                                             combatant.moves_current,
                                                                                             combatant.moves_maximum,
                                                                                             prompt_wait)
                    combatant.msg(prompt=prompt)

# SEND THIS TO DEATH

        if combatant.hitpoints_current <= 0 and "player" in combatant.tags.all():

            # Reset dead players to one hitpoint, and move to home. Mobile hitpoints will get reset by reset
            # function.
            combatant.db.hitpoints["damaged"] = (combatant.hitpoints_maximum - 1)
            combatant.move_to(combatant.home, quiet=True)

# DOWN TO HERE.            
            
        if self.db.combatants:
            self.db.rounds += 1

            self.combat_end_check()

        if self.db.combatants:
            # Check to see if any other mobiles in the room jump in before the next round.

            # Get all possible assisting mobiles.
            possible_assists = []
            for object in self.location.contents:
                if "mobile" in object.tags.all():
                    if not object.ndb.combat_handler:
                        possible_assists.append(object)

            # Get players that are in combat.
            possible_targets = []
            for combatant in self.db.combatants:
                if "player" in combatant.tags.all():
                    possible_targets.append(combatant)

            # Run through possible assisting mobiles.
            for candidate in possible_assists:

                # Get a random seen player from those found.
                seen_targets = []
                for target in possible_targets:
                    if rules.can_see(target, candidate):
                        seen_targets.append(target)
                if seen_targets:
                    random_player = seen_targets[random.randint(0, (len(seen_targets) - 1))]
                    if (candidate.level - 7) < random_player.level < (candidate.level + 7) and not (
                            random_player.alignment > 333 and candidate.alignment > 333):
                        to_be_assisted = self.db.combatants[random_player]["target"]
                        if candidate.db.vnum == to_be_assisted.db.vnum:
                            self.add_combatant(candidate, random_player)
                            break
                        elif random.randint(1, 8) == 1:
                            self.add_combatant(candidate, random_player)
                            break


                            
                            
                            
                            
                            
                            
                            
################# NEW COMBAT RULES ##############################

def do_one_character_combat_turn(attacker, victim, combat):
    """
    This handles everything that needs to happen in one round of
    combat for a character.
    """


    # Do base attacks.
    if victim.hitpoints_current > 0 and victim.location == attacker.location:
        new_attacker_string, new_victim_string, new_room_string = \
            do_one_weapon_attacks(attacker, victim, "wielded, primary")
        attacker_string += new_attacker_string
        victim_string += new_victim_string
        room_string += new_room_string
    
    # Check for dual wield.
    if victim.hitpoints_current > 0 and victim.location == attacker.location:
        if attacker.db.eq_slots["wielded, primary"] and \
                attacker.db.eq_slots["wielded, secondary"]:
            new_attacker_string, new_victim_string, new_room_string = \
                do_one_weapon_attacks(attacker, victim, "wielded, secondary")
            attacker_string += new_attacker_string
            victim_string += new_victim_string
            room_string += new_room_string

    if victim.hitpoints_current <= 0 and victim.location == attacker.location:
        new_attacker_string, new_victim_string, new_room_string = \
            do_death(attacker, victim)
        attacker_string += new_attacker_string
        victim_string += new_victim_string
        room_string += new_room_string

    # In combat handler, need to use these strings to create the full output
    # block reporting the results of everyone's attacks to all players only.
    return (attacker_string, victim_string, room_string)


def do_one_weapon_attacks(attacker, victim, eq_slot):
    """
    This determines how many hit attempts will occur for one attacker
    against one victim, with one weapon slot, and then calls do_attack
    for each. It assembles the output for each hit attempt for the
    attacker, victim and those in the room, and returns a tuple of
    those values.
    """
    attacker_string = ""
    victim_string = ""
    room_string = ""

    # If primary weapon, first hit is free.
    if victim.hitpoints_current > 0 and victim.location == attacker.location:
        if eq_slot == "wielded, primary":
            attacker_string, victim_string, room_string = do_attack(attacker,
                                                                    victim,
                                                                    eq_slot
                                                                    )
        else:
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    attacker_string, victim_string, room_string = \
                        do_attack(attacker, victim, eq_slot)
            else:
                # Save hero for dual skill implementation.
                pass

    # Check for second attack.
    if victim.hitpoints_current > 0 and victim.location == attacker.location:
        if eq_slot == "wielded, primary":
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    new_attacker_string, new_victim_string, new_room_string = \
                        do_attack(attacker, victim, eq_slot)
                    attacker_string += new_attacker_string
                    victim_string += new_victim_string
                    room_string += new_room_string
            else:
                # Wait to build out hero until skills built
                pass
        else:
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    new_attacker_string, new_victim_string, new_room_string = \
                        do_attack(attacker, victim, eq_slot)
                    attacker_string += new_attacker_string
                    victim_string += new_victim_string
                    room_string += new_room_string
            else:
                # Wait to build out hero until skills built
                pass

    # Check for third attack.
    if victim.hitpoints_current > 0 and victim.location == attacker.location:
        if eq_slot == "wielded, primary":
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    new_attacker_string, new_victim_string, new_room_string = \
                        do_attack(attacker, victim, eq_slot)
                    attacker_string += new_attacker_string
                    victim_string += new_victim_string
                    room_string += new_room_string
            else:
                # Wait to build out hero until skills built
                pass
        else:
            if "mobile" in attacker.tags.all():
                if random.randint(1, 100) < attacker.db.level:
                    new_attacker_string, new_victim_string, new_room_string = \
                        do_attack(attacker, victim, eq_slot)
                    attacker_string += new_attacker_string
                    victim_string += new_victim_string
                    room_string += new_room_string
            else:
                # Wait to build out hero until skills built
                pass

    # Check for fourth attack, for mobiles only.
    if victim.hitpoints_current > 0 and victim.location == attacker.location:
        if "mobile" in attacker.tags.all():
            if random.randint(1, 100) < (attacker.db.level / 2):
                new_attacker_string, new_victim_string, new_room_string = \
                    do_attack(attacker, victim, eq_slot)
                attacker_string += new_attacker_string
                victim_string += new_victim_string
                room_string += new_room_string

    return (attacker_string, victim_string, room_string)

