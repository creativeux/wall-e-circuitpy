# The main program. It sets up every piece of hardware, then starts one
# task per feature. All the tasks take turns, so no feature can freeze
# the others.
#
# Each feature lives in its own file in systems/ with one
# "async def run(...)".
# Right now they are stubs: they start up and do nothing.
#
# Needs the libraries: python tools/deploy.py --libs

import asyncio

import digitalio

from common import pins
from common import settings
from systems import belly
from systems import charge_meter
from systems import eyebrows
from systems import head
from systems import wipers
from common.utils import make_pixel
from common.utils import make_pot
from common.utils import make_servo
from common.utils import make_switch


# Servos. They don't move until a feature sets an angle.
head_left = make_servo(pins.HEAD_LEFT)
head_right = make_servo(pins.HEAD_RIGHT)
eyebrow_left = make_servo(pins.EYEBROW_LEFT)
eyebrow_right = make_servo(pins.EYEBROW_RIGHT)
wiper_left = make_servo(pins.WIPER_LEFT)
wiper_right = make_servo(pins.WIPER_RIGHT)
belly_door = make_servo(pins.BELLY_DOOR)

# Controls
eyebrow_button = make_switch(pins.EYEBROW_BUTTON)
wiper_toggle = make_switch(pins.WIPER_TOGGLE)
belly_toggle = make_switch(pins.BELLY_TOGGLE)
head_pot = make_pot(pins.HEAD_POT)

# LED strip
pixels = make_pixel(pins.NEOPIXEL)

# The little LED on the Pico itself
led = digitalio.DigitalInOut(pins.ONBOARD_LED)
led.switch_to_output()


async def heartbeat():
    # Blinks the on-board LED so we can see the program is still running.
    while True:
        led.value = not led.value
        await asyncio.sleep(settings.HEARTBEAT_SECONDS)


async def main():
    print("Hello from Wall-E!")
    await asyncio.gather(
        heartbeat(),
        eyebrows.run(eyebrow_button, eyebrow_left, eyebrow_right),
        wipers.run(wiper_toggle, wiper_left, wiper_right),
        head.run(head_pot, head_left, head_right),
        belly.run(belly_toggle, belly_door),
        charge_meter.run(pixels),
    )


asyncio.run(main())
