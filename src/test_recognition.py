import cv2
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.face_recognizer import FaceRecognizer


def test_recognition(image_path):
    if not os.path.exists(image_path):
        print(f"[ERROR] Image not found: {image_path}")
        return

    recognizer = FaceRecognizer()
    frame = cv2.imread(image_path)
    results = recognizer.recognize_faces(frame)
    frame = recognizer.draw_results(frame, results)

    print(f"\n[TEST] Found {len(results)} face(s):")
    for i, r in enumerate(results):
        status = "MATCH" if r["is_match"] else "UNKNOWN"
        print(f"  Face {i+1}: {r['name']} ({status}) - Confidence: {r['confidence']:.0%}")

    output_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "snapshots", "test_result.jpg"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, frame)
    print(f"\n[SAVED] Result saved to: {output_path}")

    cv2.imshow("Recognition Test", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_recognition.py <image_path>")
    else:
        test_recognition(sys.argv[1])
