import cv2
import time

def capture_photo_mac(filename="ph.jpg"):
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    if not cap.isOpened():
        print("Could not open camera")
        return

    print("Capturing image")

    for i in range(30):
        cap.read()

    ret, frame = cap.read()

    cap.release()

    cv2.imwrite(filename, frame)
    print("Worked (Potentially)")


capture_photo_mac()