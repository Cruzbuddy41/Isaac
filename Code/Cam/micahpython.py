import cv2
import time
import smtplib
import ssl
from email.message import EmailMessage
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


send = "bd6010870@ahschool.com"
unluckyrecipient = "brian.grom@ahschool.com"
app_password = "inmm taje rprm tlqu"

subject = "micah's python project"
body = """
mr grom do you know me? are we tight
"""

msg = EmailMessage()
msg.set_content(body)
msg["Subject"] = subject
msg["From"] = send
msg["To"] = unluckyrecipient


try:
    with open(namevar, "rb") as fil:
        file_data = fil.read()
        file_name = basename(namevar)

    msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=file_name)
    print(f"Attachment added: {namevar}")
except FileNotFoundError:
    print(f"Warning: Attachment file not found at {namevar}")

# Send email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(send, app_password)
        server.send_message(msg)
    print("Email sent successfully!")
except smtplib.SMTPException as e:
    print(f"Error: {e}")
