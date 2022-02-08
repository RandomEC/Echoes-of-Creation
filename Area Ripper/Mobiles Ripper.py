# Command to run in IDLE is exec(open('C:/Users/bradm/mudstuff/mygame/Area Ripper/Mobiles Ripper.py').read())
#
# Be sure that before you try to use, you make sure that if you have done this
# before (or if you already use unique numbers to refer to your rooms) that
# they do not overlap with any of the vnums of what you are going to load.
#
# Remember when running not to use the .ev suffix.

# Need to handle tagging separately.

with open("C:/Users/bradm/mudstuff/smurf_mobs.txt", "rt") as myfile:

    temp_string = ""

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

    mobiles = {}
    mobile_data = 0
    mobile_number = 0
    temp_string = ""
    program = False

    for my_line in myfile:               # for each line, read to a string

        # Remove the newline character.
        my_line = my_line.strip()

        # If the line is empty, ignore it.
        if not my_line:
            pass

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

for mobile in mobiles:
    print(mobiles[mobile].name)
    print(mobiles[mobile].vnum)
    print(mobiles[mobile].keywords)
    print(mobiles[mobile].short_description)
    print(mobiles[mobile].long_description)
    print(mobiles[mobile].look_description)
    print(mobiles[mobile].act_flags)
    print(mobiles[mobile].affected_flags)
    print(mobiles[mobile].alignment)
    print(mobiles[mobile].level)
    print(mobiles[mobile].sex)
