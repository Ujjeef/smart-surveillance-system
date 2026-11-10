from fpdf import FPDF
import os
from datetime import datetime


class ProjectPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 8, 'Smart Camera & Video Surveillance System', 0, 1, 'C')
        self.cell(0, 6, 'Week 1 Progress Report', 0, 1, 'C')
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(41, 128, 185)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f'  {title}', 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def section_title(self, title):
        self.set_font('Arial', 'B', 11)
        self.set_text_color(41, 128, 185)
        self.cell(0, 8, title, 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def body_text(self, text):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def code_block(self, code):
        self.set_font('Courier', '', 9)
        self.set_fill_color(240, 240, 240)
        lines = code.strip().split('\n')
        for line in lines:
            self.cell(0, 5, f'  {line}', 0, 1, 'L', True)
        self.ln(3)

    def bullet_point(self, text):
        self.set_font('Arial', '', 10)
        self.cell(8, 6, '')
        self.cell(5, 6, chr(149))
        self.multi_cell(0, 6, text)
        self.ln(1)

    def table_header(self, headers, widths):
        self.set_font('Arial', 'B', 9)
        self.set_fill_color(41, 128, 185)
        self.set_text_color(255, 255, 255)
        for i, header in enumerate(headers):
            self.cell(widths[i], 8, header, 1, 0, 'C', True)
        self.ln()
        self.set_text_color(0, 0, 0)

    def table_row(self, data, widths):
        self.set_font('Arial', '', 9)
        self.set_fill_color(255, 255, 255)
        for i, cell in enumerate(data):
            self.cell(widths[i], 7, cell, 1, 0, 'L')
        self.ln()


def generate_pdf():
    pdf = ProjectPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Page 1 - Title Page
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 15, 'Smart Camera &', 0, 1, 'C')
    pdf.cell(0, 15, 'Video Surveillance System', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 14)
    pdf.cell(0, 10, 'A Deep Learning based Criminal', 0, 1, 'C')
    pdf.cell(0, 10, 'Recognition and Tracking System', 0, 1, 'C')
    pdf.ln(15)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Week 1 Progress Report', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, f'Date: {datetime.now().strftime("%d %B %Y")}', 0, 1, 'C')
    pdf.cell(0, 8, 'Phase: Setup & Face Detection', 0, 1, 'C')
    pdf.cell(0, 8, 'Status: Completed', 0, 1, 'C')
    pdf.ln(30)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, 'Final Year B.Tech (CSE) Major Project', 0, 1, 'C')

    # Page 2 - Table of Contents
    pdf.add_page()
    pdf.chapter_title('Table of Contents')
    toc = [
        ('1.', 'Project Overview'),
        ('2.', 'System Requirements'),
        ('3.', 'Installation Steps'),
        ('4.', 'Project Folder Structure'),
        ('5.', 'Haar Cascade - How It Works'),
        ('6.', 'Code Explanation - face_detector.py'),
        ('7.', 'Code Explanation - webcam_capture.py'),
        ('8.', 'Code Explanation - image_face_detection.py'),
        ('9.', 'Code Explanation - dataset_collector.py'),
        ('10.', 'How to Run the Project'),
        ('11.', 'Expected Output'),
        ('12.', 'Week 1 Summary'),
    ]
    for num, item in toc:
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(10, 8, num)
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 8, item, 0, 1)

    # Page 3 - Project Overview
    pdf.add_page()
    pdf.chapter_title('1. Project Overview')
    pdf.body_text(
        'This project builds a Smart Surveillance System that uses Deep Learning and Computer Vision '
        'to make CCTV cameras intelligent. Instead of just recording footage, the camera actively '
        'watches the video feed, detects faces, and can eventually recognize known individuals.'
    )
    pdf.body_text(
        'In Week 1, we have completed the foundation - setting up the development environment, '
        'installing all required libraries, and implementing real-time face detection using OpenCV\'s '
        'Haar Cascade classifier. The system can detect faces from a live webcam feed, image files, '
        'and video files, drawing bounding boxes around each detected face.'
    )

    pdf.section_title('What is Face Detection?')
    pdf.body_text(
        'Face detection is the process of locating human faces in images or video frames. '
        'It answers the question "Is there a face in this image?" and if yes, "Where is it?" '
        'This is different from face recognition, which answers "Whose face is this?" '
        'Face detection is the first step in our surveillance pipeline.'
    )

    # Page 4 - System Requirements
    pdf.add_page()
    pdf.chapter_title('2. System Requirements')

    pdf.section_title('Hardware Requirements')
    pdf.bullet_point('Processor: Intel i3 or above (i5 recommended)')
    pdf.bullet_point('RAM: 4GB minimum (8GB recommended)')
    pdf.bullet_point('Webcam: Any USB webcam (for live detection)')
    pdf.bullet_point('Storage: 500MB free space')

    pdf.section_title('Software Requirements')
    pdf.bullet_point('Operating System: Ubuntu 20.04+ / Windows 10+ / macOS')
    pdf.bullet_point('Python: Version 3.8 or above')
    pdf.bullet_point('OpenCV: Version 4.8.1 (with contrib modules)')
    pdf.bullet_point('NumPy: Version 1.24.4')
    pdf.bullet_point('Haar Cascade XML files (pre-trained models)')

    # Page 5 - Installation Steps
    pdf.add_page()
    pdf.chapter_title('3. Installation Steps')

    pdf.section_title('Step 1: Check Python Installation')
    pdf.body_text('First, verify that Python 3 is installed on your system:')
    pdf.code_block('python3 --version\n# Output: Python 3.8.10')
    pdf.code_block('pip3 --version\n# Output: pip 20.0.2')

    pdf.section_title('Step 2: Create Project Directory')
    pdf.body_text('Create a dedicated folder for the project:')
    pdf.code_block('mkdir -p smart_surveillance/{src,known_faces,snapshots,logs,dataset,models,pdf,config}')

    pdf.section_title('Step 3: Install OpenCV')
    pdf.body_text('Install OpenCV with contrib modules (includes extra face detection algorithms):')
    pdf.code_block('pip3 install opencv-contrib-python==4.8.1.78')
    pdf.body_text(
        'Note: We use opencv-contrib-python instead of opencv-python because the contrib version '
        'includes additional modules. We also use version 4.8.1 because OpenCV 5.0 removed '
        'the CascadeClassifier module which we need.'
    )

    pdf.section_title('Step 4: Install NumPy')
    pdf.code_block('pip3 install numpy')
    pdf.body_text('NumPy is used for array and numerical operations on image data.')

    pdf.section_title('Step 5: Download Haar Cascade Models')
    pdf.body_text('Download the pre-trained XML files used for face and eye detection:')
    pdf.code_block(
        'wget -O models/haarcascade_frontalface_default.xml \\\n'
        '  https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml\n\n'
        'wget -O models/haarcascade_eye.xml \\\n'
        '  https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_eye.xml'
    )

    # Page 6 - Project Structure
    pdf.add_page()
    pdf.chapter_title('4. Project Folder Structure')
    pdf.code_block(
        'major_project/\n'
        '|\n'
        '|-- config/\n'
        '|   |-- settings.py          # All configuration constants\n'
        '|\n'
        '|-- src/\n'
        '|   |-- face_detector.py     # Core face detection class\n'
        '|   |-- webcam_capture.py    # Live webcam detection\n'
        '|   |-- image_face_detection.py  # Image/video detection\n'
        '|   |-- dataset_collector.py # Collect face dataset\n'
        '|\n'
        '|-- models/\n'
        '|   |-- haarcascade_frontalface_default.xml\n'
        '|   |-- haarcascade_eye.xml\n'
        '|\n'
        '|-- known_faces/             # Store known face images (for later phases)\n'
        '|-- snapshots/               # Auto-saved detection snapshots\n'
        '|-- dataset/                 # Collected face datasets\n'
        '|-- logs/                    # Detection logs\n'
        '|-- pdf/                     # Project documentation'
    )

    pdf.section_title('Purpose of Each Folder')
    pdf.bullet_point('config/: Contains settings.py with all project constants like camera index, email settings, etc.')
    pdf.bullet_point('src/: Contains all Python source code files')
    pdf.bullet_point('models/: Contains pre-trained Haar Cascade XML files for face and eye detection')
    pdf.bullet_point('known_faces/: Will store images of known individuals (for Phase 2)')
    pdf.bullet_point('snapshots/: Auto-saved screenshots when faces are detected')
    pdf.bullet_point('dataset/: Collected face images for building the database')
    pdf.bullet_point('logs/: Detection logs with timestamps')
    pdf.bullet_point('pdf/: Project documentation')

    # Page 7 - Haar Cascade Explanation
    pdf.add_page()
    pdf.chapter_title('5. Haar Cascade - How It Works')

    pdf.section_title('What is Haar Cascade?')
    pdf.body_text(
        'Haar Cascade is a machine learning-based approach for object detection, originally proposed '
        'by Paul Viola and Michael Jones in 2001. It uses a series of simple binary features (called '
        'Haar-like features) to detect objects in images. For face detection, it was trained on '
        'thousands of face and non-face images.'
    )

    pdf.section_title('How It Detects Faces')
    pdf.body_text('The algorithm works in four main stages:')
    pdf.ln(2)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, 'Stage 1: Haar-Like Feature Extraction', 0, 1)
    pdf.body_text(
        'The classifier looks at rectangular regions in the image and calculates the difference '
        'in intensity between adjacent rectangles. For example, the eye region is typically darker '
        'than the forehead, so the feature detector identifies this pattern.'
    )

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, 'Stage 2: Integral Image', 0, 1)
    pdf.body_text(
        'To compute these features quickly, the algorithm uses an "integral image" which allows '
        'summing pixel values in any rectangular region in constant time (O(1)).'
    )

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, 'Stage 3: AdaBoost Training', 0, 1)
    pdf.body_text(
        'AdaBoost selects the most important features from a large pool and combines them into '
        'a strong classifier. Each weak classifier looks at one feature and makes a simple decision.'
    )

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, 'Stage 4: Cascade Architecture', 0, 1)
    pdf.body_text(
        'Classifiers are arranged in a cascade (series of stages). Simple stages reject non-faces '
        'early. Only regions that pass all stages are classified as faces. This makes the algorithm '
        'very fast because most image regions are rejected early.'
    )

    # Page 8 - Key Parameters
    pdf.add_page()
    pdf.section_title('Key Parameters in detectMultiScale()')
    pdf.body_text('The detectMultiScale() function has several important parameters:')

    widths = [40, 30, 120]
    pdf.table_header(['Parameter', 'Value', 'Description'], widths)
    pdf.table_row(['scaleFactor', '1.3', 'How much the image size is reduced at each image scale'], widths)
    pdf.table_row(['minNeighbors', '5', 'How many neighbors each candidate rectangle should have'], widths)
    pdf.table_row(['minSize', '(50,50)', 'Minimum possible object size. Objects smaller are ignored'], widths)

    pdf.ln(5)
    pdf.body_text(
        'scaleFactor=1.3 means the image is scaled down by 30% at each step. This helps detect '
        'faces of different sizes. A smaller value (like 1.1) is more accurate but slower.'
    )
    pdf.body_text(
        'minNeighbors=5 means a detection must have at least 5 overlapping detections to be '
        'considered a face. Higher values mean fewer false positives but might miss some faces.'
    )

    # Page 9 - face_detector.py Explanation
    pdf.add_page()
    pdf.chapter_title('6. Code Explanation - face_detector.py')
    pdf.body_text(
        'This is the core module that handles all face detection logic. It is designed as a '
        'reusable class that can be imported by other modules.'
    )

    pdf.section_title('Class: FaceDetector')
    pdf.body_text('The FaceDetector class has four main methods:')

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, '__init__(self)', 0, 1)
    pdf.body_text(
        'Constructor method. Loads the Haar Cascade XML files for face and eye detection. '
        'Raises an error if the files cannot be loaded.'
    )

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, 'detect_faces(self, frame)', 0, 1)
    pdf.body_text(
        'Takes a video frame (as a NumPy array) and returns a list of dictionaries, each '
        'containing the face position (x, y, width, height), number of eyes detected, and timestamp.'
    )

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, 'draw_detections(self, frame, detections)', 0, 1)
    pdf.body_text(
        'Draws green bounding boxes and labels on the frame for each detected face. '
        'Returns the annotated frame for display.'
    )

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, 'save_snapshot(self, frame, detection)', 0, 1)
    pdf.body_text(
        'Saves a cropped image of the detected face with some padding. '
        'Files are saved with timestamp-based filenames to avoid conflicts.'
    )

    # Page 10 - webcam_capture.py Explanation
    pdf.add_page()
    pdf.chapter_title('7. Code Explanation - webcam_capture.py')
    pdf.body_text(
        'This module handles live webcam capture and real-time face detection. '
        'It creates a continuous loop that reads frames from the webcam, passes them '
        'to the FaceDetector, and displays the results.'
    )

    pdf.section_title('Flow of Execution')
    pdf.bullet_point('Step 1: Initialize FaceDetector and open webcam (camera index 0)')
    pdf.bullet_point('Step 2: Set resolution to 640x480')
    pdf.bullet_point('Step 3: Enter infinite loop - read frame, detect faces, draw boxes, display')
    pdf.bullet_point('Step 4: Show info bar with face count, total detections, and elapsed time')
    pdf.bullet_point('Step 5: Handle keyboard inputs - q to quit, s to snapshot, r to reset counter')

    pdf.section_title('Keyboard Controls')
    widths2 = [30, 160]
    pdf.table_header(['Key', 'Action'], widths2)
    pdf.table_row(['q', 'Quit the application'], widths2)
    pdf.table_row(['s', 'Save a snapshot of detected faces'], widths2)
    pdf.table_row(['r', 'Reset the detection counter'], widths2)

    # Page 11 - image_face_detection.py Explanation
    pdf.add_page()
    pdf.chapter_title('8. Code Explanation - image_face_detection.py')
    pdf.body_text(
        'This module provides two functions for detecting faces in static images '
        'and pre-recorded video files.'
    )

    pdf.section_title('detect_faces_in_image(image_path)')
    pdf.body_text(
        'Reads an image from the given path, detects all faces, draws bounding boxes, '
        'saves the output image to the snapshots folder, and displays it in a window.'
    )

    pdf.section_title('detect_faces_in_video(video_path)')
    pdf.body_text(
        'Opens a video file, processes every 3rd frame (to improve speed), detects faces, '
        'and displays results in real-time. Press q to stop processing early.'
    )

    # Page 12 - dataset_collector.py Explanation
    pdf.add_page()
    pdf.chapter_title('9. Code Explanation - dataset_collector.py')
    pdf.body_text(
        'This module collects face images from the webcam to build a dataset of known individuals. '
        'This dataset will be used in Phase 2 for face recognition (matching faces against a database).'
    )

    pdf.section_title('How It Works')
    pdf.bullet_point('Takes a person name as argument (e.g., "john")')
    pdf.bullet_point('Opens webcam and detects the face')
    pdf.bullet_point('Press "c" to capture a frame - face is cropped, resized to 200x200, and saved')
    pdf.bullet_point('Default: collects 50 samples per person')
    pdf.bullet_point('Images are saved in dataset/<person_name>/ folder')

    pdf.section_title('Usage')
    pdf.code_block(
        'python3 dataset_collector.py john\n'
        'python3 dataset_collector.py john 100  # collect 100 samples'
    )

    # Page 13 - How to Run
    pdf.add_page()
    pdf.chapter_title('10. How to Run the Project')

    pdf.section_title('Option A: Live Webcam Detection')
    pdf.code_block('cd major_project\npython3 -m src.webcam_capture')
    pdf.body_text('This opens your webcam and starts detecting faces in real-time.')

    pdf.section_title('Option B: Detect Faces in an Image')
    pdf.code_block('python3 -m src.image_face_detection path/to/image.jpg')
    pdf.body_text('This detects faces in a static image and saves the result.')

    pdf.section_title('Option C: Detect Faces in a Video')
    pdf.code_block('python3 -m src.image_face_detection --video path/to/video.mp4')
    pdf.body_text('This processes a video file and shows face detections frame by frame.')

    pdf.section_title('Option D: Collect Face Dataset')
    pdf.code_block('python3 -m src.dataset_collector person_name [num_samples]')
    pdf.body_text('This captures face images from webcam to build the database.')

    # Page 14 - Expected Output
    pdf.add_page()
    pdf.chapter_title('11. Expected Output')

    pdf.section_title('Webcam Detection Output')
    pdf.body_text(
        'When you run webcam_capture.py, a window opens showing your webcam feed. '
        'Each detected face gets a green bounding box around it with a label showing '
        'the number of eyes detected. An info bar at the top shows:'
    )
    pdf.bullet_point('Number of faces currently visible')
    pdf.bullet_point('Total number of faces detected since start')
    pdf.bullet_point('Elapsed time since start')

    pdf.section_title('Image Detection Output')
    pdf.body_text(
        'When you run image_face_detection.py with an image, it displays the image '
        'with green bounding boxes around all detected faces. The console prints '
        'the position and size of each face found.'
    )

    pdf.section_title('Snapshot Saving')
    pdf.body_text(
        'Press "s" during webcam detection to save a snapshot. The cropped face '
        'image is saved in the snapshots/ folder with a timestamp filename like '
        'snapshot_20260819_143022.jpg.'
    )

    # Page 15 - Week 1 Summary
    pdf.add_page()
    pdf.chapter_title('12. Week 1 Summary')

    pdf.section_title('What Was Accomplished')
    pdf.bullet_point('Set up the complete project directory structure')
    pdf.bullet_point('Installed OpenCV 4.8.1 with contrib modules')
    pdf.bullet_point('Installed NumPy 1.24.4')
    pdf.bullet_point('Downloaded pre-trained Haar Cascade XML models')
    pdf.bullet_point('Created modular Python codebase with 4 source files')
    pdf.bullet_point('Implemented real-time face detection from webcam')
    pdf.bullet_point('Implemented face detection on images and videos')
    pdf.bullet_point('Created dataset collection tool for future phases')
    pdf.bullet_point('All modules tested and verified working')

    pdf.section_title('Technologies Used This Week')
    widths3 = [45, 145]
    pdf.table_header(['Technology', 'Purpose'], widths3)
    pdf.table_row(['Python 3.8.10', 'Main programming language'], widths3)
    pdf.table_row(['OpenCV 4.8.1', 'Image processing and face detection'], widths3)
    pdf.table_row(['NumPy 1.24.4', 'Array operations for image data'], widths3)
    pdf.table_row(['Haar Cascade', 'Pre-trained face/eye detection model'], widths3)

    pdf.section_title('What Will Be Done in Week 2')
    pdf.bullet_point('Install dlib and face_recognition libraries')
    pdf.bullet_point('Implement face encoding (converting faces to numerical vectors)')
    pdf.bullet_point('Build the face database using collected dataset')
    pdf.bullet_point('Implement face matching/comparison logic')
    pdf.bullet_point('Test recognition accuracy with known individuals')

    pdf.section_title('Issues Faced')
    pdf.bullet_point(
        'OpenCV 5.0 removed CascadeClassifier - resolved by using opencv-contrib-python 4.8.1'
    )
    pdf.bullet_point(
        'dlib compilation from source takes very long - installation running in background'
    )

    # Save PDF
    output_path = '/home/rguktrkvalley/Desktop/desktop/major_project/pdf/Week1_Progress_Report.pdf'
    pdf.output(output_path)
    print(f'PDF saved to: {output_path}')
    print(f'File size: {os.path.getsize(output_path)} bytes')


if __name__ == '__main__':
    generate_pdf()
