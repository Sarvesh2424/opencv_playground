import cv2
import numpy as np
from .base import Mode


class PerspectiveMode(Mode):
    name = "Perspective Tricks"
    key = ord('0')
    instructions = "click 4 corners (TL, TR, BR, BL) | r : reset"

    WARP_SIZE = 400

    def __init__(self):
        self.points = []

    def on_activate(self, frame_shape):
        self.points = []

    def process(self, frame):
        output = frame.copy()
        for p in self.points:
            cv2.circle(output, p, 6, (0, 255, 0), -1)

        if len(self.points) == 4:
            src = np.float32(self.points)
            w = h = self.WARP_SIZE
            dst = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
            matrix = cv2.getPerspectiveTransform(src, dst)
            warped = cv2.warpPerspective(frame, matrix, (w, h))
            output[0:h, 0:w] = warped
            cv2.rectangle(output, (0, 0), (w, h), (0, 0, 255), 2)
        else:
            cv2.putText(output, "Click 4 corners in order: TL, TR, BR, BL",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        return output

    def handle_key(self, key, frame):
        if key == ord('r'):
            self.points = []
            return True
        return False

    def handle_mouse(self, event, x, y):
        if event == cv2.EVENT_LBUTTONDOWN and len(self.points) < 4:
            self.points.append((x, y))
