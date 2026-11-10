import threading
import time
import cv2
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT,
    ALERT_COOLDOWN_SECONDS, SIREN_ENABLED
)
from src.face_recognizer import FaceRecognizer
from src.object_detector import ObjectDetector
from src.email_alert import EmailAlert
from src.detection_logger import DetectionLogger
from src.siren import SirenPlayer


class VideoProcessor:
    def __init__(self):
        self.running = True
        self.frame = None
        self.faces = []
        self.objects = []
        self.last_alert_time = {}
        self.error = None

        self.recognizer = FaceRecognizer()
        self.object_detector = ObjectDetector()
        self.email_alert = EmailAlert()
        self.logger = DetectionLogger()
        self.siren = SirenPlayer() if SIREN_ENABLED else None

        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.start_time = time.time()

    def start(self):
        self.thread.start()

    def stop(self):
        self.running = False

    def _capture_loop(self):
        cap = cv2.VideoCapture(CAMERA_INDEX)
        if not cap.isOpened():
            self.error = "Cannot open camera."
            return
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

        frame_num = 0
        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue

            frame_num += 1
            faces = self.recognizer.recognize_faces(frame)
            frame = self.recognizer.draw_results(frame, faces)

            if frame_num % 3 == 0:
                self.objects = self.object_detector.detect_objects(frame)
            frame = self.object_detector.draw_objects(frame, self.objects)

            current_faces = []
            now = time.time()
            for face in faces:
                if face["is_match"]:
                    name = face["name"]
                    flag = name not in self.last_alert_time or \
                        (now - self.last_alert_time[name]) >= ALERT_COOLDOWN_SECONDS
                    if flag and self.email_alert.enabled:
                        snapshot = self.recognizer.save_recognition_snapshot(frame, face, "CAM_01")
                        self.email_alert.send_alert(
                            name=name,
                            confidence=face["confidence"],
                            camera_id="CAM_01",
                            snapshot_path=snapshot,
                            timestamp=face["timestamp"]
                        )
                        self.logger.log(name, face["confidence"], "CAM_01", snapshot, True)
                        self.last_alert_time[name] = now
                        if self.siren:
                            self.siren.play_async()
                current_faces.append({
                    "name": face["name"],
                    "confidence": face["confidence"],
                    "is_match": face["is_match"],
                    "timestamp": face["timestamp"]
                })

            elapsed = int(time.time() - self.start_time)
            suspicious_count = self.object_detector.count_suspicious(self.objects)
            info_lines = [
                f"Smart Surveillance Dashboard | Uptime: {elapsed}s",
                f"Faces: {len(faces)} | Objects: {len(self.objects)} | Suspicious: {suspicious_count}"
            ]
            for i, line in enumerate(info_lines):
                cv2.putText(frame, line, (10, 25 + i * 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            self.faces = current_faces
            self.frame = frame

        cap.release()

    def get_frame_jpeg(self):
        if self.frame is None:
            return None
        ret, jpeg = cv2.imencode(".jpg", self.frame)
        if not ret:
            return None
        return jpeg.tobytes()