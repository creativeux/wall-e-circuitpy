# Belly trash door: toggle on = open, off = closed.
#
# STUB: starts up and does nothing yet (build step 5).

import asyncio

from common import settings


async def run(toggle, door):
    print("belly: ready")
    while True:
        await asyncio.sleep(settings.LOOP_SECONDS)
