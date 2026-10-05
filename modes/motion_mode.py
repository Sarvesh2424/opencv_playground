import cv2
from .base import Mode


class MotionMode(Mode):
    name = "Motion Detection"
    key = ord('2')
    instructions = "r : reset background model"

    def __init__(self):
        self.bg_subtractor = None

    def on_activate(self, frame_shape):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=25, detectShadows=True
        )

    def process(self, frame):
        if self.bg_subtractor is None:
            self.on_activate(frame.shape)

        fg_mask = self.bg_subtractor.apply(frame)
        fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)[1]
        fg_mask = cv2.morphologyEx(
            fg_mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        )

        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        output = frame.copy()
        for c in contours:
            if cv2.contourArea(c) < 800:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return output

    def handle_key(self, key, frame):
        if key == ord('r'):
            self.on_activate(frame.shape)
            return True
        return False
