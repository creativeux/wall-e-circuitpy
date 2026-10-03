# Wall-E Costume (CircuitPython)

A Halloween Wall-E costume with moving eyebrows, eye wipers, a "binocular" head, a belly trash door, and a light-up charge meter. Built by an 11-year-old maker and his dad. The code is CircuitPython on a Raspberry Pi Pico.

This file is the project baseline: what we decided, why, how it's wired, and how the code should be laid out. Read it before changing anything.

**Goals, in priority order**

1. A costume that works on Halloween night.
2. A learning project. Code should be readable by an 11-year-old who knows Python. Prefer simple and explicit over clever.
3. Low cost. Reuse parts we own.

---

## 1. What it does

| Feature | Control | Behavior |
|---|---|---|
| Eyebrows (left + right) | Momentary push button | Held = eyebrows up. Released = eyebrows down. |
| Eye wipers (left + right) | Toggle switch | On = sweep back and forth. Off = park. |
| Belly trash door | Toggle switch | On = open. Off = closed. |
| Head halves ("binocular" effect) | 10 kΩ potentiometer | Knob position sets the angle. Left half goes to `angle`, right half goes to `180 - angle`. Movement is eased so it glides. |
| Charge meter + sun icon (chest) | Automatic (trigger TBD) | Amber bars fill from the bottom, then the sun lights. |

**Not in this version:** sound/speaker, any LCD or OLED screen, wifi or phone control, battery voltage readout. See [Deferred ideas](#9-deferred-ideas).

---

## 2. Hardware

### Parts in the build

| Part | Qty used | Role |
|---|---|---|
| Raspberry Pi Pico (RP2040, pre-soldered headers, Micro-USB, no wifi) | 1 | Runs the code |
| Waveshare Pico Servo Driver (16-channel, GPIO-driven, **not** I²C/PCA9685) | 1 | Pico plugs into it. Servo headers + battery terminal + 5 V regulator |
| MG996R standard servo (metal gear, ~10 kg·cm) | 2 | Head halves |
| MG90S micro servo (metal gear, ~2 kg·cm) | 5 | Eyebrows ×2, wipers ×2, belly door ×1 |
| Momentary push button (7 mm, prewired, normally open) | 1 | Eyebrows |
| SPST toggle switch (screw terminals) | 2 | Wipers, belly door |
| 10 kΩ linear potentiometer (WH148 B10K) | 1 | Head position |
| WS2812B / NeoPixel LED strip, cut to length | ~14 LEDs | Charge meter (10 bars) + sun icon (3–4 LEDs) |
| 1000 µF electrolytic capacitor (16 V or higher) | 1 | Across the 5 V servo rail to prevent brownout resets |
| 7.2 V 6-cell NiMH RC pack, T-plug (Deans) | 1 | Costume power |
| Female T-plug pigtail | 1 | Battery to board VIN terminal |
| Servo extension cables (1 m) | as needed | Body to head |

Spares on hand: 2 extra MG996R, 5 extra MG90S, extra buttons/switches/pots.

Full parts list with links and prices: `docs/wall-e-parts-list.xlsx`.

### Why these choices

- **Pico + CircuitPython** instead of a full Raspberry Pi (slow boot, SD corruption, jittery servo PWM) or Arduino (C++). The Pico shows up as a USB drive; edit `code.py`, save, it reruns.
- **Seven servos.** Each head half moves on its own, so each half carries its own eyebrow and wiper servo.
- **MG996R for the head** because each half carries cardboard, an eye, two micro servos and wiring, off-center from the pivot.
- **NeoPixel strip, not a screen,** for the charge meter. Bigger, brighter, closer to the movie, and far less code.

---

## 3. Power

```
7.2 V NiMH pack ──T-plug pigtail──> VIN terminal on servo board
                                      │
                              on-board 5 V regulator
                                      │
                    ┌─────────────────┼──────────────────┐
                 7 servos          Pico (VSYS)      NeoPixel strip
```

- The battery goes **only** into the board's VIN screw terminal. Red to +, black to −. Check with a meter before the first plug-in.
- The board regulates down to 5 V for the servos, the Pico, and the LED strip. No separate UBEC is used.
- **Power jumper on the board:** set to the battery/VSYS position when running from VIN. Waveshare says not to select USB and battery power at the same time.
- **Capacitor:** 1000 µF across 5 V and GND on a spare servo header. Stripe on the can = negative leg = GND.
- **Bench power:** a 9 V or 12 V DC wall adapter rated 2 A or more, into VIN through a barrel-jack-to-screw-terminal adapter. Do not feed a 5 V USB brick into VIN.
- **USB-only power** will run the Pico and maybe one micro servo. It will not run the MG996Rs.
- No power switch. Unplug the battery to turn the costume off.
- NiMH has no balance lead, so no voltage alarm. Sluggish servos mean it's time to swap packs.

---

## 4. Pin map

`src/pins.py` is the single source of truth. If the wiring changes, change that file and this table together.

| Pin | Connected to | Type |
|---|---|---|
| GP0 | Head left servo (MG996R) | PWM out, 50 Hz |
| GP1 | Head right servo (MG996R) | PWM out, 50 Hz |
| GP2 | Eyebrow left servo (MG90S) | PWM out, 50 Hz |
| GP3 | Eyebrow right servo (MG90S) | PWM out, 50 Hz |
| GP4 | Wiper left servo (MG90S) | PWM out, 50 Hz |
| GP5 | Wiper right servo (MG90S) | PWM out, 50 Hz |
| GP6 | Belly door servo (MG90S) | PWM out, 50 Hz |
| GP7 | NeoPixel strip DIN | Digital out |
| GP13 | Belly toggle → GND | Digital in, pull-up |
| GP14 | Wiper toggle → GND | Digital in, pull-up |
| GP15 | Eyebrow button → GND | Digital in, pull-up |
| GP26 (ADC0) | Potentiometer wiper (middle pin) | Analog in |
| 3V3 | Potentiometer outer pin | — |
| GND | Potentiometer other outer pin, all three switches | — |

### Wiring rules

- **Switches and the button** connect a GPIO pin to GND. The code enables the internal pull-up, so **pressed/on reads `False`**.
- **The pot gets 3.3 V, never 5 V.** The Pico's ADC pins are not 5 V tolerant.
- **NeoPixel pin order is not servo pin order.** Servo header: signal / 5 V / GND. Strip pads: 5 V / DIN / GND. Wire each lead individually. Data goes into the DIN end.
- **NeoPixel chain order:** pixels 0–9 are the bars (0 at the bottom), pixels 10–13 are the sun. The sun section is cut off and rejoined with three wires (DOUT → DIN) so it can sit separately.

### ⚠️ Not yet verified against the real board

These were planned from Waveshare's documentation, which did not spell everything out. Check them on the bench and update this file.

1. **Servo header to GPIO mapping.** We assumed header 0 = GP0 … header 6 = GP6. Read the silkscreen. If it differs, change `pins.py`, not the wiring.
2. **Where the input pins physically come from.** If all 16 servo headers use GP0–GP15, then GP13/14/15 are only reachable on servo headers (use the signal and GND pins; leave the middle 5 V pin unconnected). If that is awkward, move the three inputs to free broken-out pins (GP16–GP22) and update `pins.py`.
3. **Board revision.** Documentation shows two versions: 6–12 V in with a 3 A regulator, or 4.5–26 V in with an 8 A regulator. The 7.2 V pack works with both. Read the label on the board and record which one we have.
4. **Power jumper labels.** Record the exact silkscreen text for the battery position here once seen.
5. **NeoPixel data at 3.3 V.** Usually fine on a short wire. If colors glitch, shorten the data wire first.

---

## 5. Software

### Stack

- **CircuitPython** for the Raspberry Pi Pico (original RP2040 board). Download the `.uf2` from circuitpython.org, hold BOOTSEL while plugging in, drag the file onto the `RPI-RP2` drive.
- **Libraries** (from the Adafruit CircuitPython bundle, copied into `lib/` on the Pico):
  - `adafruit_motor` — servo control
  - `neopixel` (pulls in `adafruit_pixelbuf`) — LED strip
  - `asyncio` (pulls in `adafruit_ticks`) — one loop per feature
- Built in, no install needed: `board`, `digitalio`, `analogio`, `pwmio`, `time`.

Install libraries with `circup` from a computer with Python: `pip install circup`, then `circup install adafruit_motor neopixel asyncio`. Or copy the folders by hand from the bundle zip.

### Proposed repository layout

```
wall-e-circuitpy/
├── README.md              this file
├── docs/
│   ├── wall-e-wiring.html     wiring sheet (diagram, pin map, power-up checklist)
│   └── wall-e-parts-list.xlsx parts list + servo plan
├── src/                   everything in here gets copied to the Pico
│   ├── code.py            entry point: sets up hardware, starts the tasks
│   ├── pins.py            every pin assignment, nothing else
│   ├── settings.py        servo angles, speeds, colors, timings
│   ├── eyebrows.py
│   ├── wipers.py
│   ├── head.py
│   ├── belly.py
│   └── charge_meter.py
├── experiments/           small one-file bench tests (one servo, one button, LED strip)
└── tools/
    └── deploy.sh          copies src/ to the CIRCUITPY drive
```

Rules:

- **The Git repo is the source of truth, not the Pico.** Edit in the repo, copy to the board. Never treat the `CIRCUITPY` drive as the only copy.
- **Do not commit `lib/`.** Libraries come from the bundle. List them in this README.
- **No magic numbers in feature files.** Pins live in `pins.py`. Angles and timings live in `settings.py`.
- **One feature per file**, each exposing one `async def run(...)` task.

### Code conventions

- **Never use `time.sleep()` in the main program.** It freezes every other feature. Use `await asyncio.sleep(...)` inside a task. (`time.sleep` is fine in `experiments/`.)
- **Clamp every servo to a tested safe range.** A servo pushed past its mechanical stop strips its gears. Each servo gets a `MIN` and `MAX` in `settings.py`, found on the bench before it is mounted.
- **Ease the head.** Each loop, move a fraction of the way toward the target instead of jumping.
- **Don't move the big servos at the same instant** if the Pico resets. Stagger them.
- **Keep NeoPixel brightness at 0.2–0.3.**

Reference patterns:

```python
# Servo
import board, pwmio
from adafruit_motor import servo
brow = servo.Servo(pwmio.PWMOut(board.GP2, frequency=50))
brow.angle = 110

# Button or toggle (pressed/on reads False)
import digitalio
btn = digitalio.DigitalInOut(board.GP15)
btn.switch_to_input(pull=digitalio.Pull.UP)
pressed = not btn.value

# Potentiometer -> angle
import analogio
pot = analogio.AnalogIn(board.GP26)
target = pot.value / 65535 * 180

# Easing (run every loop)
current += (target - current) * 0.15

# NeoPixel
import neopixel
px = neopixel.NeoPixel(board.GP7, 14, brightness=0.25, auto_write=False)
px[0] = (255, 140, 0)   # amber
px.show()
```

---

## 6. Development setup

Both machines edit the same Git repo. The Pico is shared hardware: plug it into whichever computer is deploying.

### Mac (IntelliJ)

- Install the Python plugin. Open the repo folder.
- The Pico mounts at `/Volumes/CIRCUITPY`.
- Serial console / REPL: `screen /dev/tty.usbmodem* 115200` (Ctrl-A then K to quit), or use the browser editor below.
- Deploy: `rsync -av --delete --exclude lib src/ /Volumes/CIRCUITPY/`

### Chromebook (VS Code in the Linux environment)

- VS Code runs inside ChromeOS's Linux container. The repo lives in the Linux files.
- When the Pico is plugged in, `CIRCUITPY` appears in the ChromeOS Files app. Right-click it and choose **Share with Linux**. It then appears under `/mnt/chromeos/removable/CIRCUITPY`.
- Deploy: `rsync -av --delete --exclude lib src/ /mnt/chromeos/removable/CIRCUITPY/`
- Serial console / REPL: the simplest route on a Chromebook is **code.circuitpython.org** in Chrome, which connects over USB from the browser. It also works as a quick editor for experiments.
- Verify these paths on first setup and correct this section if ChromeOS differs.

### Workflow

1. `git pull`
2. Edit files in `src/` (or try something in `experiments/`).
3. Deploy to the Pico. It restarts by itself when files change.
4. Watch the serial console for errors.
5. Commit when it works. `git push`.

Add a `.gitignore` with: `.DS_Store`, `._*`, `.idea/`, `.vscode/`, `__pycache__/`, `lib/`.

---

## 7. Build order

Each step is a small win and ends with something moving or lighting up.

1. **Hello Pico.** Flash CircuitPython. Blink the on-board LED. Print to the serial console.
2. **One servo from the REPL.** Plug one MG90S into header 0. Type `brow.angle = 90`. Confirm the header-to-GPIO mapping.
3. **Find safe ranges.** Sweep each servo with nothing attached. Write MIN/MAX into `settings.py`.
4. **Eyebrows.** Button held = up.
5. **Belly door.** Toggle = open/closed.
6. **Head.** Pot → angle, mirrored, then add easing.
7. **Wipers.** First with `time.sleep` to see the problem (everything else freezes), then fix it.
8. **asyncio.** One task per feature in `code.py`.
9. **Charge meter.** Bars fill, sun lights. Decide what triggers it (power-on? a spare switch?).
10. **Power.** Move from wall adapter to battery. Add the capacitor. Test all features at once.
11. **Costume integration.** Mount servos, pushrods, controller box, cable runs.

### Mechanical notes

- Servo horn → stiff wire pushrod (coat hanger or 1.5 mm music wire) → cardboard part.
- Mount the MG996Rs to something rigid (plywood, foam-core, a printed bracket). Bare cardboard crushes.
- NeoPixel bars: set the strip back about 1" behind the panel, put a cardboard divider between LEDs, cover the slots with a diffuser (baking parchment or milk-jug plastic).
- Controller box holds the button, two toggles, and the pot. Handheld or strapped to a forearm.

---

## 8. Open questions

- What triggers the charge-meter animation?
- Final input pin choice (see "Not yet verified", item 2).
- Controller box design and cable route to the body.
- Whether the belly door needs an MG996R once the real door is built.
- Whether MG90S would be enough for the head if the halves end up light and balanced. Decide from the cardboard mockup.

---

## 9. Deferred ideas

Considered and set aside for this version.

- **Sound.** A piezo can only beep. Real clips need a DFPlayer Mini + speaker (the Pico sends "play track N" over UART).
- **Battery readout.** A two-resistor divider from VIN to GP27 lets the Pico measure pack voltage. Could drive the charge meter for real.
- **Screens.** A 16×2 I²C character LCD for status text, or a small OLED/TFT for eye graphics.
- **Eye glow** using leftover NeoPixels.
- **Arcade button** for the eyebrows.
- **Wifi / phone control.** Would need a Pico W.

---

## 10. Decision log

| Decision | Reason |
|---|---|
| Pico + CircuitPython | He already writes Python; instant-on; no OS |
| Waveshare GPIO servo board instead of PCA9685 | Plain `pwmio` code, tidy wiring, built-in regulator |
| 7 servos (2 large, 5 micro) | Independent head halves each carry their own eyebrow and wiper |
| 7.2 V NiMH RC pack into VIN | Already owned; safer than LiPo for a kid's costume |
| No separate UBEC | The board has its own regulator; a 5 V UBEC output is below the board's VIN minimum |
| NeoPixel strip for the charge meter | Closer to the film, brighter and simpler than a screen |
| No audio in v1 | Scope |
| Original Pico (no wifi) | Nothing in v1 needs it |
