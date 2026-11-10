import cv2
import os
import sys
import time
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    FACE_CASCADE_PATH, EYE_CASCADE_PATH,
    CAMERA_INDEX, SCALE_FACTOR, MIN_NEIGHBORS,
    FRAME_WIDTH, FRAME_HEIGHT, SNAPSHOTS_DIR
)


class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
        self.eye_cascade = cv2.CascadeClassifier(EYE_CASCADE_PATH)

        if self.face_cascade.empty():
            raise IOError("Failed to load face cascade classifier.")
        if self.eye_cascade.empty():
            raise IOError("Failed to load eye cascade classifier.")

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=SCALE_FACTOR, minNeighbors=MIN_NEIGHBORS, minSize=(50, 50)
        )
        results = []
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            results.append({
                "x": x, "y": y, "w": w, "h": h,
                "eyes_detected": len(eyes),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        return results

    def draw_detections(self, frame, detections):
        for det in detections:
            x, y, w, h = det["x"], det["y"], det["w"], det["h"]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            label = f"Face ({det['eyes_detected']} eyes)"
            cv2.putText(frame, label, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        return frame

    def save_snapshot(self, frame, detection):
        os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"snapshot_{timestamp}.jpg"
        filepath = os.path.join(SNAPSHOTS_DIR, filename)
        x, y, w, h = detection["x"], detection["y"], detection["w"], detection["h"]
        padding = 20
        y1 = max(0, y - padding)
        y2 = min(frame.shape[0], y + h + padding)
        x1 = max(0, x - padding)
        x2 = min(frame.shape[1], x + w + padding)
        cv2.imwrite(filepath, frame[y1:y2, x1:x2])
        return filepath
