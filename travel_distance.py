from arduino import *
from arduino_alvik import ArduinoAlvik

alvik = ArduinoAlvik()

def setup():
  alvik.begin()
  delay(1000)

def loop():
  # Drive forward
  alvik.set_wheels_speed(30,30)
  # 6 seconden voor 30cm
  delay(6000)
  alvik.set_wheels_speed(0,0)
  delay(10000)

def cleanup():
  alvik.stop()

start(setup, loop, cleanup)
