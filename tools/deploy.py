#!/usr/bin/env python3
"""Copy the code to the Pico. Works on the Mac and the Chromebook.

    python tools/deploy.py                            copy src/ to the board
    python tools/deploy.py experiments/one_servo.py   run one experiment as code.py
    python tools/deploy.py --libs                     install the libraries with circup
    python tools/deploy.py --path /some/where         use this drive instead of searching
"""

import argparse
import filecmp
import getpass
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "src"
LIBS_FILE = REPO / "requirements-circuitpython.txt"

# Files on the board that deploy never deletes.
KEEP_ON_BOARD = {"boot.py"}


def possible_board_paths():
    user = getpass.getuser()
    return [
        Path("/Volumes/CIRCUITPY"),  # Mac
        Path("/mnt/chromeos/removable/CIRCUITPY"),  # Chromebook
        Path("/media") / user / "CIRCUITPY",  # other Linux
        Path("/run/media") / user / "CIRCUITPY",
    ]


def find_board(path_from_user):
    if path_from_user:
        candidates = [Path(path_from_user)]
    else:
        candidates = possible_board_paths()

    for path in candidates:
        # Every CircuitPython board has boot_out.txt on its drive.
        if (path / "boot_out.txt").exists():
            return path

    print("Could not find the CIRCUITPY drive. Looked in:")
    for path in candidates:
        print("  ", path)
    if Path("/mnt/chromeos").exists():
        print("Chromebook: open the Files app, right-click CIRCUITPY,")
        print("and choose 'Share with Linux'.")
    else:
        print("Is the Pico plugged in with a data USB cable?")
    sys.exit(1)


def copy_if_changed(source, target):
    """Copy one file, but only if it is different. Returns True if copied."""
    if target.exists() and filecmp.cmp(source, target, shallow=False):
        return False
    # copyfile copies only the contents, which is all the board's drive needs.
    shutil.copyfile(source, target)
    return True


def deploy_src(board):
    changed = []

    # code.py goes last so the Pico restarts with every other file in place.
    sources = sorted(SRC.glob("*.py"), key=lambda f: f.name == "code.py")
    for source in sources:
        if copy_if_changed(source, board / source.name):
            changed.append("copied  " + source.name)

    # Remove .py files on the board that are no longer in src/.
    names_in_src = {source.name for source in sources}
    for on_board in board.glob("*.py"):
        if on_board.name.startswith("._"):
            continue  # Mac junk, cleaned up in main()
        if on_board.name not in names_in_src and on_board.name not in KEEP_ON_BOARD:
            on_board.unlink()
            changed.append("removed " + on_board.name)

    return changed


def deploy_experiment(board, experiment):
    if not experiment.is_file():
        print("No such file:", experiment)
        sys.exit(1)
    if copy_if_changed(experiment, board / "code.py"):
        return ["copied  " + experiment.name + " -> code.py"]
    return []


def install_libs(board):
    circup = shutil.which("circup")
    if circup is None:
        print("circup is not installed. Turn on the .venv, then run:")
        print("  pip install -r requirements-dev.txt")
        sys.exit(1)
    command = [circup, "--path", str(board), "install", "-r", str(LIBS_FILE)]
    result = subprocess.run(command)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="Copy the code to the Pico.")
    parser.add_argument("experiment", nargs="?", help="one file to run as code.py")
    parser.add_argument("--libs", action="store_true", help="install libraries with circup")
    parser.add_argument("--path", help="where the CIRCUITPY drive is")
    args = parser.parse_args()

    board = find_board(args.path)
    print("Board:", board)

    if args.libs:
        install_libs(board)
        changed = []
    elif args.experiment:
        changed = deploy_experiment(board, Path(args.experiment))
    else:
        changed = deploy_src(board)

    # The Mac leaves a hidden "._name" file next to each file it writes
    # to the board. They are junk, so remove them.
    for junk in board.glob("._*"):
        if junk.is_file():
            junk.unlink()

    # Make sure everything is really written before the Pico is unplugged.
    os.sync()

    for line in changed:
        print(line)
    if args.libs:
        print("Libraries installed.")
    elif changed:
        print("Done. The Pico restarts by itself.")
    else:
        print("Nothing changed.")


if __name__ == "__main__":
    main()
