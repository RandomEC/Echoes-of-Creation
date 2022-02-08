from commands.command import MuxCommand

class CmdWear(MuxCommand):
    """
    Wear armor that is in your inventory. Weapons cannot be equipped this
    way, you need to use wield.
    
    Usage:
      wear <obj>
      
    Takes an object from your inventory and puts it in the appropriate wear
    slot.
    """

    key = "wear"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        if not self.args:
            caller.msg("What do you want to wear?")
            return
        
        eq = caller.search(self.args, location=caller)

        if not eq:
            caller.msg("You do not appear to have a %s." % self.args)
            return
        if caller == eq:
            caller.msg("You can't wear yourself.")
            return
        
        # check to make sure equipment has valid wear location. Need to check wrist, neck and
        # finger separately as there are two wear locations for each in the character.db.eq_slots
        # dictionary.
        
        wear_location = eq.db.wear_location
        
        if wear_location == "wield":
            caller.msg("You cannot wear a weapon. Wield it instead.")
            return
        elif not (wear_location in caller.db.eq_slots.keys() or wear_location == "wrist" or wear_location == "finger" or wear_location == "neck"):
            
            caller.msg("That cannot be worn.")
            return
        
        # check to make sure character is not already wearing the equipment.
        
        if eq.db.equipped:
            caller.msg("You are already wearing that!")
            return
        
        # check for whether character is high enough level to wear

        if not eq.access(caller, "equip"):
            if eq.db.get_err_msg:
                caller.msg(eq.db.get_err_msg)
            else:
                caller.msg("You can't wear equipment more than five levels above your level.")
            return

        # calling at_before_get hook method
       # if not obj.at_before_get(caller):
       #     return

        success = eq.wear_to(caller)
        if not success:
            caller.msg("You cannot wear this.")
        else:
            if(caller.db.sex == "male"):
                possessive = "his"
            elif(caller.db.sex == "female"):
                possessive = "her"
            else:
                possessive = "its"
            
            wear_location = eq.db.wear_location
            
            if wear_location == "light":
                room_wear_string = "%s holds %s as a %s." % (caller.name, eq.name, wear_location)
                self_wear_string = "You hold %s as a %s." % (eq.name, wear_location)
            elif wear_location == "neck" or wear_location == "wrist" or wear_location == "waist":
                room_wear_string = "%s wears %s around %s %s." % (caller.name, eq.name, possessive, wear_location)
                self_wear_string = "You wear %s around your %s." % (eq.name, wear_location)
            elif wear_location == "about body":
                room_wear_string = "%s wears %s about %s body." % (caller.name, eq.name, possessive)
                self_wear_string = "You wear %s about your body." % (eq.name)
            elif wear_location == "pride":
                room_wear_string = "%s pins on %s and wears it with pride." % (caller.name, eq.name)
                self_wear_string = "You pin on %s and wear it with pride." % (eq.name)
            elif wear_location == "shield":
                room_wear_string = "%s holds %s as a shield." % (caller.name, eq.name)
                self_wear_string = "You hold %s as a shield." % (eq.name)
            elif wear_location == "held, in hands":
                room_wear_string = "%s holds %s in %s hands." % (caller.name, eq.name, possessive)
                self_wear_string = "You hold %s in your hands." % (eq.name)
            else:
                room_wear_string = "%s wears %s on %s %s." % (caller.name, eq.name, possessive, wear_location)
                self_wear_string = "You wear %s on your %s." % (eq.name, wear_location)
                
            caller.msg(self_wear_string)
            caller.location.msg_contents(room_wear_string, exclude=caller)

        if not eq.at_after_equip(caller):
            return

class CmdWield(MuxCommand):
    """
    Wield a weapon that is in your inventory. Armor cannot be equipped this
    way, you need to use wear.
    
    Usage:
      wield <obj>
      
    Takes a weapon from your inventory and puts it in the appropriate wear
    slot.
    """

    key = "wield"
    aliases = ["wie"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        if not self.args:
            caller.msg("What do you want to wield?")
            return
        
        weapon = caller.search(self.args, location=caller)

        if not weapon:
            return
        if caller == weapon:
            caller.msg("You can't wear yourself.")
            return
        
        # check to make sure character is not already wearing the equipment.
        
        if weapon.db.equipped:
            caller.msg("You are already wielding that!")
            return
        

       # check for whether character is high enough level to wield
        
        if not weapon.access(caller, "equip"):
            if weapon.db.get_err_msg:
                caller.msg(weapon.db.get_err_msg)
            else:
                caller.msg("You can't wear equipment more than five levels above your level.")
            return

        success = weapon.wield_to(caller)
        if not success:
            caller.msg("You cannot wield this.")
        else:
            caller.msg("You wield %s as a weapon." % weapon.name)
            caller.location.msg_contents(
                "%s wields a %s as a weapon." % (caller.name, weapon.name), exclude=caller
            )

        if not weapon.at_after_equip(caller):
            return

class CmdRemove(MuxCommand):
    """
    Remove armor or weapons that are equipped. 
    
    Usage:
      remove <obj>
      
    Takes an object from your inventory and puts it in the appropriate wear
    slot.
    """

    key = "remove"
    aliases = ["rem"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        if not self.args:
            caller.msg("What do you want to remove?")
            return
     
        eq = ""
     
        # checking to see if what you want to remove is actually being worn/wielded,
        # and getting the equipment object if so.
     
        for wear_location in caller.db.eq_slots:

            if caller.db.eq_slots[wear_location]:

                equipment = caller.db.eq_slots[wear_location].key.lower()

                if equipment.find(self.args.lower()) >= 0:
                    eq = caller.db.eq_slots[wear_location]
        
        if not eq:
            caller.msg("You are not using a %s as armor or a weapon." % self.args)
            return
        if caller == eq:
            caller.msg("You can't remove yourself.")
            return

       # check for whether item is cursed to prevent removal.
        
        if not eq.access(caller, "remove"):
            if eq.db.get_err_msg:
                caller.msg(eq.db.get_err_msg)
            else:
                caller.msg("This object is cursed, and cannot be removed.")
            return
        
        # calling at_before_get hook method
       # if not obj.at_before_get(caller):
       #     return

        success = eq.remove_from(caller)
        if not success:
            caller.msg("You cannot remove this.")
        else:
            caller.msg("You remove %s from your %s." % (eq.name,eq.db.wear_location))
            caller.location.msg_contents(
                "%s removes a %s from his %s." % (caller.name, eq.name, eq.db.wear_location), exclude=caller
            )

class CmdEquipment(MuxCommand):
    """
    List equipment currently worn by the character.

    Usage:
       equip

    Displays a formatted chart showing all of your worn equipment.
    """
    key = "equipment"
    aliases = ["eq", "equip"]
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        """implements the actual functionality"""

        caller = self.caller

        if any(caller.db.eq_slots.values()):

            # calling a method on the character that returns a formatted table of
            # all the equipment it is wearing.

            equipment_table = caller.get_equipment_table()

            caller.msg("You are wearing:\n")

            caller.msg(equipment_table)

        else:
            caller.msg("You are completely naked!")

class CmdIdentify(MuxCommand):

    """
    Examine an item in your inventory or worn/wielded by you to determine its
    statistics.

    Usage:
        identify <obj>

    Displays a formatted string showing the relevant statistics of an item.
    """

    key = "identify"
    aliases = ["id", "iden"]
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        """implements the actual functionality"""

        caller = self.caller

        if not self.args:
            caller.msg("What do you want to identify?")
            return
            
        item = caller.search(self.args, location=caller)

        name = item.name
        level = item.db.level
        type = item.db.item_type
        if item.db.item_type == "armor" or item.db.item_type == "weapon":
            remove = item.access(caller, "remove")
            drop = item.access(caller, "drop")
            anti_alignment = item.db.alignment_restriction

            if item.db.item_type == "armor":
                armor = item.db.armor
                wear_location = item.db.wear_location
            else:
                minimum_damage = item.db.damage_low
                maximum_damage = item.db.damage_high
                damage_type = item.db.weapon_type
        elif item.db.item_type == "pill" or item.db.item_type == "potion" or item.db.item_type == "scroll":
            spell_1 = item.db.spell1
            spell_2 = item.db.spell2
            spell_3 = item.db.spell3
            spell_level = item.db.spell_level
        elif item.db.item_type == "wand" or item.db.item_type == "staff":
            charges_maximum = item.db.charges_maximum
            charges_current = item.db.charges_current
            spell = item.db.spell_name
            spell_string = ", ".join(spell_1, spell_2, spell_3)

        if drop == True:
            drop = "yes"
        else:
            drop = "no"

        if remove == True:
            remove = "yes"
        else:
            remove = "no"

        if not anti_alignment:
            anti_string = "none"
        else:
            anti_string = " ".join(anti_alignment)

        caller.msg("%s has the following characteristics:\n" % name)

        caller.msg("Name: %s   Level: %s   Type: %s" % (name, level, type))

        if type == "armor":
            caller.msg("Droppable? %s   Removeable? %s   Can't be used by: %s" % (drop, remove, anti_string))
            caller.msg("Wear Location: %s   Armor: %s" % (wear_location, armor))
        elif type == "weapon":
            caller.msg("Droppable? %s   Removeable? %s   Can't be used by: %s" % (drop, remove, anti_string))
            caller.msg("Minimum Damage: %s   Maximum Damage: %s   Damage Type: %s" % (minimum_damage, maximum_damage, damage_type))
        elif type == "potion" or type == "pill" or type == "scroll":
            caller.msg("Spells: %s" % spell_string)
        elif type == "staff" or type == "wand":
            caller.msg("Spell: %s   Level: %d   Charges: %d/%d" % (spell, spell_level, charges_current, charges_maximum))

        for attribute in item.db.stat_modifiers:
            if item.db.stat_modifiers[attribute]:
                if item.db.stat_modifiers[attribute] > 0:
                    parity = "+"
                else:
                    parity = ""
                
                caller.msg("%-15s %s%s" % ((attribute.capitalize() + ":"), parity, item.db.stat_modifiers[attribute]))









