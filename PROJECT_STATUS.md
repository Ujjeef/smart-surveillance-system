# Project Status: FINAL / FROZEN

**Smart Camera & Video Surveillance System — A Deep Learning based Criminal Recognition and Tracking System**

- Date finalized: 2026-11-04
- Status: **The project is complete as-is. No further development.**
- This is the whole project. Do not add, remove, or modify features unless explicitly requested.
- Existing behavior and files are to be treated as the final deliverable.

## Correct order to read the `src/` files

The order below follows the actual dependency flow (foundation -> core -> integration).

1. `face_detector.py` — Haar-cascade face detection (the foundation).
2. `webcam_capture.py` — open webcam and read frames.
3. `image_face_detection.py` — detect faces in a still image.
4. `dataset_collector.py` — collect per-person training images.
5. `database.py` — SQLite storage layer (needed by the recognizer).
6. `face_recognizer.py` — **core**: detect, encode, match, snapshot.
7. `test_recognition.py` — quick test of the recognizer.
8. `register_faces.py` — add/delete/view known faces (uses the recognizer + DB).
9. `detection_logger.py` — CSV event logging and stats.
10. `email_alert.py` — SMTP email with snapshot attachment.
11. `siren.py` — generate and play the siren sound.
12. `object_detector.py` — YOLOv4-tiny object detection.
13. `surveillance.py` — terminal integration of all modules (OpenCV window).
14. `dashboard.py` — web integration background camera thread (used by `app.py`).

Supporting files outside `src/`: `config/settings.py` (read first), then `app.py` and `templates/`.
