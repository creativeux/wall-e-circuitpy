# Helpers that set up one piece of hardware on a pin.
# code.py uses these so its setup reads as a simple list.

import analogio
import digitalio
import neopixel
import pwmio
from adafruit_motor import servo

from common import settings

# Define a servo on a specified pin
def make_servo(pin):
    return servo.Servo(pwmio.PWMOut(pin, frequency=50))

# Define a switch on a specified pin
def make_switch(pin):
    # The switch connects its pin to GND, so pressed/on reads False.
    switch = digitalio.DigitalInOut(pin)
    switch.switch_to_input(pull=digitalio.Pull.UP)
    return switch

# Define a potentiometer on a specified pin
def make_pot(pin):
    return analogio.AnalogIn(pin)

# Define an LED strip on a specified pin
def make_pixel(pin):
    return neopixel.NeoPixel(
        pin,
        settings.PIXEL_COUNT,
        brightness=settings.PIXEL_BRIGHTNESS,
        auto_write=False,
    )
