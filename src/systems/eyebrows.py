# Eyebrows: button held = eyebrows up, released = eyebrows down.
#
# STUB: starts up and does nothing yet (build step 4).

import asyncio

from common import settings


async def run(button, left, right):
    print("eyebrows: ready")
    while True:
        await asyncio.sleep(settings.LOOP_SECONDS)
