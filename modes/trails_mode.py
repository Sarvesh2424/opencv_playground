import cv2
import numpy as np
from .base import Mode


class TrailsMode(Mode):
    name = "Motion Trails"
    key = ord('8')
    instructions = "r : clear trail | [ / ] : trail decay (persistence)"

    def __init__(self):
        self.decay = 0.9
        self.accumulator = None

    def on_activate(self, frame_shape):
        self.accumulator = np.zeros(frame_shape, dtype=np.float32)

    def process(self, frame):
        if self.accumulator is None:
            self.on_activate(frame.shape)
        cv2.accumulateWeighted(frame.astype(np.float32), self.accumulator, 1 - self.decay)
        return cv2.convertScaleAbs(self.accumulator)

    def handle_key(self, key, frame):
        if key == ord('r'):
            self.on_activate(frame.shape)
            return True
        if key == ord('['):
            self.decay = max(0.5, self.decay - 0.05)
            return True
        if key == ord(']'):
            self.decay = min(0.99, self.decay + 0.05)
            return True
        return False
