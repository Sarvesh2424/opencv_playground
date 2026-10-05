import cv2
import numpy as np
from .base import Mode


class OpticalFlowMode(Mode):
    name = "Optical Flow"
    key = ord('4')
    instructions = "hue = direction, brightness = speed"

    def __init__(self):
        self.prev_gray = None
        self.hsv = None

    def on_activate(self, frame_shape):
        self.prev_gray = None
        self.hsv = np.zeros(frame_shape, dtype=np.uint8)
        self.hsv[..., 1] = 255

    def process(self, frame):
        if self.hsv is None:
            self.on_activate(frame.shape)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.prev_gray is None:
            self.prev_gray = gray
            return frame

        flow = cv2.calcOpticalFlowFarneback(
            self.prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
        )
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        self.hsv[..., 0] = ang * 180 / np.pi / 2
        self.hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        self.prev_gray = gray
        return cv2.cvtColor(self.hsv, cv2.COLOR_HSV2BGR)
