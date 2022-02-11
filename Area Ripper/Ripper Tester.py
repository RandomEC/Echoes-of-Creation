# Command to run in IDLE is exec(open('C:/Users/bradm/mudstuff/mygame/
# Area Ripper/Area Ripper.py').read())
#
# Be sure that before you try to use, you make sure that if you have done this
# before (or if you already use unique numbers to refer to your rooms) that
# they do not overlap with any of the vnums of what you are going to load.
#
# Remember when running not to use the .ev suffix.

# Need to handle tagging separately.

import random
from mygame.world import rules

with open("C:/Users/bradm/mudstuff/smurfs.txt", "rt") as myfile:

    class Object:
        def __init__(self):
            self.vnum = ""
            self.keywords = ""
            self.short_description = ""
            self.long_description = ""
            self.look_description = ""
            self.item_type = ""
            self.extra_flags = list()
            self.wear_location = ""
            self.value_0 = ""
            self.value_1 = ""
            self.value_2 = ""
            self.value_3 = ""
            self.weight = 0
            self.extra_description = {}
            self.apply = {}
            self.can_take = False
            self.special_function = []

    class Mobile:
        def __init__(self):
            self.name = ""
            self.vnum = ""
            self.keywords = ""
            self.short_description = ""
            self.long_description = ""
            self.look_description = ""
            self.act_flags = list()
            self.affected_flags = list()
            self.alignment = 0
            self.level = 0
            self.sex = "neuter"
            self.race = ""
            self.item_type = ""
            self.shopkeeper = {}

    class Room:
        def __init__(self):
            self.name = ""
            self.description = ""
            self.room_flags = []
            self.terrain = ""
            self.extra_description = {}
            self.vnum = 0
            self.doors = {
                "north": {"destination": 0,
                          "key": 0,
                          "locks": [],
                          "description": "",
                          "keywords": ""
                          },
                "east": {"destination": 0,
                         "key": 0,
                         "locks": [],
                         "description": "",
                         "keywords": ""
                         },
                "south": {"destination": 0,
                          "key": 0,
                          "locks": [],
                          "description": "",
                          "keywords": ""
                          },
                "west": {"destination": 0,
                         "key": 0,
                         "locks": [],
                         "description": "",
                         "keywords": ""
                         },
                "up": {"destination": 0,
                       "key": 0,
                       "locks": [],
                       "description": "",
                       "keywords": ""
                       },
                "down": {"destination": 0,
                         "key": 0,
                         "locks": [],
                         "description": "",
                         "keywords": ""
                         }
                }

    area_name = ""
    afile_section = ""
    starting_vnum = 6201
    section_end = True
    resets = []
    reset_index = 0
    objects = {}
    object_data = 0
    temp_string = ""
    extra_line = 0
    apply_line = 0
    program = False
    extended_flags_format = 0
    mobiles = {}
    mobile_data = 0
    object_number = 0
    rooms = list()
    room_data = 0
    door_line = 0
    extra_line = 0
    exit_number = 0

    for my_line in myfile:               # for each line, read to a string

        # remove the newline character
        my_line = my_line.strip()

        # if the line is empty, ignore it
        if not my_line:

            pass

        # Pound sign denotes a new object
        elif my_line[0] == "#" and section_end:

            # Tell the program which section of the afile it is in.
            if my_line[1:5] == "AREA":

                area_string = my_line[:-1]
                area_list = area_string.split()
                area_list_size = len(area_list)
                index = 0
                line_break = 0

                for index in range(0, area_list_size):
                    if area_list[index] == "-":
                        line_break = index + 1

                area_name = " ".join(area_list[line_break:])

            elif my_line[1:] == "HELPS":
                afile_section = "helps"
                section_end = False
            elif my_line[1:] == "RECALL":
                afile_section = "recall"
                section_end = False
            elif my_line[1:] == "MOBILES":
                afile_section = "mobiles"
                section_end = False
            elif my_line[1:] == "OBJECTS":
                afile_section = "objects"
                section_end = False
            elif my_line[1:] == "ROOMS":
                afile_section = "rooms"
                section_end = False
            elif my_line[1:] == "RESETS":
                afile_section = "resets"
                section_end = False
            elif my_line[1:] == "SHOPS":
                afile_section = "shops"
                section_end = False
            elif my_line[1:] == "SPECIALS":
                afile_section = "specials"
                section_end = False
            elif my_line[1:] == "GAMES":
                afile_section = "games"
                section_end = False

        elif afile_section == "rooms":

            if my_line == "#0":
                section_end = True

            # Pound sign denotes a new object
            elif my_line[0] == "#":

                # create a new Room object
                rooms.append(Room())

                # remove the pound sign and put on the "r" to denote an rnum.
                temp_string = "r" + my_line[1:]

                # store the vnum string into an int and store
                rooms[object_number].vnum = temp_string

                # increment object number to move through list
                object_number += 1

                # tell the function the next data to get is name
                room_data = "name"

                # clear temp_string
                temp_string = ""

            elif room_data == "name":

                # strip the ~ from the name
                rooms[object_number-1].name = my_line[:-1]

                # tell the function the next data to get is room description
                room_data = "description"

            elif room_data == "description":

                # see if you are at the end of the description
                if my_line[-1] == "~":

                    # if so, strip the ~
                    if temp_string:
                        temp_string = temp_string + " " + my_line[:-1]
                    else:
                        temp_string = my_line[:-1]

                    # make sure string has content
                    if temp_string:

                        # set the description
                        rooms[object_number-1].description = temp_string

                    # clear the temp_string
                    temp_string = ""

                    # tell the function the next data to get is room_flags and
                    # terrain
                    room_data = "room flags terrain"

                else:

                    # if no ~, add to what you have so far
                    if temp_string:
                        temp_string = temp_string + " " + my_line
                    else:
                        temp_string = my_line

            elif room_data == "room flags terrain":

                # split the line into a three-item list, [0] can be ignored
                room_flags_terrain = my_line.split()

                # get room_flags as an integer
                room_flags = int(room_flags_terrain[1])

                # create list to store room flags
                room_flags_list = list()

                # convert binary to a list of flags
                if room_flags >= 134217728:
                    room_flags = room_flags - 134217728
                    room_flags_list.append("imp only")
                if room_flags >= 67108864:
                    room_flags = room_flags - 67108864
                    room_flags_list.append("gods only")
                if room_flags >= 33554432:
                    room_flags = room_flags - 33554432
                    room_flags_list.append("heroes only")
                if room_flags >= 16777216:
                    room_flags = room_flags - 16777216
                    room_flags_list.append("newbies only")
                if room_flags >= 8388608:
                    room_flags = room_flags - 8388608
                    room_flags_list.append("no astral out")
                if room_flags >= 4194304:
                    room_flags = room_flags - 4194304
                    room_flags_list.append("no astral in")
                if room_flags >= 2097152:
                    room_flags = room_flags - 2097152
                    room_flags_list.append("no tp out")
                if room_flags >= 1048576:
                    room_flags = room_flags - 1048576
                    room_flags_list.append("no summon to")
                if room_flags >= 524288:
                    room_flags = room_flags - 524288
                    room_flags_list.append("special")
                if room_flags >= 262144:
                    room_flags = room_flags - 262144
                    room_flags_list.append("no teleport in")
                if room_flags >= 131072:
                    room_flags = room_flags - 131072
                    room_flags_list.append("no summon from")
                if room_flags >= 65536:
                    room_flags = room_flags - 65536
                    room_flags_list.append("battlefield")
                if room_flags >= 32768:
                    room_flags = room_flags - 32768
                    room_flags_list.append("arena")
                if room_flags >= 16384:
                    room_flags = room_flags - 16384
                    room_flags_list.append("cone of silence")
                if room_flags >= 8192:
                    room_flags = room_flags - 8192
                    room_flags_list.append("no recall")
                if room_flags >= 4096:
                    room_flags = room_flags - 4096
                    room_flags_list.append("pet shop")
                if room_flags >= 2048:
                    room_flags = room_flags - 2048
                    room_flags_list.append("solitary")
                if room_flags >= 1024:
                    room_flags = room_flags - 1024
                    room_flags_list.append("safe")
                if room_flags >= 512:
                    room_flags = room_flags - 512
                    room_flags_list.append("private")
                if room_flags >= 256:
                    room_flags = room_flags - 256
                if room_flags >= 128:
                    room_flags = room_flags - 128
                if room_flags >= 64:
                    room_flags = room_flags - 64
                if room_flags >= 32:
                    room_flags = room_flags - 32
                    room_flags_list.append("no magic")
                if room_flags >= 16:
                    room_flags = room_flags - 16
                    room_flags_list.append("underground")
                if room_flags >= 8:
                    room_flags = room_flags - 8
                    room_flags_list.append("indoors")
                if room_flags >= 4:
                    room_flags = room_flags - 4
                    room_flags_list.append("no mob")
                if room_flags >= 2:
                    room_flags = room_flags - 2
                if room_flags >= 1:
                    room_flags = room_flags - 1
                    room_flags_list.append("dark")

                # store the flags list in the object
                rooms[object_number-1].room_flags = room_flags_list

                # turn terrain into an integer
                terrain = int(room_flags_terrain[2])

                # turn integer into a terrain type
                if terrain == 0:
                    rooms[object_number-1].terrain = "inside"
                elif terrain == 1:
                    rooms[object_number-1].terrain = "city"
                elif terrain == 2:
                    rooms[object_number-1].terrain = "field"
                elif terrain == 3:
                    rooms[object_number-1].terrain = "forest"
                elif terrain == 4:
                    rooms[object_number-1].terrain = "hills"
                elif terrain == 5:
                    rooms[object_number-1].terrain = "mountain"
                elif terrain == 6:
                    rooms[object_number-1].terrain = "water swim"
                elif terrain == 7:
                    rooms[object_number-1].terrain = "water noswim"
                elif terrain == 8:
                    rooms[object_number-1].terrain = "underwater"
                elif terrain == 9:
                    rooms[object_number-1].terrain = "air"
                else:
                    rooms[object_number-1].terrain = "desert"

                room_data = ""

            elif (len(my_line) == 2 and my_line[0] == "D") or door_line > 0:
                if door_line == 0:
                    door_direction = int(my_line[1])
                    if door_direction == 0:
                        door_direction = "north"
                    elif door_direction == 1:
                        door_direction = "east"
                    elif door_direction == 2:
                        door_direction = "south"
                    elif door_direction == 3:
                        door_direction = "west"
                    elif door_direction == 4:
                        door_direction = "up"
                    elif door_direction == 5:
                        door_direction = "down"
                    door_line = 1

                elif door_line == 1:

                    # see if you are at the end of the exit description
                    if my_line[-1] == "~":

                        # if so, strip the ~
                        if temp_string:
                            temp_string = temp_string + " " + my_line[:-1]
                        else:
                            temp_string = my_line[:-1]

                        # make sure string has content
                        if temp_string:

                            # set the description
                            rooms[object_number-1].\
                                doors[door_direction]["description"]\
                                = temp_string

                        # clear the temp_string
                        temp_string = ""

                        # tell the function the next data to get is the exit
                        # keywords line
                        door_line = 2

                    else:

                        # if no ~, add to what you have so far
                        if temp_string:
                            temp_string = temp_string + " " + my_line
                        else:
                            temp_string = my_line

                elif door_line == 2:

                    # see if you are at the end of the exit keywords
                    if my_line[-1] == "~":

                        # if so, strip the ~
                        my_line = my_line[:-1]

                        if my_line != "" and my_line != " ":
                            if temp_string:
                                temp_string = temp_string + " " + my_line
                            else:
                                temp_string = my_line

                        # make sure string has content
                        if temp_string:

                            # set the keyword list
                            rooms[object_number-1].\
                                doors[door_direction]["keywords"]\
                                = list(temp_string.split(" "))

                        # tell the function the next data to get is the exit
                        # keywords line
                        door_line = 3

                        # clear the temp string
                        temp_string = ""

                    else:

                        # if no ~, add to what you have so far
                        if temp_string:
                            temp_string = temp_string + " " + my_line
                        else:
                            temp_string = my_line

                elif door_line == 3:

                    # split the line into a three-item list
                    locks_key_destination = my_line.split()

                    # set locks
                    locks = int(locks_key_destination[0])

                    if locks == 1:
                        locks = tuple()
                    elif locks == 2:
                        locks = ("pick",)
                    elif locks == 3:
                        locks = ("bash",)
                    elif locks == 4:
                        locks = ("pick", "bash",)
                    elif locks == 5:
                        locks = ("pass",)
                    elif locks == 6:
                        locks = ("pick", "pass")
                    elif locks == 7:
                        locks = ("bash", "pass",)
                    else:
                        locks = ("pick", "bash", "pass",)

                    rooms[object_number-1].doors[door_direction]["locks"]\
                        = locks

                    rooms[object_number-1].doors[door_direction]["key"]\
                        = locks_key_destination[1]

                    rooms[object_number-1].\
                        doors[door_direction]["destination"]\
                        = locks_key_destination[2]

                    # done with this door
                    door_line = 0

            elif my_line == "E" or extra_line > 0:

                if extra_line == 0:
                    extra_line = 1

                elif extra_line == 1:

                    # see if you are at the end of the keywords
                    if my_line[-1] == "~":

                        # if so, strip the ~
                        if temp_string:
                            temp_string = temp_string + " " + my_line[:-1]
                        else:
                            temp_string = my_line[:-1]

                        # set the keywords
                        rooms[object_number-1].extra_description[temp_string]\
                            = ""

                        # set the keywords value for finding in dictionary for
                        # description
                        keywords = temp_string

                        # clear the temp_string
                        temp_string = ""

                        # tell the function the next data to get is the extra
                        # description
                        extra_line = 2

                    else:

                        # if no ~, add to what you have so far
                        if temp_string:
                            temp_string = temp_string + " " + my_line
                        else:
                            temp_string = my_line

                elif extra_line == 2:

                    # see if you are at the end of the extra description
                    if my_line[-1] == "~":

                        # if so, strip the ~
                        if temp_string:
                            temp_string = temp_string + " " + my_line[:-1]
                        else:
                            temp_string = my_line[:-1]

                        # set the description
                        rooms[object_number-1].extra_description[keywords]\
                            = temp_string

                        # clear the temp_string
                        temp_string = ""

                        # done with this extra description
                        extra_line = 0

                    else:

                        # if no ~, add to what you have so far
                        if temp_string:
                            temp_string = temp_string + " " + my_line
                        else:
                            temp_string = my_line

            else:
                pass

        elif afile_section == "mobiles":

            if my_line == "#0":
                section_end = True

            # Mprogs start with a ">" at the beginning. Tell the
            # script that one is starting, so we can skip.
            elif my_line[0] == ">":
                program = True

            # Keep skipping through the mprog until we reach the
            # end - |.
            elif program:
                if my_line == "|":
                    program = False

            # Pound sign denotes a new object.
            elif my_line[0] == "#":

                # Remove the pound sign.
                temp_string = my_line[1:]

                # Turn the vnum string into an mnum.
                mnum = "m" + temp_string

                # Create a new entry in the mobiles dictionary, with the key
                # of mnum.
                mobiles[mnum] = Mobile()

                # Just in case, store the mnum on the Mobile object as well.
                mobiles[mnum].vnum = mnum

                # Tell the function the next data to get is keywords.
                mobile_data = "keywords"

                # Clear temp_string.
                temp_string = ""

            elif mobile_data == "keywords":

                # See if you are at the end of the keywords. Really only doing
                # this check in case the area author put the ~ on the line
                # after the keywords, instead of at the end of it.
                if my_line[-1] == "~":

                    # If so, strip the ~.
                    if temp_string:
                        temp_string = temp_string + " " + my_line[:-1]
                    else:
                        temp_string = my_line[:-1]

                    # Make sure string has content.
                    if temp_string:

                        # Set the keywords.
                        mobiles[mnum].keywords = temp_string

                    # Clear the temp_string.
                    temp_string = ""

                    # Tell the function the next data to get is the short
                    # description.
                    mobile_data = "short description"

                else:

                    # If no ~, add to what you have so far.
                    if temp_string:
                        temp_string = temp_string + " " + my_line
                    else:
                        temp_string = my_line

            elif mobile_data == "short description":

                # See if you are at the end of the short description. Really
                # only doing this check in case the area author put the ~ on
                # the line after the short description, instead of at the end
                # of it.
                if my_line[-1] == "~":

                    # If so, strip the ~.
                    if temp_string:
                        temp_string = temp_string + " " + my_line[:-1]
                    else:
                        temp_string = my_line[:-1]

                    # Make sure string has content.
                    if temp_string:

                        # Set the short description.
                        mobiles[mnum].short_description = temp_string

                    # Clear the temp_string.
                    temp_string = ""

                    # Tell the function the next data to get is the long
                    # description.
                    mobile_data = "long description"

                else:

                    # If no ~, add to what you have so far.
                    if temp_string:
                        temp_string = temp_string + " " + my_line
                    else:
                        temp_string = my_line

            elif mobile_data == "long description":

                # See if you are at the end of the long description.
                if my_line[-1] == "~":

                    # If so, strip the ~.
                    if temp_string:
                        temp_string = temp_string + " " + my_line[:-1]
                    else:
                        temp_string = my_line[:-1]

                    # Make sure string has content.
                    if temp_string:

                        # Set the long description.
                        mobiles[mnum].long_description = temp_string

                    # Clear the temp_string.
                    temp_string = ""

                    # Tell the function the next data to get is look
                    # description.
                    mobile_data = "look description"

                else:

                    # If no ~, add to what you have so far.
                    if temp_string:
                        temp_string = temp_string + " " + my_line
                    else:
                        temp_string = my_line

            elif mobile_data == "look description":

                # See if you are at the end of the look description.
                if my_line[-1] == "~":

                    # If so, strip the ~.
                    if temp_string:
                        temp_string = temp_string + " " + my_line[:-1]
                    else:
                        temp_string = my_line[:-1]

                    # Make sure string has content.
                    if temp_string:

                        # Set the look description.
                        mobiles[mnum].look_description = temp_string

                    # Clear the temp_string.
                    temp_string = ""

                    # Tell the function the next data to get is act flags,
                    # affected flags and alignment.
                    mobile_data = "act affected alignment"

                else:

                    # If no ~, add to what you have so far.
                    if temp_string:
                        temp_string = temp_string + " " + my_line
                    else:
                        temp_string = my_line

            elif mobile_data == "act affected alignment":

                # Turn the string into a list of form "act flags, affected
                # flags, alignment".

                stat_list = my_line.split(" ")
                act_flags_list = list()

                act_flags = int(stat_list[0])

                # Act flags were originally a binary number that indicated
                # whether a flag was active by activating that bit. We turn it
                # into a list by taking off each successive power of two. Many
                # of these were unused on Castle Arcanum, and, so, are blank
                # below. If they carry data for the MUD you are importing
                # from, fill in below.

                if(act_flags >= 8388608):
                    act_flags = act_flags - 8388608
                if(act_flags >= 4194304):
                    act_flags = act_flags - 4194304
                if(act_flags >= 2097152):
                    act_flags = act_flags - 2097152
                if(act_flags >= 1048576):
                    act_flags = act_flags - 1048576
                if(act_flags >= 524288):
                    act_flags = act_flags - 524288
                if(act_flags >= 262144):
                    act_flags = act_flags - 262144
                if(act_flags >= 131072):
                    act_flags = act_flags - 131072
                    act_flags_list.append("total invis")
                if(act_flags >= 65536):
                    act_flags = act_flags - 65536
                    act_flags_list.append("no kill")
                if(act_flags >= 32768):
                    act_flags = act_flags - 32768
                if(act_flags >= 16384):
                    act_flags = act_flags - 16384
                if(act_flags >= 8192):
                    act_flags = act_flags - 819
                if(act_flags >= 4096):
                    act_flags = act_flags - 4096
                    act_flags_list.append("healer")
                if(act_flags >= 2048):
                    act_flags = act_flags - 2048
                    act_flags_list.append("gamble")
                if(act_flags >= 1024):
                    act_flags = act_flags - 1024
                    act_flags_list.append("practice")
                if(act_flags >= 512):
                    act_flags = act_flags - 512
                    act_flags_list.append("train")
                if(act_flags >= 256):
                    act_flags = act_flags - 256
                    act_flags_list.append("pet")
                if(act_flags >= 128):
                    act_flags = act_flags - 128
                    act_flags_list.append("wimpy")
                if(act_flags >= 64):
                    act_flags = act_flags - 64
                    act_flags_list.append("stay area")
                if(act_flags >= 32):
                    act_flags = act_flags - 32
                    act_flags_list.append("aggressive")
                if(act_flags >= 16):
                    act_flags = act_flags - 16
                if(act_flags >= 8):
                    act_flags = act_flags - 8
                if(act_flags >= 4):
                    act_flags = act_flags - 4
                    act_flags_list.append("scavenger")
                if(act_flags >= 2):
                    act_flags = act_flags - 2
                    act_flags_list.append("sentinel")
                if(act_flags >= 1):
                    act_flags_list.append("npc")

                # Stick the newly-made list into the mobile object.
                mobiles[mnum].act_flags = act_flags_list

                # Now do the same process for affected flags.
                affected_flags_list = list()
                affected_flags = int(stat_list[1])
                if(affected_flags >= 134217728):
                    affected_flags = affected_flags - 134217728
                    affected_flags_list.append("flaming")
                if(affected_flags >= 67108864):
                    affected_flags = affected_flags - 67108864
                    affected_flags_list.append("ghoul")
                if(affected_flags >= 33554432):
                    affected_flags = affected_flags - 33554432
                    affected_flags_list.append("vampire bite")
                if(affected_flags >= 16777216):
                    affected_flags = affected_flags - 16777216
                    affected_flags_list.append("gills")
                if(affected_flags >= 8388608):
                    affected_flags = affected_flags - 8388608
                    affected_flags_list.append("mute")
                if(affected_flags >= 4194304):
                    affected_flags = affected_flags - 4194304
                    affected_flags_list.append("summoned")
                if(affected_flags >= 2097152):
                    affected_flags = affected_flags - 2097152
                    affected_flags_list.append("waterwalk")
                if(affected_flags >= 1048576):
                    affected_flags = affected_flags - 1048576
                    affected_flags_list.append("pass door")
                if(affected_flags >= 524288):
                    affected_flags = affected_flags - 524288
                    affected_flags_list.append("flying")
                if(affected_flags >= 262144):
                    affected_flags = affected_flags - 262144
                    affected_flags_list.append("charm")
                if(affected_flags >= 131072):
                    affected_flags = affected_flags - 131072
                    affected_flags_list.append("sleep")
                if(affected_flags >= 65536):
                    affected_flags = affected_flags - 65536
                    affected_flags_list.append("hide")
                if(affected_flags >= 32768):
                    affected_flags = affected_flags - 32768
                    affected_flags_list.append("sneak")
                if(affected_flags >= 16384):
                    affected_flags = affected_flags - 16384
                if(affected_flags >= 8192):
                    affected_flags = affected_flags - 8192
                    affected_flags_list.append("protect")
                if(affected_flags >= 4096):
                    affected_flags = affected_flags - 4096
                    affected_flags_list.append("poison")
                if(affected_flags >= 2048):
                    affected_flags = affected_flags - 2048
                if(affected_flags >= 1024):
                    affected_flags = affected_flags - 1024
                    affected_flags_list.append("curse")
                if(affected_flags >= 512):
                    affected_flags = affected_flags - 512
                    affected_flags_list.append("infrared")
                if(affected_flags >= 256):
                    affected_flags = affected_flags - 256
                    affected_flags_list.append("faerie fire")
                if(affected_flags >= 128):
                    affected_flags = affected_flags - 128
                    affected_flags_list.append("sanctuary")
                if(affected_flags >= 64):
                    affected_flags = affected_flags - 64
                    affected_flags_list.append("hold")
                if(affected_flags >= 32):
                    affected_flags = affected_flags - 32
                    affected_flags_list.append("detect hidden")
                if(affected_flags >= 16):
                    affected_flags = affected_flags - 16
                    affected_flags_list.append("detect magic")
                if(affected_flags >= 8):
                    affected_flags = affected_flags - 8
                    affected_flags_list.append("detect invis")
                if(affected_flags >= 4):
                    affected_flags = affected_flags - 4
                    affected_flags_list.append("detect evil")
                if(affected_flags >= 2):
                    affected_flags = affected_flags - 2
                    affected_flags_list.append("invisible")
                if(affected_flags >= 1):
                    affected_flags = affected_flags - 1
                    affected_flags_list.append("blind")

                # Stick the newly-made list into the mobile object.
                mobiles[mnum].affected_flags = affected_flags_list

                # After all the fuss above, assigning alignment feels
                # anticlimactic.
                mobiles[mnum].alignment = int(stat_list[2])

                # Tell the function the next data to get is level.
                mobile_data = "level"

            elif mobile_data == "level":

                # Again, split the line on spaces.
                stat_list = my_line.split(" ")

                # The only real data here is the level, which is in the zeroth
                # slot. The rest was used historically. Store the level in the
                # mobile object.
                mobiles[mnum].level = int(stat_list[0])

                # Tell the function the next data to get is the line of zeros.
                mobile_data = "zeros line"

            # I don't know what the purpose of this line was, historically, but
            # we just ignore it.
            elif mobile_data == "zeros line":

                # Tell the function the next data to get is race and sex.
                mobile_data = "race sex"

            elif mobile_data == "race sex":

                # Again, split the line on spaces.
                stat_list = my_line.split(" ")

                # Pull race out of the list.
                race = stat_list[1]

                # Strip off the ~.
                race = race[:-1]

                # Store the race in the mobile object.
                mobiles[mnum].race = race

                # Pull the sex from the list and turn into an int to evaluate.
                sex = int(stat_list[2])

                # Check sex and assign.
                if(sex == 1):
                    mobiles[mnum].sex = "male"
                elif(sex == 2):
                    mobiles[mnum].sex = "female"
                else:
                    mobiles[mnum].sex = "neuter"

        elif afile_section == "objects":

            if my_line == "#0":
                section_end = True

            # some files have the item-type, extra-flags, wear-flags triad as
            # a three-line list instead of one line. This accommodates that.
            elif extended_flags_format == 1:

                # Extra flags used to be a binary, where they used each bit as
                # a flag to know if the flag was active. We disaggregate into
                # a list.
                extra_flags_list = list()
                extra_flags = int(my_line)
                if extra_flags >= 262114:
                    extra_flags = extra_flags - 262114
                    extra_flags_list.append("timed")
                if extra_flags >= 131072:
                    extra_flags = extra_flags - 131072
                    extra_flags_list.append("machine")
                if extra_flags >= 65536:
                    extra_flags = extra_flags - 65536
                    extra_flags_list.append("holy")
                if extra_flags >= 32768:
                    extra_flags = extra_flags - 32768
                    extra_flags_list.append("vampire bane")
                if extra_flags >= 16384:
                    extra_flags = extra_flags - 16384
                    extra_flags_list.append("poisoned")
                if extra_flags >= 8192:
                    extra_flags = extra_flags - 8192
                    extra_flags_list.append("inventory")
                if extra_flags >= 4096:
                    extra_flags = extra_flags - 4096
                    extra_flags_list.append("no remove")
                if extra_flags >= 2048:
                    extra_flags = extra_flags - 2048
                    extra_flags_list.append("anti neutral")
                if extra_flags >= 1024:
                    extra_flags = extra_flags - 1024
                    extra_flags_list.append("anti evil")
                if extra_flags >= 512:
                    extra_flags = extra_flags - 512
                    extra_flags_list.append("anti good")
                if extra_flags >= 256:
                    extra_flags = extra_flags - 256
                    extra_flags_list.append("bless")
                if extra_flags >= 128:
                    extra_flags = extra_flags - 128
                    extra_flags_list.append("no drop")
                if extra_flags >= 64:
                    extra_flags = extra_flags - 64
                    extra_flags_list.append("magic")
                if extra_flags >= 32:
                    extra_flags = extra_flags - 32
                    extra_flags_list.append("invisible")
                if extra_flags >= 16:
                    extra_flags = extra_flags - 16
                    extra_flags_list.append("evil")
                if extra_flags >= 8:
                    extra_flags = extra_flags - 8
                    extra_flags_list.append("lock")
                if extra_flags >= 4:
                    extra_flags = extra_flags - 4
                    extra_flags_list.append("dark")
                if extra_flags >= 2:
                    extra_flags = extra_flags - 2
                    extra_flags_list.append("hum")
                if extra_flags >= 1:
                    extra_flags = extra_flags - 1
                    extra_flags_list.append("glow")

                # stick the newly-made list into the object.
                if extra_flags_list:
                    objects[onum].extra_flags = extra_flags_list

                # Increment to get the last line of the flags.
                extended_flags_format += 1

            elif extended_flags_format == 2:
                # Wear flags used to be a binary, where they used each bit as
                # a flag to know if the flag was active. We split off the
                # ability to take the item, and disaggregate the rest into a
                # list. We won't allow multiple wear locations, so we will
                # take the lowest allowable wear slot at the end.
                wear_flags_list = list()
                wear_flags = int(my_line)
                if wear_flags >= 2097152:
                    wear_flags = wear_flags - 2097152
                    wear_flags_list.append("ankle")
                if wear_flags >= 1048576:
                    wear_flags = wear_flags - 1048576
                    wear_flags_list.append("face")
                if wear_flags >= 524288:
                    wear_flags = wear_flags - 524288
                    wear_flags_list.append("back")
                if wear_flags >= 262144:
                    wear_flags = wear_flags - 262144
                    wear_flags_list.append("eyes")
                if wear_flags >= 131072:
                    wear_flags = wear_flags - 131072
                    wear_flags_list.append("nose")
                if wear_flags >= 65536:
                    wear_flags = wear_flags - 65536
                    wear_flags_list.append("ears")
                if wear_flags >= 32768:
                    wear_flags = wear_flags - 32768
                    wear_flags_list.append("pride")
                if wear_flags >= 16384:
                    wear_flags = wear_flags - 16384
                    wear_flags_list.append("hold")
                if wear_flags >= 8192:
                    wear_flags = wear_flags - 8192
                    wear_flags_list.append("wield")
                if wear_flags >= 4096:
                    wear_flags = wear_flags - 4096
                    wear_flags_list.append("wrist")
                if wear_flags >= 2048:
                    wear_flags = wear_flags - 2048
                    wear_flags_list.append("waist")
                if wear_flags >= 1024:
                    wear_flags = wear_flags - 1024
                    wear_flags_list.append("about body")
                if wear_flags >= 512:
                    wear_flags = wear_flags - 512
                    wear_flags_list.append("shield")
                if wear_flags >= 256:
                    wear_flags = wear_flags - 256
                    wear_flags_list.append("arms")
                if wear_flags >= 128:
                    wear_flags = wear_flags - 128
                    wear_flags_list.append("hands")
                if wear_flags >= 64:
                    wear_flags = wear_flags - 64
                    wear_flags_list.append("feet")
                if wear_flags >= 32:
                    wear_flags = wear_flags - 32
                    wear_flags_list.append("legs")
                if wear_flags >= 16:
                    wear_flags = wear_flags - 16
                    wear_flags_list.append("head")
                if wear_flags >= 8:
                    wear_flags = wear_flags - 8
                    wear_flags_list.append("body")
                if wear_flags >= 4:
                    wear_flags = wear_flags - 4
                    wear_flags_list.append("neck")
                if wear_flags >= 2:
                    wear_flags = wear_flags - 2
                    wear_flags_list.append("finger")
                if wear_flags >= 1:
                    objects[onum].can_take = True

                # if there is a wear slot, take the lowest numbered one and
                # put it on the object.
                if wear_flags_list:
                    objects[onum].wear_location = wear_flags_list[-1]

                extended_flags_format = 0

            # Pound sign denotes a new object
            elif my_line[0] == "#":

                # remove the pound sign
                temp_string = my_line[1:]

                # Turn the vnum string into an onum and store.
                onum = "o" + temp_string

                # Create a new Object object with the key of that onum.
                objects[onum] = Object()

                # Store the onum in the Object itself, as well.
                objects[onum].vnum = onum

                # Tell the function the next data to get is keywords.
                object_data = "keywords"

                # Clear temp_string.
                temp_string = ""

            elif object_data == "keywords":

                # See if you are at the end of the keywords, really only doing
                # this check in case they put the ~ on the line after the
                # keywords, instead of at the end of it.
                if my_line[-1] == "~":

                    # if so, strip the ~
                    if temp_string:
                        temp_string = temp_string + " " + my_line[:-1]
                    else:
                        temp_string = my_line[:-1]

                    # make sure string has content
                    if temp_string:

                        # set the description
                        objects[onum].keywords = temp_string

                    # clear the temp_string
                    temp_string = ""

                    # tell the function the next data to get is room_flags and
                    # terrain
                    object_data = "short description"

                else:

                    # if no ~, add to what you have so far
                    if temp_string:
                        temp_string = temp_string + " " + my_line
                    else:
                        temp_string = my_line

            elif object_data == "short description":

                # see if you are at the end of the short description, really
                # only doing this check in case they put the ~ on the line
                # after the short description, instead of at the end of it.
                if my_line[-1] == "~":

                    # if so, strip the ~
                    if temp_string:
                        temp_string = temp_string + " " + my_line[:-1]
                    else:
                        temp_string = my_line[:-1]

                    # make sure string has content
                    if temp_string:

                        # Set the description.
                        objects[onum].short_description = temp_string

                    # Clear the temp_string.
                    temp_string = ""

                    # Tell the function the next data to get is the long
                    # description.
                    object_data = "long description"

                else:

                    # if no ~, add to what you have so far
                    if temp_string:
                        temp_string = temp_string + " " + my_line
                    else:
                        temp_string = my_line

            elif object_data == "long description":

                # See if you are at the end of the long description.
                if my_line[-1] == "~":

                    # if so, strip the ~
                    if temp_string:
                        temp_string = temp_string + " " + my_line[:-1]
                    else:
                        temp_string = my_line[:-1]

                    # Make sure string has content.
                    if temp_string:

                        # Set the description.
                        objects[onum].long_description = temp_string

                    # Clear the temp_string.
                    temp_string = ""

                    # Tell the function the next data to get is the look
                    # description.
                    object_data = "look description"

                else:

                    # if no ~, add to what you have so far
                    if temp_string:
                        temp_string = temp_string + " " + my_line
                    else:
                        temp_string = my_line

            elif object_data == "look description":

                # Most area files won't have a look description for objects,
                # but some will. In any event, there WILL be a ~ where one
                # should be if there WAS a look description, so we may as well
                # handle it the same way, which will cover both cases anyway.
                if my_line[-1] == "~":

                    # if so, strip the ~
                    if temp_string:
                        temp_string = temp_string + " " + my_line[:-1]
                    else:
                        temp_string = my_line[:-1]

                    # make sure string has content
                    if temp_string:

                        # Set the description
                        objects[onum].look_description = temp_string

                    # Clear the temp_string
                    temp_string = ""

                    # Tell the function the next data to get is item type,
                    # extra flags and wear flags.
                    object_data = "type extra wear"

                else:

                    # If no terminal ~, add to what you have so far.
                    if temp_string:
                        temp_string = temp_string + " " + my_line
                    else:
                        temp_string = my_line

            elif object_data == "type extra wear":

                # Turn the string into a list of form "item type, extra flags,
                # wear flag"
                stat_list = my_line.split(" ")
                act_flags_list = list()

                item_type = int(stat_list[0])

                # Item type was a number. We'll convert it into a string.

                if item_type == 1:
                    item_type = "light"
                elif item_type == 2:
                    item_type = "scroll"
                elif item_type == 3:
                    item_type = "wand"
                elif item_type == 4:
                    item_type = "staff"
                elif item_type == 5:
                    item_type = "weapon"
                elif item_type == 8:
                    item_type = "treasure"
                elif item_type == 9:
                    item_type = "armor"
                elif item_type == 10:
                    item_type = "potion"
                elif item_type == 12:
                    item_type = "furniture"
                elif item_type == 15:
                    item_type = "container"
                elif item_type == 17:
                    item_type = "drink container"
                elif item_type == 18:
                    item_type = "key"
                elif item_type == 19:
                    item_type = "food"
                elif item_type == 20:
                    item_type = "money"
                elif item_type == 22:
                    item_type = "boat"
                elif item_type == 23:
                    item_type = "corpse npc"
                elif item_type == 24:
                    item_type = "corpse pc"
                elif item_type == 25:
                    item_type = "fountain"
                elif item_type == 26:
                    item_type = "pill"
                elif item_type == 27:
                    item_type = "fly"
                elif item_type == 28:
                    item_type = "portal"
                elif item_type == 29:
                    item_type = "scroll"
                else:
                    item_type = "trash"

                # Stick the item type into the object.
                objects[onum].item_type = item_type

                if len(stat_list) == 1:
                    extended_flags_format = 1

                else:
                    # Extra flags used to be a binary, where they used each
                    # bit as a flag to know if the flag was active. We will
                    # disaggregate this into a list.
                    extra_flags_list = list()
                    extra_flags = int(stat_list[1])
                    if extra_flags >= 262114:
                        extra_flags = extra_flags - 262114
                        extra_flags_list.append("timed")
                    if extra_flags >= 131072:
                        extra_flags = extra_flags - 131072
                        extra_flags_list.append("machine")
                    if extra_flags >= 65536:
                        extra_flags = extra_flags - 65536
                        extra_flags_list.append("holy")
                    if extra_flags >= 32768:
                        extra_flags = extra_flags - 32768
                        extra_flags_list.append("vampire bane")
                    if extra_flags >= 16384:
                        extra_flags = extra_flags - 16384
                        extra_flags_list.append("poisoned")
                    if extra_flags >= 8192:
                        extra_flags = extra_flags - 8192
                        extra_flags_list.append("inventory")
                    if extra_flags >= 4096:
                        extra_flags = extra_flags - 4096
                        extra_flags_list.append("no remove")
                    if extra_flags >= 2048:
                        extra_flags = extra_flags - 2048
                        extra_flags_list.append("anti neutral")
                    if extra_flags >= 1024:
                        extra_flags = extra_flags - 1024
                        extra_flags_list.append("anti evil")
                    if extra_flags >= 512:
                        extra_flags = extra_flags - 512
                        extra_flags_list.append("anti good")
                    if extra_flags >= 256:
                        extra_flags = extra_flags - 256
                        extra_flags_list.append("bless")
                    if extra_flags >= 128:
                        extra_flags = extra_flags - 128
                        extra_flags_list.append("no drop")
                    if extra_flags >= 64:
                        extra_flags = extra_flags - 64
                        extra_flags_list.append("magic")
                    if extra_flags >= 32:
                        extra_flags = extra_flags - 32
                        extra_flags_list.append("invisible")
                    if extra_flags >= 16:
                        extra_flags = extra_flags - 16
                        extra_flags_list.append("evil")
                    if extra_flags >= 8:
                        extra_flags = extra_flags - 8
                        extra_flags_list.append("lock")
                    if extra_flags >= 4:
                        extra_flags = extra_flags - 4
                        extra_flags_list.append("dark")
                    if extra_flags >= 2:
                        extra_flags = extra_flags - 2
                        extra_flags_list.append("hum")
                    if extra_flags >= 1:
                        extra_flags = extra_flags - 1
                        extra_flags_list.append("glow")

                    # stick the newly-made list into the object.
                    if extra_flags_list:
                        objects[onum].extra_flags = extra_flags_list

                    # Wear flags used to be a binary, where they used each bit
                    # as a flag to know if the flag was active. We split off
                    # the ability to take the item, and disaggregate the rest
                    # into a list. We won't allow multiple wear locations, so
                    # we will take the lowest allowable wear slot at the end.
                    wear_flags_list = list()
                    wear_flags = int(stat_list[2])
                    if wear_flags >= 2097152:
                        wear_flags = wear_flags - 2097152
                        wear_flags_list.append("ankle")
                    if wear_flags >= 1048576:
                        wear_flags = wear_flags - 1048576
                        wear_flags_list.append("face")
                    if wear_flags >= 524288:
                        wear_flags = wear_flags - 524288
                        wear_flags_list.append("back")
                    if wear_flags >= 262144:
                        wear_flags = wear_flags - 262144
                        wear_flags_list.append("eyes")
                    if wear_flags >= 131072:
                        wear_flags = wear_flags - 131072
                        wear_flags_list.append("nose")
                    if wear_flags >= 65536:
                        wear_flags = wear_flags - 65536
                        wear_flags_list.append("ears")
                    if wear_flags >= 32768:
                        wear_flags = wear_flags - 32768
                        wear_flags_list.append("pride")
                    if wear_flags >= 16384:
                        wear_flags = wear_flags - 16384
                        wear_flags_list.append("hold")
                    if wear_flags >= 8192:
                        wear_flags = wear_flags - 8192
                        wear_flags_list.append("wield")
                    if wear_flags >= 4096:
                        wear_flags = wear_flags - 4096
                        wear_flags_list.append("wrist")
                    if wear_flags >= 2048:
                        wear_flags = wear_flags - 2048
                        wear_flags_list.append("waist")
                    if wear_flags >= 1024:
                        wear_flags = wear_flags - 1024
                        wear_flags_list.append("about body")
                    if wear_flags >= 512:
                        wear_flags = wear_flags - 512
                        wear_flags_list.append("shield")
                    if wear_flags >= 256:
                        wear_flags = wear_flags - 256
                        wear_flags_list.append("arms")
                    if wear_flags >= 128:
                        wear_flags = wear_flags - 128
                        wear_flags_list.append("hands")
                    if wear_flags >= 64:
                        wear_flags = wear_flags - 64
                        wear_flags_list.append("feet")
                    if wear_flags >= 32:
                        wear_flags = wear_flags - 32
                        wear_flags_list.append("legs")
                    if wear_flags >= 16:
                        wear_flags = wear_flags - 16
                        wear_flags_list.append("head")
                    if wear_flags >= 8:
                        wear_flags = wear_flags - 8
                        wear_flags_list.append("body")
                    if wear_flags >= 4:
                        wear_flags = wear_flags - 4
                        wear_flags_list.append("neck")
                    if wear_flags >= 2:
                        wear_flags = wear_flags - 2
                        wear_flags_list.append("finger")
                    if wear_flags >= 1:
                        objects[onum].can_take = True

                    # If there is a wear slot, take the lowest numbered one and
                    # put it on the object.
                    if wear_flags_list:
                        objects[onum].wear_location = wear_flags_list[-1]

                # Tell the function the next data to get is item values.
                object_data = "values"

            elif object_data == "values":

                # Again, split the line on spaces.
                stat_list = my_line.split("~")

                # Store the value_0 in the mobile object.
                objects[onum].value_0 = stat_list[0].strip()

                # Store the value_0 in the mobile object.
                objects[onum].value_1 = stat_list[1].strip()

                # Store the value_0 in the mobile object.
                objects[onum].value_2 = stat_list[2].strip()

                # Store the value_0 in the mobile object.
                objects[onum].value_3 = stat_list[3].strip()

                # Tell the function the next data to get is the weight.
                object_data = "weight"

            # Take the weight off this line and discard the rest, which have
            # unknown historical use.
            elif object_data == "weight":

                # Again, split the line on spaces.
                stat_list = my_line.split(" ")

                # Store the weight in the mobile object.
                objects[onum].weight = int(stat_list[0])

                object_data = ""

            elif my_line == "E" or extra_line > 0:

                if extra_line == 0:
                    extra_line = 1

                elif extra_line == 1:

                    if my_line[0] == "\\" or my_line[0] == ">":
                        program = True

                    elif program:
                        if my_line == "E":
                            program = False
                            extra_line = 1

                    elif my_line[0] == "@":
                        spec_fun_string = my_line[1:]
                        if spec_fun_string[-1] == "~":
                            spec_fun_string = spec_fun_string[:-1]
                        if spec_fun_string[0:6] == "speco~":
                            spec_fun_string = spec_fun_string[6:]
                        if spec_fun_string[0:6] == "speco_":
                            spec_fun_string = spec_fun_string[6:]

                        objects[onum].special_function.append(spec_fun_string)
                        extra_line = 0

                    else:

                        # see if you are at the end of the keywords
                        if my_line[-1] == "~":

                            # if so, strip the ~
                            if temp_string:
                                temp_string = temp_string + " " + my_line[:-1]
                            else:
                                temp_string = my_line[:-1]

                            # Set the keywords.
                            objects[onum].extra_description[temp_string] = ""

                            # Set the keywords value for finding in dictionary
                            # below for description.
                            keywords = temp_string

                            # Clear the temp_string.
                            temp_string = ""

                            # Tell the function the next data to get is the
                            # extra description itself.
                            extra_line = 2

                        else:

                            # If no terminal ~, add to what you have so far.
                            if temp_string:
                                temp_string = temp_string + " " + my_line
                            else:
                                temp_string = my_line

                elif extra_line == 2:

                    # See if you are at the end of the extra description.
                    if my_line[-1] == "~":

                        # If so, strip the ~.
                        if temp_string:
                            temp_string = temp_string + " " + my_line[:-1]
                        else:
                            temp_string = my_line[:-1]

                        # Set the description.
                        objects[onum].extra_description[keywords] = temp_string

                        # Clear the temp_string.
                        temp_string = ""

                        # Done with this extra description.
                        extra_line = 0

                    else:

                        # If no ~, add to what you have so far.
                        temp_string = temp_string + " " + my_line

            elif my_line == "A" or apply_line > 0:

                if apply_line == 0:
                    apply_line = 1

                elif apply_line == 1:

                    # Again, split the line on spaces.
                    stat_list = my_line.split(" ")

                    apply_type = int(stat_list[0])
                    if apply_type == 1:
                        apply_type = "strength"
                    elif apply_type == 2:
                        apply_type = "dexterity"
                    elif apply_type == 3:
                        apply_type = "intelligence"
                    elif apply_type == 4:
                        apply_type = "wisdom"
                    elif apply_type == 5:
                        apply_type = "constitution"
                    elif apply_type == 12:
                        apply_type = "mana"
                    elif apply_type == 13:
                        apply_type = "hitpoints"
                    elif apply_type == 14:
                        apply_type = "moves"
                    elif apply_type == 17:
                        apply_type = "armor class"
                    elif apply_type == 18:
                        apply_type = "hitroll"
                    elif apply_type == 19:
                        apply_type = "damroll"
                    elif apply_type == 24:
                        apply_type = "saving throw"

                    apply_value = int(stat_list[1])

                    # Set the apply type for this apply.
                    objects[onum].apply[apply_type] = apply_value
                    apply_line = 0

        elif afile_section == "resets":
            if my_line == "S":
                section_end = True
            else:
                # Create a new dictionary for each reset.
                resets.append({})

                # Turn the reset string into a list.
                reset_list = my_line.split()

                # Mobile inventory and mobile equipped resets depend
                # on knowing what the last mobile reset was. This
                # tracks that.
                last_mobile = ""

                type = reset_list[0]
                if type == "M":
                    type = "mobile"
                    reset_vnum = "m" + reset_list[2]
                    last_mobile = reset_vnum
                    world_limit = reset_list[3]
                    location = "r" + reset_list[4]
                elif type == "O":
                    type = "object, room"
                    reset_vnum = "o" + reset_list[2]
                    location = "r" + reset_list[4]
                elif type == "P":
                    type = "object, in container"
                    reset_vnum = "o" + reset_list[2]
                    location = "o" + reset_list[4]
                elif type == "G":
                    type = "object, in mobile inventory"
                    reset_vnum = "o" + reset_list[2]
                    location = last_mobile
                elif type == "E":
                    type = "object, equipped"
                    reset_vnum = "o" + reset_list[2]
                    location = last_mobile
                elif type == "D":
                    type = "door"
                    location = "r" + reset_list[2]
                    if reset_list[3] == 0:
                        direction = "north"
                    elif reset_list[3] == 1:
                        direction = "east"
                    elif reset_list[3] == 2:
                        direction = "south"
                    elif reset_list[3] == 3:
                        direction = "west"
                    elif reset_list[3] == 4:
                        direction = "up"
                    else:
                        direction = "down"

                    if reset_list[4] == 0:
                        state = "open"
                    elif reset_list[4] == 1:
                        state = "closed"
                    else:
                        state = "locked"

                resets[reset_index]["type"] = type
                if type != "door":
                    resets[reset_index]["vnum to reset"] = reset_vnum
                else:
                    resets[reset_index]["door direction"] = direction
                    resets[reset_index]["door state"] = state
                if type == "mobile":
                    resets[reset_index]["world limit"] = world_limit
                resets[reset_index]["location"] = location

                # When implementing these resets, keep track of the level
                # of the last mobile reset. Objects reset into a room or
                # container get their level set as the last mobile's level
                # minus 2!

                reset_index += 1

        elif afile_section == "shops":
            if my_line == "0":
                section_end = True
            else:
                # Turn the string into a list of form "mob, item_type_0,
                # item_type_1, item_type_2, item_type_3, sell_percentage,
                # buy_percentage, open, close.

                shops_list = my_line.split(" ")

                # Get the mnum of the shopkeeper mobile.
                mnum = "m" + shops_list[0]

                # Iterate through shops_list item types and turn from numbers
                # into text.
                for index in range(1, 5):

                    item_type = int(shops_list[index])

                    if item_type == 1:
                        item_type = "light"
                    elif item_type == 2:
                        item_type = "scroll"
                    elif item_type == 3:
                        item_type = "wand"
                    elif item_type == 4:
                        item_type = "staff"
                    elif item_type == 5:
                        item_type = "scroll"
                    elif item_type == 8:
                        item_type = "treasure"
                    elif item_type == 9:
                        item_type = "armor"
                    elif item_type == 10:
                        item_type = "potion"
                    elif item_type == 12:
                        item_type = "furniture"
                    elif item_type == 15:
                        item_type = "container"
                    elif item_type == 17:
                        item_type = "drink container"
                    elif item_type == 18:
                        item_type = "key"
                    elif item_type == 19:
                        item_type = "food"
                    elif item_type == 20:
                        item_type = "money"
                    elif item_type == 22:
                        item_type = "boat"
                    elif item_type == 23:
                        item_type = "corpse npc"
                    elif item_type == 24:
                        item_type = "corpse pc"
                    elif item_type == 25:
                        item_type = "fountain"
                    elif item_type == 26:
                        item_type = "pill"
                    elif item_type == 27:
                        item_type = "fly"
                    elif item_type == 28:
                        item_type = "portal"
                    elif item_type == 29:
                        item_type = "scroll"
                    else:
                        item_type = "trash"

                    shops_list[index] = item_type

                # Populate the shopkeeper dictionary for that mobile.
                mobiles[mnum].shopkeeper["item will buy 1"] = shops_list[1]
                mobiles[mnum].shopkeeper["item will buy 2"] = shops_list[2]
                mobiles[mnum].shopkeeper["item will buy 3"] = shops_list[3]
                mobiles[mnum].shopkeeper["item will buy 4"] = shops_list[4]
                mobiles[mnum].shopkeeper["sell percentage"] = shops_list[5]
                mobiles[mnum].shopkeeper["buy percentage"] = shops_list[6]
                mobiles[mnum].shopkeeper["opening hour"] = shops_list[7]
                mobiles[mnum].shopkeeper["closing hour"] = shops_list[8]

        elif afile_section == "specials":
            if my_line == "S":
                section_end = True
            else:
                # Turn the string into a list of form "letter, vnum,
                # special_function".

                special_function_list = my_line.split(" ")

                if special_function_list[0] == "M":
                    mnum = "m" + special_function_list[1]
                    mobiles[mnum].special_function\
                        = special_function_list[2][5:]
                elif special_function_list[0] == "O":
                    onum = "o" + special_function_list[1]
                    objects[onum].special_function\
                        = special_function_list[2][6:]

# Now we are going to build out the batch file by iterating through each
# room.

# First we need to dig all the rooms, using the vnums with a leading R to
# create unique aliases for each so that we can do the next step and link
# all in one go, and preserve the ability to use M and O with vnums for
# mobiles and objects.

total_resets = len(resets)
door_list = []

for index in range(total_resets):
    reset = index-1
    print(resets[reset])