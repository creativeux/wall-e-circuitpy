# Servo angles, speeds, colors and timings. No pins in this file.
#
# The servo MIN/MAX values below are PLACEHOLDERS. They are a small, safe
# range around the middle. Find the real limits on the bench (build step 3)
# before a servo is mounted, then write them here. A servo pushed past its
# mechanical stop strips its gears.

# Head halves (MG996R)
HEAD_LEFT_MIN = 80
HEAD_LEFT_MAX = 100
HEAD_RIGHT_MIN = 80
HEAD_RIGHT_MAX = 100
HEAD_EASING = 0.15  # fraction of the way to the target moved each loop

# Eyebrows (MG90S)
EYEBROW_LEFT_MIN = 80
EYEBROW_LEFT_MAX = 100
EYEBROW_RIGHT_MIN = 80
EYEBROW_RIGHT_MAX = 100

# Wipers (MG90S)
WIPER_LEFT_MIN = 80
WIPER_LEFT_MAX = 100
WIPER_RIGHT_MIN = 80
WIPER_RIGHT_MAX = 100

# Belly door (MG90S)
BELLY_DOOR_MIN = 80
BELLY_DOOR_MAX = 100

# NeoPixel strip: pixels 0-9 are the bars (0 at the bottom),
# pixels 10-13 are the sun.
PIXEL_COUNT = 14
BAR_COUNT = 10
PIXEL_BRIGHTNESS = 0.25  # keep between 0.2 and 0.3
AMBER = (255, 140, 0)
