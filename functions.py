from arduino import *
from arduino_alvik import ArduinoAlvik

alvik = ArduinoAlvik()

def pivot_90_right():
  alvik.set_wheels_speed(30, -30)
  delay(1350)

def pivot_90_left():
  alvik.set_wheels_speed(-30, 30)
  delay(1350)

def forward(speed, t):
    alvik.set_wheels_speed(speed, speed)  # use speed directly
    delay(t * 1000)  # convert seconds to ms
    alvik.set_wheels_speed(0, 0)

def backward(speed, t):
    alvik.set_wheels_speed(-speed, -speed)
    delay(t * 1000)
    alvik.set_wheels_speed(0, 0)
  

def setup():
  alvik.begin()
  delay(1000)
  
def loop():
  forward(30, 12)
  
  pivot_90_right()
  
  foward(30, 7)
  
  pivot_90_right()
  
  forward(30, 7)
  
  pivot_90_left()
  pivot_90_left()
  
  forward(30, 7)
  
  pivot_90_left()
  
  forward(30, 7)
  
  pivot_90_left()
  forward(30, 12)
  
  pivot_90_right()
  pivot_90_right()


def cleanup():
  alvik.stop()
  
start(setup, loop, cleanup)