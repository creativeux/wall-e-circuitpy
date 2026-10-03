#!/usr/bin/env python3
"""Copy the code to the Pico. Works on the Mac and the Chromebook.

    python tools/deploy.py                            copy src/ to the board
    python tools/deploy.py experiments/one_servo.py   run one experiment as code.py
                                                      (the rest of src/ goes along too)
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
KEEP_ON_BOARD = {"boot.py", "safemode.py"}


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
    target.parent.mkdir(parents=True, exist_ok=True)
    # copyfile copies only the contents, which is all the board's drive needs.
    shutil.copyfile(source, target)
    return True


def our_folders(board):
    """The places on the board that deploy looks after.

    That is the top of the drive and the folders that src/ has (like
    systems/). Every other folder on the board is left alone.
    """
    folders = [board]
    for folder in sorted(f for f in SRC.rglob("*") if f.is_dir() and f.name != "__pycache__"):
        on_board = board / folder.relative_to(SRC)
        if on_board.is_dir():
            folders.append(on_board)
    return folders


def deploy(board, code_file):
    """Copy src/ to the board, with code_file as the board's code.py.

    code_file is normally src/code.py. For an experiment it is the
    experiment file, so the experiment can still import pins and settings.
    """
    changed = []

    # Every .py file in src/ and its folders, as paths relative to src/.
    helpers = sorted(f.relative_to(SRC) for f in SRC.rglob("*.py"))
    helpers.remove(Path("code.py"))
    for name in helpers:
        if copy_if_changed(SRC / name, board / name):
            changed.append("copied  " + str(name))

    # code.py goes last so the Pico restarts with every other file in place.
    if copy_if_changed(code_file, board / "code.py"):
        if code_file.name == "code.py":
            changed.append("copied  code.py")
        else:
            changed.append("copied  " + code_file.name + " -> code.py")

    # Remove .py files on the board that are no longer in src/.
    # The board's drive treats Head.py and head.py as the same file, so
    # names are compared in lower case.
    names_to_keep = {str(name).lower() for name in helpers} | {"code.py"} | KEEP_ON_BOARD
    for folder in our_folders(board):
        for on_board in sorted(folder.iterdir()):
            if on_board.name.startswith("._"):
                continue  # Mac junk, cleaned up in main()
            if not on_board.is_file() or on_board.suffix.lower() != ".py":
                continue
            name = str(on_board.relative_to(board))
            if name.lower() not in names_to_keep:
                on_board.unlink()
                changed.append("removed " + name)

    return changed


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
        experiment = Path(args.experiment)
        if not experiment.is_file():
            print("No such file:", experiment)
            sys.exit(1)
        changed = deploy(board, experiment)
    else:
        changed = deploy(board, SRC / "code.py")

    # The Mac leaves a hidden "._name" file next to each file it writes
    # to the board. They are junk, so remove them.
    for folder in our_folders(board):
        for junk in folder.glob("._*"):
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
