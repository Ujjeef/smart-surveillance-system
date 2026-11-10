from fpdf import FPDF
import os
from datetime import datetime


class ProjectPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 8, 'Smart Camera & Video Surveillance System', 0, 1, 'C')
        self.cell(0, 6, 'Object Detection (YOLO) & Web Dashboard', 0, 1, 'C')
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

    # Title page
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font('Helvetica', 'B', 24)
    pdf.cell(0, 15, 'Smart Camera &', 0, 1, 'C')
    pdf.cell(0, 15, 'Video Surveillance System', 0, 1, 'C')
    pdf.ln(8)
    pdf.set_font('Helvetica', '', 14)
    pdf.cell(0, 10, 'New Features Documentation', 0, 1, 'C')
    pdf.ln(8)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Object Detection (YOLO) + Web Dashboard', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 8, f'Date: {datetime.now().strftime("%d %B %Y")}', 0, 1, 'C')
    pdf.cell(0, 8, 'Phase: Feature Expansion (80% Complete)', 0, 1, 'C')
    pdf.cell(0, 8, 'Status: Implemented & Tested', 0, 1, 'C')
    pdf.ln(25)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, 'Final Year B.Tech (CSE) Major Project', 0, 1, 'C')

    # TOC
    pdf.add_page()
    pdf.chapter_title('Table of Contents')
    toc = [
        ('1.', 'Introduction - What Was Added'),
        ('2.', 'What is YOLO Object Detection?'),
        ('3.', 'Object Detector Module (object_detector.py)'),
        ('4.', 'Web Dashboard - How It Works'),
        ('5.', 'Dashboard Video Processor (dashboard.py)'),
        ('6.', 'Flask Web App (app.py)'),
        ('7.', 'HTML Templates (base, index, alerts, known_faces)'),
        ('8.', 'How All Modules Work Together'),
        ('9.', 'How to Run the New Features'),
        ('10.', 'What You See on Screen'),
        ('11.', 'Files in This Update'),
        ('12.', 'Troubleshooting'),
    ]
    for num, item in toc:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(10, 7, num)
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 7, item, 0, 1)

    # Section 1
    pdf.add_page()
    pdf.chapter_title('1. Introduction - What Was Added')

    pdf.body_text(
        'Two major features were added on top of the existing 60% surveillance system:'
    )
    pdf.body_text(
        'FEATURE A - OBJECT DETECTION WITH YOLO: The camera can now detect not just faces, '
        'but also objects (people, bags, cell phones, suitcases, etc.) in the frame. '
        'Suspicious objects (backpack, handbag, suitcase, cell phone) are highlighted '
        'in red with a warning status.'
    )
    pdf.body_text(
        'FEATURE B - WEB DASHBOARD: The system now runs as a web application. You open '
        'a browser, see the live camera feed with all detections drawn on it in real-time, '
        'view detection history, registered faces, and statistics - all from any device '
        'connected to the same network.'
    )

    # Section 2 - YOLO explanation
    pdf.add_page()
    pdf.chapter_title('2. What is YOLO Object Detection?')
    pdf.body_text(
        'YOLO stands for "You Only Look Once". It is a famous deep learning algorithm '
        'for detecting objects in images. Unlike older methods that scanned an image '
        'piece-by-piece, YOLO looks at the whole image ONCE (in a single pass) and '
        'directly predicts: what objects are there, where they are, and how confident it is.'
    )
    pdf.section_title('How YOLO Works (Simple Explanation)')
    pdf.body_text(
        '1. The image is divided into a grid (e.g., 13 x 13 cells).\n'
        '2. Each cell predicts a few bounding boxes and a confidence score.\n'
        '3. Each box gets a class label from 80 known classes (person, car, dog, backpack...).\n'
        '4. NMS (Non-Maximum Suppression) removes duplicate boxes around the same object.\n'
        '5. Final output: list of (label, confidence, box) for each object found.'
    )
    pdf.section_title('YOLOv4-tiny - The Model We Use')
    pdf.body_text(
        'We use a lightweight version called YOLOv4-tiny. It is small (~24MB) and fast, '
        'so it can run in real-time on a normal laptop CPU without a graphics card. '
        'It still knows all 80 common object classes.'
    )
    pdf.section_title('How We Run It (OpenCV DNN)')
    pdf.body_text(
        'We do NOT run YOLO directly in Python. Instead, OpenCV has a module called '
        '"dnn" (Deep Neural Network) that can load YOLO model files and run them. '
        'This avoids installing heavy deep-learning frameworks.'
    )
    widths = [50, 140]
    pdf.table_header(['File', 'Purpose'], widths)
    pdf.table_row(['yolov4-tiny.cfg', 'Network architecture (how many layers, what sizes)'], widths)
    pdf.table_row(['yolov4-tiny.weights', 'The trained weights (the learned knowledge)'], widths)
    pdf.table_row(['coco.names', 'List of 80 class names that the model knows'], widths)

    # Section 3 - object_detector.py
    pdf.add_page()
    pdf.chapter_title('3. Object Detector Module (src/object_detector.py)')

    pdf.section_title('Purpose')
    pdf.body_text(
        'This module loads the YOLO model and provides reusable functions to detect '
        'and draw objects on any image or video frame.'
    )

    pdf.section_title('Class: ObjectDetector')
    pdf.body_text('It has 6 methods. Here is what each one does:')

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, '__init__(self)', 0, 1)
    pdf.body_text(
        'Constructor. Calls three helper methods to load the network, load class names, '
        'and compute the output layer names. Stored as self.net, self.classes, self.output_layers.'
    )

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, '_load_network(self)', 0, 1)
    pdf.body_text(
        'Checks that the .cfg and .weights files exist. Then calls '
        'cv2.dnn.readNetFromDarknet() to create the network object. Sets backend to OpenCV '
        'and target to CPU so it works on any laptop.'
    )

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, '_load_classes(self)', 0, 1)
    pdf.body_text(
        'Reads coco.names line by line and stores the 80 class names in a list.'
    )

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, '_get_boxes(self, outputs, width, height)', 0, 1)
    pdf.body_text(
        'This is the "decoder". YOLO gives raw numbers; this method translates them into '
        'boxes. For each detection it picks the class with the highest score, filters out '
        'low-confidence ones (below YOLO_CONFIDENCE=0.4), converts center-point coordinates '
        'into x,y,width,height, and finally runs Non-Maximum-Suppression (NMSBoxes) to '
        'remove overlapping boxes for the same object.'
    )

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'detect_objects(self, frame)', 0, 1)
    pdf.body_text(
        'The main function. Converts the frame into a "blob" (a standardized numerical '
        'format the model expects: resized to 416x416, scaled to 0-1). Feeds it to the '
        'network with setInput(), runs forward(), decodes with _get_boxes(), and returns '
        'a list of dictionaries: {label, confidence, box, is_suspicious}.'
    )

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'draw_objects(self, frame, detections)', 0, 1)
    pdf.body_text(
        'Draws a colored rectangle + label for each object. Suspicious objects are RED, '
        'normal objects are BLUE. Returns the annotated frame.'
    )

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'count_suspicious(self, detections)', 0, 1)
    pdf.body_text('Counts how many suspicious objects were found in the current frame.')

    pdf.section_title('Important Settings (config/settings.py)')
    pdf.code_block(
        'YOLO_CFG         = models/yolov4-tiny.cfg\n'
        'YOLO_WEIGHTS     = models/yolov4-tiny.weights\n'
        'YOLO_NAMES       = models/coco.names\n'
        'YOLO_CONFIDENCE  = 0.4   # min confidence to accept a detection\n'
        'YOLO_THRESHOLD   = 0.4   # NMS overlap threshold\n'
        'SUSPICIOUS_OBJECTS = ["backpack", "handbag", "suitcase", "cell phone", "knife", "scissors"]'
    )

    # Section 4 - Dashboard overview
    pdf.add_page()
    pdf.chapter_title('4. Web Dashboard - How It Works')

    pdf.body_text(
        'The dashboard is a Flask web application. Flask is a small Python web framework '
        'that turns Python functions into web pages. The dashboard shows a LIVE camera '
        'feed in the browser with detection boxes drawn on every frame.'
    )

    pdf.section_title('The Big Challenge: Live Video in a Browser')
    pdf.body_text(
        'A browser cannot directly use a webcam in Python. So we use a technique called '
        'MJPEG streaming (Motion JPEG):'
    )
    pdf.bullet_point('A background thread captures webcam frames continuously')
    pdf.bullet_point('Each frame is processed (face + object detection)')
    pdf.bullet_point('The processed frame is encoded into JPEG image bytes')
    pdf.bullet_point('Flask sends these JPEG images one after another in an endless stream')
    pdf.bullet_point('The browser displays them like a live video (30 small images per second look like video)')

    pdf.section_title('Key: Threading')
    pdf.body_text(
        'The camera loop runs in a separate "thread" (a background worker) so that it runs '
        'continuously while Flask waits for browser requests. Without threading, the camera '
        'would block the web page and vice versa.'
    )

    # Section 5 - dashboard.py
    pdf.add_page()
    pdf.chapter_title('5. Dashboard Video Processor (src/dashboard.py)')

    pdf.section_title('Class: VideoProcessor')
    pdf.body_text(
        'This class runs the whole video pipeline in a background thread. '
        'It has these attributes:'
    )
    pdf.bullet_point('frame - the latest processed frame ready to stream')
    pdf.bullet_point('faces - list of the faces detected in the current frame')
    pdf.bullet_point('objects - list of objects detected in the current frame')
    pdf.bullet_point('running - flag used to stop the thread')
    pdf.bullet_point('thread - the background threading.Thread object')
    pdf.bullet_point('recognizer, object_detector, email_alert, logger - the modules from before')

    pdf.section_title('Methods')

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'start() / stop()', 0, 1)
    pdf.body_text('Starts the background thread and stops it safely.')

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, '_capture_loop(self)', 0, 1)
    pdf.body_text('The main loop running inside the thread. Step by step:')
    pdf.bullet_point('Open the webcam (same as before)')
    pdf.bullet_point('Loop forever while running is True:')
    pdf.bullet_point('  -> read one frame')
    pdf.bullet_point('  -> recognize faces and draw boxes on the frame')
    pdf.bullet_point('  -> every 3rd frame, run object detection (saves CPU)')
    pdf.bullet_point('  -> draw object boxes on the frame')
    pdf.bullet_point('  -> if a known face matched AND cooldown passed AND email enabled: save snapshot, send email, log it')
    pdf.bullet_point('  -> draw an info bar (uptime, counts)')
    pdf.bullet_point('  -> store the finished frame in self.frame')

    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'get_frame_jpeg(self)', 0, 1)
    pdf.body_text(
        'Takes the latest frame, encodes it into JPEG bytes using cv2.imencode(".jpg", frame), '
        'and returns the bytes. Flask uses this to serve the video stream.'
    )

    # Section 6 - app.py
    pdf.add_page()
    pdf.chapter_title('6. Flask Web App (app.py)')

    pdf.body_text(
        'app.py is the entry point. Running it starts the camera thread and the web server. '
        'It defines all the web pages (routes). Here is each route:'
    )

    widths = [35, 60, 95]
    pdf.table_header(['Route', 'Kind', 'What it does'], widths)
    pdf.table_row(['/', 'Page', 'Main dashboard: live feed + stats + current detections'], widths)
    pdf.table_row(['/video_feed', 'Stream', 'Endless JPEG video stream (MJPEG)'], widths)
    pdf.table_row(['/alerts', 'Page', 'Table of all detection history'], widths)
    pdf.table_row(['/known_faces', 'Page', 'List of registered faces with photos'], widths)
    pdf.table_row(['/snapshot/<id>', 'Image', 'Serves the photo of a known face'], widths)
    pdf.table_row(['/api/stats', 'JSON', 'Statistics for programs/APIs'], widths)
    pdf.table_row(['/api/streaming_status', 'JSON', 'Email-on/off and pipeline status'], widths)

    pdf.section_title('Important Code Details')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 6, 'The video feed generator', 0, 1)
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
        'This "generator" loop never ends. It keeps yielding JPEG images. The browser shows '
        'them one after another as a live video. Each yield ends with the marker --frame so '
        'the browser knows where one picture ends and the next begins.'
    )

    pdf.section_title('Server Startup (bottom of app.py)')
    pdf.code_block(
        "if __name__ == '__main__':\n"
        "    processor.start()                          # start camera thread\n"
        "    try:\n"
        "        app.run(host='0.0.0.0', port=5000)     # start web server\n"
        "    finally:\n"
        "        processor.stop()                       # stop camera on exit"
    )
    pdf.body_text(
        'host="0.0.0.0" means ANY device on the same Wi-Fi network can open the dashboard. '
        'port=5000 is the door number. use_reloader=False prevents Flask from restarting '
        'twice (which would open two cameras).'
    )

    # Section 7 - Templates
    pdf.add_page()
    pdf.chapter_title('7. HTML Templates (templates/)')

    pdf.body_text(
        'Flask uses HTML "templates" for pages. They live in the templates/ folder. '
        'They use Jinja2 syntax ({{ variable }}) to fill in data from Python.'
    )

    pdf.section_title('base.html')
    pdf.body_text(
        'The layout shared by all pages. Contains the top navigation bar (Live Feed, Alerts, '
        'Known Faces) and all the CSS styling (colors, tables, badges). Other templates '
        '"extend" this one, so the design stays consistent.'
    )

    pdf.section_title('index.html (Live Feed page)')
    pdf.body_text('Shows:')
    pdf.bullet_point('Five stat boxes: Known Faces, Total Detections, Matches, Unknown, Email status')
    pdf.bullet_point('The live video: <img src="/video_feed"> - the browser loads this URL and streams video')
    pdf.bullet_point('"Currently Detected" card: lists names and objects seen right now with color badges')

    pdf.section_title('alerts.html (Alerts page)')
    pdf.body_text(
        'A table of the last 100 detections from the database: ID, timestamp, name, '
        'confidence, camera, and a MATCH/UNKNOWN badge.'
    )

    pdf.section_title('known_faces.html (Known Faces page)')
    pdf.body_text(
        'A table of everyone registered in the database: ID, name, photo (loaded via '
        '/snapshot/<id>), and the registration date.'
    )

    # Section 8 - Together
    pdf.add_page()
    pdf.chapter_title('8. How All Modules Work Together')

    pdf.code_block(
        'app.py (Flask server + routes)\n'
        '  |\n'
        '  |-- uses --> src/dashboard.py (VideoProcessor thread)\n'
        '  |              |-- uses --> src/face_recognizer.py (faces)\n'
        '  |              |-- uses --> src/object_detector.py (YOLO objects)\n'
        '  |              |-- uses --> src/email_alert.py (emails)\n'
        '  |              |-- uses --> src/detection_logger.py (CSV logs)\n'
        '  |\n'
        '  |-- uses --> src/database.py (SQLite: known faces + detections)\n'
        '  |\n'
        '  +-- renders --> templates/ (HTML pages)\n'
        '  |\n'
        '  +-- streams --> /video_feed (MJPEG)\n'
        '\n'
        'Browser <---> Flask <---> VideoProcessor thread <---> webcam\n'
        '                     |---> YOLO draws boxes\n'
        '                     |---> faces drawn\n'
        '                     |---> email when match'
    )

    # Section 9 - How to run
    pdf.add_page()
    pdf.chapter_title('9. How to Run the New Features')

    pdf.section_title('Run the Dashboard')
    pdf.code_block(
        'cd ~/Desktop/Desktop/major_project\n'
        '/usr/bin/python3 app.py'
    )
    pdf.body_text(
        'Then open your browser and go to:  http://localhost:5000  '
        '(or http://127.0.0.1:5000)'
    )
    pdf.body_text(
        'To open the dashboard from YOUR PHONE (same Wi-Fi): find your computer IP with '
        '`ip addr` or `hostname -I`, then visit http://YOUR_IP:5000'
    )

    pdf.section_title('Run the Old Terminal Version (still works)')
    pdf.code_block(
        '/usr/bin/python3 -m src.surveillance'
    )

    pdf.section_title('Test Object Detection Alone')
    pdf.code_block(
        '/usr/bin/python3 -c "from src.object_detector import ObjectDetector; '
        'print(len(ObjectDetector().classes))"'
    )

    # Section 10 - What you see
    pdf.add_page()
    pdf.chapter_title('10. What You See on Screen')

    pdf.section_title('In the Browser Dashboard')
    pdf.bullet_point('Top-left: camera uptime and counts bar (drawn on the video)')
    pdf.bullet_point('Green box = unknown face')
    pdf.bullet_point('Red box + "MATCH: name" = recognized person')
    pdf.bullet_point('Blue box = normal object (person, chair...)')
    pdf.bullet_point('Red box + yellow badge = SUSPICIOUS object (backpack, bag, phone)')
    pdf.bullet_point('Below the video: badges listing current faces and objects')

    pdf.section_title('Dashboard Pages')
    pdf.bullet_point('/  -> live feed + statistics')
    pdf.bullet_point('/alerts -> full detection history table')
    pdf.bullet_point('/known_faces -> registered people with photos')

    # Section 11 - Files
    pdf.add_page()
    pdf.chapter_title('11. Files in This Update')

    widths = [30, 75, 85]
    pdf.table_header(['Folder', 'File', 'What it is'], widths)
    pdf.table_row(['src/', 'object_detector.py', 'YOLO object detection module (NEW)'], widths)
    pdf.table_row(['src/', 'dashboard.py', 'VideoProcessor background thread (NEW)'], widths)
    pdf.table_row(['root', 'app.py', 'Flask web application (NEW)'], widths)
    pdf.table_row(['templates/', 'base.html', 'Shared page layout (NEW)'], widths)
    pdf.table_row(['templates/', 'index.html', 'Live feed page (NEW)'], widths)
    pdf.table_row(['templates/', 'alerts.html', 'Alerts history page (NEW)'], widths)
    pdf.table_row(['templates/', 'known_faces.html', 'Known faces page (NEW)'], widths)
    pdf.table_row(['models/', 'yolov4-tiny.cfg', 'YOLO config file (NEW)'], widths)
    pdf.table_row(['models/', 'yolov4-tiny.weights', 'YOLO weights ~24MB (NEW)'], widths)
    pdf.table_row(['models/', 'coco.names', '80 class names (NEW)'], widths)
    pdf.table_row(['config/', 'settings.py', 'Added YOLO + dashboard settings'], widths)
    pdf.table_row(['src/', 'database.py', 'Fixed thread-safety (check_same_thread=False + lock)'], widths)

    # Section 12 - Troubleshooting
    pdf.add_page()
    pdf.chapter_title('12. Troubleshooting')

    pdf.section_title('"Address already in use" when running app.py')
    pdf.body_text('Port 5000 is busy (maybe another server). Close it or change the port in app.py.')
    pdf.code_block(
        'pkill -f "app.py"\n'
        '# or change port=5000 to port=5001 in app.py'
    )

    pdf.section_title('YOLO detects nothing')
    pdf.body_text('Make sure an object is actually in view (a person, a bag). Detection confidence must be above 0.4.')
    pdf.body_text('Lower YOLO_CONFIDENCE in settings.py to 0.25 for more detections (but more false positives).')

    pdf.section_title('Dashboard shows black/empty video')
    pdf.body_text('The webcam may be busy. Check no other program uses it, then restart app.py with Ctrl+C and rerun.')

    pdf.section_title('"No module named flask"')
    pdf.body_text('Install it for the correct Python:')
    pdf.code_block('/usr/bin/python3 -m pip install flask')

    pdf.section_title('YOLO files missing')
    pdf.body_text('Put yolov4-tiny.cfg, yolov4-tiny.weights and coco.names inside the models/ folder.')

    # Save
    output_path = '/home/rguktrkvalley/Desktop/desktop/major_project/pdf/ObjectDetection_Dashboard_Documentation.pdf'
    pdf.output(output_path)
    print(f'PDF saved to: {output_path}')
    print(f'File size: {os.path.getsize(output_path)} bytes')
    print(f'Pages: {pdf.page_no()}')


if __name__ == '__main__':
    generate_pdf()