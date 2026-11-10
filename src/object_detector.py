import cv2
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    YOLO_CFG, YOLO_WEIGHTS, YOLO_NAMES,
    YOLO_CONFIDENCE, YOLO_THRESHOLD, SUSPICIOUS_OBJECTS
)


class ObjectDetector:
    def __init__(self):
        self.net = self._load_network()
        self.classes = self._load_classes()
        self.output_layers = self.net.getUnconnectedOutLayersNames()

    def _load_network(self):
        if not os.path.exists(YOLO_CFG) or not os.path.exists(YOLO_WEIGHTS):
            raise IOError(
                "YOLO model files missing. Place yolov4-tiny.cfg and "
                "yolov4-tiny.weights in the models/ folder."
            )
        net = cv2.dnn.readNetFromDarknet(YOLO_CFG, YOLO_WEIGHTS)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        return net

    def _load_classes(self):
        if not os.path.exists(YOLO_NAMES):
            raise IOError("coco.names file not found.")
        with open(YOLO_NAMES, "r") as f:
            return [line.strip() for line in f.readlines()]

    def _get_boxes(self, outputs, width, height):
        boxes, confidences, class_ids = [], [], []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = int(scores.argmax())
                confidence = float(scores[class_id])
                if confidence > YOLO_CONFIDENCE:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(confidence)
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, YOLO_CONFIDENCE, YOLO_THRESHOLD)
        return boxes, confidences, class_ids, indexes

    def detect_objects(self, frame):
        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            frame, 1 / 255.0, (416, 416), swapRB=True, crop=False
        )
        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)

        boxes, confidences, class_ids, indexes = self._get_boxes(outputs, width, height)

        detections = []
        if len(indexes) > 0:
            indexes = indexes.flatten() if hasattr(indexes, "flatten") else indexes
            for i in indexes:
                label = self.classes[class_ids[i]]
                detections.append({
                    "label": label,
                    "confidence": round(confidences[i], 2),
                    "box": tuple(boxes[i]),
                    "is_suspicious": label in SUSPICIOUS_OBJECTS
                })
        return detections

    def draw_objects(self, frame, detections):
        for det in detections:
            x, y, w, h = det["box"]
            if det["is_suspicious"]:
                color = (0, 0, 255)
                label = f"{det['label']} {det['confidence']:.0%}"
            else:
                color = (255, 0, 0)
                label = det["label"]

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.rectangle(frame, (x, y - 25), (x + w, y), color, cv2.FILLED)
            cv2.putText(frame, label, (x + 4, y - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return frame

    def count_suspicious(self, detections):
        return sum(1 for d in detections if d["is_suspicious"])