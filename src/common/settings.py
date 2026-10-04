# Servo angles, speeds, colors and timings. No pins in this file.
#
# The servo MIN/MAX values below are BENCH values, set with nothing attached
# to the servo horns. The belly door is still a placeholder (a small, safe
# range around the middle). Before a servo is mounted in the costume, find
# how far its part can really move and write those limits here. A servo
# pushed past a mechanical stop strips its gears.

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
HEAD_POT_END_ZONE = 0.02  # this close to an end of the knob counts as the end

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
BELLY_DOOR_MIN = 80
BELLY_DOOR_MAX = 100

# NeoPixel strip: pixels 0-9 are the bars (0 at the bottom),
# pixels 10-13 are the sun.
PIXEL_COUNT = 14
BAR_COUNT = 10
PIXEL_BRIGHTNESS = 0.25  # keep between 0.2 and 0.3
AMBER = (255, 140, 0)
