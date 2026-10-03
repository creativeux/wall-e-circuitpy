# Build step 2: one servo.
# Plug one MG90S into servo header 0 with nothing attached to the horn.
# It should swing gently back and forth around the middle.
# If it doesn't move, header 0 may not be GP0. Read the silkscreen on the
# board and fix src/pins.py.
#
# Needs the adafruit_motor library: python tools/deploy.py --libs
# Run it with: python tools/deploy.py experiments/one_servo.py

import time

import board
import pwmio
from adafruit_motor import servo

my_servo = servo.Servo(pwmio.PWMOut(board.GP0, frequency=50))

while True:
    my_servo.angle = 80
    print("angle 80")
    time.sleep(1)
    my_servo.angle = 100
    print("angle 100")
    time.sleep(1)
