from fpdf import FPDF
import os


class Doc(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def section_title(self, text):
        self.set_font('Helvetica', 'B', 14)
        self.set_fill_color(41, 128, 185)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f'  {text}', 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def h2(self, text):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(41, 128, 185)
        self.cell(0, 8, text, 0, 1)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def body(self, text):
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def code(self, code):
        self.set_font('Courier', '', 8)
        self.set_fill_color(240, 240, 240)
        for line in code.strip().split('\n'):
            self.cell(0, 5, f'  {line}', 0, 1, 'L', True)
        self.ln(3)

    def bullet(self, text):
        self.set_font('Helvetica', '', 10)
        self.cell(8, 6, '')
        self.cell(5, 6, chr(149))
        self.multi_cell(0, 6, text)
        self.ln(1)


def main():
    pdf = Doc()
    pdf.add_page()

    pdf.h2('SIREN ALERT FEATURE - Audio Warning When a Match is Found')
    pdf.body(
        'When the system detects a registered (known) person, besides sending the email '
        'and saving a snapshot, it now also plays a POLICE-STYLE SIREN sound as an '
        'audio alarm. This grabs immediate attention at the control room.'
    )

    pdf.section_title('1. New File: src/siren.py')
    pdf.h2('Class: SirenPlayer')
    pdf.bullet('__init__(): stores the sound file path and creates it if missing')
    pdf.bullet('_generate_siren_wav(): produces the siren sound WAV file using numpy + wave')
    pdf.bullet('play(): plays the sound using the platform audio tool (aplay/paplay on Linux, winsound on Windows, afplay on Mac)')
    pdf.bullet('play_async(): plays the sound in a BACKGROUND thread so the camera loop is not blocked')
    pdf.bullet('test(): quickly plays the siren to verify your speakers work')

    pdf.h2('How the Siren Sound is Created (no internet needed)')
    pdf.body('We generate a "wee-oo-wee-oo" police siren mathematically:')
    pdf.code(
        't = time samples (0..3 seconds)\n'
        'freq = 500 + 450 * sin(2*pi*1.5*t)\n'
        '       -> the pitch smoothly rises and falls between 500-950 Hz\n'
        'wave = sin(2*pi * cumsum(freq))   -> build the sine wave\n'
        'envelope -> fade in/out so there is no click at the edges\n'
        'save as 44.1 kHz 16-bit stereo-compatible WAV file'
    )

    pdf.section_title('2. How It Is Wired In')
    pdf.h2('settings.py (new lines)')
    pdf.code(
        'SIREN_ENABLED = True\n'
        'SIREN_SOUND_PATH = sounds/siren.wav'
    )

    pdf.h2('surveillance.py (terminal version)')
    pdf.code(
        "from src.siren import SirenPlayer\n"
        "self.siren = SirenPlayer() if SIREN_ENABLED else None\n"
        "...\n"
        "when match detected:\n"
        "    self.siren.play_async()   # one line added"
    )

    pdf.h2('dashboard.py (web version)')
    pdf.code(
        "from src.siren import SirenPlayer\n"
        "self.siren = SirenPlayer() if SIREN_ENABLED else None\n"
        "...\n"
        "when match detected:\n"
        "    self.siren.play_async()   # one line added"
    )

    pdf.h2('Why play_async() ?')
    pdf.body(
        'Playing a 3-second sound blocks the program for 3 seconds. If we call play() directly '
        'inside the camera loop, the live video would freeze for 3 seconds. play_async() starts '
        'a tiny background thread that plays the sound while the camera keeps running smoothly.'
    )

    pdf.section_title('3. How to Run')
    pdf.code(
        '# Test the siren alone:\n'
        '/usr/bin/python3 -m src.siren\n\n'
        '# Terminal surveillance (siren now rings on match):\n'
        '/usr/bin/python3 -m src.surveillance\n\n'
        '# Web dashboard (siren rings on match in the browser stream too):\n'
        '/usr/bin/python3 app.py'
    )

    pdf.section_title('4. To Turn the Siren OFF')
    pdf.body('Open config/settings.py and set SIREN_ENABLED = False')

    pdf.section_title('5. Files Touched')
    pdf.bullet('NEW: src/siren.py - SirenPlayer class')
    pdf.bullet('NEW: sounds/siren.wav - generated sound file (auto-created)')
    pdf.bullet('EDIT: config/settings.py - SIREN_ENABLED, SIREN_SOUND_PATH')
    pdf.bullet('EDIT: src/surveillance.py - play siren on match')
    pdf.bullet('EDIT: src/dashboard.py - play siren on match')

    out = '/home/rguktrkvalley/Desktop/desktop/major_project/pdf/Siren_Alert_Documentation.pdf'
    pdf.output(out)
    print(f'PDF saved: {out} ({os.path.getsize(out)} bytes)')


if __name__ == '__main__':
    main()