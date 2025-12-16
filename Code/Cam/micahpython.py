import cv2
import time
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from os.path import basename

ssl._create_default_https_context = ssl._create_unverified_context

namevar = "ph.jpg"


def capture_photo_mac(filename="ph.jpg"):
    global namevar
    namevar = filename

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Could not open camera")
        return

    print("Capturing image...")
    time.sleep(2)

    ret, frame = cap.read()
    cap.release()

    if ret:
        cv2.imwrite(filename, frame)
        print(f"Photo captured as {filename}")
    else:
        print("Failed to grab frame")


capture_photo_mac()

sender_email = "bd6010870@ahschool.com"
receiver_email = "brian.grom@ahschool.com"
app_password = "inmm taje rprm tlqu"

subject = "micah's python project"
body = """
mr grom do you know me? are we tight
"""

msg = EmailMessage()
msg.set_content(body)
msg["Subject"] = subject
msg["From"] = sender_email
msg["To"] = receiver_email

try:
    with open(namevar, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(namevar)
        )
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(namevar)
    msg.attach(part)
    print(f"Attachment added: {namevar}")
except FileNotFoundError:
    print(f"Warning: Attachment file not found at {namevar}")

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)
    print("Email sent successfully!")
except smtplib.SMTPException as e:
    print(f"Error: {e}")
