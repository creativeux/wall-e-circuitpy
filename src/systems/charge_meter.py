# Charge meter: amber bars fill from the bottom, then the sun lights.
#
# STUB: starts up and does nothing yet (build step 9).

import asyncio

from common import settings


async def run(pixels):
    print("charge meter: ready")
    while True:
        await asyncio.sleep(settings.LOOP_SECONDS)
