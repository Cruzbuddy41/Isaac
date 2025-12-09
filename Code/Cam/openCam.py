"""import cv2
import numpy as np

lower_blue = np.array([100, 150, 50])
upper_blue = np.array([140, 255, 255])

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Webcam initialized. Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Video", frame)

cap.release()
cv2.destroyAllWindows()
