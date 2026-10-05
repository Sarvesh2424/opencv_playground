import time
import cv2
from .base import Mode


class DebugMode(Mode):
    name = "CV Debug Mode"
    key = ord('d')
    instructions = "shows FPS, resolution, brightness stats, and a live histogram"

    def __init__(self):
        self.prev_time = time.time()

    def process(self, frame):
        now = time.time()
        fps = 1 / max(now - self.prev_time, 1e-6)
        self.prev_time = now

        output = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean, std = cv2.meanStdDev(gray)

        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist, 0, 150, cv2.NORM_MINMAX)
        h, w = output.shape[:2]
        for i in range(1, 256):
            cv2.line(
                output,
                (w - 256 + i - 1, h - int(hist[i - 1])),
                (w - 256 + i, h - int(hist[i])),
                (0, 255, 0), 1,
            )

        cv2.putText(output, f"FPS: {fps:.1f}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(output, f"Res: {w}x{h}", (20, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(output, f"Mean/Std: {mean[0][0]:.1f}/{std[0][0]:.1f}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        return output
