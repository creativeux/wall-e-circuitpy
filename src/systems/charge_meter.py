# Charge meter: the lights on the chest. There are 6 bars, bar 0 at the
# bottom. The bottom bar is two pixels (0 and 1) that always light together;
# each bar above it is one pixel.
#
# It works like a battery that runs down. First the bars fill up one at a
# time. Then a bar drops every few seconds. The last few bars are orange.
# When only the bottom bar is left it blinks red. Every light fades on and
# off instead of snapping.
#
# This file only knows what the lights should look like. The belly system
# decides when the meter starts again: see belly.py.
#
# A "picture" is two things: is the red light on, and how many yellow bars
# are lit.

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
        return (False, loops // bar)

    # Running down: one bar drops each time.
    dropped = (loops - full_at) // drop
    bars = settings.BAR_COUNT - dropped
    if bars > 1:
        return (False, bars)

    # Only the bottom bar left: it blinks red, starting with the light on.
    red_at = full_at + (settings.BAR_COUNT - 1) * drop
    red_on = (loops - red_at) % (2 * flash) < flash
    return (red_on, 0)


def bars_left(loops):
    # How many bars the meter has right now. Blinking red counts as one.
    bar = loops_for(settings.METER_BAR_SECONDS)
    drop = loops_for(settings.METER_DROP_SECONDS)

    full_at = settings.BAR_COUNT * bar
    if loops < full_at:
        return loops // bar

    dropped = (loops - full_at) // drop
    return max(settings.BAR_COUNT - dropped, 1)


def describe(loops):
    # The charge in words, for the serial console.
    red_on, bars = picture(loops)
    left = bars_left(loops)
    if left == 1 and bars == 0:
        return "low, blinking red"
    if left == settings.BAR_COUNT:
        return "full"
    if left == 1:
        return "1 bar"
    return str(left) + " bars"


def refill(loops):
    # Start filling up again from however many bars are lit right now.
    # Returns the new loop count for the meter: the point in the filling up
    # where that many bars are lit. If the meter is already full, that is
    # the moment it starts running down again.
    bar = loops_for(settings.METER_BAR_SECONDS)
    return bars_left(loops) * bar


def pixels_for(bar):
    # The pixels that make up one bar. The bottom bar is more than one pixel.
    if bar == 0:
        return range(settings.BOTTOM_BAR_PIXELS)
    first = bar + settings.BOTTOM_BAR_PIXELS - 1
    return range(first, first + 1)


def colors(picture):
    # The color each pixel should be for this picture.
    red_on, bars = picture
    wanted: list = [settings.OFF] * settings.PIXEL_COUNT

    # The bars are yellow, or orange when the meter is low.
    color = settings.YELLOW
    if bars <= settings.METER_LOW_BARS:
        color = settings.ORANGE
    for bar in range(bars):
        for i in pixels_for(bar):
            wanted[i] = color
    if red_on:
        for i in pixels_for(0):
            wanted[i] = settings.RED
    return wanted


# Fading. A light never jumps to a new color: it fades there a small step
# each time around the loop, the same way the belly door moves. Each pixel
# remembers its own fade as [start color, goal color, progress], where
# progress counts from 0.0 to 1.0.


def new_fades():
    # Every pixel starts off, with nothing to fade.
    return [[settings.OFF, settings.OFF, 1.0] for _ in range(settings.PIXEL_COUNT)]


def mix(start, goal, progress):
    # The color part of the way from start to goal.
    return tuple(int(a + (b - a) * progress + 0.5) for a, b in zip(start, goal))


def fade(pixels, fades, wanted):
    # Move every pixel one step toward the color it should be. Only sends
    # to the strip while something is still fading.
    step = settings.LOOP_SECONDS / settings.METER_FADE_SECONDS
    moved = False
    for i in range(settings.PIXEL_COUNT):
        start, goal, progress = fades[i]
        if wanted[i] != goal:
            # Begin a new fade from wherever this pixel is right now.
            start = mix(start, goal, progress)
            goal = wanted[i]
            progress = 0.0
        if progress < 1.0:
            progress = min(progress + step, 1.0)
            pixels[i] = mix(start, goal, progress)
            moved = True
        fades[i] = [start, goal, progress]
    if moved:
        pixels.show()
