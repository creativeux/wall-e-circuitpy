# Head halves: the knob sets the angle. The two halves mirror each other,
# and movement is eased so it glides.

import asyncio

from common import settings


def read_knob(pot):
    # The reading wobbles a little, so take a few and average them.
    total = 0
    for _ in range(settings.HEAD_POT_SAMPLES):
        total += pot.value

    # pot.value goes from 0 to 65535. Turn the average into 0.0 to 1.0.
    reading = total / settings.HEAD_POT_SAMPLES / 65535

    # A knob almost never reads exactly 0.0 or 1.0 at its ends. Stretch the
    # reading a little so the last bit of travel counts as the end.
    end_zone = settings.HEAD_POT_END_ZONE
    reading = (reading - end_zone) / (1 - 2 * end_zone)
    return max(0.0, min(1.0, reading))


def move_left(left, position):
    # position goes from 0.0 (knob all the way down) to 1.0 (all the way up).
    left_range = settings.HEAD_LEFT_HIGH - settings.HEAD_LEFT_LOW
    left.angle = settings.HEAD_LEFT_LOW + left_range * position


def move_right(right, position):
    right_range = settings.HEAD_RIGHT_HIGH - settings.HEAD_RIGHT_LOW
    right.angle = settings.HEAD_RIGHT_LOW + right_range * position


async def run(pot, left, right):
    print("head: ready")

    # Start where the knob is. Move one half, wait, then move the other, so
    # the two big servos don't both pull power at the same instant.
    target = read_knob(pot)
    position = target
    print("head: knob", round(target * 100), "%")
    move_left(left, position)
    await asyncio.sleep(settings.HEAD_STAGGER_SECONDS)
    move_right(right, position)

    while True:
        # Only follow the knob when it has really moved, or when it has
        # reached one of its ends.
        reading = read_knob(pot)
        at_an_end = reading == 0.0 or reading == 1.0
        moved = abs(reading - target) > settings.HEAD_POT_WOBBLE
        if reading != target and (moved or at_an_end):
            target = reading
            print("head: knob", round(target * 100), "%")

        # Ease: move a fraction of the way to the target each loop.
        old_position = position
        position += (target - position) * settings.HEAD_EASING
        if abs(target - position) < settings.HEAD_CLOSE_ENOUGH:
            position = target  # close enough, stop here

        if position != old_position:
            move_left(left, position)
            move_right(right, position)

        await asyncio.sleep(settings.LOOP_SECONDS)
