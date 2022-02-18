import random
from world import rules_race

def check_death(victim):
    """
    This checks for death of the victim, and, if it finds a death, returns
    a boolean True.
    """
    if victim.hitpoints_current <= 0:
        return True
    else:
        return False
        
def do_all_attacks(attacker, victim):
    """
    This calls do_attack_round for all relevant weapon slots for one
    attacker on one victim, which should be ALL attacks for that
    attacker.
    """
    
    attacker_string, victim_string, room_string = do_attack_round(attacker, victim, "wielded, primary")
    
    if attacker.db.eq_slots["wielded, primary"] and attacker.db.eq_slots["wielded, secondary"]:
        new_attacker_string, new_victim_string, new_room_string = do_attack_round(attacker, victim, "wielded, secondary")
        attacker_string += new_attacker_string
        victim_string += new_victim_string
        room_string += new_room_string
    
    if check_death(victim):
        # Build a string for reporting death to characters, and add to output strings.
        attacker_string += ("With your final %s, %s falls to the ground, DEAD!!!" % (get_damagetype(attacker), victim.key))
        victim_string += "You have been KILLED!!!"
        room_string += ("%s has been KILLED by %s!!!" % ((victim.key[0].upper() + victim.key[1:0]), attacker.key))
                
        if "mobile" in victim.tags.all():
            # Create corpse.
            corpse = create_object("objects.NPC_Corpse", key=("corpse of %s" % victim.key))
            corpse.desc = ("The corpse of %s lies here." % victim.key)
            
            # Move all victim items to corpse.
            for item in victim.contents:
                if item.equipped:
                    item.remove_from(victim)
                # Eventually, will want the below to have , quiet = True after done testing.
                item.move_to(corpse)
            
            # Move victim to None location to be reset later.
            victim.location = None
            
            # Reinstate base spell affects.
            victim.db.spell_affects = victim.db.spell_affects_reset
            
            # Refill hitpoints.
            victim.db.hitpoints["damaged"] = 0
            
            # Award xp.
            attacker.db.experience_total += victim.db.experience_current
            attacker_string += ("You receive %s experience as a result of your kill!" % victim.db.experience_current)
            
            # Figure out how to calculate gold on mobile and award.
            
            # attacker_string += ("You receive |y%s gold|n as a result of your kill!" % victim.)
        
        else:
            # Create corpse.
            corpse = create_object("objects.PC_Corpse", key=("corpse of %s" % victim.key))
            corpse.desc = ("The corpse of %s lies here." % victim.key)
            
            # Heroes keep their items.
            
            # Move hero to their home location.
            victim.move_to(victim.home, quiet=True)
            
            # Clear spell affects.
            victim.db.spell_affects = {}
            
            # Refill hitpoints.
            victim.db.hitpoints["damaged"] = 0
            
            # Do xp penalty, after figuring out how much it should be.
            # victim_string += ("You lose %s experience as a result of your death! %s 
            
            # Do gold penalty, after figuring out how much it should be.
    
    # In combat handler, need to use these strings to create the full output block
    # reporting the results of everyone's attacks to all players only.
    return (attacker_string, victim_string, room_string)

def do_attack(attacker, victim):
    """
    This function implements the effects of a single hit. It
    both calls the take_damage method on the victim, doing the
    damage, and returns a tuple of strings of output for the
    attacker, the victim, and those watching in the room for
    that single hit attempt.
    """
    
    hit = True
    damage = 6
    damage_type = get_damagetype(attacker)

    attacker.msg("In do_attack.")

    if hit:
        victim.take_damage(damage)
        attacker_string = ("You |g%s|n %s with your %s." % (get_damagestring("attacker", damage), victim.key, damage_type))
        victim_string = ("%s |r%s|n you with its %s." % (attacker.key, get_damagestring("victim", damage), damage_type))
        room_string = ("%s %s %s with its %s." % (attacker.key, get_damagestring("victim", damage), victim.key, damage_type))
    else:
        return "You miss %s with your %s." % (victim.key, damage_type)

    return (attacker_string, victim_string, room_string)

def do_attack_round(attacker, victim, eq_slot):
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
    if eq_slot == "wielded, primary":
        attacker_string, victim_string, room_string = do_attack(attacker, victim)
    else:
        if "mobile" in attacker.tags.all():
            if random.randint(1, 100) < attacker.db.level:
                attacker_string, victim_string, room_string = do_attack(attacker, victim)
        else:
            # Save hero for dual skill implementation.
            pass
    
    # Check for second attack.
    if eq_slot == "wielded, primary":
        if "mobile" in attacker.tags.all():
            if random.randint(1, 100) < attacker.db.level:
                new_attacker_string, new_victim_string, new_room_string = do_attack(attacker, victim, eq_slot)
                attacker_string += new_attacker_string
                victim_string += new_victim_string
                room_string += new_room_string
        else:
            # Wait to build out hero until skills built
            pass
    if eq_slot == "wielded, secondary":
        if "mobile" in attacker.tags.all():
            if random.randint(1, 100) < attacker.db.level:
                new_attacker_string, new_victim_string, new_room_string = do_attack(attacker, victim, eq_slot)
                attacker_string += new_attacker_string
                victim_string += new_victim_string
                room_string += new_room_string
        else:
            # Wait to build out hero until skills built
            pass
        

    # Check for third attack.
    if eq_slot == "wielded, primary":
        if "mobile" in attacker.tags.all():
            if random.randint(1, 100) < attacker.db.level:
                new_attacker_string, new_victim_string, new_room_string = do_attack(attacker, victim, eq_slot)
                attacker_string += new_attacker_string
                victim_string += new_victim_string
                room_string += new_room_string
        else:
            # Wait to build out hero until skills built
            pass
    if eq_slot == "wielded, secondary":
        if "mobile" in attacker.tags.all():
            if random.randint(1, 100) < attacker.db.level:
                new_attacker_string, new_victim_string, new_room_string = do_attack(attacker, victim, eq_slot)
                attacker_string += new_attacker_string
                victim_string += new_victim_string
                room_string += new_room_string
        else:
            # Wait to build out hero until skills built
            pass
    
    # Check for fourth attack, for mobiles only.
    if "mobile" in attacker.tags.all():
        if random.randint(1,100) < (attacker.db.level / 2):
            new_attacker_string, new_victim_string, new_room_string = do_attack(attacker, victim, eq_slot)
            attacker_string += new_attacker_string
            victim_string += new_victim_string
            room_string += new_room_string
            
    return (attacker_string, victim_string, room_string)

def do_damage(attacker, eq_slot):
    """
    This is called on a successful hit, and returns the total
    damage for that hit.
    """
    
    if "mobile" in attacker.tags.all():
        damage_low = int(attacker.db.level*3/4)
        damage_high = int(attacker.db.level*3/2)
        
        # Damage is a random number between high damage and low damage.
        damage = random.randint(damage_low, damage_high)
        
        # If mobile is wielding a weapon, they get a 50% bonus.
        if attacker.db.eq_slots["wielded, primary"]:
            damage = int(damage * 1.5)

        # Get a bonus to damage from damroll.
        dam_bonus = int(attacker.damroll)
        
        damage += dam_bonus

    else:
        if attacker.db.eq_slots[eq_slot]:
            weapon = attacker.db.eq_slots[eq_slot]
            damage = random.randint(weapon.db.damage_low, weapon.db.damage_high)
        
            dam_bonus = int(attacker.damroll)
            
            # You only get the damroll bonus for the weapon you are using
            # on the attack. As a result, we subtract out the damroll
            # from the weapon not being used in the attack, if there is
            # more than one.
            
            if eq_slot == "wielded, primary":
                if attacker.db.eq_slots["wielded, secondary"]:
                    eq = attacker.db.eq_slots["wielded, secondary"]
                    dam_bonus -= eq.db.stat_modifiers["damroll"]
            else: 
                eq = attacker.db.eq_slots["wielded, secondary"]
                dam_bonus -= eq.db.stat_modifiers["damroll"]
                        
            damage += dam_bonus
            
        else:
            damage = random.randint(1, 2)*attacker.size
    
            # Get a bonus to damage from damroll, since we got here, there is no
            # weapon to worry about.
            dam_bonus = attacker.damroll
            
            damage += dam_bonus
    
    return damage

def do_single_hit(attacker, victim):
    """
    This function simply evaluates whether the attempted hit actually
    hits.
    """
    
    hit_chance = get_hit_chance(attacker, victim)
    if random.randint(1,100) <= hit_chance:
        return True
    else:
        return False

def get_avoidskill(victim):
    if victim.get_affect_status("blindness"):
        blind_penalty = 60
    else:
        blind_penalty = 0

    avoidskill = get_warskill(victim) + (100 - get_ac(victim)/3) - blind_penalty + 10*(victim.get_modified_attribute("dexterity") - 10)
    if avoidskill > 1:
        return avoidskill
    else:
        return 1

def get_damagestring(combatant, damage):
    if combatant == "attacker":
        if damage < 1:
            damagestring = "miss"
        elif damage < 4:
            damagestring = "scratch"
        elif damage < 7:
            damagestring = "graze"
        elif damage < 10:
            damagestring = "bruise"
        elif damage < 13:
            damagestring = "injure"
        elif damage < 16:
            damagestring = "wound"
        elif damage < 22:
            damagestring = "clobber"
        elif damage < 28:
            damagestring = "maul"
        elif damage < 34:
            damagestring = "devastate"
        elif damage < 43:
            damagestring = "MUTILATE"
        elif damage < 52:
            damagestring = "MASSACRE"
        elif damage < 61:
            damagestring = "DISEMBOWEL"
        elif damage < 70:
            damagestring = "EVISCERATE"
        elif damage < 82:
            damagestring = "do EXTRAORDINARY damage to"
        elif damage < 94:
            damagestring = "***OBLITERATE***"
        elif damage < 118:
            damagestring = "***DEMOLISH***"
        elif damage < 142:
            damagestring = "***SLAUGHTER***"
        elif damage < 166:
            damagestring = "do TERRIFIC damage to"
        elif damage < 201:
            damagestring = "***PULVERIZE***"
        elif damage < 236:
            damagestring = "***>PULVERIZE<***"
        elif damage < 271:
            damagestring = "do HORRIFIC damage to"
        elif damage < 323:
            damagestring = "do unspeakable things to"
        elif damage < 375:
            damagestring = "do UNSPEAKABLE things to"
        elif damage < 427:
            damagestring = "do incredible damage to"
        elif damage < 503:
            damagestring = "do INCREDIBLE damage to"
        elif damage < 579:
            damagestring = "do unbelievable damage to"
        elif damage < 664:
            damagestring = "do UNBELIEVABLE damage to"
        elif damage < 749:
            damagestring = "do inconceivable damage to"
        elif damage < 846:
            damagestring = "do INCONCEIVABLE damage to"
        elif damage < 1000:
            damagestring = "do colossal damage to"
        elif damage < 1220:
            damagestring = "do COLOSSAL damage to"
        elif damage < 2105:
            damagestring = "do GHASTLY damage to"
        elif damage < 3007:
            damagestring = "do HORRENDOUS damage to"
        elif damage < 3846:
            damagestring = "do PHENOMENAL damage to"
        elif damage < 7981:
            damagestring = "do MIND-NUMBING damage to"
        elif damage < 16404:
            damagestring = "do OBSCENE damage to"
        elif damage < 32097:
            damagestring = "do EARTH-SHATTERING damage to"
        else:
            damagestring = "**>*>*>*VAPORIZE*<*<*<**"
    if combatant == "victim":
        if damage < 1:
            damagestring = "misses"
        elif damage < 4:
            damagestring = "scratches"
        elif damage < 7:
            damagestring = "grazes"
        elif damage < 10:
            damagestring = "bruises"
        elif damage < 13:
            damagestring = "injures"
        elif damage < 16:
            damagestring = "wounds"
        elif damage < 22:
            damagestring = "clobbers"
        elif damage < 28:
            damagestring = "mauls"
        elif damage < 34:
            damagestring = "devastates"
        elif damage < 43:
            damagestring = "MUTILATES"
        elif damage < 52:
            damagestring = "MASSACRES"
        elif damage < 61:
            damagestring = "DISEMBOWELS"
        elif damage < 70:
            damagestring = "EVISCERATES"
        elif damage < 82:
            damagestring = "does EXTRAORDINARY damage to"
        elif damage < 94:
            damagestring = "***OBLITERATES***"
        elif damage < 118:
            damagestring = "***DEMOLISHES***"
        elif damage < 142:
            damagestring = "***SLAUGHTERS***"
        elif damage < 166:
            damagestring = "does TERRIFIC damage to"
        elif damage < 201:
            damagestring = "***PULVERIZES***"
        elif damage < 236:
            damagestring = "***>PULVERIZES<***"
        elif damage < 271:
            damagestring = "does HORRIFIC damage to"
        elif damage < 323:
            damagestring = "does unspeakable things to"
        elif damage < 375:
            damagestring = "does UNSPEAKABLE things to"
        elif damage < 427:
            damagestring = "does incredible damage to"
        elif damage < 503:
            damagestring = "does INCREDIBLE damage to"
        elif damage < 579:
            damagestring = "does unbelievable damage to"
        elif damage < 664:
            damagestring = "does UNBELIEVABLE damage to"
        elif damage < 749:
            damagestring = "does inconceivable damage to"
        elif damage < 846:
            damagestring = "does INCONCEIVABLE damage to"
        elif damage < 1000:
            damagestring = "does colossal damage to"
        elif damage < 1220:
            damagestring = "does COLOSSAL damage to"
        elif damage < 2105:
            damagestring = "does GHASTLY damage to"
        elif damage < 3007:
            damagestring = "does HORRENDOUS damage to"
        elif damage < 3846:
            damagestring = "does PHENOMENAL damage to"
        elif damage < 7981:
            damagestring = "does MIND-NUMBING damage to"
        elif damage < 16404:
            damagestring = "does OBSCENE damage to"
        elif damage < 32097:
            damagestring = "does EARTH-SHATTERING damage to"
        else:
            damagestring = "**>*>*>*VAPORIZES*<*<*<**"

    return damagestring

def get_damagetype(attacker):
    if attacker.db.eq_slots["wielded, primary"]:
        weapon = attacker.db.eq_slots["wielded, primary"]
        damagetype = weapon.db.weapon_type
    else:
        if "damage message" in rules_race.get_race(attacker.race):
            damagetype = rules_race.get_race(attacker.race)["damage message"]
        else:
            damagetype = "punch"

    return damagetype

def get_hit_chance(attacker, victim):
    hit_chance = int(100 * (get_hitskill(attacker, victim) + attacker.db.level - victim.db.level)/(get_hitskill(attacker, victim) + get_avoidskill(victim)))
    if hit_chance > 95:
        return 95
    elif hit_chance < 5:
        return 5
    else:
        return hit_chance

def get_hitskill(attacker, victim):
    # Make sure that hitroll does not include hitroll from weapon if can't wield it.
    hitskill = get_warskill(attacker) + attacker.hitroll + get_race_hitbonus(attacker, victim) + 10*(attacker.dexterity - 10)
    if hitskill > 1:
        return hitskill
    else:
        return 1

def get_race_hitbonus(attacker, victim):
    hitbonus = victim.size - attacker.size
    return hitbonus

def get_warskill(combatant):
    if combatant.db.type == "mobile":
        warskill_factor = combatant.db.level/101
        warskill = int(120*warskill_factor)
        return warskill
    else:
        # Will eventually deal with variable player warskill based on
        # class-type skills learned.
        warskill_factor = combatant.db.level/101
        warskill = int(120*warskill_factor)
        return warskill


            
            
