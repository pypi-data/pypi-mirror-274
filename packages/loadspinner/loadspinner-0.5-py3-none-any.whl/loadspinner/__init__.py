"""A CLI based loading spinner."""

from ._spinners import all_spinners
from time import sleep
from time import time as getEpoch
import multiprocessing

__all__ = [
    "Spinner",
    "functionSpinner",
    "makeSpinner",
]

__version__ = "0.5"
__description__ = "a CLI based loading spinner."
__author__ = "xyzpw"
__license__ = "MIT"

class Spinner:
    def __init__(self, spinner_type: str = "classic"):
        self.spinner_type = spinner_type
        self.frames = all_spinners[spinner_type]["frames"]
        self.interval = all_spinners[spinner_type]["interval"]
        self._process = None
    def __enter__(self):
        self.start()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
    def _changeCursorVisibility(self, visible: bool = True):
        print("\x1b[?25h" if visible else "\x1b[?25l", end="")
    def _createProcess(self, alive_time=None, hide_cursor: bool = True): # Not intended for user use
        if hide_cursor:
            self._changeCursorVisibility(False)
        frameIndex = 0
        creationTime = getEpoch()
        newSpaceSize = 0
        for f in self.frames:
            if len(f) > newSpaceSize:
                newSpaceSize = len(f)
        print("\x1b[%sC" % newSpaceSize, end="")
        while True:
            if frameIndex == len(self.frames):
                frameIndex = 0
            currentFrame = self.frames[frameIndex]
            frameLength = len(str(currentFrame))
            print(f"\x1b[{frameLength}D{currentFrame}", end="", flush=True)
            if alive_time != None:
                if getEpoch() - creationTime >= alive_time:
                    self._changeCursorVisibility(True)
                    break
            try:
                sleep(self.interval)
            except:
                print("\x1b[?25h", end="")
                break
            frameIndex += 1
    def start(self, alive_time: int | float = None, hide_cursor: bool = True):
        """Initiates the spinner animation which will be displayed.

        :param alive_time:  how long the spinner will be active before stopping (optional)
        :param hide_cursor: hides the terminal cursor while the spinner is active"""
        self._process = multiprocessing.Process(target=self._createProcess, daemon=True, args=[alive_time, hide_cursor])
        self._process.start()
    def stop(self, message: str = None, clearline: bool = None, newline: bool = None, show_cursor: bool = True):
        """Terminates the spinner process.

        :param message:     optional message upon completion
        :param clearline:   clears the entire line which the spinner was on
        :param newline:     prints a newline upon spinner completion
        :param show_cursor: enables cursor visibility upon spinner completion"""
        if show_cursor:
            self._changeCursorVisibility(True)
        self._process.terminate()
        if clearline:
            print("\x1b[2K\r", end="")
        if message != None:
            print(message, end="")
        if newline:
            print("\n", end="")

def functionSpinner(spinner_type: str):
    def func_wrapper(func):
        def wrapper(*args, **kwargs):
            with Spinner(spinner_type):
                return func(*args, **kwargs)
        return wrapper
    return func_wrapper

def makeSpinner(name: str, frames: list, interval: int):
    """Creates a custom spinner which can be used with specified name.

    :param name: the name of which the spinner will be given
    :param frames: the frames of which each will be printed to display the spinner
    :param interval: the interval in milliseconds between each frame being printed"""
    if not (isinstance(name, str) and isinstance(frames, list) and isinstance(interval, int)):
        raise TypeError("invalid variable type")
    all_spinners[name] = {
        "frames": frames,
        "interval": interval/1e3,
    }
