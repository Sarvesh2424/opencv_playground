import cv2

from modes.edge_mode import EdgeMode
from modes.motion_mode import MotionMode
from modes.tracking_mode import TrackingMode
from modes.optical_flow_mode import OpticalFlowMode
from modes.invisible_mode import InvisibleMode
from modes.clone_mode import CloneMode
from modes.teleport_mode import TeleportMode
from modes.trails_mode import TrailsMode
from modes.ar_mode import ARMode
from modes.perspective_mode import PerspectiveMode
from modes.debug_mode import DebugMode

WINDOW = "OpenCV Playground"


def build_modes():
    modes = [
        EdgeMode(), MotionMode(), TrackingMode(), OpticalFlowMode(),
        InvisibleMode(), CloneMode(), TeleportMode(), TrailsMode(),
        ARMode(), PerspectiveMode(), DebugMode(),
    ]
    return {m.key: m for m in modes}


def print_help(modes):
    print("OpenCV Playground — keys:")
    for m in modes.values():
        label = chr(m.key) if m.key < 256 else str(m.key)
        line = f"  {label} : {m.name}"
        if m.instructions:
            line += f"  ({m.instructions})"
        print(line)
    print("  q / ESC : quit\n")


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam (index 0). Check camera permissions/index.")

    modes = build_modes()
    active = None  # None = raw passthrough until a mode key is pressed
    print_help(modes)

    cv2.namedWindow(WINDOW)

    def on_mouse(event, x, y, flags, param):
        if active is not None:
            active.handle_mouse(event, x, y)

    cv2.setMouseCallback(WINDOW, on_mouse)

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)  # mirror, feels natural for a webcam

        key = cv2.waitKey(1) & 0xFF
        if key in (ord('q'), 27):
            break
        if key in modes:
            active = modes[key]
            active.on_activate(frame.shape)
        elif active is not None:
            active.handle_key(key, frame)

        output = active.process(frame) if active is not None else frame.copy()
        label = active.name if active is not None else "Live Feed (press a number/letter to start)"
        cv2.putText(output, label, (10, output.shape[0] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.imshow(WINDOW, output)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
