# Servo angles, speeds, colors and timings. No pins in this file.
#
# The servo MIN/MAX values below are BENCH values, set with nothing attached
# to the servo horns. Before a servo is mounted in the costume, find how far
# its part can really move and write those limits here. A servo pushed past
# a mechanical stop strips its gears.

# Timing
LOOP_SECONDS = 0.02  # how long each feature waits between checks
HEARTBEAT_SECONDS = 0.5  # on-board LED blink

# Head halves (MG996R)
HEAD_LEFT_MIN = 0
HEAD_LEFT_MAX = 180
HEAD_RIGHT_MIN = 0
HEAD_RIGHT_MAX = 180
HEAD_EASING = 0.15  # fraction of the way to the target moved each loop
HEAD_CLOSE_ENOUGH = 0.001  # this close to the target counts as arrived
HEAD_STAGGER_SECONDS = 0.3  # at startup, wait this long between the two halves
HEAD_POT_SAMPLES = 8  # knob readings averaged together each loop
HEAD_POT_WOBBLE = 0.02  # ignore knob changes smaller than this (0.02 = 2%)
HEAD_POT_FOLLOW_SECONDS = 0.5  # after the knob moves, follow it exactly for this long
HEAD_POT_END_ZONE = 0.005  # this close to an end of the knob counts as the end

# Where each head half sits with the knob turned all the way down (LOW)
# and all the way up (HIGH). The right half mirrors the left one, so it
# turns the other way. If a half moves the wrong way, swap its LOW and HIGH.
HEAD_LEFT_LOW = HEAD_LEFT_MIN
HEAD_LEFT_HIGH = HEAD_LEFT_MAX
HEAD_RIGHT_LOW = HEAD_RIGHT_MAX
HEAD_RIGHT_HIGH = HEAD_RIGHT_MIN

# Eyebrows (MG90S)
EYEBROW_LEFT_MIN = 0
EYEBROW_LEFT_MAX = 160
EYEBROW_RIGHT_MIN = 0
EYEBROW_RIGHT_MAX = 160

# Where each eyebrow sits when it is down and when it is up.
# The right servo is mounted as a mirror image of the left one, so it turns
# the other way. If an eyebrow moves the wrong way, swap its UP and DOWN.
EYEBROW_LEFT_DOWN = EYEBROW_LEFT_MIN
EYEBROW_LEFT_UP = EYEBROW_LEFT_MAX
EYEBROW_RIGHT_DOWN = EYEBROW_RIGHT_MAX
EYEBROW_RIGHT_UP = EYEBROW_RIGHT_MIN

# Wipers (MG90S)
WIPER_LEFT_MIN = 20
WIPER_LEFT_MAX = 160
WIPER_RIGHT_MIN = 20
WIPER_RIGHT_MAX = 160

# Where each wiper parks, and the far end of its sweep.
# Both wipers turn the same way. If a wiper parks at the wrong end, swap
# its PARK and FAR.
WIPER_LEFT_PARK = WIPER_LEFT_MIN
WIPER_LEFT_FAR = WIPER_LEFT_MAX
WIPER_RIGHT_PARK = WIPER_RIGHT_MIN
WIPER_RIGHT_FAR = WIPER_RIGHT_MAX
WIPER_SWEEP_SECONDS = 0.5  # time to sweep one way. Bigger = slower

# Belly door (MG90S)
BELLY_DOOR_MIN = 0
BELLY_DOOR_MAX = 180

# Where the door sits when it is closed and when it is open.
# If the door moves the wrong way, swap CLOSED and OPEN.
BELLY_DOOR_CLOSED = BELLY_DOOR_MIN
BELLY_DOOR_OPEN = BELLY_DOOR_MAX
BELLY_DOOR_SECONDS = 1.5  # time to open or close. Bigger = slower
BELLY_DOOR_EASE_IN = 0  # part of the time spent speeding up. 0.2 = 20%
BELLY_DOOR_EASE_OUT = 0.75  # part of the time spent slowing down

# NeoPixel strip: pixels 0-7 are the bars (0 at the bottom),
# pixel 8 is the sun.
PIXEL_COUNT = 9
BAR_COUNT = 8
SUN_PIXEL = 8
PIXEL_BRIGHTNESS = 0.25  # keep between 0.2 and 0.3
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 180, 0)
ORANGE = (255, 60, 0)

# Charge meter. It works like a battery that runs down:
# when the belly door closes, the bars fill up one at a time and the sun
# lights. Then a bar drops every few seconds. The last few bars are orange.
# When only one bar is left it blinks red, and stays that way until the door
# opens and closes again.
METER_BAR_SECONDS = 0.3  # filling up: time between one bar lighting and the next
METER_DROP_SECONDS = 3.0  # running down: time between one bar dropping and the next
METER_LOW_BARS = 3  # with this many bars or fewer, the bars are orange
METER_FLASH_SECONDS = 0.75  # the red light is on this long, then off this long
