import cv2
from .base import Mode


class EdgeMode(Mode):
    name = "Edge Detection"
    key = ord('1')
    instructions = "[ / ] : lower / raise Canny thresholds"

    def __init__(self):
        self.low = 50
        self.high = 150

    def process(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, self.low, self.high)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def handle_key(self, key, frame):
        if key == ord('['):
            self.low = max(0, self.low - 10)
            self.high = max(self.low + 1, self.high - 10)
            return True
        if key == ord(']'):
            self.low += 10
            self.high += 10
            return True
        return False
