import cv2
import time

cap = None

def get_camera():
    global cap
    if cap is None or not cap.isOpened():
        print("Initializing camera resource...")
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        time.sleep(1)
    return cap

def capture_photo_linux(filename="lane.jpg"):
    camera = get_camera()

    if not camera.isOpened():
        print("Capture failed: Camera resource unavailable.")
        return None

    for _ in range(2):
        camera.grab()

    ret, frame = camera.read()

    if ret:
        cv2.imwrite(filename, frame)
        print("Capture successful!")
        return frame
    else:
        print("Capture failed: Frame is empty.")
        return None