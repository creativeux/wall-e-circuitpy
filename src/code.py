# Build step 1: Hello Pico.
# Blinks the on-board LED and prints to the serial console.
#
# time.sleep is OK here because nothing else is running yet. Once there is
# more than one feature it freezes everything else, and build step 8
# replaces it with asyncio.

import time

import digitalio

import pins

led = digitalio.DigitalInOut(pins.ONBOARD_LED)
led.switch_to_output()

print("Hello from Wall-E!")

while True:
    led.value = not led.value
    print("LED on" if led.value else "LED off")
    time.sleep(0.5)
