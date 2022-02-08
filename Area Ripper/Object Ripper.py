# Command to run in IDLE is exec(open('C:/Users/bradm/mudstuff/mygame/Area Ripper/Object Ripper.py').read())
#
# Be sure that before you try to use, you make sure that if you have done this
# before (or if you already use unique numbers to refer to your rooms) that
# they do not overlap with any of the vnums of what you are going to load.
#
# Remember when running not to use the .ev suffix.

# Need to handle tagging separately.

with open ("C:/Users/bradm/mudstuff/smurf_objects.txt","rt") as myfile:

    temp_string = ""

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
            

    objects = {}
    object_data = 0
    object_number = 0
    temp_string = ""
    extra_line = 0
    apply_line = 0
    program = False
    extended_flags_format = 0
    
    for my_line in myfile:               # for each line, read to a string

        # remove the newline character
        my_line = my_line.strip()

        # if the line is empty, ignore it
        if not my_line:
            pass

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
            objects[onum].weight = stat_list[0]

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

            elif apply_line == 1:

                # again, split the line on spaces
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
                
                # set the apply type for this apply.
                objects[onum].apply[apply_type] = apply_value
                apply_line = 0

for object in objects:
    print(objects[object].vnum)
    print(objects[object].keywords)
    print(objects[object].short_description)
    print(objects[object].long_description)
    print(objects[object].look_description)
    print(objects[object].item_type)
    print(objects[object].extra_flags)
    print(objects[object].wear_location)
    print(objects[object].value_0)
    print(objects[object].value_1)
    print(objects[object].value_2)
    print(objects[object].value_3)
    print(objects[object].weight)
    print(objects[object].extra_description)
    print(objects[object].apply)
    print(objects[object].can_take)
    print(objects[object].special_function)
