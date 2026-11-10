from fpdf import FPDF
import os
from datetime import datetime


class ProjectPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 8, 'Smart Camera & Video Surveillance System', 0, 1, 'C')
        self.cell(0, 6, '60% Progress Report', 0, 1, 'C')
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_fill_color(41, 128, 185)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f'  {title}', 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(41, 128, 185)
        self.cell(0, 8, title, 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def code_block(self, code):
        self.set_font('Courier', '', 8)
        self.set_fill_color(240, 240, 240)
        for line in code.strip().split('\n'):
            self.cell(0, 5, f'  {line}', 0, 1, 'L', True)
        self.ln(3)

    def bullet_point(self, text):
        self.set_font('Helvetica', '', 10)
        self.cell(8, 6, '')
        self.cell(5, 6, chr(149))
        self.multi_cell(0, 6, text)
        self.ln(1)

    def table_header(self, headers, widths):
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(41, 128, 185)
        self.set_text_color(255, 255, 255)
        for i, header in enumerate(headers):
            self.cell(widths[i], 8, header, 1, 0, 'C', True)
        self.ln()
        self.set_text_color(0, 0, 0)

    def table_row(self, data, widths):
        self.set_font('Helvetica', '', 8)
        for i, cell in enumerate(data):
            self.cell(widths[i], 7, cell, 1, 0, 'L')
        self.ln()


def generate_pdf():
    pdf = ProjectPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Title Page
    pdf.add_page()
    pdf.ln(35)
    pdf.set_font('Helvetica', 'B', 24)
    pdf.cell(0, 15, 'Smart Camera &', 0, 1, 'C')
    pdf.cell(0, 15, 'Video Surveillance System', 0, 1, 'C')
    pdf.ln(8)
    pdf.set_font('Helvetica', '', 14)
    pdf.cell(0, 10, 'A Deep Learning based Criminal', 0, 1, 'C')
    pdf.cell(0, 10, 'Recognition and Tracking System', 0, 1, 'C')
    pdf.ln(12)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, '60% Progress Report', 0, 1, 'C')
    pdf.ln(8)
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 8, f'Date: {datetime.now().strftime("%d %B %Y")}', 0, 1, 'C')
    pdf.cell(0, 8, 'Phase: Setup + Detection + Recognition + Alerts + Logging', 0, 1, 'C')
    pdf.cell(0, 8, 'Status: 60% Complete', 0, 1, 'C')
    pdf.ln(25)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, 'Final Year B.Tech (CSE) Major Project', 0, 1, 'C')

    # Table of Contents
    pdf.add_page()
    pdf.chapter_title('Table of Contents')
    toc = [
        ('1.', 'Project Overview (60% Complete)'),
        ('2.', 'System Architecture'),
        ('3.', 'Technologies & Libraries Used'),
        ('4.', 'Project Folder Structure'),
        ('5.', 'Module 1: Face Detection (face_detector.py)'),
        ('6.', 'Module 2: Face Recognition (face_recognizer.py)'),
        ('7.', 'Module 3: Database Management (database.py)'),
        ('8.', 'Module 4: Email Alert System (email_alert.py)'),
        ('9.', 'Module 5: Detection Logger (detection_logger.py)'),
        ('10.', 'Module 6: Main Surveillance (surveillance.py)'),
        ('11.', 'Module 7: Face Registration (register_faces.py)'),
        ('12.', 'How to Run the Complete System'),
        ('13.', 'How Face Recognition Works (CNN + Embeddings)'),
        ('14.', 'Testing Results'),
        ('15.', 'Progress Summary & Remaining Work'),
    ]
    for num, item in toc:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(10, 7, num)
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 7, item, 0, 1)

    # Page 3 - Overview
    pdf.add_page()
    pdf.chapter_title('1. Project Overview (60% Complete)')
    pdf.body_text(
        'This project builds a Smart Surveillance System that makes CCTV cameras intelligent. '
        'Instead of just recording footage, the camera actively watches the video feed, detects faces, '
        'recognizes known individuals, and sends instant email alerts when a match is found.'
    )
    pdf.body_text(
        'At 60% completion, the system has the following working components:'
    )
    pdf.bullet_point('Real-time face detection from webcam using OpenCV Haar Cascade')
    pdf.bullet_point('Face recognition using dlib + face_recognition library (128-dim embeddings)')
    pdf.bullet_point('SQLite database for storing face encodings and detection logs')
    pdf.bullet_point('Automated email alert system with snapshot attachment')
    pdf.bullet_point('CSV-based detection logging with statistics')
    pdf.bullet_point('Interactive face registration system (add new faces to database)')
    pdf.bullet_point('Main integrated surveillance system with all features wired together')

    # Progress Bar
    pdf.ln(5)
    pdf.section_title('Progress Breakdown')
    widths = [80, 40, 70]
    pdf.table_header(['Component', 'Status', 'Completion'], widths)
    pdf.table_row(['Face Detection (Haar Cascade)', 'DONE', '100%'], widths)
    pdf.table_row(['Face Recognition (CNN Embeddings)', 'DONE', '100%'], widths)
    pdf.table_row(['Database (SQLite)', 'DONE', '100%'], widths)
    pdf.table_row(['Email Alert System', 'DONE', '100%'], widths)
    pdf.table_row(['Detection Logging', 'DONE', '100%'], widths)
    pdf.table_row(['Face Registration UI', 'DONE', '100%'], widths)
    pdf.table_row(['Main Integration', 'DONE', '100%'], widths)
    pdf.table_row(['Flask Web Dashboard', 'PENDING', '0%'], widths)
    pdf.table_row(['Multi-camera Support', 'PENDING', '0%'], widths)
    pdf.table_row(['Behavior Analysis', 'PENDING', '0%'], widths)
    pdf.table_row(['Testing & Documentation', 'PENDING', '0%'], widths)

    # Page 4 - Architecture
    pdf.add_page()
    pdf.chapter_title('2. System Architecture')
    pdf.body_text(
        'The system follows a modular pipeline architecture. Each component is a separate Python '
        'module that can be used independently or combined into the main surveillance system.'
    )
    pdf.code_block(
        'CAMERA FEED\n'
        '    |\n'
        '    v\n'
        'FRAME CAPTURE (OpenCV)\n'
        '    |\n'
        '    v\n'
        'FACE DETECTION (Haar Cascade)\n'
        '    |\n'
        '    v\n'
        'FACE ENCODING (dlib/face_recognition)\n'
        '    |--- 128-dimensional vector\n'
        '    |\n'
        '    v\n'
        'COMPARE WITH DATABASE (SQLite)\n'
        '    |--- Distance < 0.6 = MATCH\n'
        '    |--- Distance >= 0.6 = UNKNOWN\n'
        '    |\n'
        '    +--> MATCH FOUND\n'
        '    |      |-- Save snapshot\n'
        '    |      |-- Log detection\n'
        '    |      |-- Send email alert\n'
        '    |\n'
        '    +--> NO MATCH\n'
        '           |-- Log as unknown\n'
        '           |-- Continue monitoring'
    )

    # Page 5 - Technologies
    pdf.add_page()
    pdf.chapter_title('3. Technologies & Libraries Used')
    widths = [45, 50, 95]
    pdf.table_header(['Technology', 'Version', 'Role in Project'], widths)
    pdf.table_row(['Python', '3.8.10', 'Main programming language'], widths)
    pdf.table_row(['OpenCV', '4.8.1', 'Video capture, face detection, image processing'], widths)
    pdf.table_row(['dlib', '20.0.1', 'Face encoding, facial landmark detection'], widths)
    pdf.table_row(['face_recognition', 'Latest', 'High-level face recognition API'], widths)
    pdf.table_row(['NumPy', '1.24.4', 'Array operations, distance calculations'], widths)
    pdf.table_row(['SQLite', 'Built-in', 'Face database and detection logs'], widths)
    pdf.table_row(['smtplib', 'Built-in', 'Email alert via SMTP protocol'], widths)
    pdf.table_row(['Haar Cascade', 'XML', 'Pre-trained face/eye detection model'], widths)

    pdf.ln(5)
    pdf.section_title('How face_recognition Works Under the Hood')
    pdf.body_text(
        'The face_recognition library uses dlib\'s deep learning model. It works in two steps:'
    )
    pdf.body_text(
        'Step 1 - Face Detection: Uses HOG (Histogram of Oriented Gradients) or CNN to '
        'locate faces in the image. Returns the bounding box coordinates.'
    )
    pdf.body_text(
        'Step 2 - Face Encoding: Takes the detected face and passes it through a deep neural '
        'network (ResNet trained on ~3 million faces). Outputs a 128-dimensional vector '
        '(embedding) that uniquely represents that face. Similar faces have similar vectors.'
    )

    # Page 6 - Folder Structure
    pdf.add_page()
    pdf.chapter_title('4. Project Folder Structure')
    pdf.code_block(
        'major_project/\n'
        '|\n'
        '|-- config/\n'
        '|   |-- settings.py              # All configuration constants\n'
        '|\n'
        '|-- src/\n'
        '|   |-- face_detector.py         # Haar Cascade face detection\n'
        '|   |-- face_recognizer.py       # CNN-based face recognition\n'
        '|   |-- database.py              # SQLite database operations\n'
        '|   |-- email_alert.py           # SMTP email alerts\n'
        '|   |-- detection_logger.py      # CSV logging system\n'
        '|   |-- surveillance.py          # Main integrated system\n'
        '|   |-- register_faces.py        # Add faces to database\n'
        '|   |-- webcam_capture.py        # Week 1 webcam detection\n'
        '|   |-- image_face_detection.py  # Week 1 image detection\n'
        '|   |-- dataset_collector.py     # Week 1 dataset collection\n'
        '|   |-- test_recognition.py      # Recognition test utility\n'
        '|\n'
        '|-- models/\n'
        '|   |-- haarcascade_frontalface_default.xml\n'
        '|   |-- haarcascade_eye.xml\n'
        '|\n'
        '|-- known_faces/                 # Known face images\n'
        '|-- snapshots/                   # Detection snapshots\n'
        '|-- dataset/                     # Collected face datasets\n'
        '|-- logs/\n'
        '|   |-- faces.db                 # SQLite database\n'
        '|   |-- detection_log.csv        # CSV detection log\n'
        '|-- pdf/                         # Documentation'
    )

    # Page 7 - Module 1
    pdf.add_page()
    pdf.chapter_title('5. Module 1: face_detector.py (Week 1)')
    pdf.section_title('Purpose')
    pdf.body_text(
        'Handles basic face detection using OpenCV\'s Haar Cascade classifier. '
        'Detects faces and eyes in images, webcam feed, or video files.'
    )
    pdf.section_title('Class: FaceDetector')
    pdf.bullet_point('__init__(): Loads Haar Cascade XML files for face and eye detection')
    pdf.bullet_point('detect_faces(frame): Detects all faces in a frame, returns list of results')
    pdf.bullet_point('draw_detections(frame, detections): Draws green bounding boxes on frame')
    pdf.bullet_point('save_snapshot(frame, detection): Saves cropped face image to snapshots/')

    pdf.section_title('How Haar Cascade Detection Works')
    pdf.body_text(
        '1. Convert frame to grayscale\n'
        '2. Scale image at multiple sizes (scaleFactor=1.3)\n'
        '3. Slide a window across the image\n'
        '4. Check each window using pre-trained Haar features\n'
        '5. If enough features match, classify as face\n'
        '6. Merge overlapping detections (minNeighbors=5)'
    )

    # Page 8 - Module 2
    pdf.add_page()
    pdf.chapter_title('6. Module 2: face_recognizer.py')
    pdf.section_title('Purpose')
    pdf.body_text(
        'The core recognition module. Converts detected faces into 128-dimensional '
        'numerical vectors (embeddings) and compares them against the database to identify people.'
    )
    pdf.section_title('Class: FaceRecognizer')
    pdf.bullet_point('load_known_faces(): Loads all known face encodings from SQLite database')
    pdf.bullet_point('add_new_face(name, image_path): Encodes a face from image and stores in DB')
    pdf.bullet_point('add_face_from_frame(name, frame, location): Adds face from live camera')
    pdf.bullet_point('recognize_faces(frame): Main function - detects and recognizes all faces')
    pdf.bullet_point('save_recognition_snapshot(): Saves snapshot and logs to database')
    pdf.bullet_point('draw_results(frame, results): Draws red boxes for matches, green for unknown')

    pdf.section_title('How Recognition Works')
    pdf.code_block(
        '1. Resize frame to 25% (faster processing)\n'
        '2. Convert BGR to RGB (face_recognition expects RGB)\n'
        '3. Detect face locations using HOG detector\n'
        '4. Generate 128-dim encoding for each face\n'
        '5. Calculate Euclidean distance to all known faces\n'
        '6. Find smallest distance (best match)\n'
        '7. If distance < 0.6 = MATCH, else = UNKNOWN\n'
        '8. Scale coordinates back to original size (x4)'
    )

    # Page 9 - Module 3
    pdf.add_page()
    pdf.chapter_title('7. Module 3: database.py')
    pdf.section_title('Purpose')
    pdf.body_text(
        'Manages the SQLite database that stores known face encodings and detection logs. '
        'SQLite is used because it requires no separate server - the database is a single file.'
    )
    pdf.section_title('Class: FaceDatabase')
    pdf.bullet_point('create_tables(): Creates known_faces and detections tables')
    pdf.bullet_point('add_known_face(name, encoding): Stores a face encoding as binary blob')
    pdf.bullet_point('get_all_known_faces(): Returns all stored face encodings')
    pdf.bullet_point('log_detection(name, confidence, camera_id, path, is_match): Logs each detection')
    pdf.bullet_point('get_detection_history(limit): Returns recent detections')
    pdf.bullet_point('get_known_face_count(): Returns total known faces')
    pdf.bullet_point('delete_known_face(face_id): Removes a face from database')

    pdf.section_title('Database Schema')
    pdf.code_block(
        'TABLE known_faces:\n'
        '  id          INTEGER PRIMARY KEY\n'
        '  name        TEXT NOT NULL\n'
        '  encoding    BLOB (128-dim float64 vector)\n'
        '  image_path  TEXT\n'
        '  added_date  TEXT\n'
        '\n'
        'TABLE detections:\n'
        '  id              INTEGER PRIMARY KEY\n'
        '  name            TEXT\n'
        '  confidence      REAL\n'
        '  camera_id       TEXT\n'
        '  snapshot_path   TEXT\n'
        '  timestamp       TEXT\n'
        '  is_match        INTEGER (0 or 1)'
    )

    # Page 10 - Module 4
    pdf.add_page()
    pdf.chapter_title('8. Module 4: email_alert.py')
    pdf.section_title('Purpose')
    pdf.body_text(
        'Sends automated email alerts with snapshot attachments when a known person '
        '(criminal/suspect) is detected by the system. Uses Python\'s smtplib with SMTP.'
    )
    pdf.section_title('Class: EmailAlert')
    pdf.bullet_point('send_alert(name, confidence, camera_id, snapshot_path, timestamp)')
    pdf.bullet_point('test_connection(): Tests SMTP login before deployment')

    pdf.section_title('How Email Alert Works')
    pdf.bullet_point('Step 1: System detects a known face (match found)')
    pdf.bullet_point('Step 2: Snapshot is saved to snapshots/ folder')
    pdf.bullet_point('Step 3: Email is composed with alert details')
    pdf.bullet_point('Step 4: Snapshot is attached to the email')
    pdf.bullet_point('Step 5: Email is sent via SMTP (Gmail)')
    pdf.bullet_point('Step 6: Alert is logged to database')

    pdf.section_title('Email Configuration')
    pdf.body_text(
        'To enable email alerts, set environment variables before running:\n'
        '  export SENDER_EMAIL="your_email@gmail.com"\n'
        '  export SENDER_PASSWORD="your_app_password"\n\n'
        'Note: For Gmail, you need to generate an "App Password" from Google Account settings, '
        'not your regular password. This is required for SMTP access.'
    )

    # Page 11 - Module 5
    pdf.add_page()
    pdf.chapter_title('9. Module 5: detection_logger.py')
    pdf.section_title('Purpose')
    pdf.body_text(
        'Logs every detection (match or unknown) to a CSV file for later review and analysis. '
        'Provides statistics and export functionality.'
    )
    pdf.section_title('Class: DetectionLogger')
    pdf.bullet_point('log(name, confidence, camera_id, snapshot_path, is_match): Write to CSV')
    pdf.bullet_point('get_logs(limit): Read recent log entries')
    pdf.bullet_point('get_stats(): Get total, matches, and unknown counts')
    pdf.bullet_point('export_report(filepath): Export logs to a new CSV file')

    pdf.section_title('CSV Log Format')
    pdf.code_block(
        'Timestamp,Name,Confidence,Camera_ID,Is_Match,Snapshot_Path\n'
        '2026-08-19 14:30:22,John,0.92,CAM_01,1,snapshots/MATCH_John_20260819.jpg\n'
        '2026-08-19 14:30:25,Unknown,0.00,CAM_01,0,\n'
        '2026-08-19 14:30:28,Mary,0.87,CAM_01,1,snapshots/MATCH_Mary_20260819.jpg'
    )

    # Page 12 - Module 6
    pdf.add_page()
    pdf.chapter_title('10. Module 6: surveillance.py (Main System)')
    pdf.section_title('Purpose')
    pdf.body_text(
        'The main integration script that wires all modules together into a single, '
        'working surveillance system. This is what you run to use the full system.'
    )
    pdf.section_title('Class: SurveillanceSystem')
    pdf.bullet_point('run(): Main loop - captures video, recognizes faces, sends alerts')
    pdf.bullet_point('add_face_interactive(): Add a new face to the database during runtime')
    pdf.bullet_point('show_logs(): Display detection log statistics')

    pdf.section_title('System Flow')
    pdf.code_block(
        '1. Initialize FaceRecognizer, EmailAlert, DetectionLogger\n'
        '2. Open webcam (camera index 0)\n'
        '3. Display system info (known faces, email status)\n'
        '4. LOOP:\n'
        '   a. Read frame from webcam\n'
        '   b. Detect and recognize faces\n'
        '   c. Draw bounding boxes (red=match, green=unknown)\n'
        '   d. If match found AND new detection:\n'
        '      - Save snapshot\n'
        '      - Send email alert\n'
        '      - Log to database\n'
        '   e. Display frame with info overlay\n'
        '   f. Handle keyboard input (q/s/a/l/r)\n'
        '5. On quit: Display session summary'
    )

    pdf.section_title('Keyboard Controls')
    widths = [30, 160]
    pdf.table_header(['Key', 'Action'], widths)
    pdf.table_row(['q', 'Quit the surveillance system'], widths)
    pdf.table_row(['s', 'Save snapshot of current detections'], widths)
    pdf.table_row(['a', 'Add a new face to the database (interactive)'], widths)
    pdf.table_row(['l', 'Show detection log statistics'], widths)
    pdf.table_row(['r', 'Refresh known faces from database'], widths)

    # Page 13 - Module 7
    pdf.add_page()
    pdf.chapter_title('11. Module 7: register_faces.py')
    pdf.section_title('Purpose')
    pdf.body_text(
        'Interactive tool to register known faces into the database. Supports registration '
        'from individual image files or entire dataset folders.'
    )
    pdf.section_title('Options')
    pdf.bullet_point('1. Register from image file - Provide name and image path')
    pdf.bullet_point('2. Register from dataset folder - Auto-register all images in a person\'s folder')
    pdf.bullet_point('3. View registered faces - List all faces in the database')
    pdf.bullet_point('4. Delete a face - Remove a face by ID')

    # Page 14 - How to Run
    pdf.add_page()
    pdf.chapter_title('12. How to Run the Complete System')

    pdf.section_title('Step 1: Register Known Faces First')
    pdf.body_text('Before running the surveillance system, register the people you want to track:')
    pdf.code_block(
        'cd ~/Desktop/Desktop/major_project\n\n'
        '# Option A: Register from an image file\n'
        'python3 -m src.register_faces\n'
        '# Select option 1, enter name, enter image path\n\n'
        '# Option B: Register from dataset folder\n'
        '# First collect dataset:\n'
        'python3 -m src.dataset_collector john 50\n'
        '# Then register:\n'
        'python3 -m src.register_faces\n'
        '# Select option 2, choose john'
    )

    pdf.section_title('Step 2: Run the Surveillance System')
    pdf.code_block(
        'python3 -m src.surveillance\n\n'
        '# The system will:\n'
        '# - Open webcam\n'
        '# - Show green boxes around unknown faces\n'
        '# - Show red boxes around known/matched faces\n'
        '# - Send email if a match is found\n'
        '# - Log all detections'
    )

    pdf.section_title('Step 3: Enable Email Alerts (Optional)')
    pdf.code_block(
        'export SENDER_EMAIL="your_email@gmail.com"\n'
        'export SENDER_PASSWORD="your_app_password"\n'
        'python3 -m src.surveillance'
    )

    pdf.section_title('Step 4: Test Recognition on an Image')
    pdf.code_block(
        'python3 -m src.test_recognition path/to/photo.jpg'
    )

    # Page 15 - CNN Explained
    pdf.add_page()
    pdf.chapter_title('13. How Face Recognition Works (CNN + Embeddings)')

    pdf.section_title('What is a CNN?')
    pdf.body_text(
        'A Convolutional Neural Network (CNN) is a type of deep learning model specifically '
        'designed for processing images. It learns to recognize patterns like edges, textures, '
        'and shapes by passing filters (kernels) over the image.'
    )

    pdf.section_title('What are Face Embeddings?')
    pdf.body_text(
        'A face embedding is a 128-dimensional numerical vector that represents a face. '
        'Think of it as a "face fingerprint" - a unique set of 128 numbers that describes '
        'the face. Similar faces produce similar vectors.'
    )

    pdf.section_title('How Comparison Works')
    pdf.code_block(
        'Person A embedding: [0.12, -0.34, 0.56, ...] (128 numbers)\n'
        'Person B embedding: [0.11, -0.33, 0.55, ...] (128 numbers)\n\n'
        'Euclidean Distance = sqrt(sum((A[i] - B[i])^2))\n\n'
        'Distance < 0.6  --> SAME PERSON (match)\n'
        'Distance >= 0.6 --> DIFFERENT PERSON (no match)\n\n'
        'Lower distance = more similar faces\n'
        '0.0 = identical, 0.6+ = completely different'
    )

    pdf.section_title('The dlib ResNet Model')
    pdf.body_text(
        'The model used is a ResNet (Residual Network) trained on 3 million face images. '
        'It learns to map any face to a point in 128-dimensional space where faces of the '
        'same person are close together and faces of different people are far apart. '
        'This is called a "siamese network" training approach.'
    )

    # Page 16 - Testing
    pdf.add_page()
    pdf.chapter_title('14. Testing Results')

    pdf.section_title('Module Tests')
    pdf.body_text('All 8 modules were tested successfully:')
    pdf.bullet_point('[OK] Database module - SQLite create, insert, read, delete')
    pdf.bullet_point('[OK] FaceRecognizer - Load known faces, encode, compare')
    pdf.bullet_point('[OK] EmailAlert - Initialize, check configuration')
    pdf.bullet_point('[OK] DetectionLogger - CSV write, read, statistics')
    pdf.bullet_point('[OK] SurveillanceSystem - Import and initialize')
    pdf.bullet_point('[OK] register_faces - Import and initialize')
    pdf.bullet_point('[OK] FaceDetector (Week 1) - Haar Cascade loaded')
    pdf.bullet_point('[OK] DB insert + read - Test encoding stored and retrieved')

    pdf.section_title('Test Commands')
    pdf.code_block(
        '# Test all modules\n'
        'cd ~/Desktop/Desktop/major_project\n'
        'python3 -c "from src.database import FaceDatabase; print(\"DB OK\")"\n'
        'python3 -c "from src.face_recognizer import FaceRecognizer; print(\"FR OK\")"\n'
        'python3 -c "from src.email_alert import EmailAlert; print(\"EA OK\")"\n'
        'python3 -c "from src.detection_logger import DetectionLogger; print(\"DL OK\")"\n'
        'python3 -c "from src.surveillance import SurveillanceSystem; print(\"SS OK\")"'
    )

    # Page 17 - Summary
    pdf.add_page()
    pdf.chapter_title('15. Progress Summary & Remaining Work')

    pdf.section_title('Completed (60%)')
    pdf.bullet_point('Face detection using OpenCV Haar Cascade')
    pdf.bullet_point('Face recognition using dlib CNN embeddings')
    pdf.bullet_point('SQLite database for face encodings')
    pdf.bullet_point('Automated email alert system')
    pdf.bullet_point('CSV detection logging')
    pdf.bullet_point('Interactive face registration')
    pdf.bullet_point('Main surveillance system integration')
    pdf.bullet_point('Week 1 documentation')

    pdf.section_title('Remaining (40%)')
    pdf.bullet_point('Flask web dashboard for live monitoring')
    pdf.bullet_point('Multi-camera support and tracking')
    pdf.bullet_point('Behavior analysis (loitering, zone intrusion)')
    pdf.bullet_point('YOLO object detection for weapons/objects')
    pdf.bullet_point('Anti-spoofing (block photo/video attacks)')
    pdf.bullet_point('Testing with real-world scenarios')
    pdf.bullet_point('Performance optimization')
    pdf.bullet_point('Final documentation and report')

    pdf.section_title('Next Steps')
    pdf.bullet_point('Week 3: Build Flask dashboard with live video feed')
    pdf.bullet_point('Week 4: Add multi-camera and YOLO detection')
    pdf.bullet_point('Week 5: Add behavior analysis and anti-spoofing')
    pdf.bullet_point('Week 6: Testing, optimization, final report')

    # Save
    output_path = '/home/rguktrkvalley/Desktop/desktop/major_project/pdf/Week1-6_60_Percent_Progress_Report.pdf'
    pdf.output(output_path)
    print(f'PDF saved to: {output_path}')
    print(f'File size: {os.path.getsize(output_path)} bytes')
    print(f'Pages: {pdf.page_no()}')


if __name__ == '__main__':
    generate_pdf()
