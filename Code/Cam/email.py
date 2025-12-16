import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# --- Configuration ---
# Update these variables with your information
SMTP_SERVER = 'smtp.gmail.com' # Use 'smtp.mail.yahoo.com', etc. for other providers
SMTP_PORT = 587
SENDER_EMAIL = 'bd6011080@ahschool.com'
# Use an App Password for Gmail/Yahoo for security (not your main password)
SENDER_PASSWORD = 'Trentontc1'
RECEIVER_EMAIL = 'sadfeen.sadiq@ahschool.com'
EMAIL_SUBJECT = 'Raspberry Pi Photo'
EMAIL_BODY = 'Here is the photo captured by the Raspberry Pi.'
IMAGE_PATH = '/home/isaac/Isaac/code/cam/ph.jpg' # Ensure your 'pi' user has access to this path

# --- 1. Capture the image using picamera2 ---
def capture_image(path):
    print("Initializing camera and capturing photo...")
    try:
        from picamera2 import Picamera2
        picam2 = Picamera2()
        camera_config = picam2.create_preview_configuration(main={"size": (1280, 720)})
        picam2.configure(camera_config)
        picam2.start()
        time.sleep(2) # Give camera time to adjust light levels
        picam2.capture_file(path)
        picam2.stop()
        print(f"Photo saved to {path}")
    except ImportError:
        print("Picamera2 not found. Please install it using: sudo apt install python3-picamera2")
        exit()
    except Exception as e:
        print(f"Error capturing image: {e}")
        exit()

# --- 2. Send the email with the image attachment ---
def send_email(subject, body, sender, recipient, password, image_path):
    print(f"Attempting to send email to {recipient}...")

    # Create the root message and fill in the headers
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg.attach(MIMEText(body, 'plain'))

    # Attach the image
    try:
        with open(image_path, 'rb') as fp:
            img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
        msg.attach(img)
    except FileNotFoundError:
        print(f"Attachment file not found at {image_path}. Skipping attachment.")
        return

    # Send the email via SMTP server
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() # Secure the connection
            server.login(sender, password)
            server.send_message(msg)
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Authentication error. Check your email address and App Password.")
        print("For Gmail, you may need to generate an App Password in your [Google Account security settings](myaccount.google.com).")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")

# --- Main execution ---
if __name__ == "__main__":
    capture_image(IMAGE_PATH)
    if os.path.exists(IMAGE_PATH):
        send_email(EMAIL_SUBJECT, EMAIL_BODY, SENDER_EMAIL, RECEIVER_EMAIL, SENDER_PASSWORD, IMAGE_PATH)
    else:
        print("Cannot send email because the image file was not created.")
