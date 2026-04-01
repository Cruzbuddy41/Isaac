import cv2
import time


def capture_photo_linux(filename="lane.jpg"):
    cap = cv2.VideoCapture(0)
    time.sleep(1)

    if not cap.isOpened():
        print("Could not open camera. Trying V4L2 backend...")
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        if not cap.isOpened():
            return None
    for i in range(30):
        cap.grab()

    ret, frame = cap.read()
    cap.release()

    if ret == True:
        cv2.imwrite(filename, frame)
        print("Capture successful!")
        return frame
    else:
        print("Capture failed: Frame is empty.")
        return None
