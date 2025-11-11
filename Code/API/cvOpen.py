import cv2
import time

video_capture = cv2.VideoCapture(0)
time.sleep(0.5) # Wait for half a second for auto-exposure
ret, frame = video_capture.read()
if ret:
    cv2.imwrite('image.jpg', frame)
else:
    print("Failed to capture image")
video_capture.release()
