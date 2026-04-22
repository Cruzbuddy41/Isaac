import cv2
import numpy as np
import os
import time
import the_robot_photo
import movement
import chud_detection


def regionOfInterest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img


# Sync these paths with app.py
FLAG_FILE = 'stop.txt'
LOG_FILE = 'log.txt'

try:
    while True:
        if os.path.exists(FLAG_FILE):
            movement.stop_all()
            with open(LOG_FILE, 'w') as f: f.write("STOPPED (Manual Flag)")
            time.sleep(0.5)
            continue

        img = the_robot_photo.capture_photo_linux()
        if img is None:
            img = cv2.imread('lane.jpg')
        if img is None:
            continue

        if not chud_detection.chud_detected:
            chud_detection.detect(img)

        h, w = img.shape[:2]
        center_x = w // 2
        output_img = img.copy()

        # Image processing
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 150, 100])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        blurred = cv2.GaussianBlur(mask, (5, 5), 0)
        edges = cv2.Canny(cv2.dilate(blurred, np.ones((5, 5), np.uint8), iterations=1), 50, 150)

        # Region of Interest setup
        big_pts = np.array([[[0, h], [w, h], [w, 100], [0, 100]]], np.int32)
        small_pts = np.array([[[int(w * 0.3), int(h * 0.75)], [int(w * 0.7), int(h * 0.75)], [w // 2, int(h * 0.4)]]],
                             np.int32)

        big_lines = cv2.HoughLinesP(regionOfInterest(edges, big_pts), 1, np.pi / 180, 30, minLineLength=40,
                                    maxLineGap=50)
        small_lines = cv2.HoughLinesP(regionOfInterest(edges, small_pts), 1, np.pi / 180, 20, minLineLength=20,
                                      maxLineGap=50)

        big_right, big_left, top_detected = False, False, False

        if big_lines is not None:
            for line in big_lines:
                x1, y1, x2, y2 = line[0]
                slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 999
                if slope > 0.3 and x1 > center_x: big_right = True
                if slope < -0.3 and x1 < center_x: big_left = True

        if small_lines is not None: top_detected = True

        # Decision Logic
        if top_detected and big_left and big_right:
            direction = "STOP"
            movement.stop_all()
        elif top_detected and big_right:
            direction = "LEFT"
            movement.move_left(55, 0.3)
        elif big_right and not top_detected:
            direction = "FORWARD"
            movement.move_forward(40, 0.3)
        elif big_left and not top_detected:
            direction = "FORWARD"
            movement.move_forward(40, 0.3)
        elif top_detected and big_left:
            direction = "RIGHT"
            movement.move_right(55, 0.3)
        else:
            direction = "SEARCHING"
            movement.move_forward(40, 0.3)

        # Log status to file for the web server
        with open(LOG_FILE, 'w') as f:
            f.write(direction)

        print(f"Status: {direction}")
        cv2.imwrite('lanes_result.jpg', output_img)

except KeyboardInterrupt:
    movement.stop_all()
    if os.path.exists(FLAG_FILE): os.remove(FLAG_FILE)
    print("Stopped by user")