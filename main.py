from arduino import *
from arduino_alvik import ArduinoAlvik
import time

alvik = ArduinoAlvik()

scripts = [
    {"name": "Escape Room",   "file": "colors.py",   "color": (1, 0, 0)},  # red
    {"name": "Walk the Bridge","file": "NoWayOut.py","color": (0, 1, 0)},  # green
    {"name": "Rainbow Road",  "file": "level1.py",   "color": (0, 0, 1)},  # blue
]

index = 0
pressed = False
DEBOUNCE = 0.12

def show_color():
    c = scripts[index]["color"]
    alvik.left_led.set_color(c[0], c[1], c[2])
    alvik.right_led.set_color(c[0], c[1], c[2])

def setup():
    alvik.begin()
    show_color()

def loop():
    global index, pressed

    up = alvik.get_touch_up()
    down = alvik.get_touch_down()
    ok = alvik.get_touch_ok()

    if not pressed:
        if up:
            index = (index + 1) % len(scripts)
            show_color()
            pressed = True

        elif down:
            index = (index - 1) % len(scripts)
            show_color()
            pressed = True

        elif ok:
            try:
                exec(open(scripts[index]["file"]).read())
            except Exception as e:
                print("Error:", e)
            pressed = True

    if not (up or down or ok):
        pressed = False

    time.sleep(DEBOUNCE)

def cleanup():
    alvik.left_led.set_color(0, 0, 0)
    alvik.right_led.set_color(0, 0, 0)
    alvik.stop()

start(setup, loop, cleanup)
