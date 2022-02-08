# Command to run in IDLE is exec(open('Room Ripper.py').read())
#
# Be sure that before you try to use, you make sure that if you have done this
# before (or if you already use unique numbers to refer to your rooms) that
# they do not overlap with any of the vnums of what you are going to load.
# Also remember to set starting_vnum, below, so that exits can get vnums, and
# area_name, so that everything can get tagged.
#
# Remember when running not to use the .ev suffix.

# Need to handle tagging separately.

with open("C:/Users/bradm/mudstuff/school.txt", "rt") as myfile:

    temp_string = ""

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

    starting_vnum =
    area_name =
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


