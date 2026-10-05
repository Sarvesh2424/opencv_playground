import cv2
from .base import Mode


class TrackingMode(Mode):
    name = "Object Tracking"
    key = ord('3')
    instructions = "s : select object to track (drag a box, Enter to confirm)"

    def __init__(self):
        self.tracker = None

    def on_activate(self, frame_shape):
        self.tracker = None

    def process(self, frame):
        output = frame.copy()
        if self.tracker is not None:
            ok, bbox = self.tracker.update(frame)
            if ok:
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(output, (x, y), (x + w, y + h), (255, 0, 0), 2)
            else:
                cv2.putText(output, "Lost - press 's' to reselect", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(output, "Press 's' to select an object", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        return output

    def handle_key(self, key, frame):
        if key == ord('s'):
            bbox = cv2.selectROI("Select object - Enter to confirm", frame, False)
            cv2.destroyWindow("Select object - Enter to confirm")
            if bbox[2] > 0 and bbox[3] > 0:
                # requires opencv-contrib-python (see requirements.txt)
                self.tracker = cv2.TrackerCSRT_create()
                self.tracker.init(frame, bbox)
            return True
        return False
