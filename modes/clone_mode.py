import cv2
import numpy as np
from .base import Mode


class CloneMode(Mode):
    name = "Clone Yourself"
    key = ord('6')
    instructions = "b : capture empty background | c : stamp a clone at current pose"

    def __init__(self):
        self.background = None
        self.canvas = None

    def on_activate(self, frame_shape):
        self.background = None
        self.canvas = None

    def process(self, frame):
        if self.background is None:
            output = frame.copy()
            cv2.putText(output, "Press 'b' for empty background, then 'c' to stamp clones",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
            return output

        preview = self.canvas.copy()
        mask = self._foreground_mask(frame)
        preview[mask > 0] = frame[mask > 0]
        return preview

    def _foreground_mask(self, frame):
        diff = cv2.absdiff(
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
            cv2.cvtColor(self.background, cv2.COLOR_BGR2GRAY),
        )
        _, mask = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
        return mask

    def handle_key(self, key, frame):
        if key == ord('b'):
            self.background = frame.copy()
            self.canvas = frame.copy()
            return True
        if key == ord('c') and self.background is not None:
            mask = self._foreground_mask(frame)
            self.canvas[mask > 0] = frame[mask > 0]
            return True
        return False
