from arduino import *
from arduino_alvik import ArduinoAlvik

import math

alvik = ArduinoAlvik()

lastColor = []
colors = []

average_color = []

unique = []

state = 0

STATE_CHECKING = 1
STATE_EVALUATE = 2
STATE_BACKWARDS = 3
STATE_FINISH = 4



def average(r, g, b):
    global average_color
    # pop first index if average_color already has 3.
    if len(average_color) >= 3:
        average_color.pop(0)
    # add rgb to list.
    average_color.append((r, g, b))

    # takes the first second and third values of each individual color in average color, adds them up and divides them to get an average.

    # example list of last 3 colors:
    # [(169, 123, 131), (168, 123, 129), (167, 123, 130)]
    # output:
    # [168 123 130]
    avg_r = sum(c[0] for c in average_color) / len(average_color)
    avg_g = sum(c[1] for c in average_color) / len(average_color)
    avg_b = sum(c[2] for c in average_color) / len(average_color)

    print("average rbg: ", int(avg_r), int(avg_g), int(avg_b))
    print("consists of: ", average_color)
    return int(avg_r), int(avg_g), int(avg_b)


def checkIfNewColor(r, g, b):
    global lastColor, colors, average_colors

    # if lastColor is empty, set it with the last rgb values read.
    if not lastColor:
        lastColor = (r, g, b)

        # if last color was empty, it adds it to the colors list as its always on first read.
        colors.append(lastColor)
        average_color.append(lastColor)
        return False

    # average color isnt empty, so get averages for calculating differences per color.
    if average_color:
        avg_r = sum(c[0] for c in average_color) / len(average_color)
        avg_g = sum(c[1] for c in average_color) / len(average_color)
        avg_b = sum(c[2] for c in average_color) / len(average_color)

        # abs so ints arent turning out negative.
        diff_r = abs(lastColor[0] - avg_r)
        diff_g = abs(lastColor[1] - avg_g)
        diff_b = abs(lastColor[2] - avg_b)

    else:
        diff_r = 0
        diff_g = 0
        diff_b = 0
        return False

    margin = 25
    # make sure we have all 3 colors
    if len(average_color) == 3:
        if diff_r > margin or diff_g > margin or diff_b > margin:  # margin
            lastColor = [r, g, b]
            colors.append(lastColor)
            average_color.clear()

            alvik.left_led.set_color(1, 0, 0)
            alvik.right_led.set_color(1, 0, 0)
            delay(100)
            alvik.left_led.set_color(0, 0, 0)
            alvik.right_led.set_color(0, 0, 0)
            delay(100)

            print("New color detected: " + str(lastColor))
            return True
        else:
            return False


def getCurrentColor(checkIfNew = True):
    r, g, b = alvik.get_color_raw()

    # remap values
    r8 = int(r * 255 / 500)
    g8 = int(g * 255 / 500)
    b8 = int(b * 255 / 500)
    if checkIfNew:
        result = checkIfNewColor(r8, g8, b8)

        if not result:
            average(r8, g8, b8)
    else:
      return [r8, g8, b8]

def handleDriving():
    alvik.set_wheels_speed(30, 30)
    L, CL, C, CR, R = alvik.get_distance()
    # print(C)
    if C < 5:
        alvik.set_wheels_speed(0, 0)
        return True


def turnAround():
    alvik.set_wheels_speed(-30, 30)
    delay(1350)
    alvik.set_wheels_speed(0, 0)
    alvik.set_wheels_speed(-30, 30)
    delay(1350)
    alvik.set_wheels_speed(0, 0)


def evaluate(colors):
    margin = 15
    unique = []

    # enumerate for getting index + value
    for i, color1 in enumerate(colors):
        match_found = False
        for j, color2 in enumerate(colors):
            # dont check same index
            if i != j:
                # calculate the difference for all, check margin
                if all(abs(color1[k] - color2[k]) <= margin for k in range(3)):
                    match_found = True
                    break
        if not match_found:
            # if theres no match found
            unique.append(color1)

    return unique

def driveBack(unique):
    alvik.set_wheels_speed(-30, -30)

    currentColor = getCurrentColor(False)

    if checkIfFoundUique(unique[0], currentColor):
      alvik.set_wheels_speed(0, 0)
      return True
    return False

def checkIfFoundUique(unique, currentColor):
    margin = 15
    if all(abs(unique[i] - currentColor[i]) <= margin for i in range(3)):
        return True
    return False

def dance():
    while True:
        alvik.set_wheels_speed(30, 30)
        delay(500)
        alvik.set_wheels_speed(0, 0)
        delay(50)
        alvik.set_wheels_speed(-30, -30)
        delay(500)
        alvik.set_wheels_speed(0, 0)
        delay(50)
        alvik.set_wheels_speed(30, -30)
        delay(250)
        alvik.set_wheels_speed(0, 0)
        delay(50)

def setup():
    alvik.begin()
    delay(1000)


def loop():
    global state
    global colors
    global unique
    # print("state: " + str(state))
    if state == 0:
        state = STATE_CHECKING

    elif state == STATE_CHECKING:
        result = handleDriving()
        getCurrentColor(True)

        if result == True:
            state = STATE_EVALUATE

            print(colors)

    elif state == STATE_EVALUATE:
        unique = evaluate(colors)
        # turnAround()
        state = STATE_BACKWARDS

    elif state == STATE_BACKWARDS:
        print("going to look for: ", unique)
        if driveBack(unique):
          state = STATE_FINISH
    elif state == STATE_FINISH:
        dance()

    delay(100)


def cleanup():
    alvik.stop()


start(setup, loop, cleanup)
