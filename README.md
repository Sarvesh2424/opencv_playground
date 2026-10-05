# OpenCV Playground

A little webcam-driven CV sandbox. Run it, press a key, watch the effect —
each mode is one self-contained file under `modes/`.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

Needs a working webcam. `opencv-contrib-python` (not plain `opencv-python`)
is required for the tracking mode's `TrackerCSRT`.

## Controls

| Key | Mode              | Notes                                             |
|-----|-------------------|----------------------------------------------------|
| 1   | Edge Detection    | `[` / `]` to adjust Canny thresholds               |
| 2   | Motion Detection  | `r` to reset the background model                  |
| 3   | Object Tracking   | `s` to drag-select an object, then it's tracked    |
| 4   | Optical Flow      | hue = direction, brightness = speed                |
| 5   | Invisible Person  | `b` to grab an empty background, then wear red     |
| 6   | Clone Yourself    | `b` background, `c` to stamp a clone at your pose  |
| 7   | Object Teleport   | `s` select object, click anywhere to place it      |
| 8   | Motion Trails     | `r` clear, `[` / `]` adjust trail persistence      |
| 9   | AR Effects        | auto face detection + sunglasses overlay           |
| 0   | Perspective Trick | click 4 corners (TL, TR, BR, BL) to unwarp a plane |
| d   | Debug Mode        | FPS, resolution, brightness stats, live histogram  |
| q / Esc | —             | quit                                               |

Before any mode is selected you just see the raw mirrored feed.

## How it's structured

`modes/base.py` defines a tiny `Mode` interface: `process(frame)` returns
the frame to display, `on_activate` resets state when you switch to a
mode, `handle_key`/`handle_mouse` are optional hooks for mode-specific
controls. `main.py` just owns the webcam loop and dispatches keys/clicks
to whichever mode is active — each mode file is completely independent,
so you can read or rewrite one without touching the others.

## Ideas to extend it

- **Invisible Person**: swap the fixed red-HSV range for a color picked
  live by clicking on the cloak.
- **Clone Yourself**: instead of press-to-stamp, auto-stamp every N
  frames for a "chorus line" effect.
- **Tracking**: try `TrackerKCF_create()` vs `TrackerCSRT_create()` and
  compare speed/accuracy.
- **AR Effects**: replace the drawn sunglasses with a PNG overlay using
  alpha blending — the more classic AR-filter approach.
- **Perspective Tricks**: feed the warped bird's-eye view into Edge or
  Motion mode to see document-scanner-style pipelines.
