import cv2
import numpy as np
import time

def nothing(x):
    pass

cv2.namedWindow("Picker")
cv2.createTrackbar("Color", "Picker", 0, 245, nothing)

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hue = cv2.getTrackbarPos("Color", "Picker")
    lower = np.array([hue - 10, 100, 100])
    upper = np.array([hue + 10, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    cv2.imshow("Picker", frame)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()
o