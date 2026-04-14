import cv2
import smtplib
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "bd554192@ahschool.com"
SENDER_PASSWORD = "cxgi kdfb abxw sftl"
RECEIVER_EMAIL = "bd554192@ahschool.com"

def email(img):
    currentTime = time.strftime("%m-%d-%Y %H:%M:%S", time.localtime())
    subject = "Photo capture: " + currentTime
    body = "Here is the photo showing proof of Chud detection."

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        photo_to_send = 'phototosend.jpg'
        cv2.imwrite('phototosend.jpg', img)
        with open('phototosend.jpg', 'rb') as f:
            img_data = f.read()
        image_part = MIMEImage(img_data, name=os.path.basename('phototosend.jpg'))
        image_part.add_header('Content-Disposition', f'attachment; filename="{img}"')
        msg.attach(image_part)
    except FileNotFoundError:
        print(f"Attachment file not found. Cannot send email.")
        return


    print(f"Attempting to send email to {RECEIVER_EMAIL}...")
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Authentication Error: Check your sender email and App Password.")
    except Exception as e:
        print(f"An error occurred: {e}")




if __name__ == "__main__":
    email()
