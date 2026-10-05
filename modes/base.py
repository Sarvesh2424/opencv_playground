from abc import ABC, abstractmethod


class Mode(ABC):
    """Common interface every playground mode implements.

    Subclasses set `name`, `key` (an ord('x') value) and `instructions`
    (shown on startup), then implement `process`. Override `on_activate`
    to reset state when the mode is (re)selected, `handle_key` for extra
    keyboard controls, and `handle_mouse` for click-driven modes.
    """

    name = "Base Mode"
    key = None
    instructions = ""

    def on_activate(self, frame_shape):
        """Called once when this mode becomes active. Reset state here."""
        pass

    @abstractmethod
    def process(self, frame):
        """Take a BGR frame, return the BGR frame to display."""
        raise NotImplementedError

    def handle_key(self, key, frame):
        """Handle a mode-specific keypress. Return True if you used it."""
        return False

    def handle_mouse(self, event, x, y):
        """Handle a mouse event on the display window (optional)."""
        pass
