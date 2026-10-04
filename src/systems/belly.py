# Belly trash door: toggle on = open, off = closed.
#
# A servo always moves at full speed, so to open and close the door gently
# we move it a small step each time around the loop. The steps are eased:
# the door speeds up at the start, moves at full speed through the middle,
# and slows down to a stop at the end.

import asyncio

from common import settings


def ease(progress):
    # Bend a steady 0.0 to 1.0 into a curve with three parts: speed up,
    # hold full speed, slow down. 0.0 stays 0.0 and 1.0 stays 1.0.
    speed_up = settings.BELLY_DOOR_EASE_IN  # part of the time spent speeding up
    slow_down = settings.BELLY_DOOR_EASE_OUT  # part of the time spent slowing down

    # The door covers less ground while it speeds up or slows down, so full
    # speed has to be faster than a steady move to finish on time.
    full_speed = 1 / (1 - speed_up / 2 - slow_down / 2)

    if progress < speed_up:
        # Speeding up.
        return full_speed * progress * progress / (2 * speed_up)
    if progress <= 1 - slow_down:
        # Full speed.
        return full_speed * (progress - speed_up / 2)
    # Slowing down.
    left = 1 - progress
    return 1 - full_speed * left * left / (2 * slow_down)


def move(door, place):
    # place goes from 0.0 (closed) to 1.0 (open).
    swing = settings.BELLY_DOOR_OPEN - settings.BELLY_DOOR_CLOSED
    door.angle = settings.BELLY_DOOR_CLOSED + swing * place


async def run(toggle, door):
    print("belly: ready")

    # How much of a full swing to do each time around the loop.
    step = settings.LOOP_SECONDS / settings.BELLY_DOOR_SECONDS

    # Start wherever the toggle says: open if it is on, closed if it is off.
    # The toggle connects its pin to GND, so on reads False.
    was_on = not toggle.value
    place = 1.0 if was_on else 0.0  # where the door is now
    move(door, place)
    print("belly: open" if was_on else "belly: closed")

    # A move goes from start to goal. progress counts from 0.0 to 1.0.
    start = place
    goal = place
    progress = 1.0  # 1.0 means the move is finished

    while True:
        on = not toggle.value

        if on != was_on:
            print("belly: opening" if on else "belly: closing")
            was_on = on

            # Begin a new move from wherever the door is right now.
            start = place
            goal = 1.0 if on else 0.0
            progress = 0.0 if start != goal else 1.0

        if progress < 1.0:
            # A move that covers only part of the swing takes less time.
            progress = min(progress + step / abs(goal - start), 1.0)
            place = start + (goal - start) * ease(progress)
            move(door, place)

        await asyncio.sleep(settings.LOOP_SECONDS)
