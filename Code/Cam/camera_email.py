import cv2
import smtplib
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# --- Configuration (Update these details) ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "bd6011080@ahschool.com"
# Use an App Password for Gmail/Yahoo for security
SENDER_PASSWORD = "zons uhwz jlvo pemu"
RECEIVER_EMAIL = "brian.grom@ahschool.com"  # <-- Change this to your recipient email
IMAGE_FILENAME = "ph.jpg"


def capture_photo_and_email(receiver_email):
    # --- 1. Capture the image using OpenCV ---
    print("Opening camera...")
    # Use index 0 for the first camera connected (USB or CSI camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera. Exiting.")
        return

    print("Warming up camera sensor and capturing frame...")
    # Essential for preventing black frames: read a few frames to allow auto-exposure to adjust
    for i in range(30):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Failed to grab frame.")
        return

    # Save the frame temporarily to a file (or encode directly)
    cv2.imwrite(IMAGE_FILENAME, frame)
    print(f"Photo saved as {IMAGE_FILENAME}")

    # --- 2. Prepare email variables ---
    currentTime = time.strftime("%m-%d-%Y %H:%M:%S", time.localtime())
    subject = "Photo capture: " + currentTime
    body = "Here is the photo captured by the Raspberry Pi camera."

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # --- 3. Attach the image file ---
    try:
        with open(IMAGE_FILENAME, 'rb') as fp:
            img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(IMAGE_FILENAME))
        msg.attach(img)
    except FileNotFoundError:
        print(f"Attachment file not found at {IMAGE_FILENAME}. Cannot send email.")
        return

    # --- 4. Send the email ---
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

    # Optional: Clean up the image file after sending
    if os.path.exists(IMAGE_FILENAME):
        os.remove(IMAGE_FILENAME)


# --- Main execution block ---
if __name__ == "__main__":
    capture_photo_and_email(RECEIVER_EMAIL)
