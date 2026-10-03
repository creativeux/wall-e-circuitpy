# Eye wipers: toggle on = sweep back and forth, off = park.
#
# STUB: starts up and does nothing yet (build step 7).

import asyncio

from common import settings


async def run(toggle, left, right):
    print("wipers: ready")
    while True:
        await asyncio.sleep(settings.LOOP_SECONDS)
