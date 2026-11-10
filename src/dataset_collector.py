import cv2
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, DATASET_DIR
from src.face_detector import FaceDetector


def collect_dataset(person_name, num_samples=50):
    detector = FaceDetector()
    person_dir = os.path.join(DATASET_DIR, person_name)
    os.makedirs(person_dir, exist_ok=True)

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("[ERROR] Cannot open webcam.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    print(f"[INFO] Collecting {num_samples} samples for '{person_name}'")
    print("[INFO] Press 'c' to capture, 'q' to quit early.")

    count = 0
    while count < num_samples:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect_faces(frame)
        for det in detections:
            x, y, w, h = det["x"], det["y"], det["w"], det["h"]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.putText(frame, f"Collected: {count}/{num_samples}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Dataset Collection", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c') and detections:
            det = detections[0]
            x, y, w, h = det["x"], det["y"], det["w"], det["h"]
            face_img = frame[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (200, 200))
            filepath = os.path.join(person_dir, f"{person_name}_{count+1:04d}.jpg")
            cv2.imwrite(filepath, face_img)
            count += 1
            print(f"  Captured {count}/{num_samples}")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"[INFO] Dataset collection complete. {count} images saved to {person_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dataset_collector.py <person_name> [num_samples]")
        print("Example: python dataset_collector.py john 50")
    else:
        name = sys.argv[1]
        samples = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        collect_dataset(name, samples)
