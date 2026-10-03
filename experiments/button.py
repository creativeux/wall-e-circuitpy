# Read the eyebrow button.
# The button connects GP15 to GND and the code turns on the internal
# pull-up, so pressed reads False.
#
# Run it with: python tools/deploy.py experiments/button.py

import time

import board
import digitalio

button = digitalio.DigitalInOut(board.GP15)
button.switch_to_input(pull=digitalio.Pull.UP)

while True:
    pressed = not button.value
    print("pressed" if pressed else "released")
    time.sleep(0.2)
