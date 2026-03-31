import cv2
import numpy as np
import the_robot_photo
import movement
import chud_detection

try:
    while True:
        img = the_robot_photo.capture_photo_linux()
        if img is None:
            img = cv2.imread('lane.jpg')
        if img is None:
            continue

        chud_detection.detect(img)

        h, w = img.shape[:2]
        center_x = w // 2
        output_img = img.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 100, 50])
        upper_blue = np.array([130, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        v1 = [int(w * 0.05), int(h * 0.95)]  # Bottom Left
        v2 = [int(w * 0.95), int(h * 0.95)]  # Bottom Right
        v3 = [w // 2, int(h * 0.05)]  # Top Peak
        pts = np.array([v1, v2, v3], np.int32)

        roi_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(roi_mask, [pts], 255)
        masked_blue = cv2.bitwise_and(blue_mask, roi_mask)
        lines = cv2.HoughLinesP(masked_blue, 1, np.pi / 180, threshold=30,
                                minLineLength=40, maxLineGap=100)

        left_slopes = []
        right_slopes = []

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 999
                cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                if slope < -0.3 and x1 < center_x:
                    left_slopes.append(slope)
                elif slope > 0.3 and x1 > center_x:
                    right_slopes.append(slope)
        if len(left_slopes) > 0 and len(right_slopes) > 0:
            direction = "FORWARD"
            movement.move_forward(100, 0.2)
        elif len(left_slopes) > 0:
            direction = "RIGHT"
            movement.move_right(85, 0.2)
        elif len(right_slopes) > 0:
            direction = "LEFT"
            movement.move_left(85, 0.2)
        else:
            direction = "SEARCHING"
            movement.move_forward(60, 0.1)
        cv2.polylines(output_img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(output_img, f"Dir: {direction}", (50, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imwrite('lanes_result.jpg', output_img)
        print(f"Status: {direction}")

except KeyboardInterrupt:
    movement.stop()
    print("Stopped by user")

img = cv2.imread('lane.jpg')
if img is None:
    exit()

h, w = img.shape[:2]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

v1 = [int(w * 0.05), h - 1]
v2 = [int(w * 0.95), h - 1]
v3 = [w // 2, int(h * 0.3)]
pts = np.array([v1, v2, v3], np.int32)
roi_mask = np.zeros((h, w), dtype=np.uint8)
cv2.fillPoly(roi_mask, [pts], 255)

masked_blue = cv2.bitwise_and(blue_mask, roi_mask)

output_img = img.copy()
output_img[masked_blue > 0] = [0, 0, 255]
cv2.polylines(output_img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

center_x = w // 2
turn_y_boundary = int(h * 0.5)

turn_zone = masked_blue[:turn_y_boundary, :]
top_pixels = cv2.countNonZero(turn_zone)

correction_zone = masked_blue[turn_y_boundary:, :]
left_correction = correction_zone[:, :center_x]
right_correction = correction_zone[:, center_x:]

left_pixels = cv2.countNonZero(left_correction)
right_pixels = cv2.countNonZero(right_correction)
pixel_diff = right_pixels - left_pixels

cv2.line(output_img, (center_x, turn_y_boundary), (center_x, h), (255, 255, 0), 2)
cv2.line(output_img, (0, turn_y_boundary), (w, turn_y_boundary), (255, 165, 0), 2)

turn_threshold = 12000
correction_threshold = 2000

direction = "FORWARD"

if top_pixels > turn_threshold:
    if right_pixels > left_pixels:
        direction = "HARD LEFT"
    else:
        direction = "HARD RIGHT"
elif abs(pixel_diff) > correction_threshold:
    if pixel_diff > 0:
        direction = "SLIGHT LEFT"
    else:
        direction = "SLIGHT RIGHT"

cv2.putText(output_img, f"Dir: {direction}", (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(output_img, f"Top Px: {top_pixels} (Need >{turn_threshold})", (30, 90),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
cv2.putText(output_img, f"L: {left_pixels}  R: {right_pixels}", (30, 130),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
cv2.putText(output_img, f"Diff: {pixel_diff} (Need >{correction_threshold} or <-{correction_threshold})", (30, 170),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

cv2.imwrite('lanes_result.jpg', output_img)
