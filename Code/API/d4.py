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
    return cv2.bitwise_and(img, mask)


FLAG_FILE = 'stop.txt'
LOG_FILE = 'log.txt'

try:
    while True:
        if os.path.exists(FLAG_FILE):
            movement.stop_all()
            with open(LOG_FILE, 'w') as f: f.write("LOCKED (STOP)")
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

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([100, 150, 100]), np.array([130, 255, 255]))
        edges = cv2.Canny(cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1), 50, 150)
        big_pts = np.array([[[0, h], [w, h], [w, 100], [0, 100]]], np.int32)
        small_pts = np.array([[[int(w * 0.3), int(h * 0.75)], [int(w * 0.7), int(h * 0.75)], [w // 2, int(h * 0.4)]]],
                             np.int32)
        cv2.polylines(output_img, big_pts, True, (0, 255, 0), 2)  # Green ROI
        cv2.polylines(output_img, small_pts, True, (0, 255, 255), 2)  # Yellow ROI

        big_lines = cv2.HoughLinesP(regionOfInterest(edges, big_pts), 1, np.pi / 180, 30, minLineLength=40,
                                    maxLineGap=50)
        small_lines = cv2.HoughLinesP(regionOfInterest(edges, small_pts), 1, np.pi / 180, 20, minLineLength=20,
                                      maxLineGap=50)

        big_r, big_l, top = False, False, False
        if big_lines is not None:
            for line in big_lines:
                x1, y1, x2, y2 = line[0]
                slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 999
                if slope > 0.3 and x1 > center_x: big_r = True; cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                if slope < -0.3 and x1 < center_x: big_l = True; cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255),
                                                                          3)

        if small_lines is not None: top = True

        if top and big_l and big_r:
            direction = "STOP"; movement.stop_all()
        elif top and big_r:
            direction = "LEFT"; movement.move_left(55, 0.3)
        elif top and big_l:
            direction = "RIGHT"; movement.move_right(55, 0.3)
        else:
            direction = "FORWARD"; movement.move_forward(40, 0.3)

        with open(LOG_FILE, 'w') as f:
            f.write(direction)
        cv2.putText(output_img, f"Dir: {direction}", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imwrite('lanes_result.jpg', output_img)
        print(f"Driving: {direction}")

except KeyboardInterrupt:
    movement.stop_all()
    if os.path.exists(FLAG_FILE): os.remove(FLAG_FILE)