# Read the head knob (potentiometer).
# Prints the voltage on all three of the Pico's analog pins, so we can see
# which pin the knob is really connected to. Turn the knob slowly and watch
# which column follows it. It should be GP26.
# A pin with nothing connected shows small, random voltages. That is normal.
#
# Run it with: python tools/deploy.py experiments/pot.py

import time

import analogio
import board

gp26 = analogio.AnalogIn(board.GP26)
gp27 = analogio.AnalogIn(board.GP27)
gp28 = analogio.AnalogIn(board.GP28)


def volts(pin):
    # pin.value goes from 0 to 65535, which means 0 V to 3.3 V.
    return pin.value / 65535 * 3.3


while True:
    print(f"GP26 {volts(gp26):.2f} V   GP27 {volts(gp27):.2f} V   GP28 {volts(gp28):.2f} V")
    time.sleep(0.25)
