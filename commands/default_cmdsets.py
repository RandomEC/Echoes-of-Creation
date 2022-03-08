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
from commands.command import CmdScore
from commands.command import CmdCharCreate
from commands.command import CmdInventory
from commands.command import CmdDrop
from commands.command import CmdLook
from commands.command import CmdRepop
from commands.command import CmdDestroy
from commands.command import CmdLock
from commands.command import CmdPut
from commands.command import CmdTag
from commands.command import CmdSetHome
from commands.command import CmdTalk
from commands.command import CmdInspect
from commands.command import CmdGet
from commands.command import CmdSleep
from commands.command import CmdRest
from commands.command import CmdStand
from commands.command import CmdSay
from commands.build_commands import CmdOpen
from commands.build_commands import CmdSetObjAlias
from commands.build_commands import CmdDig
from commands.build_commands import CmdCreate
from commands.build_commands import CmdName
from commands.equipment_commands import CmdWear
from commands.equipment_commands import CmdWield
from commands.equipment_commands import CmdRemove
from commands.equipment_commands import CmdEquipment
from commands.equipment_commands import CmdIdentify
from commands.equipment_commands import CmdWearTo
from commands.equipment_commands import CmdWieldTo
from commands.equipment_commands import CmdRemoveFrom
from commands.door_commands import CmdDoorOpen
from commands.door_commands import CmdDoorClose
from commands.door_commands import CmdDoorUnlock
from commands.door_commands import CmdDoorLock
from commands.combat_commands import CmdAttack
from commands.combat_commands import CmdConsider
from commands.combat_commands import CmdFlee
from commands.combat_commands import CmdWimpy
from commands.growth_commands import CmdTrain

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
        self.add(CmdScore())
        self.add(CmdWear())
        self.add(CmdWield())
        self.add(CmdRemove())
        self.add(CmdEquipment())
        self.add(CmdInventory())
        self.add(CmdLook())
        self.add(CmdDrop())
        self.add(CmdIdentify())
        self.add(CmdOpen())
        self.add(CmdDoorOpen())
        self.add(CmdDoorClose())
        self.add(CmdDoorUnlock())
        self.add(CmdDoorLock())
        self.add(CmdRepop())
        self.add(CmdDestroy())
        self.add(CmdLock())
        self.add(CmdPut())
        self.add(CmdWearTo())
        self.add(CmdWieldTo())
        self.add(CmdRemoveFrom())
        self.add(CmdTag())
        self.add(CmdSetHome())
        self.add(CmdTalk())
        self.add(CmdInspect())
        self.add(CmdAttack())
        self.add(CmdGet())
        self.add(CmdSleep())
        self.add(CmdRest())
        self.add(CmdStand())
        self.add(CmdSetObjAlias())
        self.add(CmdDig())
        self.add(CmdCreate())
        self.add(CmdName())
        self.add(CmdConsider())
        self.add(CmdFlee())
        self.add(CmdWimpy())
        self.add(CmdTrain())
        self.add(CmdSay())

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
        self.add(CmdCharCreate())          # character creation

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
