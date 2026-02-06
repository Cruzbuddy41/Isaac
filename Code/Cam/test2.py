import os
import sys

# Remove the path that causes the 'xcb' error
os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH", None)
# Force the output to the Pi's HDMI monitor
os.environ["DISPLAY"] = ":0"

import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

# Define the static lower and upper bounds
# Lower: [81, 100, 100
# Upper: [101, 255, 255]
lower = np.array([81, 100, 100])
upper = np.array([101, 255, 255])

while True:
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create the mask using the fixed bounds
    mask = cv2.inRange(hsv, lower, upper)

    # Find and draw contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    # Show the result
    cv2.imshow("Object Detection", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()