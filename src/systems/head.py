# Head halves: the knob sets the angle. The left half goes to angle,
# the right half goes to 180 - angle. Movement is eased so it glides.
#
# STUB: starts up and does nothing yet (build step 6).

import asyncio

from common import settings


async def run(pot, left, right):
    print("head: ready")
    while True:
        await asyncio.sleep(settings.LOOP_SECONDS)
