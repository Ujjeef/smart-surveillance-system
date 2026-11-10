import cv2
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.face_detector import FaceDetector


def detect_faces_in_image(image_path):
    if not os.path.exists(image_path):
        print(f"[ERROR] Image not found: {image_path}")
        return

    detector = FaceDetector()
    frame = cv2.imread(image_path)

    if frame is None:
        print(f"[ERROR] Cannot read image: {image_path}")
        return

    detections = detector.detect_faces(frame)
    frame = detector.draw_detections(frame, detections)

    print(f"[INFO] Found {len(detections)} face(s) in the image.")
    for i, det in enumerate(detections):
        print(f"  Face {i+1}: Position=({det['x']},{det['y']}) Size=({det['w']}x{det['h']}) Eyes={det['eyes_detected']}")

    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "snapshots")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "detected_" + os.path.basename(image_path))
    cv2.imwrite(output_path, frame)
    print(f"[INFO] Output saved to: {output_path}")

    cv2.imshow("Detected Faces", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detect_faces_in_video(video_path):
    if not os.path.exists(video_path):
        print(f"[ERROR] Video not found: {video_path}")
        return

    detector = FaceDetector()
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[ERROR] Cannot open video: {video_path}")
        return

    total_detections = 0
    frame_count = 0

    print("[INFO] Processing video... Press 'q' to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 3 != 0:
            continue

        detections = detector.detect_faces(frame)
        frame = detector.draw_detections(frame, detections)
        total_detections += len(detections)

        cv2.imshow("Video Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"[INFO] Video processing complete. Frames processed: {frame_count}, Total faces found: {total_detections}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python image_face_detection.py <image_path>")
        print("  python image_face_detection.py --video <video_path>")
    elif sys.argv[1] == "--video" and len(sys.argv) >= 3:
        detect_faces_in_video(sys.argv[2])
    else:
        detect_faces_in_image(sys.argv[1])
