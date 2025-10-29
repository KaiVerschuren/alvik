from arduino import *
from arduino_alvik import ArduinoAlvik

alvik = ArduinoAlvik()

currentPitch = 0;

state = 0

hasGoneDown = False

STATE_BEFORE_RAMP = 1
STATE_UP_RAMP = 2
STATE_WAIT_RAMP = 3
STATE_DOWN_RAMP = 4
STATE_END = 5

def getOrientation():
  roll, pitch, yaw = alvik.get_orientation()

  roll, pitch, yaw = round(roll, 2), round(pitch, 2), round(yaw, 2)
  currentPitch = pitch
  print("Pitch: ", pitch, "| State: ", state)
  return pitch

def setup():
  alvik.begin()
  delay(1000)

def loop():
    global state, currentPitch, hasGoneDown

    pitch = getOrientation()

    if state == 0:
        state = STATE_BEFORE_RAMP

    elif state == STATE_BEFORE_RAMP:
        alvik.set_wheels_speed(20, 20)
        if pitch <= 10:
            state = STATE_UP_RAMP

    elif state == STATE_UP_RAMP:
        alvik.set_wheels_speed(20, 20)
        if abs(pitch) < 2:
            state = STATE_WAIT_RAMP

    elif state == STATE_WAIT_RAMP:
        alvik.set_wheels_speed(0, 0)
        delay(1000)
        alvik.set_wheels_speed(20, 20)

        state = STATE_DOWN_RAMP

    elif state == STATE_DOWN_RAMP:
        alvik.set_wheels_speed(20, 20)
        if abs(pitch) > 4:
            if hasGoneDown == False:
              hasGoneDown = True
              print(hasGoneDown)
        if abs(pitch) < 2 and hasGoneDown == True:
            alvik.set_wheels_speed(0, 0)
    delay(200)


def cleanup():
  alvik.stop()

start(setup, loop, cleanup)

