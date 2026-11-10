import face_recognition
import cv2
import numpy as np
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import CONFIDENCE_THRESHOLD, SNAPSHOTS_DIR, SNAPSHOT_KEEP, SCALE_FACTOR
from src.database import FaceDatabase


class FaceRecognizer:
    def __init__(self):
        self.db = FaceDatabase()
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces()

    def load_known_faces(self):
        faces = self.db.get_all_known_faces()
        self.known_encodings = [f["encoding"] for f in faces]
        self.known_names = [f["name"] for f in faces]
        print(f"[INFO] Loaded {len(self.known_names)} known faces from database.")

    def add_new_face(self, name, image_path):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            print(f"[ERROR] No face found in {image_path}")
            return False
        encoding = encodings[0]
        self.db.add_known_face(name, encoding, image_path)
        self.known_encodings.append(encoding)
        self.known_names.append(name)
        print(f"[INFO] Added '{name}' to database.")
        return True

    def add_face_from_frame(self, name, frame, face_location):
        top, right, bottom, left = face_location
        face_image = frame[top:bottom, left:right]
        rgb_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_face)
        if not encodings:
            return False
        encoding = encodings[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = os.path.join(SNAPSHOTS_DIR, f"{name}_{timestamp}.jpg")
        os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
        cv2.imwrite(img_path, frame)
        self.db.add_known_face(name, encoding, img_path)
        self.known_encodings.append(encoding)
        self.known_names.append(name)
        print(f"[INFO] Added '{name}' to database from live frame.")
        return True

    def recognize_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        results = []
        for encoding, location in zip(face_encodings, face_locations):
            name = "Unknown"
            confidence = 0.0
            is_match = False

            if self.known_encodings:
                distances = face_recognition.face_distance(self.known_encodings, encoding)
                best_match_idx = np.argmin(distances)
                best_distance = distances[best_match_idx]

                if best_distance < CONFIDENCE_THRESHOLD:
                    name = self.known_names[best_match_idx]
                    confidence = 1.0 - best_distance
                    is_match = True

            top, right, bottom, left = location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            results.append({
                "name": name,
                "confidence": round(confidence, 2),
                "is_match": is_match,
                "location": (top, right, bottom, left),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        return results

    def save_recognition_snapshot(self, frame, result, camera_id="CAM_01"):
        os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        status = "MATCH" if result["is_match"] else "UNKNOWN"
        filename = f"{status}_{result['name']}_{timestamp}.jpg"
        filepath = os.path.join(SNAPSHOTS_DIR, filename)

        top, right, bottom, left = result["location"]
        padding = 30
        y1 = max(0, top - padding)
        y2 = min(frame.shape[0], bottom + padding)
        x1 = max(0, left - padding)
        x2 = min(frame.shape[1], right + padding)
        cv2.imwrite(filepath, frame[y1:y2, x1:x2])

        self.db.log_detection(
            name=result["name"],
            confidence=result["confidence"],
            camera_id=camera_id,
            snapshot_path=filepath,
            is_match=result["is_match"]
        )
        self.cleanup_old_snapshots()
        return filepath

    def cleanup_old_snapshots(self, keep=None):
        if keep is None:
            keep = SNAPSHOT_KEEP
        if not os.path.exists(SNAPSHOTS_DIR):
            return
        files = [f for f in os.listdir(SNAPSHOTS_DIR) if f.endswith(".jpg")]
        if len(files) <= keep:
            return
        files.sort(key=lambda f: os.path.getmtime(os.path.join(SNAPSHOTS_DIR, f)))
        for old in files[:-keep]:
            os.remove(os.path.join(SNAPSHOTS_DIR, old))
        print(f"[CLEANUP] Removed {len(files) - keep} old snapshot(s). Kept last {keep}.")

    def draw_results(self, frame, results):
        for result in results:
            top, right, bottom, left = result["location"]
            if result["is_match"]:
                color = (0, 0, 255)
                label = f"MATCH: {result['name']} ({result['confidence']:.0%})"
            else:
                color = (0, 255, 0)
                label = "Unknown"

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 10),
                        cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

        return frame
