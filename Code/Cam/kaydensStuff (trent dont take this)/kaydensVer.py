import cv2
import os
import kaydensUpload
import makeLines


def capture_photo_linux(filename="lanes.jpg"):
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=zoom_absolute=100")

    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    for i in range(30):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if ret:
        cv2.imwrite(filename, frame)
        print(f"Captured: {filename}")
        return frame
    return None


def capture_photo_mac(filename="lanes.jpg"):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_ZOOM, 100)

    if not cap.isOpened():
        print("Could not open camera")
        return None

    for i in range(30):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if ret:
        cv2.imwrite(filename, frame)
        return frame
    return None


print("Input mac for mac Input linux for linux")
choice = input().strip().lower()

if choice == "mac":
    image = capture_photo_mac()
else:
    image = capture_photo_linux()

cv2.imwrite("lanes.jpg", image)
makeLines.lanes()