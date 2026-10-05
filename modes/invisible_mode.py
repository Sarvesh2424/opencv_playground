import cv2
import numpy as np
from .base import Mode


class InvisibleMode(Mode):
    name = "Invisible Person"
    key = ord('5')
    instructions = "b : capture empty background | wear something RED to vanish"

    # HSV ranges covering red (wraps around hue 0/180)
    LOWER_RED_1 = np.array([0, 120, 70])
    UPPER_RED_1 = np.array([10, 255, 255])
    LOWER_RED_2 = np.array([170, 120, 70])
    UPPER_RED_2 = np.array([180, 255, 255])

    def __init__(self):
        self.background = None

    def on_activate(self, frame_shape):
        self.background = None

    def process(self, frame):
        if self.background is None:
            output = frame.copy()
            cv2.putText(output, "Press 'b' to capture background (step out of frame first)",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
            return output

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOWER_RED_1, self.UPPER_RED_1)
        mask |= cv2.inRange(hsv, self.LOWER_RED_2, self.UPPER_RED_2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)
        mask_inv = cv2.bitwise_not(mask)

        cloak_area = cv2.bitwise_and(self.background, self.background, mask=mask)
        visible_area = cv2.bitwise_and(frame, frame, mask=mask_inv)
        return cv2.add(cloak_area, visible_area)

    def handle_key(self, key, frame):
        if key == ord('b'):
            self.background = frame.copy()
            return True
        return False
