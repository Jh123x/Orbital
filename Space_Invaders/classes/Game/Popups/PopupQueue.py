from collections import deque

from . import Popup


class PopupQueue():

    def __init__(self, screen_width: int, screen_height: int, fps: int, screen, debug: bool = False):
        """A queue for the popup to appear in order"""

        # Store the vars
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.fps = fps
        self.debug = debug

        # Initialise the queue
        self.queue = deque()

    def add(self, name: str, time: int):
        """Add a popup to the queue"""
        item = Popup(400, 50, name, self.fps * time, self.screen_width // 2 , 10, self.screen, font=Popup.h2_font,
                     debug=self.debug)
        self.append(item)

    def append(self, item):
        """Add the item to the queue"""
        self.queue.append(item)

    def __len__(self) -> int:
        """Return the length of the queue"""
        return len(self.queue)

    def popleft(self):
        """Pop the item at the front"""
        return self.queue.popleft()
