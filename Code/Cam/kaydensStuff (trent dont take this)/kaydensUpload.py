import cv2
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send(image, receiver):
    smtpServer = "smtp.gmail.com"
    smtpPort = 587
    currentTime = time.strftime("%m-%d-%Y", time.localtime())
    subject = "Photo capture: " + currentTime
    sender = "bd568711@ahschool.com"
    password = "xbgq zkzv pvwz odkv"
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText('plain'))

    is_success, buffer = cv2.imencode(".jpg", image)

    img_data = buffer.tobytes()
    image = MIMEImage(img_data, name="image.jpg")
    msg.attach(image)

    server = smtplib.SMTP(smtpServer, smtpPort)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
    print("Email sent successfully!")