#!/usr/bin/python

from math import pi

# converts command into a linear and angular number, signed for direction
# the linear component is in meters, the angular component is in degrees
def parse_command(command):
    command = command.lower()
    linear = 0
    angular = 0
    speed = 0
    tokens = command.split()

    # some things to ignore
    if len(tokens) < 2:
        return linear, angular, speed

    # custom speed specified
    if tokens[-2] == "s":
        try:
            speed = float(tokens[-1])
            print speed
        except ValueError:
            print "\tError: {0} is not a valid floating point number"
        
        if speed > 1:
            speed = 1
        if speed < 0:
            speed = 0
        
        tokens = tokens[:-2]
        print tokens, speed
    
    # simple move or turn command
    if len(tokens) == 2:
        if tokens[0] == "up" or tokens[0] == "down":
            try:
                linear = float(tokens[1])
            except ValueError:
                print "\tERROR: {0} is not a valid floating point number".format(tokens[1])

        elif tokens[0] == "left" or tokens[0] == "right":
            try:
                angular = float(tokens[1])
            except ValueError:
                print "\tERROR: {0} is not a valid floating point number".format(tokens[1])

        # invalid command
        else:
            print "\tERROR: invalid command, see BATCH_FORMAT.md for command structure"
        
        if tokens[0] == "down":
            linear *= -1
        if tokens[0] == "right":
            angular *= -1
    
    # arc command
    elif len(tokens) == 5:
        if tokens[0] == "up" or tokens[0] == "down":
            if tokens[1] == "left" or tokens[1] == "right":
                if tokens[3] == "r":
                    try:
                        linear = float(tokens[2])
                    except ValueError:
                        print "\tERROR: {0} is not a valid floating point number".format(tokens[2])
                    
                    try:
                        radius = float(tokens[4])
                    except ValueError:
                        print "\tERROR: {0} is not a valid floating point number".format(tokens[4])

                    angular = radius
                    
                    # angular = (linear / radius) * 180/pi
                    # linear is arc length, divide by radius to get angle in radians
                    # multiply by 180/pi to convert to degrees

        # invalid command
        else:
            print "\tERROR: invalid command, see BATCH_FORMAT.md for command structure"
        
        if tokens[0] == "down":
            linear *= -1
        if tokens[1] == "right":
            angular *= -1
    
    # invalid command
    else:
        print "\tERROR: invalid command, see BATCH_FORMAT.md for command structure"
    
    return linear, angular, speed
