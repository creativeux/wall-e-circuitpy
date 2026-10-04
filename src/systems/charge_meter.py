# Charge meter: the lights on the chest. Pixels 0-7 are the bars (0 at the
# bottom) and pixel 8 is the sun.
#
# It works like a battery that runs down. First the bars fill up one at a
# time and the sun lights. Then a bar drops every few seconds. The last few
# bars are orange. When only one bar is left it blinks red.
#
# This file only knows what the lights should look like. The belly system
# decides when the meter starts again: see belly.py.
#
# A "picture" is three things: is the red light on, how many yellow bars
# are lit, and is the sun lit.

from common import settings


def loops_for(seconds):
    # How many times around the loop fit into this many seconds.
    return max(1, int(seconds / settings.LOOP_SECONDS + 0.5))


def picture(loops):
    # What the lights look like, this many times around the loop after the
    # meter started.
    bar = loops_for(settings.METER_BAR_SECONDS)
    drop = loops_for(settings.METER_DROP_SECONDS)
    flash = loops_for(settings.METER_FLASH_SECONDS)

    # Filling up: one more bar each time, from the bottom.
    full_at = settings.BAR_COUNT * bar
    if loops < full_at:
        return (False, loops // bar, False)

    # Full. The sun lights one beat after the last bar.
    sun_at = full_at + bar
    if loops < sun_at:
        return (False, settings.BAR_COUNT, False)

    # Running down: one bar drops each time. The sun goes out with the
    # first bar.
    dropped = (loops - sun_at) // drop
    bars = settings.BAR_COUNT - dropped
    if bars > 1:
        return (False, bars, dropped == 0)

    # Only one bar left: it blinks red.
    red_on = loops % (2 * flash) < flash
    return (red_on, 0, False)


def bars_left(loops):
    # How many bars the meter has right now. Blinking red counts as one.
    bar = loops_for(settings.METER_BAR_SECONDS)
    drop = loops_for(settings.METER_DROP_SECONDS)

    full_at = settings.BAR_COUNT * bar
    if loops < full_at:
        return loops // bar

    sun_at = full_at + bar
    if loops < sun_at:
        return settings.BAR_COUNT

    dropped = (loops - sun_at) // drop
    return max(settings.BAR_COUNT - dropped, 1)


def describe(loops):
    # The charge in words, for the serial console.
    red_on, bars, sun_on = picture(loops)
    left = bars_left(loops)
    if left == 1 and bars == 0:
        return "low, blinking red"
    if sun_on:
        return "full, sun lit"
    if left == 1:
        return "1 bar"
    return str(left) + " bars"


def refill(loops):
    # Start filling up again from however many bars are lit right now.
    # Returns the new loop count for the meter: the point in the filling up
    # where that many bars are lit.
    bar = loops_for(settings.METER_BAR_SECONDS)
    bars = bars_left(loops)
    if bars == settings.BAR_COUNT:
        # Already full: go straight to the sun, and start running down again.
        return (settings.BAR_COUNT + 1) * bar
    return bars * bar


def draw(pixels, picture):
    red_on, bars, sun_on = picture
    pixels.fill(settings.OFF)

    # The bars are yellow, or orange when the meter is low.
    color = settings.YELLOW
    if bars <= settings.METER_LOW_BARS:
        color = settings.ORANGE
    for i in range(bars):
        pixels[i] = color
    if sun_on:
        pixels[settings.SUN_PIXEL] = settings.YELLOW
    if red_on:
        pixels[0] = settings.RED
    pixels.show()
