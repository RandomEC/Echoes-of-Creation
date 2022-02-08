# Command to run in IDLE is exec(open('C:/Users/bradm/mudstuff/mygame/Area Ripper/Object Ripper.py').read())
#
# Be sure that before you try to use, you make sure that if you have done this
# before (or if you already use unique numbers to refer to your rooms) that
# they do not overlap with any of the vnums of what you are going to load.
#
# Remember when running not to use the .ev suffix.

# Need to handle tagging separately.

import random
from C:/Users/bradm/mudstuff/mygame/world import rules 

with open ("C:/Users/bradm/mudstuff/smurf_objects.txt","rt") as myfile:


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
        elif my_line[0] == "#" and section_end = True:

            # Tell the program which section of the afile it is in.
            if my_line[1:] == "AREA":
                afile_section = "area"
            elif my_line[1:] == "HELPS":
                afile_section = "helps"
            elif my_line[1:] == "RECALL":
                afile_section = "recall"
            elif my_line[1:] == "MOBILES":
                afile_section = "mobiles"
            elif my_line[1:] == "OBJECTS":
                afile_section = "objects"
            elif my_line[1:] == "ROOMS":
                afile_section = "rooms"
            elif my_line[1:] == "RESETS":
                afile_section = "resets"
            elif my_line[1:] == "SHOPS":
                afile_section = "shops"
            elif my_line[1:] == "SPECIALS":
                afile_section = "specials"
            elif my_line[1:] == "GAMES":
                afile_section = "games"
            
            # Since you have started a new section, set section_end
            # back to False.
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
                    temp_string = temp_string + " " + my_line[:-1]

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
                    temp_string = temp_string + " " + my_line

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
                        temp_string = temp_string + " " + my_line[:-1]

                        # make sure string has content
                        if temp_string:

                            # set the description
                            rooms[object_number-1].\
                                doors[door_direction]["description"] = temp_string

                        # clear the temp_string
                        temp_string = ""

                        # tell the function the next data to get is the exit
                        # keywords line
                        door_line = 2

                    else:

                        # if no ~, add to what you have so far
                        temp_string = temp_string + " " + my_line

                elif door_line == 2:

                    # see if you are at the end of the exit keywords
                    if my_line[-1] == "~":

                        # if so, strip the ~
                        my_line = my_line[:-1]

                        if my_line != "" and my_line != " ":
                            temp_string = temp_string + " " + my_line

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
                        temp_string = temp_string + " " + my_line

                elif door_line == 3:

                    # split the line into a three-item list
                    locks_key_destination = my_line.split()

                    # set locks
                    locks = int(locks_key_destination[0])

                    if locks == 1:
                        locks = tuple()
                    elif locks == 2:
                        locks = ("pickproof",)
                    elif locks == 3:
                        locks = ("bashproof",)
                    elif locks == 4:
                        locks = ("pickproof", "bashproof",)
                    elif locks == 5:
                        locks = ("passproof",)
                    elif locks == 6:
                        locks = ("pickproof", "passproof")
                    elif locks == 7:
                        locks = ("bashproof", "passproof",)
                    else:
                        locks = ("pickproof", "bashproof", "passproof",)

                    rooms[object_number-1].doors[door_direction]["locks"] = locks

                    rooms[object_number-1].doors[door_direction]["key"]\
                        = locks_key_destination[1]

                    rooms[object_number-1].doors[door_direction]["destination"]\
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
                        temp_string = temp_string + " " + my_line[:-1]

                        # set the keywords
                        rooms[object_number-1].extra_description[temp_string] = ""

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
                        temp_string = temp_string + " " + my_line

                elif extra_line == 2:

                    # see if you are at the end of the extra description
                    if my_line[-1] == "~":

                        # if so, strip the ~
                        temp_string = temp_string + " " + my_line[:-1]

                        # set the description
                        rooms[object_number-1].extra_description[keywords]\
                            = temp_string

                        # clear the temp_string
                        temp_string = ""

                        # done with this extra description
                        extra_line = 0

                    else:

                        # if no ~, add to what you have so far
                        temp_string = temp_string + " " + my_line

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

                # See if you are at the end of the keywords. Really only doing this
                # check in case the area author put the ~ on the line after the
                # keywords, instead of at the end of it.
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

                    # Tell the function the next data to get is look description.
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

                # Turn the string into a list of form "act flags, affected flags,
                # alignment".

                stat_list = my_line.split(" ")
                act_flags_list = list()

                act_flags = int(stat_list[0])

                # Act flags were originally a binary number that indicated whether
                # a flag was active by activating that bit. We turn it into a list
                # by taking off each successive power of two. Many of these were
                # unused on Castle Arcanum, and, so, are blank below. If they carry
                # data for the MUD you are importing from, fill in below.

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

                # Extra flags used to be a binary, where they used each bit as a flag to know if the
                # flag was active. We disaggregate into a list.
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
                    extra_flags = extra_flags - 1;
                    extra_flags_list.append("glow")

                # stick the newly-made list into the object.
                if extra_flags_list:
                    objects[onum].extra_flags = extra_flags_list

                # Increment to get the last line of the flags.
                extended_flags_format += 1

            elif extended_flags_format == 2:
                # Wear flags used to be a binary, where they used each bit as a flag to know if the
                # flag was active. We split off the ability to take the item, and disaggregate the 
                # rest into a list. We won't allow multiple wear locations, so we will take the 
                # lowest allowable wear slot at the end.
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

                # turn the vnum string into an onum and store
                onum = "o" + temp_string

                # create a new Object object with the key of that onum
                objects[onum] = Object()

                # store the onum in the Object itself, as well
                objects[onum].vnum = onum

                # tell the function the next data to get is keywords
                object_data = "keywords"

                # clear temp_string
                temp_string = ""

            elif object_data == "keywords":

                # see if you are at the end of the keywords, really only doing this
                # check in case they put the ~ on the line after the keywords,
                # instead of at the end of it.
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

                    # tell the function the next data to get is room_flags and terrain
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
                        
                        # set the description
                        objects[onum].short_description = temp_string

                    # clear the temp_string
                    temp_string = ""

                    # tell the function the next data to get is room_flags and terrain
                    object_data = "long description"

                else:

                    # if no ~, add to what you have so far
                    if temp_string:
                        temp_string = temp_string + " " + my_line
                    else:
                        temp_string = my_line

            elif object_data == "long description":

                # see if you are at the end of the long description.
                if my_line[-1] == "~":

                    # if so, strip the ~
                    if temp_string:
                        temp_string = temp_string + " " + my_line[:-1]
                    else:
                        temp_string = my_line[:-1]

                    # make sure string has content
                    if temp_string:
                        
                        # set the description
                        objects[onum].long_description = temp_string

                    # clear the temp_string
                    temp_string = ""

                    # tell the function the next data to get is look description
                    object_data = "look description"

                else:

                    # if no ~, add to what you have so far
                    if temp_string:
                        temp_string = temp_string + " " + my_line
                    else:
                        temp_string = my_line

            elif object_data == "look description":

                # most area files won't have a look description for objects, but some will. 
                # In any event, there WILL be a ~ where one should be, so we may as well 
                # handle it the same way, which will cover both cases anyway.
                if my_line[-1] == "~":

                    # if so, strip the ~
                    if temp_string:
                        temp_string = temp_string + " " + my_line[:-1]
                    else:
                        temp_string = my_line[:-1]

                    # make sure string has content
                    if temp_string:
                        
                        # set the description
                        objects[onum].look_description = temp_string

                    # clear the temp_string
                    temp_string = ""

                    # tell the function the next data to get is room_flags and terrain
                    object_data = "type extra wear"

                else:

                    # if no ~, add to what you have so far
                    if temp_string:
                        temp_string = temp_string + " " + my_line
                    else:
                        temp_string = my_line

            elif object_data == "type extra wear":

                # Turn the string into a list of form "item type, extra flags, wear flag"
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
                
                # Stick the item type into the object.
                objects[onum].item_type = item_type

                if len(stat_list) == 1:
                    extended_flags_format = 1

                else:
                    # Extra flags used to be a binary, where they used each bit as a flag to know if the
                    # flag was active. We disaggregate into a list.
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
                        extra_flags = extra_flags - 1;
                        extra_flags_list.append("glow")

                    # stick the newly-made list into the object.
                    if extra_flags_list:
                        objects[onum].extra_flags = extra_flags_list

                    # Wear flags used to be a binary, where they used each bit as a flag to know if the
                    # flag was active. We split off the ability to take the item, and disaggregate the 
                    # rest into a list. We won't allow multiple wear locations, so we will take the 
                    # lowest allowable wear slot at the end.
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
                    
                    # if there is a wear slot, take the lowest numbered one and
                    # put it on the object.
                    if wear_flags_list:
                        objects[onum].wear_location = wear_flags_list[-1]

                # tell the function the next data to get is item values
                object_data = "values"

            elif object_data == "values":

                # again, split the line on spaces
                stat_list = my_line.split("~")

                # store the value_0 in the mobile object            
                objects[onum].value_0 = stat_list[0].strip()

                # store the value_0 in the mobile object            
                objects[onum].value_1 = stat_list[1].strip()

                # store the value_0 in the mobile object            
                objects[onum].value_2 = stat_list[2].strip()

                # store the value_0 in the mobile object            
                objects[onum].value_3 = stat_list[3].strip()

                # tell the function the next data to get is the weight.
                object_data = "weight"

            # Take the weight off this line and discard the rest, which have
            # unknown historical use.
            elif object_data == "weight":

                # again, split the line on spaces
                stat_list = my_line.split(" ")

                # store the weight in the mobile object            
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
                            
                            # set the keywords
                            objects[onum].extra_description[temp_string] = ""

                            # set the keywords value for finding in dictionary below for description
                            keywords = temp_string
                    
                            # clear the temp_string
                            temp_string = ""

                            # tell the function the next data to get is the extra description
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
                        objects[onum].extra_description[keywords] = temp_string
                
                        # clear the temp_string
                        temp_string = ""

                        # done with this extra description
                        extra_line = 0
                    
                    else:

                        # if no ~, add to what you have so far
                        temp_string = temp_string + " " + my_line

            elif my_line == "A" or apply_line > 0:

                if apply_line == 0:
                    apply_line = 1
                    print("Test 0")

                elif apply_line == 1:
                    print("Test 1")

                    # again, split the line on spaces
                    stat_list = my_line.split(" ")
                    print("test")
                    
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
                    
                    # set the apply type for this apply.
                    objects[onum].apply[apply_type] = apply_value
                    apply_line = 0
        
        elif afile_section == "resets":
            if my_line == "S":
                section_end = True
        
            # Create a new dictionary for each reset.
            resets[reset_index] = {}

            # Turn the reset string into a list.
            reset_list = my_line.split(" ")

            # For door resets, purge the list of any "" instances.
            reset_list.remove("")

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

        elif afile_section == "shops"
            if my_line == "0":
                section_end = True
        
        
            # Turn the string into a list of form "mob, item_type_0,
            # item_type_1, item_type_2, item_type_3, sell_percentage,
            # buy_percentage, open, close.

            shops_list = my_line.split(" ")

            # Get the mnum of the shopkeeper mobile.
            mnum = "m" + shops_list[0]

            # Iterate through shops_list item types and turn from numbers
            # into text.
            for index in range(1,5):
                
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

        elif afile_section == "specials"
            if my_line == "#0":
                section_end = True
        

            # Turn the string into a list of form "letter, vnum,
            # special_function".

            special_function_list = my_line.split(" ")

            if special_function_list[0] == "M":
                mnum = "m" + special_function_list[1]
                mobiles[mnum].special_function = special_function_list[2][5:]
            elif special_function_list[0] == "O":
                onum = "o" + special_function_list[1]
                objects[onum].special_function = special_function_list[2][6:]

# Now we are going to build out the batch file by iterating through each room

# First we need to dig all the rooms, using the vnums with a leading R to
# create unique aliases for each so that we can do the next step and link all
# in one go, and preserve the ability to use M and O with vnums for mobiles
# and objects.

total_rooms = len(rooms)
door_list = []

for index in range(total_rooms):

    room = index - 1

    print("dig/tel %s; R%s" % (rooms[room].name, rooms[room].vnum))
    print("#")
    print("tag %s = %s, category = area names" % (rooms[room].vnum,
                                                  area_name.lower()))
    print("#")
    print('desc R%s = %s' % (rooms[room].vnum, rooms[room].description))
    print("#")
    print("desc/edit R%s" % rooms[room].vnum)
    print("#")
    print(":j l")
    print("#")
    print(":wq")
    print("#")
    print('set R%s/terrain = "%s"' % (rooms[room].vnum, rooms[room].terrain))
    print("#")

    if rooms[room].extra_description:

        extra_string = ""

        for keyword in rooms[room].extra_description:
            extra_string = extra_string \
                           + ('"%s":"%s"' %
                              (keyword,
                               rooms[room].extra_description[keyword]
                               ))

        print("set R%s/extra_description = {%s}" % (rooms[room].vnum,
                                                    extra_string
                                                    ))
        print("#")

    if rooms[room].room_flags:

        print("set R%s/room_flags = %s" % (rooms[room].vnum,
                                           rooms[room].room_flags))
        print("#")

for index in range(total_rooms):

    room = index - 1
    print("tel R%s" % rooms[room].vnum)
    print("#")

    for door in rooms[room].doors:

        if rooms[room].doors[door]["destination"]:

            # Assigning vnum and one letter direction alias to door.
            vnum = ("e%s" % (starting_vnum + exit_number))
            exit_number += 1
            door_and_vnum = list(door[0], vnum)
            aliases = "; ".join(door_and_vnum)
            # if the door has its own keywords, add those to the above.
            if rooms[room].doors[door]["keywords"] != " " \
                    and rooms[room].doors[door]["keywords"] != "":

                rooms[room].doors[door]["keywords"].append(aliases)

                aliases = "; ".join(rooms[room].doors[door]["keywords"])

            # this comparison is to make sure that only one set of doors gets
            # opened.

            room_set = ""
            room1 = int(rooms[room].vnum)
            room2 = int(rooms[room].doors[door]["destination"])

            if room1 < room2:
                room_set = ("%d, %d" % (room1, room2))
            else:
                room_set = ("%d, %d" % (room2, room1))

            if room_set not in door_list:

                if door == "north":
                    opposite_door = "south"
                elif door == "east":
                    opposite_door = "west"
                elif door == "south":
                    opposite_door = "north"
                elif door == "west":
                    opposite_door = "east"
                elif door == "up":
                    opposite_door = "down"
                elif door == "down":
                    opposite_door = "up"

                print('open %s; %s, %s = R%s' % (door,
                                                 aliases,
                                                 opposite_door,
                                                 rooms[room].
                                                 doors[door]["destination"]
                                                 ))
                print("#")
                print("tag %s = %s, category = area names" % (vnum,
                                                              area_name.lower()
                                                              ))
                print("#")
                door_list.append(room_set)

            else:

                print("alias %s = %s" % (door, aliases))
                print("#")
                print("tag %s = %s, category = area names" % (vnum,
                                                              area_name.lower()
                                                              ))
                print("#")

            if rooms[room].doors[door]["description"]:
                print("desc %s = %s" % (door,
                                        rooms[room].doors[door]["description"]
                                        ))
                print("#")

            if int(rooms[room].doors[door]["key"]) >= 0:
                print("set %s/key = %s" % (door,
                                           rooms[room].doors[door]["key"]
                                           ))
                print("#")

            if rooms[room].doors[door]["locks"]:
                print("set %s/locks = %s" % (door,
                                             rooms[room].doors[door]["locks"]
                                             ))
                print("#")

        



for reset in reset_list:

    # 1. Get the reset data.

    # First, the data that all resets have.
    reset_location = reset_list[reset]["location"]
    reset_type = reset_list[reset]["type"]

    # Get the data specific to certain types of resets.
    if reset_list[reset]["type"] != "door":

        # Both mobiles and objects have a vnum.
        reset_vnum = reset_list[reset]["vnum to reset"]

        # Use the vnum to get the actual object in memory that you are
        # placing and creating a reset for.
        if reset_list[reset]["type"] == "mobile":
            object = mobiles[reset_vnum]
        else:
            object = objects[reset_vnum]
            
    # And if it is a door, get the door-specific data.
    else:
        reset_direction = resets[reset_index]["door direction"]
        reset_state = resets[reset_index]["door state"]        
    
    # 2. Teleport to the location that the object resets to, and create
    # an instance of the mobile/object. For objects that reset in
    # containers, we will later teleport to the room to create the
    # reset itself.
    print("tel %s" % reset_location)
    print("#")

    # Create the instance of the thing, unless it is a door, or a portal,
    # which is just a door in hiding. We'll take the information
    # for portals and make an exit later.
    if reset_type != "door" and object.item_type != "portal":

        # Turn keywords string into a semicolon-delineated list, as that is
        # the syntax for aliases, which is what they'll be.
        keyword_list = object.keywords.split(" ")
        keyword_string = ";".join(keyword_list)

        # Generalize the mobile/object as "object".
        if type == "mobile":
            print("create/drop %s;%s:characters.Mobile" % (object.short_description, keyword_string))
        else:
            print("create/drop %s;%s:objects.%s" % (object.short_description, keyword_string, object.item_type.capitalize()))

        print("#")

        # Set the long description for the object/mobile.
        print("desc %s = %s" % (reset_vnum, object.long_description))
        print("#")

        # Setting level is slightly complex, as objects in Diku muds took their
        # level from either the mobile that they reset on, or the last mobile to
        # be reset.
        if reset_type == "mobile":
            
            # Store the mobile's level for use on an object not loaded on a
            # mobile, if necessary.
            last_mobile_level = object.level
            
            # If the object is a mobile, use its own level.
            level = object.level
    
        else:
            # Check to see if the object resets on a mobile.
            if reset_location[0] == "m":
                
                # Get the level from the mobile it resets on.
                level = mobiles[reset_location].level

            # If the object does not reset on a mobile, get the level of the
            # last mob.
            else:
                level = last_mobile_level

        # Use the level you got above to set level.
        print("set %s/level = %d" % (reset_vnum, level))
        print("#")

        # Objects and mobiles also get a base level so that some variation
        # can be put in their level when they are reset.
        print("set %s/level_base = %d" % (reset_vnum, level))
        print("#")
        print("set %s/vnum = %s" % (reset_vnum, reset_vnum))
        print("#")

        # Not everything has a look description so check before setting.
        if object.look_description:
            print("set %s/look_description = %s" % (reset_vnum, object.look_description))
            print("#")

        # Now, set the mobile-specific characteristics.
        if type == "mobile":

            if object.act_flags:
                print("set %s/act_flags = %s" % (reset_vnum, object.act_flags))
                print("#")
                
            print("set %s/alignment = %d" % (reset_vnum, object.alignment))
            print("#")
            print("set %s/sex = %s" % (reset_vnum, object.sex))
            print("#")

            # Turn the affected flags list into a dictionary. All of the affects that
            # would be on mobiles are all boolean affects, so all we need to know is
            # that they are on the mobile. So the dictionary is all keys of the affect
            # and a blank string.
            if object.affected_flags:
                affects_dictionary = {}
                for affect in object.affected_flags:
                    affects_dictionary[affect] = ""
            print("set %s/spell_affects = %s" % (reset_vnum, affects_dictionary))
            print("#")
            
            print("set %s/race = %s" % (reset_vnum, object.race))
            print("#")
            print("tag %s = %s:area name" % (reset_vnum, area_name))
            print("#")

            # Setting hitpoints for mobiles is a factor of the mobile's level. Set
            # both max hp and current hitpoints to it.
            level = object.level
            hitpoints = level*8 + random.randint((level/4),(level*level))
            print("set %s/hitpoints[maximum] = %d" % (reset_vnum, hitpoints))
            print("#")
            print("set %s/position = \"standing\"" % reset_vnum)
            print("#")

            # Special functions and shopkeepers are both things not every mobile
            # will have. So, check to make sure that they are on things before
            # setting it.
            if mobiles[reset_vnum].special_function:
                print("set %s/special_function = %s" % (reset_vnum, object.special_function))
                print("#")
            if mobiles[reset_vnum].shopkeeper:
                print("set %s/shopkeeper = %s" % (reset_vnum, object.shopkeeper))
                print("#")

        # Deal with object-specific characteristics for all non-portal objects.
        else:

            
            if object.item_type:
                print("set %s/item_type = %s" % (reset_vnum, object.item_type))
                print("#")
            if object.wear_location:
                print("set %s/wear_location = %s" % (reset_vnum, object.wear_location))
                print("#")
            print("set %s/weight = %d" % (reset_vnum, object.weight))
            print("#")
            if object.extra_descriptions:
                print("set %s/extra_descriptions = %s" % (reset_vnum, object.extra_description))
                print("#")
            alignment_restriction = []
            if "anti neutral" in object.extra_flags:
                alignment_restriction.append("neutral")
            if "anti good" in object.extra_flags:
                alignment_restriction.append("good")
            if "anti evil" in object.extra_flags:
                alignment_restriction.append("evil")
            if alignment_restriction:
                print("set %s/alignment_restriction = %s" % (reset_vnum, alignment_restriction))
                print("#")
            extra_flags = []
            for flag in object.extra_flags:
                if flag not in ["anti neutral", "anti good", "anti evil"]:
                    extra_flags.append(flag)
            if extra_flags:
                print("set %s/extra_flags = %s" % (reset_vnum, extra_flags))
                print("#")
            if object.special_function:
                print("set %s/special_function = %s" % (reset_vnum, object.special_function))
                print("#")
            if object.apply:
                for apply_type in object.apply:
                    print("set %s/stat_modifiers[%s] = %d" % (reset_vnum, apply_type, object.apply[apply_type]))
                    print("#")
            if object.value_0:
                value_0 = int(object.value_0)
                if object.item_type in ("scroll", "pill", "wand", "staff", "potion"):
                    print("set %s/spell_level = %d" % (reset_vnum, value_0))
                    print("#")
                    print("set %s/spell_level_base = %d" % (reset_vnum, value_0))
                    print("#")
                elif object.item_type == "furniture":
                    print("set %s/people_maximum = %d" % (reset_vnum, value_0))
                    print("#")
                elif object.item_type == "container":
                    print("set %s/weight_maximum = %d" % (reset_vnum, value_0))
                    print("#")
                elif object.item_type == "drink container":
                    print("set %s/capacity_maximum = %d" % (reset_vnum, value_0))
                    print("#")
                elif object.item_type == "food":
                    print("set %s/hours_fed = %d" % (reset_vnum, value_0))
                    print("#")
                elif object.item_type == "money":
                    print("set %s/value = %d" % (reset_vnum, value_0))
                    print("#")
                elif object.item_type == "scuba":
                    print("set %s/charges = %d" % (reset_vnum, value_0))
                    print("#")
            if object.value_1:
                if object.item_type in ("scroll", "pill", "potion"):
                    print("set %s/spell_name_1 = %s" % (reset_vnum, object.value_1))
                    print("#")
                elif object.item_type in ("wand", "staff"):
                    value_1 = int(object.value_1)
                    print("set %s/charges_maximum = %d" % (reset_vnum, value_1))
                    print("#")
                    print("set %s/charges_maximum_base = %d" % (reset_vnum, value_1))
                    print("#")
                elif object.item_type == "furniture":
                    value_1 = int(object.value_1)
                    print("set %s/weight_maximum = %d" % (reset_vnum, value_1))
                    print("#")
                elif object.item_type == "container":
                    last_container_room = reset_location
                    value_1 = int(object.value_1)
                    container_state_list = []
                    if value_1 >= 8:
                        container_state_list.append("locked")
                        value_1 -= 8
                    if value_1 >= 4:
                        container_state_list.append("closed")
                        value_1 -= 4
                    if value_1 >= 2:
                        container_state_list.append("pickproof")
                        value_1 -= 2
                    if value_1 >= 1:
                        container_state_list.append("closeable")
                    print("set %s/state = %s" % (reset_vnum, container_state_list))
                    print("#")
                elif object.item_type == "drink container":
                    value_1 = int(object.value_1)
                    print("set %s/capacity_current = %d" % (reset_vnum, value_1))
                    print("#")
                elif object.item_type == "scuba":
                    value_1 = int(object.value_1)
                    print("set %s/charge_maximum = %d" % (reset_vnum, value_1))
                    print("#")
            if object.value_2:
                if object.item_type in ("scroll", "pill", "potion"):
                    print("set %s/spell_name_2 = %s" % (reset_vnum, object.value_2))
                    print("#")
                elif object.item_type in ("wand", "staff"):
                    value_2 = int(object.value_2)
                    print("set %s/charges_current = %d" % (reset_vnum, value_2))
                    print("#")
                elif object.item_type == "light":
                    value_2 = int(object.value_2)
                    print("set %s/light_hours= %d" % (reset_vnum, value_2))
                    print("#")
                elif object.item_type == "furniture":
                    value_2 = int(object.value_2)
                    furniture_position_list = []
                    if value_2 >= 2048:
                        furniture_position_list.append("sleep in")
                        value_2 -= 2048
                    if value_2 >= 1024:
                        furniture_position_list.append("sleep on")
                        value_2 -= 1024
                    if value_2 >= 512:
                        furniture_position_list.append("sleep at")
                        value_2 -= 512
                    if value_2 >= 256:
                        furniture_position_list.append("rest in")
                        value_2 -= 256
                    if value_2 >= 128:
                        furniture_position_list.append("rest on")
                        value_2 -= 128
                    if value_2 >= 64:
                        furniture_position_list.append("rest at")
                        value_2 -= 64
                    if value_2 >= 32:
                        furniture_position_list.append("sit in")
                        value_2 -= 32
                    if value_2 >= 16:
                        furniture_position_list.append("sit on")
                        value_2 -= 16
                    if value_2 >= 8:
                        furniture_position_list.append("sit at")
                        value_2 -= 8
                    if value_2 >= 4:
                        furniture_position_list.append("stand in")
                        value_2 -= 4
                    if value_2 >= 2:
                        furniture_position_list.append("stand on")
                        value_2 -= 2
                    if value_2 >= 1:
                        furniture_position_list.append("stand at")
                    print("set %s/use_positions = %s" % (reset_vnum, furniture_position_list))
                    print("#")
                elif object.item_type == "container":
                    key = "o" + object.value_2
                    print("set %s/key = %s" % (reset_vnum, key))
                    print("#")
                elif object.item_type == "drink container":
                    drink = int(object.value_2)
                    if drink == 0:
                        drink = "water"
                    elif drink == 1:
                        drink = "beer"
                    elif drink == 2:
                        drink = "wine"
                    elif drink == 3:
                        drink = "ale"
                    elif drink == 4:
                        drink = "dark ale"
                    elif drink == 5:
                        drink = "whiskey"
                    elif drink == 6:
                        drink = "lemonade"
                    elif drink == 7:
                        drink = "firebreather"
                    elif drink == 8:
                        drink = "local specialty"
                    elif drink == 9:
                        drink = "slime mold juice"
                    elif drink == 10:
                        drink = "milk"
                    elif drink == 11:
                        drink = "tea"
                    elif drink == 12:
                        drink = "coffee"
                    elif drink == 13:
                        drink = "blood"
                    elif drink == 14:
                        drink = "salt water"
                    elif drink == 15:
                        drink = "Coke"
                    elif drink == 16:
                        drink = "Dr. Pepper"
                    elif drink == 17:
                        drink = "Mountain Dew"
                    elif drink == 18:
                        drink = "Diet Coke"
                    elif drink == 19:
                        drink = "Sprite"
                    elif drink == 20:
                        drink = "hot chocolate"
                    elif drink == 21:
                        drink = "brandy"
                    elif drink == 22:
                        drink = "special hot chocolate"
                    print("set %s/liquid_type = %s" % (reset_vnum, drink))
                    print("#")
            if object.value_3:
                if object.item_type in ("scroll", "pill", "potion"):
                    print("set %s/spell_name_3 = %s" % (reset_vnum, object.value_3))
                    print("#")
                elif object.item_type in ("wand", "staff"):
                    print("set %s/spell_name = %s" % (reset_vnum, object.countvalue_3))
                    print("#")
                elif object.item_type == "weapon":
                    weapon_type = object.value_3
                    if weapon_type == 0:
                        weapon_type = "hit"
                    elif weapon_type == 1:
                        weapon_type = "slice"
                    elif weapon_type == 2:
                        weapon_type = "stab"
                    elif weapon_type == 3:
                        weapon_type = "slash"
                    elif weapon_type == 4:
                        weapon_type = "whip"
                    elif weapon_type == 5:
                        weapon_type = "claw"
                    elif weapon_type == 6:
                        weapon_type = "blast"
                    elif weapon_type == 7:
                        weapon_type = "pound"
                    elif weapon_type == 8:
                        weapon_type = "crush"
                    elif weapon_type == 9:
                        weapon_type = "grep"
                    elif weapon_type == 10:
                        weapon_type = "bite"
                    elif weapon_type == 11:
                        weapon_type = "pierce"
                    elif weapon_type == 12:
                        weapon_type = "suction"
                    elif weapon_type == 13:
                        weapon_type = "chop"
                    print("set %s/weapon_type = %s" % (reset_vnum, weapon_type))
                    print("#")
                elif object.item_type == "furniture":
                    heal_mana_gain = int(object.value_3)
                    print("set %s/heal_mana_gain = %d" % (reset_vnum, heal_mana_gain))
                    print("#")
                elif object.item_type in ("drink container", "food"):
                    poison = int(object.value_3)
                    print("set %s/poison = %d" % (reset_vnum, poison))
                    print("#")
            if object.item_type == "armor":
                armor = rules.set_armor(level)
                print("set %s/armor = %d" % (reset_vnum, armor))
                print("#")
            if object.item_type == "weapon":
                damage_low, damage_high = rules.set_weapon_low_high(level)
                print("set %s/damage_low = %d" % (reset_vnum, damage_low))
                print("#")
                print("set %s/damage_low = %d" % (reset_vnum, damage_low))
                print("#")

    elif object.item_type == "portal":

        # We are going to turn portals into just a special door.
        # Assigning vnum and one letter direction alias to door.
        vnum = ("e%s" % (starting_vnum + exit_number))
        exit_number += 1
        door_and_vnum = list("portal", vnum)
        aliases = "; ".join(door_and_vnum)

        # if the door has its own keywords, add those to the above.
        if object.keywords:
            keywords = object.keywords
            keywords.append(aliases)
            aliases = "; ".join(rooms[room].doors[door]["keywords"])

        # this comparison is to make sure that only one set of doors gets
        # opened.

        room_set = ""

        room1 = int(reset_location[1:])
        room2 = int(object.value_3)

        if room1 < room2:
            room_set = ("%d, %d" % (room1, room2))
        else:
            room_set = ("%d, %d" % (room2, room1))

        if room_set not in door_list:

            print('open portal; %s, portal = R%s' % (door,
                                         aliases,
                                         opposite_door,
                                         object.value_3
                                         ))
            print("#")
            print("tag %s = %s, category = area names" % (vnum,
                                                          area_name.lower()
                                                          ))
            print("#")
            door_list.append(room_set)

        else:

            print("alias portal = %s" % (aliases))
            print("#")
            print("tag %s = %s, category = area names" % (vnum,
                                                          area_name.lower()
                                                          ))
            print("#")

        if object.long_description:
            print("desc %s = %s" % (vnum,
                                    object.long_description
                                    ))
            print("#")


    # Check here if object needs to be equipped to mobile, and do so, if
    # necessary.

    if reset_type == "object, equipped":
        # set eq_slot on mobile equal to object - may need to add functionality to do this.
        # Maybe make a new switch on set - set/equip that calls equip on object, and make
        # set/remove a thing as well.
        # set equipped equal to True on object

    # 3. Create the reset for the object/mobile that was just created. For
    # mobiles, doors and objects that do not reset in containers, the
    # reset can be created where we currently are.
    
    # Reset for doors
    if reset_type == "door":
        state_list = []
        if reset_state == "open":
            state_list.append("open")
        elif reset_state == "closed":
            state_list.append("closeable")
        else:
            state_list.append("lockable")
            state_list.append("locked")
        print("set %s/door_attributes = %s" % (reset_direction, state_list))
        print("#")
        print("set %s/reset_door_attributes = %s" % (reset_direction, state_list))
        print("#")
    
    # Reset for objects in mobile inventory
    if reset_type == "object, in mobile inventory":
        print("set %s/reset_objects[\"%s\"] = \"inventory\"" % (reset_location, reset_vnum))
        print("#")
        
    # Reset for objects equipped to mobiles
    elif reset_type == "object, equipped":
        print("set %s/reset_objects[\"%s\"] = \"equipped\"" % (reset_location, reset_vnum))
        print("#")

    # Reset for objects in room inventory
    elif reset_type == "object, room":
        print("set %s/reset_objects[\"%s\"] = \"inventory\"" % (reset_location, reset_vnum))
        print("#")
        
    # Reset for objects in a container in a room
    elif reset_type == "object, in container"
        # Teleport to the room the container is in to do the reset.
        print("tel %s.location" % reset_location)
        print("#")
        # Now create the reset.
        print("set $s/reset_objects[\"%s\"] = \"%s\"" % (last_container_room, reset_vnum, reset_location))
        print("#")