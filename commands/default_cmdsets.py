"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds
from commands.command import CmdAffects
from commands.command import CmdColleges
from commands.command import CmdCSkills
from commands.command import CmdDestroy
from commands.command import CmdDrop
from commands.command import CmdGet
from commands.command import CmdGive
from commands.command import CmdHome
from commands.command import CmdInspect
from commands.command import CmdInventory
from commands.command import CmdLock
from commands.command import CmdLook
from commands.command import CmdPut
from commands.command import CmdRepop
from commands.command import CmdRest
from commands.command import CmdSacrifice
from commands.command import CmdSay
from commands.command import CmdScan
from commands.command import CmdScore
from commands.command import CmdSetHome
from commands.command import CmdSleep
from commands.command import CmdStand
from commands.command import CmdTag
from commands.command import CmdTalk
from commands.command import CmdTest
from commands.build_commands import CmdCreate
from commands.build_commands import CmdDig
from commands.build_commands import CmdName
from commands.build_commands import CmdOpen
from commands.build_commands import CmdSetObjAlias
from commands.combat_commands import CmdAttack
from commands.combat_commands import CmdConsider
from commands.combat_commands import CmdDirtKicking
from commands.combat_commands import CmdFlee
from commands.combat_commands import CmdKick
from commands.combat_commands import CmdPeace
from commands.combat_commands import CmdTrip
from commands.combat_commands import CmdWimpy
from commands.door_commands import CmdDoorClose
from commands.door_commands import CmdDoorLock
from commands.door_commands import CmdDoorOpen
from commands.door_commands import CmdDoorUnlock
from commands.equipment_commands import CmdEquipment
from commands.equipment_commands import CmdIdentify
from commands.equipment_commands import CmdRemove
from commands.equipment_commands import CmdRemoveFrom
from commands.equipment_commands import CmdWear
from commands.equipment_commands import CmdWearTo
from commands.equipment_commands import CmdWield
from commands.equipment_commands import CmdWieldTo
from commands.growth_commands import CmdPractice
from commands.growth_commands import CmdTrain
from commands.quest_commands import CmdQuestList
from commands.skill_commands import CmdBashDoor
from commands.skill_commands import CmdChameleonPower
from commands.skill_commands import CmdDowse
from commands.skill_commands import CmdForage
from commands.skill_commands import CmdHide
from commands.skill_commands import CmdPickLock
from commands.skill_commands import CmdShadowForm
from commands.skill_commands import CmdSkills
from commands.skill_commands import CmdSneak
from commands.skill_commands import CmdSteal
from commands.spell_commands import CmdAdrenalineControl
from commands.spell_commands import CmdAgitation
from commands.spell_commands import CmdBamf
from commands.spell_commands import CmdBless
from commands.spell_commands import CmdBurningHands
from commands.spell_commands import CmdCauseLight
from commands.spell_commands import CmdChillTouch
from commands.spell_commands import CmdContinualLight
from commands.spell_commands import CmdCreateFood
from commands.spell_commands import CmdCreateSound
from commands.spell_commands import CmdCreateSpring
from commands.spell_commands import CmdCreateWater
from commands.spell_commands import CmdCureBlindness
from commands.spell_commands import CmdCureLight
from commands.spell_commands import CmdDetectEvil
from commands.spell_commands import CmdDetectHidden
from commands.spell_commands import CmdDetectInvis
from commands.spell_commands import CmdDetectMagic
from commands.spell_commands import CmdFaerieFog
from commands.spell_commands import CmdFirebolt
from commands.spell_commands import CmdFly
from commands.spell_commands import CmdGiantStrength
from commands.spell_commands import CmdInfravision
from commands.spell_commands import CmdInvisible
from commands.spell_commands import CmdKnowAlignment
from commands.spell_commands import CmdLevitation
from commands.spell_commands import CmdMagicMissile
from commands.spell_commands import CmdMentalBarrier
from commands.spell_commands import CmdMindThrust
from commands.spell_commands import CmdProtection
from commands.spell_commands import CmdPsychicHeal
from commands.spell_commands import CmdRefresh
from commands.spell_commands import CmdShield
from commands.spell_commands import CmdShockingGrasp
from commands.spell_commands import CmdSlumber
from commands.spell_commands import CmdSummonWeapon
from commands.spell_commands import CmdThoughtShield
from commands.spell_commands import CmdVentriloquate

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """

    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(CmdAdrenalineControl())
        self.add(CmdAffects())
        self.add(CmdAgitation())
        self.add(CmdAttack())
        self.add(CmdBamf())
        self.add(CmdBashDoor())
        self.add(CmdBless())
        self.add(CmdBurningHands())
        self.add(CmdCauseLight())
        self.add(CmdChameleonPower())
        self.add(CmdChillTouch())
        self.add(CmdColleges())
        self.add(CmdConsider())
        self.add(CmdContinualLight())
        self.add(CmdCreate())
        self.add(CmdCreateFood())
        self.add(CmdCreateSound())
        self.add(CmdCreateSpring())
        self.add(CmdCreateWater())
        self.add(CmdCSkills())
        self.add(CmdCureBlindness())
        self.add(CmdCureLight())
        self.add(CmdDestroy())
        self.add(CmdDetectEvil())
        self.add(CmdDetectHidden())
        self.add(CmdDetectInvis())
        self.add(CmdDetectMagic())
        self.add(CmdDig())
        self.add(CmdDirtKicking())
        self.add(CmdDoorClose())
        self.add(CmdDoorLock())
        self.add(CmdDoorOpen())
        self.add(CmdDoorUnlock())
        self.add(CmdDowse())
        self.add(CmdDrop())
        self.add(CmdEquipment())
        self.add(CmdFaerieFog())
        self.add(CmdFirebolt())
        self.add(CmdFlee())
        self.add(CmdFly())
        self.add(CmdForage())
        self.add(CmdGet())
        self.add(CmdGiantStrength())
        self.add(CmdGive())
        self.add(CmdHide())
        self.add(CmdHome())
        self.add(CmdIdentify())
        self.add(CmdInfravision())
        self.add(CmdInspect())
        self.add(CmdInventory())
        self.add(CmdInvisible())
        self.add(CmdKick())
        self.add(CmdKnowAlignment())
        self.add(CmdLevitation())
        self.add(CmdLock())
        self.add(CmdLook())
        self.add(CmdMagicMissile())
        self.add(CmdMentalBarrier())
        self.add(CmdMindThrust())
        self.add(CmdName())
        self.add(CmdOpen())
        self.add(CmdPeace())
        self.add(CmdPickLock())
        self.add(CmdPractice())
        self.add(CmdProtection())
        self.add(CmdPsychicHeal())
        self.add(CmdPut())
        self.add(CmdQuestList())
        self.add(CmdRefresh())
        self.add(CmdRemove())
        self.add(CmdRemoveFrom())
        self.add(CmdRepop())
        self.add(CmdRest())
        self.add(CmdSacrifice())
        self.add(CmdSay())
        self.add(CmdScan())
        self.add(CmdScore())
        self.add(CmdSetHome())
        self.add(CmdSetObjAlias())
        self.add(CmdShadowForm())
        self.add(CmdShield())
        self.add(CmdShockingGrasp())
        self.add(CmdSleep())
        self.add(CmdSlumber())
        self.add(CmdSkills())
        self.add(CmdSneak())
        self.add(CmdStand())
        self.add(CmdSteal())
        self.add(CmdSummonWeapon())
        self.add(CmdTag())
        self.add(CmdTalk())
        self.add(CmdTest())
        self.add(CmdThoughtShield())
        self.add(CmdTrain())
        self.add(CmdTrip())
        self.add(CmdWear())
        self.add(CmdWearTo())
        self.add(CmdWield())
        self.add(CmdWieldTo())
        self.add(CmdWimpy())
        self.add(CmdVentriloquate())

class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """

    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #

class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """

    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #

class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """

    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
