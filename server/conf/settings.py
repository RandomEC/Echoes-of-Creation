r"""
Evennia settings file.

The available options are found in the default settings file found
here:

c:\users\bradm\mudstuff\evennia\evennia\settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

# Overriding to allow more than one character per player
MULTISESSION_MODE = 2

# Typeclass for character objects linked to an account (fallback)
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.Player"
BASE_ACCOUNT_TYPECLASS = "typeclasses.accounts.Account"

BASE_ROOM_TYPECLASS = "typeclasses.rooms.Room"

# Definitions for experience cost calculations.
EXPERIENCE_STEP_TWO = 2700
EXPERIENCE_STEP_EXPONENT = 3
EXPERIENCE_STEP_MULTIPLIER = 400
ATTRIBUTES_TOTAL_UPGRADES = 25
ATTRIBUTES_EXPONENT = 3

# Experience loss factors.
EXPERIENCE_LOSS_DEATH = 0.25
EXPERIENCE_LOSS_FLEE = 0.0125
EXPERIENCE_LOSS_FLEE_FAIL = 0.005

# Times for item disintegration.
PULSES_PER_SECOND = 4
TICK_ATTACK_ROUND = PULSES_PER_SECOND * 2
TICK_OBJECT_TIMER = 30
DEFAULT_DISINTEGRATE_TIME = 30 * TICK_OBJECT_TIMER
PC_CORPSE_DISINTEGRATE_TIME = 60 * TICK_OBJECT_TIMER

EMPTY_AREA_RESET_TIME = 30#0   # 5 minute reset if no player in area

# Added to cleanup command parsing.
COMMAND_DEFAULT_ARG_REGEX = r'^[ /]+.*$|$'

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Echoes of Creation"


######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
