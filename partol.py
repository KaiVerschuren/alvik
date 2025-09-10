from arduino import *
from arduino_alvik import ArduinoAlvik

alvik = ArduinoAlvik()

def setup():
    alvik.begin()
    delay(1000)
  
def loop():
    alvik.set_wheels_speed(30, 30)
    delay(12000)
    alvik.set_wheels_speed(0, 0)

    alvik.set_wheels_speed(30, -30)
    delay(1350)
    alvik.set_wheels_speed(0, 0)

    alvik.set_wheels_speed(30, 30)
    delay(7000)
    alvik.set_wheels_speed(0, 0)

    alvik.set_wheels_speed(30, -30)
    delay(1350)
    alvik.set_wheels_speed(0, 0)

    alvik.set_wheels_speed(30, 30)
    delay(7000)
    alvik.set_wheels_speed(0, 0)

    alvik.set_wheels_speed(-30, 30)
    delay(1350)
    alvik.set_wheels_speed(0, 0)
    alvik.set_wheels_speed(-30, 30)
    delay(1350)
    alvik.set_wheels_speed(0, 0)

    alvik.set_wheels_speed(30, 30)
    delay(7000)
    alvik.set_wheels_speed(0, 0)

    alvik.set_wheels_speed(-30, 30)
    delay(1350)
    alvik.set_wheels_speed(0, 0)

    alvik.set_wheels_speed(30, 30)
    delay(7000)
    alvik.set_wheels_speed(0, 0)

    alvik.set_wheels_speed(-30, 30)
    delay(1350)
    alvik.set_wheels_speed(0, 0)

    alvik.set_wheels_speed(30, 30)
    delay(12000)
    alvik.set_wheels_speed(0, 0)

    alvik.set_wheels_speed(30, -30)
    delay(1350)
    alvik.set_wheels_speed(0, 0)
    alvik.set_wheels_speed(30, -30)
    delay(1350)
    alvik.set_wheels_speed(0, 0)

def cleanup():
    alvik.stop()
  
start(setup, loop, cleanup)
