from fpdf import FPDF
import os
from datetime import datetime


class ProjectPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 8, 'Smart Camera & Video Surveillance System', 0, 1, 'C')
        self.cell(0, 6, 'Object Detection (YOLO) + Web Dashboard + Siren Alert', 0, 1, 'C')
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

    # ---------------- TITLE PAGE ----------------
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font('Helvetica', 'B', 24)
    pdf.cell(0, 15, 'Smart Camera &', 0, 1, 'C')
    pdf.cell(0, 15, 'Video Surveillance System', 0, 1, 'C')
    pdf.ln(8)
    pdf.set_font('Helvetica', '', 14)
    pdf.cell(0, 10, 'Today\'s Features Documentation', 0, 1, 'C')
    pdf.ln(8)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Object Detection (YOLO)', 0, 1, 'C')
    pdf.cell(0, 10, 'Web Dashboard', 0, 1, 'C')
    pdf.cell(0, 10, 'Siren Alert System', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 8, f'Date: {datetime.now().strftime("%d %B %Y")}', 0, 1, 'C')
    pdf.cell(0, 8, 'Phase: Feature Expansion (80% Complete)', 0, 1, 'C')
    pdf.cell(0, 8, 'Status: Implemented & Tested', 0, 1, 'C')
    pdf.ln(25)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, 'Final Year B.Tech (CSE) Major Project', 0, 1, 'C')

    # ---------------- TABLE OF CONTENTS ----------------
    pdf.add_page()
    pdf.chapter_title('Table of Contents')
    toc = [
        ('1.', 'PART A - Object Detection (YOLO)'),
        ('2.', '    2.1  What is YOLO?'),
        ('3.', '    2.2  YOLOv4-tiny + OpenCV DNN'),
        ('4.', '    2.3  object_detector.py - method by method'),
        ('5.', '    2.4  Suspicious object settings'),
        ('6.', 'PART B - Web Dashboard'),
        ('7.', '    5.1  How live video streams to a browser'),
        ('8.', '    5.2  dashboard.py (VideoProcessor)'),
        ('9.', '    5.3  app.py (Flask routes)'),
        ('10.', '    5.4  HTML templates'),
        ('11.', '    5.5  How all modules work together'),
        ('12.', 'PART C - Siren Alert System'),
        ('13.', '    10.1  SirenPlayer class'),
        ('14.', '    10.2  How the siren sound is generated'),
        ('15.', '    10.3  Where the siren is wired in'),
        ('16.', 'How to Run Everything'),
        ('17.', 'Files in This Update'),
        ('18.', 'Troubleshooting'),
    ]
    for num, item in toc:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(10, 7, num)
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 7, item, 0, 1)

    # ================= PART A: OBJECT DETECTION =================
    pdf.add_page()
    pdf.chapter_title('PART A - Object Detection (YOLO)')

    pdf.body_text(
        'FEATURE: The camera can now detect not just faces, but also OBJECTS '
        '(people, bags, cell phones, suitcases, bottles, etc.) in the frame. '
        'Suspicious objects (backpack, handbag, suitcase, cell phone) are highlighted '
        'in RED with a warning, while normal objects are drawn in BLUE.'
    )

    pdf.section_title('A.1  What is YOLO?')
    pdf.body_text(
        'YOLO stands for "You Only Look Once". It is a deep learning algorithm for object '
        'detection. Unlike older methods that scanned an image piece by piece, YOLO looks '
        'at the WHOLE image once (single pass) and directly predicts: what objects are '
        'there, where they are, and how confident it is about each.'
    )
    pdf.body_text(
        'How YOLO works in 5 steps:\n'
        '1. The image is divided into a grid of cells (13 x 13 for tiny).\n'
        '2. Each cell predicts a few bounding boxes and a confidence score.\n'
        '3. Each box is labelled from 80 known classes (person, car, backpack...).\n'
        '4. NMS (Non-Maximum Suppression) removes duplicate boxes on the same object.\n'
        '5. Output: a list of (label, confidence, box) for every object found.'
    )

    pdf.section_title('A.2  YOLOv4-tiny + OpenCV DNN')
    pdf.body_text(
        'We use a lightweight version called YOLOv4-tiny (~24MB, fast on a normal laptop '
        'CPU, no graphics card needed). We do NOT run YOLO directly - we load its model '
        'files through OpenCV\'s "dnn" (Deep Neural Network) module. This avoids installing '
        'a heavy deep-learning framework.'
    )
    widths = [45, 145]
    pdf.table_header(['Model file', 'Purpose'], widths)
    pdf.table_row(['yolov4-tiny.cfg', 'Network architecture (layers and sizes)'], widths)
    pdf.table_row(['yolov4-tiny.weights', 'Trained weights (the learned knowledge) ~24MB'], widths)
    pdf.table_row(['coco.names', 'List of 80 class names the model knows'], widths)

    pdf.section_title('A.3  object_detector.py - method by method')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, '__init__(self)', 0, 1)
    pdf.body_text('Constructor. Loads the network, loads class names, and gets the output layer names.')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, '_load_network(self)', 0, 1)
    pdf.body_text('Checks the .cfg and .weights files exist, then cv2.dnn.readNetFromDarknet() builds the network. Sets backend = OpenCV, target = CPU.')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, '_load_classes(self)', 0, 1)
    pdf.body_text('Reads coco.names line by line into a list of 80 class names.')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, '_get_boxes(self, outputs, width, height)', 0, 1)
    pdf.body_text('The decoder. Translates YOLO raw numbers into boxes: keeps only detections above YOLO_CONFIDENCE (0.4), converts center-points to x,y,w,h, and runs NMSBoxes to remove duplicates.')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'detect_objects(self, frame)', 0, 1)
    pdf.body_text('Main function. Converts the frame into a "blob" (resized 416x416, scaled 0-1), feeds it to the network, runs forward(), decodes, and returns a list of dictionaries: {label, confidence, box, is_suspicious}.')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'draw_objects(self, frame, detections)', 0, 1)
    pdf.body_text('Draws rectangles + labels. Suspicious = RED, normal = BLUE.')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'count_suspicious(self, detections)', 0, 1)
    pdf.body_text('Returns how many suspicious objects are in the current frame.')

    pdf.section_title('A.4  Suspicious object settings (config/settings.py)')
    pdf.code_block(
        'YOLO_CONFIDENCE = 0.4\n'
        'YOLO_THRESHOLD  = 0.4\n'
        'SUSPICIOUS_OBJECTS = ["backpack", "handbag", "suitcase", "cell phone", "knife", "scissors"]'
    )

    # ================= PART B: DASHBOARD =================
    pdf.add_page()
    pdf.chapter_title('PART B - Web Dashboard')

    pdf.body_text(
        'FEATURE: The system now runs as a web application. Open a browser, and you see '
        'the LIVE camera feed with all detection boxes drawn in real time, plus pages for '
        'detection history and registered faces.'
    )

    pdf.section_title('B.1  How live video streams to a browser')
    pdf.body_text(
        'A browser cannot use a webcam directly. We use MJPEG streaming (Motion JPEG):'
    )
    pdf.bullet_point('A background THREAD captures webcam frames continuously')
    pdf.bullet_point('Each frame is processed (face + object detection)')
    pdf.bullet_point('The processed frame is encoded into JPEG image bytes')
    pdf.bullet_point('Flask sends these JPEG images one after another in an endless stream')
    pdf.bullet_point('The browser displays them like a live video')

    pdf.section_title('B.2  dashboard.py (class VideoProcessor)')
    pdf.body_text('Runs the whole video pipeline in a background thread. Key attributes:')
    pdf.bullet_point('frame - the latest processed frame ready to stream')
    pdf.bullet_point('faces / objects - detections from the current frame')
    pdf.bullet_point('thread - the background threading.Thread worker')
    pdf.bullet_point('recognizer, object_detector, email_alert, logger, siren - the modules')

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'start() / stop()', 0, 1)
    pdf.body_text('Starts and safely stops the background thread.')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, '_capture_loop(self)', 0, 1)
    pdf.body_text('The loop inside the thread:')
    pdf.bullet_point('Open the webcam')
    pdf.bullet_point('Loop while running: read frame')
    pdf.bullet_point('  -> recognize faces, draw boxes')
    pdf.bullet_point('  -> every 3rd frame run object detection (saves CPU)')
    pdf.bullet_point('  -> draw object boxes')
    pdf.bullet_point('  -> if a known face matched and cooldown passed: save snapshot, email, log, play siren')
    pdf.bullet_point('  -> store the finished frame in self.frame')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'get_frame_jpeg(self)', 0, 1)
    pdf.body_text('Encodes the latest frame into JPEG bytes for the browser; returns None if no frame yet.')

    pdf.section_title('B.3  app.py (Flask routes)')
    widths = [35, 55, 100]
    pdf.table_header(['Route', 'Kind', 'What it does'], widths)
    pdf.table_row(['/', 'Page', 'Main dashboard: stats + live feed + current detections'], widths)
    pdf.table_row(['/video_feed', 'Stream', 'Endless JPEG video stream (MJPEG)'], widths)
    pdf.table_row(['/alerts', 'Page', 'Table of all detection history'], widths)
    pdf.table_row(['/known_faces', 'Page', 'List of registered faces with photos'], widths)
    pdf.table_row(['/snapshot/<id>', 'Image', 'Serves a known face photo'], widths)
    pdf.table_row(['/api/stats', 'JSON', 'Statistics for programs'], widths)
    pdf.table_row(['/api/streaming_status', 'JSON', 'Email/siren/pipeline status'], widths)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'The MJPEG generator (the heart of live video)', 0, 1)
    pdf.code_block(
        "def generate():\n"
        "    while True:\n"
        "        jpeg = processor.get_frame_jpeg()\n"
        "        if jpeg:\n"
        "            yield (b'--frame\\r\\n'\n"
        "                   b'Content-Type: image/jpeg\\r\\n\\r\\n' + jpeg + b'\\r\\n')\n"
        "return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')"
    )
    pdf.body_text(
        'This generator never ends. Each yield is one JPEG picture separated by a --frame marker. '
        'The browser plays them one after another = live video.'
    )
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'Server startup', 0, 1)
    pdf.code_block(
        "if __name__ == '__main__':\n"
        "    processor.start()                 # start camera thread\n"
        "    try:\n"
        "        app.run(host='0.0.0.0', port=5000, use_reloader=False)\n"
        "    finally:\n"
        "        processor.stop()              # stop camera on exit"
    )
    pdf.body_text('host="0.0.0.0" = any device on your Wi-Fi can open it at http://YOUR_IP:5000. use_reloader=False avoids opening two cameras.')

    pdf.section_title('B.4  HTML templates (templates/)')
    pdf.bullet_point('base.html - shared navbar (Live Feed / Alerts / Known Faces) and all CSS')
    pdf.bullet_point('index.html - stat boxes + <img src="/video_feed"> live video + current detection badges')
    pdf.bullet_point('alerts.html - table of last 100 detections with MATCH/UNKNOWN badges')
    pdf.bullet_point('known_faces.html - table of registered people with photos via /snapshot/<id>')

    pdf.section_title('B.5  How all modules work together')
    pdf.code_block(
        'app.py (Flask) -> src/dashboard.py (VideoProcessor thread)\n'
        '                    |-> src/face_recognizer.py (faces)\n'
        '                    |-> src/object_detector.py (YOLO)\n'
        '                    |-> src/email_alert.py (emails)\n'
        '                    |-> src/siren.py (audio alarm)\n'
        '                    |-> src/detection_logger.py (CSV logs)\n'
        'app.py -> src/database.py (SQLite)\n'
        'app.py -> templates/ (HTML)\n'
        'app.py -> /video_feed (MJPEG stream)\n'
        'Browser <-> Flask <-> VideoProcessor <-> webcam'
    )

    # ================= PART C: SIREN =================
    pdf.add_page()
    pdf.chapter_title('PART C - Siren Alert System')

    pdf.body_text(
        'FEATURE: When a registered (known) person is detected, besides the email and the '
        'snapshot, the system now also plays a POLICE-STYLE SIREN sound as an audio alarm '
        'to grab immediate attention.'
    )

    pdf.section_title('C.1  siren.py (class SirenPlayer)')
    pdf.bullet_point('__init__(): stores the sound path and creates the sound file if missing')
    pdf.bullet_point('_generate_siren_wav(): builds the siren WAV mathematically (numpy + wave)')
    pdf.bullet_point('play(): plays via aplay/paplay (Linux), winsound (Windows), afplay (Mac)')
    pdf.bullet_point('play_async(): plays in a background thread so the camera video never freezes')
    pdf.bullet_point('test(): plays the siren once to check speakers')

    pdf.section_title('C.2  How the siren sound is generated (no internet needed)')
    pdf.code_block(
        't     = time samples for 3 seconds\n'
        'freq  = 500 + 450 * sin(2*pi*1.5*t)   (500..950 Hz, rises+falls)\n'
        'wave  = sin(2*pi * cumsum(freq))       (the sine tone)\n'
        'envelope = fade in/out to avoid clicks\n'
        'save  = 44100 Hz, 16-bit WAV  ->  sounds/siren.wav'
    )

    pdf.section_title('C.3  Where the siren is wired in')
    pdf.code_block(
        '# settings.py\n'
        'SIREN_ENABLED = True\n'
        'SIREN_SOUND_PATH = sounds/siren.wav\n\n'
        '# surveillance.py and dashboard.py\n'
        "from src.siren import SirenPlayer\n"
        "self.siren = SirenPlayer() if SIREN_ENABLED else None\n"
        '...\n'
        'when a face matches:\n'
        '    if self.siren:\n'
        '        self.siren.play_async()'
    )

    pdf.section_title('C.4  Why play_async()?')
    pdf.body_text(
        'A 3-second sound blocks the program for 3 seconds. If we called play() directly, '
        'the live video would freeze. play_async() starts a small background thread that '
        'plays the sound while the camera loop keeps running smoothly.'
    )

    # ================= HOW TO RUN =================
    pdf.add_page()
    pdf.chapter_title('How to Run Everything')

    pdf.section_title('Web Dashboard (recommended for demo)')
    pdf.code_block(
        'cd ~/Desktop/Desktop/major_project\n'
        '/usr/bin/python3 app.py\n'
        '# open browser -> http://localhost:5000\n'
        '# from phone (same Wi-Fi): http://YOUR_IP:5000'
    )

    pdf.section_title('Terminal Surveillance (with siren)')
    pdf.code_block('/usr/bin/python3 -m src.surveillance')

    pdf.section_title('Test the pieces')
    pdf.code_block(
        '/usr/bin/python3 -m src.siren                     # hear the siren\n'
        '/usr/bin/python3 -c "from src.object_detector import ObjectDetector; print(len(ObjectDetector().classes))"'
    )

    # ================= FILES =================
    pdf.add_page()
    pdf.chapter_title('Files in This Update')

    widths = [30, 75, 85]
    pdf.table_header(['Folder', 'File', 'What it is'], widths)
    pdf.table_row(['src/', 'object_detector.py', 'YOLO object detection (NEW)'], widths)
    pdf.table_row(['src/', 'dashboard.py', 'VideoProcessor background thread (NEW)'], widths)
    pdf.table_row(['src/', 'siren.py', 'Siren audio alarm (NEW)'], widths)
    pdf.table_row(['root', 'app.py', 'Flask web application (NEW)'], widths)
    pdf.table_row(['templates/', 'base.html', 'Shared page layout (NEW)'], widths)
    pdf.table_row(['templates/', 'index.html', 'Live feed page (NEW)'], widths)
    pdf.table_row(['templates/', 'alerts.html', 'Alerts history page (NEW)'], widths)
    pdf.table_row(['templates/', 'known_faces.html', 'Known faces page (NEW)'], widths)
    pdf.table_row(['sounds/', 'siren.wav', 'Generated siren sound (NEW)'], widths)
    pdf.table_row(['models/', 'yolov4-tiny.cfg', 'YOLO config (NEW)'], widths)
    pdf.table_row(['models/', 'yolov4-tiny.weights', 'YOLO weights ~24MB (NEW)'], widths)
    pdf.table_row(['models/', 'coco.names', '80 class names (NEW)'], widths)
    pdf.table_row(['config/', 'settings.py', 'Added YOLO + dashboard + siren settings'], widths)
    pdf.table_row(['src/', 'database.py', 'Fixed thread-safety (check_same_thread=False + lock)'], widths)
    pdf.table_row(['src/', 'surveillance.py', 'Added siren on match'], widths)

    # ================= TROUBLESHOOTING =================
    pdf.add_page()
    pdf.chapter_title('Troubleshooting')

    pdf.section_title('"Address already in use" when running app.py')
    pdf.body_text('Port 5000 is busy. Close it or change the port in app.py.')
    pdf.code_block('pkill -f "app.py"   # or change port=5000 to port=5001')

    pdf.section_title('YOLO detects nothing')
    pdf.body_text('Make sure an object is in view. Lower YOLO_CONFIDENCE to 0.25 in settings.py for more detections (but more false positives).')

    pdf.section_title('Dashboard shows black/empty video')
    pdf.body_text('The webcam may be busy. Close other camera apps, then restart app.py.')

    pdf.section_title('No sound from siren')
    pdf.body_text('Check speakers. Verify aplay exists (Linux): `which aplay`. Sound file auto-creates in sounds/siren.wav.')

    pdf.section_title('"No module named flask"')
    pdf.code_block('/usr/bin/python3 -m pip install flask')

    # ================= FULL PIPELINE =================
    pdf.add_page()
    pdf.chapter_title('The Complete Pipeline (Today\'s Full Version)')
    pdf.code_block(
        'WEBCAM\n'
        '   |\n'
        '   v\n'
        'VideoProcessor thread\n'
        '   |-- Haar Cascade face detection\n'
        '   |-- dlib 128-dim face encoding\n'
        '   |-- SQLite distance match\n'
        '   |-- YOLO object detection (every 3rd frame)\n'
        '   |-- draw green/red face boxes + blue/red object boxes\n'
        '   |\n'
        '   +-- MATCH? --> snapshot + email + SIREN + log\n'
        '   |\n'
        '   v\n'
        'self.frame (latest)\n'
        '   |\n'
        '   v\n'
        'Flask /video_feed (MJPEG) -----> Browser live feed\n'
        'Flask /alerts             -----> detection history\n'
        'Flask /known_faces        -----> registered people\n'
        'Flask /api/*              -----> JSON statistics'
    )

    output_path = '/home/rguktrkvalley/Desktop/desktop/major_project/pdf/ObjectDetection_Dashboard_Siren_Complete_Documentation.pdf'
    pdf.output(output_path)
    print(f'PDF saved to: {output_path}')
    print(f'File size: {os.path.getsize(output_path)} bytes')
    print(f'Pages: {pdf.page_no()}')


if __name__ == '__main__':
    generate_pdf()