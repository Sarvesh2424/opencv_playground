import cv2
from .base import Mode


class ARMode(Mode):
    name = "AR Effects"
    key = ord('9')
    instructions = "auto-detects faces and overlays AR sunglasses"

    def __init__(self):
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def process(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(80, 80))
        output = frame.copy()
        for (x, y, w, h) in faces:
            eye_y = y + int(h * 0.35)
            eye_h = int(h * 0.18)
            cv2.rectangle(output, (x + int(w * 0.1), eye_y),
                          (x + int(w * 0.9), eye_y + eye_h), (20, 20, 20), -1)
            cv2.circle(output, (x + int(w * 0.28), eye_y + eye_h // 2), eye_h // 2, (0, 200, 255), 3)
            cv2.circle(output, (x + int(w * 0.72), eye_y + eye_h // 2), eye_h // 2, (0, 200, 255), 3)
        return output
