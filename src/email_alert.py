import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    ALERT_EMAIL, SMTP_SERVER, SMTP_PORT
)


class EmailAlert:
    def __init__(self, sender_email=None, sender_password=None, receiver_email=None):
        self.sender_email = sender_email or os.environ.get("SENDER_EMAIL", "")
        self.sender_password = sender_password or os.environ.get("SENDER_PASSWORD", "")
        self.receiver_email = receiver_email or ALERT_EMAIL
        self.enabled = bool(self.sender_email and self.sender_password)

    def send_alert(self, name, confidence, camera_id, snapshot_path, timestamp):
        if not self.enabled:
            print("[ALERT] Email not configured. Skipping email. Set SENDER_EMAIL and SENDER_PASSWORD.")
            return False

        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = self.receiver_email
        msg["Subject"] = f"[ALERT] Known Person Detected: {name}"

        body = f"""
        SMART SURVEILLANCE ALERT
        ========================

        A known person has been detected by the surveillance system.

        Person Name  : {name}
        Confidence   : {confidence:.0%}
        Camera ID    : {camera_id}
        Timestamp    : {timestamp}
        Snapshot     : {os.path.basename(snapshot_path)}

        Please review the attached snapshot and take necessary action.

        ---
        This is an automated alert from the Smart Camera & Video Surveillance System.
        """
        msg.attach(MIMEText(body, "plain"))

        if snapshot_path and os.path.exists(snapshot_path):
            with open(snapshot_path, "rb") as f:
                img = MIMEImage(f.read())
                img.add_header("Content-Disposition", "attachment", filename=os.path.basename(snapshot_path))
                msg.attach(img)

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            server.quit()
            print(f"[EMAIL] Alert sent to {self.receiver_email} for '{name}'")
            return True
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send: {e}")
            return False

    def test_connection(self):
        if not self.enabled:
            print("[ERROR] Email not configured. Set SENDER_EMAIL and SENDER_PASSWORD.")
            return False
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.quit()
            print("[EMAIL] SMTP connection successful.")
            return True
        except Exception as e:
            print(f"[EMAIL ERROR] Connection failed: {e}")
            return False
