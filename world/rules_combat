import random

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

def get_damage(attacker, weapon_slot):
    if attacker.db.character_type == "mobile":
        damage_low = int(attacker.db.level*3/4)
        damage_high = int(attacker.dg.level*3/2)
        
        damage = random.randint(damage_low, damage_high)
        
        if attacker.db.eq_slots["wielded, primary"]:
            damage *= 1.5
 
    else:
        if attacker.db.eq_slots[weapon_slot]:
            weapon = attacker.db.eq_slots[weapon_slot]
            damage = random.randint(weapon.db.damage_low, weapon.db.damage_high)
        else:
            damage = random.randint(1, 2)*attacker.db.size   # Need to create a method to get character size from race.
    
    # Get damroll
    # Subtract damroll for other hand weapon, or both weapons, if can't use weapon

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
    hitskill = get_warskill(attacker) + attacker..get_modified_attribute("hitroll") + get_race_hitbonus(attacker, victim) + 10*(attacker.get_modified_attribute("dexterity") - 10)
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
