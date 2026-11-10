import csv
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import LOGS_DIR


class DetectionLogger:
    def __init__(self):
        os.makedirs(LOGS_DIR, exist_ok=True)
        self.csv_path = os.path.join(LOGS_DIR, "detection_log.csv")
        self.ensure_csv_exists()

    def ensure_csv_exists(self):
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp", "Name", "Confidence",
                    "Camera_ID", "Is_Match", "Snapshot_Path"
                ])

    def log(self, name, confidence, camera_id, snapshot_path, is_match):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, name, confidence,
                camera_id, 1 if is_match else 0, snapshot_path
            ])

    def get_logs(self, limit=100):
        if not os.path.exists(self.csv_path):
            return []
        with open(self.csv_path, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
        return rows[-limit:] if len(rows) > limit else rows

    def get_stats(self):
        if not os.path.exists(self.csv_path):
            return {"total": 0, "matches": 0, "unknown": 0}
        with open(self.csv_path, "r") as f:
            reader = csv.reader(f)
            next(reader, None)
            rows = list(reader)
        matches = sum(1 for r in rows if len(r) > 4 and r[4] == "1")
        return {
            "total": len(rows),
            "matches": matches,
            "unknown": len(rows) - matches
        }

    def export_report(self, filepath=None):
        if filepath is None:
            filepath = os.path.join(LOGS_DIR, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        if not os.path.exists(self.csv_path):
            print("[ERROR] No logs to export.")
            return None
        import shutil
        shutil.copy2(self.csv_path, filepath)
        print(f"[LOG] Report exported to: {filepath}")
        return filepath
