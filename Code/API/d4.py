import cv2
import numpy as np
import the_robot_photo
import movement
LOWER_BLUE = np.array([100, 100, 50])
UPPER_BLUE = np.array([130, 255, 255])

try:
    while True:
        img = the_robot_photo.capture_photo_linux()
        if img is None: continue
        img = cv2.resize(img, (320, 240))
        h, w = img.shape[:2]
        center_x = w // 2
        roi_mask = np.zeros((h, w), dtype=np.uint8)
        pts = np.array([[int(w * 0.05), int(h * 0.95)], [int(w * 0.95), int(h * 0.95)], [w // 2, int(h * 0.05)]])
        cv2.fillPoly(roi_mask, [pts], 255)
        img_roi = cv2.bitwise_and(img, img, mask=roi_mask)
        hsv = cv2.cvtColor(img_roi, cv2.COLOR_BGR2HSV)
        blue_mask = cv2.inRange(hsv, LOWER_BLUE, UPPER_BLUE)
        lines = cv2.HoughLinesP(blue_mask, 2, np.pi / 180, threshold=40, minLineLength=20, maxLineGap=80)

        left_exists = False
        right_exists = False

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                dx = x2 - x1
                if dx == 0: continue
                slope = (y2 - y1) / dx
                if slope < -0.3 and x1 < center_x:
                    left_exists = True
                elif slope > 0.3 and x1 > center_x:
                    right_exists = True
                if left_exists and right_exists: break
        if left_exists and right_exists:
            movement.move_forward(100, 0.1)
            direction = "FORWARD"
        elif left_exists:
            movement.move_right(85, 0.1)
            direction = "RIGHT"
        elif right_exists:
            movement.move_left(85, 0.1)
            direction = "LEFT"
        else:
            movement.move_forward(60, 0.1)
            direction = "SEARCHING"
except KeyboardInterrupt:
    movement.stop()
