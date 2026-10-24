# Eyebrows: button held = eyebrows up, released = eyebrows down.

import asyncio

from common import settings


def mirror(angle):
    # The right servo is mounted as a mirror image of the left one, so it
    # has to turn the other way. Flipping the angle here means the same
    # number in settings.py gives the same eyebrow position on both sides.
    return 180 - angle


def move(left, right, up):
    if up:
        left.angle = settings.EYEBROW_LEFT_MAX
        right.angle = mirror(settings.EYEBROW_RIGHT_MAX)
    else:
        left.angle = settings.EYEBROW_LEFT_MIN
        right.angle = mirror(settings.EYEBROW_RIGHT_MIN)


async def run(button, left, right):
    print("eyebrows: ready")

    # Start with the eyebrows down.
    was_pressed = False
    move(left, right, up=False)

    while True:
        # The button connects its pin to GND, so pressed reads False.
        pressed = not button.value

        # Only move when the button changes, not every time around the loop.
        if pressed != was_pressed:
            print("eyebrows: up" if pressed else "eyebrows: down")
            move(left, right, up=pressed)
            was_pressed = pressed

        await asyncio.sleep(settings.LOOP_SECONDS)
