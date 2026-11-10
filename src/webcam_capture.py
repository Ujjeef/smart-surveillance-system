import cv2
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT
from src.face_detector import FaceDetector


def run_webcam_detection():
    detector = FaceDetector()
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print("[ERROR] Cannot open webcam. Check if camera is connected.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    print("[INFO] Webcam started. Press 'q' to quit.")
    print("[INFO] Press 's' to save a snapshot manually.")
    print("[INFO] Press 'r' to reset detection counter.")

    detection_count = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break

        detections = detector.detect_faces(frame)
        frame = detector.draw_detections(frame, detections)

        if detections:
            detection_count += len(detections)

        elapsed = time.time() - start_time
        fps = detection_count / elapsed if elapsed > 0 else 0

        info_text = f"Faces: {len(detections)} | Total Detections: {detection_count} | Time: {elapsed:.1f}s"
        cv2.putText(frame, info_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Smart Surveillance - Face Detection (Week 1)", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s') and detections:
            for det in detections:
                path = detector.save_snapshot(frame, det)
                print(f"[SNAPSHOT] Saved: {path}")
        elif key == ord('r'):
            detection_count = 0
            start_time = time.time()
            print("[INFO] Counter reset.")

    cap.release()
    cv2.destroyAllWindows()
    print(f"[INFO] Session ended. Total detections: {detection_count}")


if __name__ == "__main__":
    run_webcam_detection()
