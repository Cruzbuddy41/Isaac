import cv2
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_photo_email(image, receiver_email):
    """
    Takes an OpenCV image frame and emails it to a recipient.
    """
    # --- Email Configuration (Update these details) ---
    smtpServer = "smtp.gmail.com"
    smtpPort = 587
    sender = "bd6011080@ahschool.com"  # Your sender email
    # This must be an App Password if using Gmail/Yahoo
    password = "Trentontc1"  # Your generated App Password

    currentTime = time.strftime("%m-%d-%Y", time.localtime())
    subject = "Photo capture: " + currentTime

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach a plain text body
    msg.attach(MIMEText("A photo captured by the camera.", 'plain'))

    # Encode the OpenCV image frame into JPEG data
    is_success, buffer = cv2.imencode(".jpg", image)
    if not is_success:
        print("Failed to encode image.")
        return

    img_data = buffer.tobytes()
    # Create the email image attachment
    image_attachment = MIMEImage(img_data, name="image.jpg")
    msg.attach(image_attachment)

    # --- Send the email ---
    try:
        server = smtplib.SMTP(smtpServer, smtpPort)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Authentication Error: Check your sender email and App Password.")
        print("Ensure you are using an App Password for Gmail, not your main account password.")
    except Exception as e:
        print(f"An error occurred: {e}")


# --- Main execution block ---
if __name__ == "__main__":
    # Configure the recipient email address here:
    RECIPIENT_EMAIL_ADDRESS = "sadfeen.sadiq@ahschool.com"

    print("Opening camera (using OpenCV)...")
    # Use index 0 for the first camera connected (USB or CSI camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera. Exiting.")
        exit()

    # Capture a single frame
    ret, frame = cap.read()

    if ret:
        print("Frame captured. Preparing email...")
        send_photo_email(frame, RECIPIENT_EMAIL_ADDRESS)
    else:
        print("Failed to grab frame.")

    # Release the camera resource
    cap.release()