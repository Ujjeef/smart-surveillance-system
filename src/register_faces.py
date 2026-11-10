import cv2
import face_recognition
import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import KNOWN_FACES_DIR, DATASET_DIR
from src.face_recognizer import FaceRecognizer


def register_known_faces():
    recognizer = FaceRecognizer()

    print("=" * 50)
    print("  REGISTER KNOWN FACES")
    print("=" * 50)
    print("  1. Register from image file")
    print("  2. Register from dataset folder")
    print("  3. View registered faces")
    print("  4. Delete a face")
    print("  5. Back")
    print("=" * 50)

    choice = input("  Select option: ").strip()

    if choice == "1":
        name = input("  Enter person name: ").strip()
        path = input("  Enter image path: ").strip()
        if not os.path.exists(path):
            print(f"[ERROR] File not found: {path}")
            return
        success = recognizer.add_new_face(name, path)
        if success:
            print(f"[SUCCESS] '{name}' registered successfully!")
            print(f"  Total known faces: {recognizer.db.get_known_face_count()}")

    elif choice == "2":
        dataset_path = DATASET_DIR
        if not os.path.exists(dataset_path):
            print("[ERROR] Dataset folder not found.")
            return

        persons = [d for d in os.listdir(dataset_path)
                   if os.path.isdir(os.path.join(dataset_path, d))]

        if not persons:
            print("[INFO] No person folders found in dataset/.")
            return

        print(f"\n  Found {len(persons)} person(s) in dataset:")
        for i, p in enumerate(persons, 1):
            img_count = len([f for f in os.listdir(os.path.join(dataset_path, p))
                            if f.endswith(('.jpg', '.png', '.jpeg'))])
            print(f"    {i}. {p} ({img_count} images)")

        person_idx = int(input("\n  Select person number: ").strip()) - 1
        if 0 <= person_idx < len(persons):
            person_name = persons[person_idx]
            person_dir = os.path.join(dataset_path, person_name)
            images = [f for f in os.listdir(person_dir)
                     if f.endswith(('.jpg', '.png', '.jpeg'))]

            print(f"\n  Registering '{person_name}' with {len(images)} images...")
            count = 0
            for img_file in images:
                img_path = os.path.join(person_dir, img_file)
                if recognizer.add_new_face(person_name, img_path):
                    count += 1
            print(f"[SUCCESS] Added {count} encodings for '{person_name}'")
        else:
            print("[ERROR] Invalid selection.")

    elif choice == "3":
        faces = recognizer.db.get_all_known_faces()
        if not faces:
            print("[INFO] No faces registered yet.")
            return
        print(f"\n  Registered Faces ({len(faces)}):")
        print("  " + "-" * 40)
        for f in faces:
            print(f"  ID: {f['id']} | Name: {f['name']} | Added: {f['added_date']}")

    elif choice == "4":
        faces = recognizer.db.get_all_known_faces()
        if not faces:
            print("[INFO] No faces to delete.")
            return
        for f in faces:
            print(f"  ID: {f['id']} | Name: {f['name']}")
        face_id = int(input("  Enter ID to delete: ").strip())
        recognizer.db.delete_known_face(face_id)
        recognizer.load_known_faces()
        print("[SUCCESS] Deleted.")

    elif choice == "5":
        return


if __name__ == "__main__":
    register_known_faces()
