import cv2
import time
import makeLines


def capture_photo_linux():
    cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
    if not cap.isOpened():
        return None

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    time.sleep(2)
    for _ in range(30):
        cap.read()

    ret, frame = cap.read()
    cap.release()
    return frame if ret else None


def capture_photo_mac():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None
    for _ in range(30):
        cap.read()
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None
print("Input 'mac' for Mac, 'linux' for Linux:")
choice = input().strip().lower()

image = capture_photo_mac() if choice == "mac" else capture_photo_linux()

if image is not None:
    cv2.imwrite("lane.jpg", image)
    lane_center = makeLines.lanes()

    if lane_center is None:
        print("Error: No lanes detected.")
    else:
        height, width, _ = image.shape
        img_midpoint = width // 2
        threshold = 250
        if lane_center < (img_midpoint - threshold):
            print("Action: Left Turn")
        elif lane_center > (img_midpoint + threshold):
            print("Action: Right Turn")
        else:
            print("Action: Forward")
else:
    print("Error: Could not capture image.")
