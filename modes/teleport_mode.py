import cv2
import numpy as np
from .base import Mode


class TeleportMode(Mode):
    name = "Object Teleportation"
    key = ord('7')
    instructions = "s : select object | click anywhere : teleport it there"

    def __init__(self):
        self.cutout = None
        self.mask = None
        self.target = None

    def on_activate(self, frame_shape):
        self.cutout = None
        self.mask = None
        self.target = None

    def process(self, frame):
        output = frame.copy()
        if self.cutout is not None and self.target is not None:
            h, w = self.mask.shape
            x = max(w // 2, min(frame.shape[1] - w // 2 - 1, self.target[0]))
            y = max(h // 2, min(frame.shape[0] - h // 2 - 1, self.target[1]))
            try:
                output = cv2.seamlessClone(self.cutout, output, self.mask, (x, y), cv2.NORMAL_CLONE)
            except cv2.error:
                pass  # target too close to an edge for this frame size; skip a frame
        if self.cutout is None:
            cv2.putText(output, "Press 's' to select an object to teleport",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        return output

    def handle_key(self, key, frame):
        if key == ord('s'):
            bbox = cv2.selectROI("Select object - Enter to confirm", frame, False)
            cv2.destroyWindow("Select object - Enter to confirm")
            x, y, w, h = [int(v) for v in bbox]
            if w > 0 and h > 0:
                self.cutout = frame[y:y + h, x:x + w].copy()
                self.mask = 255 * np.ones(self.cutout.shape[:2], dtype=np.uint8)
            return True
        return False

    def handle_mouse(self, event, x, y):
        if event == cv2.EVENT_LBUTTONDOWN and self.cutout is not None:
            self.target = (x, y)
