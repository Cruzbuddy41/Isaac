import cv2
import time
import makeLines

def capture_photo_linux(filename="lanes.jpg"):
    cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

    if not cap.isOpened():
        print("2")
        return None
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    time.sleep(2)
    for i in range(15):
        cap.read()

    ret, frame = cap.read()
    cap.release()
    return frame if ret else None


def capture_photo_mac(filename="lanes.jpg"):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None
    for i in range(30):
        cap.read()
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None
#
print("Input mac for mac, Input linux for linux")
choice = input().strip().lower()
if choice == "mac":
    image = capture_photo_mac()
else:
    image = capture_photo_linux()

if image is not None:
    cv2.imwrite("lane.jpg", image)