# Experiments

Small one-file bench tests: one servo, one button, the LED strip. Try things here before they go into `src/`.

- An experiment can `import pins` and `import settings`. Deploying an experiment also copies the latest `src/pins.py` and `src/settings.py` to the board.
- `time.sleep()` is fine here.
- Run one on the Pico with `python tools/deploy.py experiments/one_servo.py`. It is copied to the board as `code.py`.
- To go back to the real program, run `python tools/deploy.py`.
