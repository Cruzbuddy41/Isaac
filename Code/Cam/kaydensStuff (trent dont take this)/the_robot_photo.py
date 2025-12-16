import cv2
import kaydensUpload

def capture_photo_linux(filename="ph.jpg"):
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    if not cap.isOpened():
        print("Could not open camera")
        return

    print("Capturing image")

    for i in range(30):
        cap.read()

    ret, frame = cap.read()

    cap.release()
    if ret:
        cv2.imwrite(filename, frame)
        print(f"Worked (Potentially)")
        return frame

def capture_photo_mac(filename="ph.jpg"):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Could not open camera")
        return

    print("Capturing image")

    for i in range(30):
        cap.read()

    ret, frame = cap.read()

    cap.release()
    if ret:
        cv2.imwrite(filename, frame)
        print(f"Worked (Potentially)")
        return frame

print("Input mac for mac Input linux for linux")
choice = input()

if(choice == "mac"):
    image = capture_photo_mac()
else:
    image = capture_photo_linux()

kaydensUpload.send(image, "brian.grom@ahschool.com")
