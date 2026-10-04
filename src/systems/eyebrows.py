# Eyebrows: button held = eyebrows up, released = eyebrows down.

import asyncio

from common import settings


def move(left, right, up):
    if up:
        left.angle = settings.EYEBROW_LEFT_UP
        right.angle = settings.EYEBROW_RIGHT_UP
    else:
        left.angle = settings.EYEBROW_LEFT_DOWN
        right.angle = settings.EYEBROW_RIGHT_DOWN


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
