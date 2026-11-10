import os
import sys
import glob

from flask import Flask, render_template, Response, send_file, jsonify

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config.settings import BASE_DIR, SNAPSHOTS_DIR
from src.dashboard import VideoProcessor
from src.database import FaceDatabase
from src.detection_logger import DetectionLogger

app = Flask(__name__)

processor = VideoProcessor()
db = FaceDatabase()
logger = DetectionLogger()


@app.route("/")
def index():
    stats = logger.get_stats()
    stats["known_faces"] = db.get_known_face_count()

    video = {
        "faces": list(processor.faces)[-6:],
        "objects": list(processor.objects),
        "on": processor.email_alert.enabled
    }

    return render_template(
        "index.html",
        active="home",
        stats=stats,
        video=video
    )


@app.route("/video_feed")
def video_feed():
    def generate():
        while True:
            jpeg = processor.get_frame_jpeg()
            if jpeg:
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n")
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/alerts")
def alerts():
    rows = db.get_detection_history(limit=100)
    return render_template("alerts.html", active="alerts", alerts=rows)


@app.route("/known_faces")
def known_faces():
    faces = db.get_all_known_faces()
    return render_template("known_faces.html", active="faces", faces=faces)


@app.route("/snapshot/<int:face_id>")
def snapshot(face_id):
    for face in db.get_all_known_faces():
        if face["id"] == face_id and face["image_path"] and os.path.exists(face["image_path"]):
            return send_file(face["image_path"], mimetype="image/jpeg")
    return "", 404


@app.route("/api/stats")
def api_stats():
    stats = logger.get_stats()
    stats["known_faces"] = db.get_known_face_count()
    return jsonify(stats)


@app.route("/api/streaming_status")
def api_status():
    return jsonify({
        "running": processor.running,
        "email_alerts": processor.email_alert.enabled,
        "siren_alerts": processor.siren is not None,
        "error": processor.error
    })


if __name__ == "__main__":
    processor.start()
    try:
        app.run(host="0.0.0.0", port=5000, debug=False, threaded=True, use_reloader=False)
    finally:
        processor.stop()