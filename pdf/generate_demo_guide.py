from fpdf import FPDF
import os
from datetime import datetime


class DemoPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')


def main():
    pdf = DemoPDF()
    pdf.add_page()
    pdf.set_margins(18, 18, 18)

    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_text_color(26, 35, 126)
    pdf.cell(0, 12, '5-MINUTE GUIDE DEMO', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, 'Show your guide the whole project quickly and confidently', 0, 1, 'C')
    pdf.ln(6)

    def section(title, steps):
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(41, 128, 185)
        pdf.cell(0, 8, title, 0, 1)
        pdf.ln(1)
        pdf.set_draw_color(41, 128, 185)
        pdf.line(18, pdf.get_y(), 192, pdf.get_y())
        pdf.ln(3)
        for i, (action, say) in enumerate(steps, 1):
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 6, f'STEP {i}: {action}', 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(60, 60, 60)
            pdf.multi_cell(0, 6, f'   Say: "{say}"')
            pdf.ln(2)

    section('PART A - Show the Live Dashboard (2 min)', [
        ('Open a terminal, go to project folder, start dashboard',
         'Sir/Ma\'am, this is our Smart Surveillance Web Dashboard. '
         'It streams the live camera feed into a browser in real time.'),
        ('Open browser at http://localhost:5000',
         'Watch - the camera feed is live. As anyone comes in front of the camera, '
         'the system draws boxes around their face.'),
    ])

    section('PART B - Show Face Detection + Recognition (1.5 min)', [
        ('Point webcam at yourself / guidance',
         'A GREEN box means an unknown person. Now watch - when a face matches our '
         'registered database, the box turns RED and shows the person\'s name and confidence %.'),
        ('If ujjeef face is shown (photo/another person).',
         'Here it found a match with 90% confidence. The system just saved a snapshot '
         'and logged this detection into the database.'),
    ])

    section('PART C - Show Object Detection (YOLO) (1 min)', [
        ('Hold an object in view (bag/person/bottle)',
         'The BLUE boxes are objects detected by YOLO - a deep learning model trained '
         'on 80 classes. It detects people, bags, phones, and more in every frame.'),
        ('Show a bag/backpack',
         'Suspicious objects like bags and backpacks are drawn in RED with a warning, '
         'because in a surveillance context they need attention.'),
    ])

    section('PART D - Show Alerts + Email (0.5 min)', [
        ('Click the Alerts page in the top bar',
         'Every detection is recorded here - time, name, confidence, camera, and if it '
         'was a match. This is audit-ready evidence.'),
        ('Mention email system',
         'When a registered person is detected, the system instantly emails a snapshot '
         'to the authority with time and camera location.'),
    ])

    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 8, 'BACKUP KEY POINTS (if they ask details)', 0, 1)
    pdf.ln(2)
    for q, a in [
        ('How do you detect faces?', 'Haar Cascade in OpenCV - a pre-trained face finder.'),
        ('How do you identify WHO a person is?', 'We convert each face into a 128-number embedding with dlib, then compare with a database using Euclidean distance. Low distance = same person.'),
        ('What is YOLO doing?', 'YOLO is a single-pass CNN detecting 80 object classes. We run it through OpenCV\'s DNN module.'),
        ('What happens on a match?', 'Snapshot saved + email sent via SMTP + logged to SQLite/CSV with timestamp and camera ID.'),
        ('Where is data stored?', 'SQLite database (logs/faces.db) plus CSV logs.'),
        ('Is it real-time?', 'Yes - the camera thread runs continuously and the dashboard streams it.'),
    ]:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 6, 'Q: ' + q, 0, 1)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 6, 'A: ' + a)
        pdf.ln(1)

    pdf.set_text_color(26, 35, 126)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_y(-30)
    pdf.cell(0, 8, 'Remember: stay calm, let the camera do the talking.', 0, 1, 'C')

    out = '/home/rguktrkvalley/Desktop/desktop/major_project/pdf/5Minute_Guide_Demo.pdf'
    pdf.output(out)
    print(f'PDF saved: {out} ({os.path.getsize(out)} bytes)')


if __name__ == '__main__':
    main()