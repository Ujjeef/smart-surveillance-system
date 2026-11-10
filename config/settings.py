import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _load_env():
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip()
                    if value and not os.environ.get(key):
                        os.environ[key] = value

_load_env()
KNOWN_FACES_DIR = os.path.join(BASE_DIR, "known_faces")
SNAPSHOTS_DIR = os.path.join(BASE_DIR, "snapshots")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODELS_DIR = os.path.join(BASE_DIR, "models")

FACE_CASCADE_PATH = os.path.join(MODELS_DIR, "haarcascade_frontalface_default.xml")
EYE_CASCADE_PATH = os.path.join(MODELS_DIR, "haarcascade_eye.xml")

CAMERA_INDEX = 0
CONFIDENCE_THRESHOLD = 0.4
ALERT_COOLDOWN_SECONDS = 30
SNAPSHOT_KEEP = 50
SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 5
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
ALERT_EMAIL = "your_email@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD", "")

YOLO_CFG = os.path.join(MODELS_DIR, "yolov4-tiny.cfg")
YOLO_WEIGHTS = os.path.join(MODELS_DIR, "yolov4-tiny.weights")
YOLO_NAMES = os.path.join(MODELS_DIR, "coco.names")
YOLO_CONFIDENCE = 0.4
YOLO_THRESHOLD = 0.4
SUSPICIOUS_OBJECTS = ["backpack", "handbag", "suitcase", "cell phone", "knife", "scissors"]
SIREN_ENABLED = True
SIREN_SOUND_PATH = os.path.join(BASE_DIR, "sounds", "siren.wav")
