# Experiments

Small one-file bench tests: one servo, one button, the LED strip. Try things here before they go into `src/`.

- An experiment can use `from common import pins` and `from common import settings`. Deploying an experiment also copies the latest `src/common/` to the board.
- `time.sleep()` is fine here.
- Run one on the Pico with `python tools/deploy.py experiments/one_servo.py`. It is copied to the board as `code.py`.
- To go back to the real program, run `python tools/deploy.py`.
