import cv2
import numpy as np
import movement
import time
print("wsp brodie")

cap = cv2.VideoCapture(0)

try:
    while True:
        ret, img = cap.read()
        if not ret:
            continue

        h, w = img.shape[:2]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        v1, v2, v3 = [int(w * 0.05), h - 1], [int(w * 0.95), h - 1], [w // 2, int(h * 0.3)]
        pts = np.array([v1, v2, v3], np.int32)
        roi_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(roi_mask, [pts], 255)
        masked_blue = cv2.bitwise_and(blue_mask, roi_mask)

        center_x = w // 2
        turn_y_boundary = int(h * 0.5)
        top_pixels = cv2.countNonZero(masked_blue[:turn_y_boundary, :])

        left_pixels = cv2.countNonZero(masked_blue[turn_y_boundary:, :center_x])
        right_pixels = cv2.countNonZero(masked_blue[turn_y_boundary:, center_x:])
        pixel_diff = right_pixels - left_pixels

        turn_threshold = 12000
        correction_threshold = 2000
        direction = "FORWARD"

        if top_pixels > turn_threshold:
            if right_pixels > left_pixels:
                direction = "HARD LEFT"
                movement.move_left(80, 2)
            else:
                direction = "HARD RIGHT"
                movement.move_right(80, 2)
        elif abs(pixel_diff) > correction_threshold:
            if pixel_diff > 0:
                direction = "SLIGHT LEFT"
                movement.move_left(80, 2)
            else:
                direction = "SLIGHT RIGHT"
                movement.move_right(80, 2)
        elif (left_pixels + right_pixels) > 500:
            direction = "FORWARD"
            movement.move_forward(80, 1)
        else:
            direction = "SEARCHING"
        time.sleep(2)
        output_img = img.copy()
        output_img[masked_blue > 0] = [0, 0, 255]
        cv2.polylines(output_img, [pts], True, (0, 255, 0), 2)
        cv2.putText(output_img, f"Dir: {direction}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imwrite('lanes_result.jpg', output_img)

except KeyboardInterrupt:
    try:
        movement.stop_all()
    except:
        movement.move_forward(0, 0)

finally:
    cap.release()
    cv2.destroyAllWindows()
