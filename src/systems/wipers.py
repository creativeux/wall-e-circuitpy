# Eye wipers: toggle on = sweep back and forth, off = park.
# When the toggle is switched off mid-sweep, the wipers finish that sweep
# (out to the far end and back) and then stop at park.
#
# A servo always moves at full speed, so to sweep slowly we move it a small
# step each time around the loop.

import asyncio

from common import settings


def move(left, right, position):
    # position goes from 0.0 (parked) to 1.0 (the far end of the sweep).
    left_sweep = settings.WIPER_LEFT_FAR - settings.WIPER_LEFT_PARK
    right_sweep = settings.WIPER_RIGHT_FAR - settings.WIPER_RIGHT_PARK
    left.angle = settings.WIPER_LEFT_PARK + left_sweep * position
    right.angle = settings.WIPER_RIGHT_PARK + right_sweep * position


async def run(toggle, left, right):
    print("wipers: ready")

    # How far to move each time around the loop.
    step = settings.LOOP_SECONDS / settings.WIPER_SWEEP_SECONDS

    # Start parked.
    position = 0.0
    direction = 1  # 1 = moving away from park, -1 = moving back
    was_on = False
    move(left, right, position)

    while True:
        # The toggle connects its pin to GND, so on reads False.
        on = not toggle.value

        if on != was_on:
            print("wipers: on" if on else "wipers: off")
            was_on = on

        old_position = position
        # Keep sweeping while the toggle is on. When it is off, keep going
        # only until the wipers are back at park.
        if on or position > 0.0:
            position += step * direction
            if position >= 1.0:
                position = 1.0
                direction = -1
            elif position <= 0.0:
                position = 0.0
                direction = 1

        if position != old_position:
            move(left, right, position)

        await asyncio.sleep(settings.LOOP_SECONDS)
