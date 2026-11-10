import cv2
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT,
    ALERT_COOLDOWN_SECONDS, SIREN_ENABLED
)
from src.face_recognizer import FaceRecognizer
from src.email_alert import EmailAlert
from src.detection_logger import DetectionLogger
from src.siren import SirenPlayer


class SurveillanceSystem:
    def __init__(self, camera_id="CAM_01"):
        self.camera_id = camera_id
        self.recognizer = FaceRecognizer()
        self.email_alert = EmailAlert()
        self.logger = DetectionLogger()
        self.siren = SirenPlayer() if SIREN_ENABLED else None
        self.recognizer.cleanup_old_snapshots()

    def run(self):
        cap = cv2.VideoCapture(CAMERA_INDEX)
        if not cap.isOpened():
            print("[ERROR] Cannot open webcam.")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

        known_count = self.recognizer.db.get_known_face_count()
        print("=" * 60)
        print("  SMART CAMERA & VIDEO SURVEILLANCE SYSTEM")
        print("=" * 60)
        print(f"  Camera       : {self.camera_id}")
        print(f"  Known Faces  : {known_count}")
        print(f"  Email Alerts : {'ON' if self.email_alert.enabled else 'OFF'}")
        print("=" * 60)
        print("  Controls:")
        print("    q - Quit")
        print("    s - Save snapshot")
        print("    a - Add new face to database")
        print("    l - Show detection logs")
        print("    r - Refresh known faces")
        print("=" * 60)

        start_time = time.time()
        match_count = 0
        unknown_count = 0
        last_alert_time = {}

        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Failed to grab frame.")
                break

            results = self.recognizer.recognize_faces(frame)
            frame = self.recognizer.draw_results(frame, results)

            for result in results:
                if result["is_match"]:
                    match_count += 1
                    name = result["name"]
                    now = time.time()

                    if name not in last_alert_time or (now - last_alert_time[name]) >= ALERT_COOLDOWN_SECONDS:
                        snapshot_path = self.recognizer.save_recognition_snapshot(
                            frame, result, self.camera_id
                        )
                        self.email_alert.send_alert(
                            name=name,
                            confidence=result["confidence"],
                            camera_id=self.camera_id,
                            snapshot_path=snapshot_path,
                            timestamp=result["timestamp"]
                        )
                        self.logger.log(
                            name, result["confidence"],
                            self.camera_id, snapshot_path, True
                        )
                        last_alert_time[name] = now
                        if self.siren:
                            self.siren.play_async()
                        print(f"[ALERT] {name} detected! Confidence: {result['confidence']:.0%}")
                else:
                    unknown_count += 1

            elapsed = time.time() - start_time
            fps = len(results) / elapsed if elapsed > 0 else 0

            info_lines = [
                f"Smart Surveillance | {self.camera_id}",
                f"Known: {known_count} | Matches: {match_count} | Unknown: {unknown_count}",
                f"Runtime: {elapsed:.0f}s | Faces/sec: {fps:.1f}"
            ]

            for i, line in enumerate(info_lines):
                cv2.putText(frame, line, (10, 25 + i * 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            cv2.imshow("Smart Surveillance System", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s') and results:
                for r in results:
                    path = self.recognizer.save_recognition_snapshot(frame, r, self.camera_id)
                    print(f"[SNAPSHOT] Saved: {path}")
            elif key == ord('a'):
                self.add_face_interactive(cap)
            elif key == ord('l'):
                self.show_logs()
            elif key == ord('r'):
                self.recognizer.load_known_faces()
                known_count = self.recognizer.db.get_known_face_count()
                print(f"[INFO] Refreshed. {known_count} known faces loaded.")

        cap.release()
        cv2.destroyAllWindows()

        stats = self.logger.get_stats()
        print("\n" + "=" * 60)
        print("  SESSION SUMMARY")
        print("=" * 60)
        print(f"  Total Detections : {stats['total']}")
        print(f"  Matches          : {stats['matches']}")
        print(f"  Unknown          : {stats['unknown']}")
        print("=" * 60)

    def add_face_interactive(self, cap):
        print("\n[ADD FACE] Enter the person's name:")
        name = input("  Name: ").strip()
        if not name:
            print("[CANCELLED] No name entered.")
            return

        print("[ADD FACE] Position face in front of camera. Press 'c' to capture...")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Add Face - Press 'c' to Capture", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                import face_recognition
                face_locations = face_recognition.face_locations(rgb_frame)
                if face_locations:
                    success = self.recognizer.add_face_from_frame(name, frame, face_locations[0])
                    if success:
                        print(f"[SUCCESS] '{name}' added to database!")
                    else:
                        print("[ERROR] Could not encode face.")
                else:
                    print("[ERROR] No face detected. Try again.")
                break
            elif key == ord('q'):
                print("[CANCELLED]")
                break

    def show_logs(self):
        stats = self.logger.get_stats()
        print("\n" + "=" * 50)
        print("  DETECTION LOG SUMMARY")
        print("=" * 50)
        print(f"  Total Detections : {stats['total']}")
        print(f"  Matches          : {stats['matches']}")
        print(f"  Unknown          : {stats['unknown']}")
        print("=" * 50)

        logs = self.logger.get_logs(limit=10)
        if len(logs) > 1:
            print("\n  Last 10 Detections:")
            for row in logs[1:]:
                print(f"    {row[0]} | {row[1]} | Conf: {row[2]} | {row[3]}")
        else:
            print("  No detections logged yet.")


if __name__ == "__main__":
    system = SurveillanceSystem()
    system.run()
