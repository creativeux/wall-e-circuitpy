# Every pin assignment for the costume. Nothing else goes in this file.
#
# If the wiring changes, change this file and the pin table in README.md
# (section 4) together.

import board

# Servos (PWM out, 50 Hz)
HEAD_LEFT = board.GP0
HEAD_RIGHT = board.GP1
EYEBROW_LEFT = board.GP2
EYEBROW_RIGHT = board.GP3
WIPER_LEFT = board.GP4
WIPER_RIGHT = board.GP5
BELLY_DOOR = board.GP6

# NeoPixel strip data (DIN)
NEOPIXEL = board.GP7

# Switches and button. Each one connects its pin to GND,
# so pressed/on reads False.
BELLY_TOGGLE = board.GP13
WIPER_TOGGLE = board.GP14
EYEBROW_BUTTON = board.GP15

# Potentiometer wiper (middle pin). The pot gets 3.3 V, never 5 V.
HEAD_POT = board.GP26

# The little LED on the Pico itself
ONBOARD_LED = board.LED
