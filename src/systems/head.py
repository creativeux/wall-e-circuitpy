# Head halves: the knob sets the angle. The two halves mirror each other,
# and movement is eased so it glides.

import asyncio

from common import settings


def read_knob(pot):
    # pot.value goes from 0 to 65535. Turn it into 0.0 to 1.0.
    return pot.value / 65535


def move(left, right, position):
    # position goes from 0.0 (knob all the way down) to 1.0 (all the way up).
    left_range = settings.HEAD_LEFT_HIGH - settings.HEAD_LEFT_LOW
    right_range = settings.HEAD_RIGHT_HIGH - settings.HEAD_RIGHT_LOW
    left.angle = settings.HEAD_LEFT_LOW + left_range * position
    right.angle = settings.HEAD_RIGHT_LOW + right_range * position


async def run(pot, left, right):
    print("head: ready")

    # Start where the knob is.
    target = read_knob(pot)
    position = target
    move(left, right, position)
    print("head: knob", round(target * 100), "%")

    while True:
        # The knob reading wobbles a little even when nobody touches it,
        # so only follow it when it has really moved.
        reading = read_knob(pot)
        if abs(reading - target) > settings.HEAD_POT_WOBBLE:
            target = reading
            print("head: knob", round(target * 100), "%")

        # Ease: move a fraction of the way to the target each loop.
        old_position = position
        position += (target - position) * settings.HEAD_EASING
        if abs(target - position) < 0.001:
            position = target  # close enough, stop here

        if position != old_position:
            move(left, right, position)

        await asyncio.sleep(settings.LOOP_SECONDS)
