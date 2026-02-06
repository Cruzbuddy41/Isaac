import cv2
import smtplib
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "bd6011080@ahschool.com"
SENDER_PASSWORD = "zons uhwz jlvo pemu"
RECEIVER_EMAIL = "brian.grom@ahschool.com"
IMAGE_FILENAME = "ph.jpg"


def capture_photo_and_email(receiver_email):
    print("Opening camera...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera. Exiting.")
        return

    print("Warming up camera sensor and capturing frame...")

    for i in range(30):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Failed to grab frame.")
        return


    cv2.imwrite(IMAGE_FILENAME, frame)
    print(f"Photo saved as {IMAGE_FILENAME}")


    currentTime = time.strftime("%m-%d-%Y %H:%M:%S", time.localtime())
    subject = "Photo capture: " + currentTime
    body = "Here is the photo captured by the Raspberry Pi camera."

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))


    try:
        with open(IMAGE_FILENAME, 'rb') as fp:
            img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(IMAGE_FILENAME))
        msg.attach(img)
    except FileNotFoundError:
        print(f"Attachment file not found at {IMAGE_FILENAME}. Cannot send email.")
        return


    print(f"Attempting to send email to {receiver_email}...")
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Authentication Error: Check your sender email and App Password.")
    except Exception as e:
        print(f"An error occurred: {e}")


    if os.path.exists(IMAGE_FILENAME):
        os.remove(IMAGE_FILENAME)



if __name__ == "__main__":
    capture_photo_and_email(RECEIVER_EMAIL)
