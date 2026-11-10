import sqlite3
import threading
import numpy as np
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import BASE_DIR


class FaceDatabase:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(BASE_DIR, "logs", "faces.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.lock = threading.Lock()
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS known_faces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                encoding BLOB NOT NULL,
                image_path TEXT,
                added_date TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                confidence REAL,
                camera_id TEXT,
                snapshot_path TEXT,
                timestamp TEXT NOT NULL,
                is_match INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_known_face(self, name, encoding, image_path=""):
        with self.lock:
            cursor = self.conn.cursor()
            encoding_blob = encoding.tobytes()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO known_faces (name, encoding, image_path, added_date) VALUES (?, ?, ?, ?)",
                (name, encoding_blob, image_path, timestamp)
            )
            self.conn.commit()
            return cursor.lastrowid

    def get_all_known_faces(self):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, name, encoding, image_path, added_date FROM known_faces")
            rows = cursor.fetchall()
            faces = []
            for row in rows:
                encoding = np.frombuffer(row[2], dtype=np.float64)
                faces.append({
                    "id": row[0],
                    "name": row[1],
                    "encoding": encoding,
                    "image_path": row[3],
                    "added_date": row[4]
                })
            return faces

    def log_detection(self, name, confidence, camera_id, snapshot_path, is_match=False):
        with self.lock:
            cursor = self.conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            match_flag = 1 if is_match else 0
            cursor.execute(
                "INSERT INTO detections (name, confidence, camera_id, snapshot_path, timestamp, is_match) VALUES (?, ?, ?, ?, ?, ?)",
                (name, confidence, camera_id, snapshot_path, timestamp, match_flag)
            )
            self.conn.commit()

    def get_detection_history(self, limit=50):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT * FROM detections ORDER BY id DESC LIMIT ?", (limit,)
            )
            return cursor.fetchall()

    def get_known_face_count(self):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM known_faces")
            return cursor.fetchone()[0]

    def delete_known_face(self, face_id):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM known_faces WHERE id = ?", (face_id,))
            self.conn.commit()

    def close(self):
        self.conn.close()
