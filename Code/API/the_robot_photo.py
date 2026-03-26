import cv2
import time


def capture_photo_linux(filename="lane.jpg"):
    # 1. Try standard index first
    cap = cv2.VideoCapture(0)

    # 2. Wait for camera to warm up
    time.sleep(1)

    if not cap.isOpened():
        print("Could not open camera. Trying V4L2 backend...")
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        if not cap.isOpened():
            return None

    # 3. Flush the buffer (30 frames is good for auto-exposure)
    for i in range(30):
        cap.grab()  # grab() is faster than read() for flushing

    ret, frame = cap.read()
    cap.release()

    if ret and frame is not None:
        cv2.imwrite(filename, frame)
        print("Capture successful!")
        return frame
    else:
        print("Capture failed: Frame is empty.")
        return None