import random
from world import rules_race

def do_attack(attacker, victim):
    hit = True
    damage = 1
    
    if hit:
        victim.take_damage(damage)
        return "%s does %d damage to %s" % (attacker.key.capitalize(), damage, victim.key)
    else:
        return "%s misses %s" % (attacker.key.capitalize(), victim.key)

def do_damage(attacker, weapon_slot):
    
    if "mobile" in attacker.tags.all():
        damage_low = int(attacker.db.level*3/4)
        damage_high = int(attacker.db.level*3/2)
        
        # Damage is a random number between high damage and low damage.
        damage = random.randint(damage_low, damage_high)
        
        # If mobile is wielding a weapon, they get a 50% bonus.
        if attacker.db.eq_slots["wielded, primary"]:
            damage *= 1.5

        # Get a bonus to damage from damroll.
        dam_bonus = attacker.damroll
        
        damage += dam_bonus

    else:
        if attacker.db.eq_slots[weapon_slot]:
            weapon = attacker.db.eq_slots[weapon_slot]
            damage = random.randint(weapon.db.damage_low, weapon.db.damage_high)
        
            dam_bonus = attacker.damroll
            
            # Subtract out damroll from weapon not being used in the attack, if
            # more than one.
            if weapon_slot == "wielded, primary":
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
    hit_chance = get_hit_chance(attacker, victim)
    if random.randint(1,100) <= hit_chance:
        return True
    else:
        return False
    
def get_ac(combatant): # MOVE THIS TO CHARACTER CLASS FETCH COMMAND
    if combatant.db.type == "mobile":
        # On CA, mobile armor was interpolated between 100 and -400
        ac = 100 + int((combatant.level-1)*(-500)/100)
    else:
        return combatant.get_modified_attribute("armor class")

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

def get_damagestring(attacker, victim, damage):
    if "mobile" in victim.tags.all():
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
    if "player" in victim.tags.all():
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
    hitskill = get_warskill(attacker) + attacker.get_modified_attribute("hitroll") + get_race_hitbonus(attacker, victim) + 10*(attacker.get_modified_attribute("dexterity") - 10)
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


            
            
