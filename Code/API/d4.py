import cv2
import numpy as np
import the_robot_photo
import movement

print("GNG PRESS Ctrl+C TO STOP.")

try:
    while True:
        the_robot_photo.capture_photo_linux()
        img = cv2.imread('lane.jpg')
        if img is None:
            continue

        h, w = img.shape[:2]
        center_x = w / 2

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 100, 50])
        upper_blue = np.array([130, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        v1, v2, v3 = [0, h], [w, h], [w // 2, int(h * 0.3)]
        pts = np.array([v1, v2, v3], np.int32)
        roi_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(roi_mask, [pts], 255)
        masked_blue = cv2.bitwise_and(blue_mask, roi_mask)

        lines = cv2.HoughLinesP(masked_blue, 1, np.pi / 180, threshold=30,
                                minLineLength=40, maxLineGap=100)

        left_x = []
        right_x = []

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                mid_x = (x1 + x2) / 2
                if mid_x < center_x:
                    left_x.append(mid_x)
                else:
                    right_x.append(mid_x)

        if len(left_x) > 0 and len(right_x) > 0:
            lane_center = (np.mean(left_x) + np.mean(right_x)) / 2
            cv2.line(img, (int(lane_center), h), (int(lane_center), int(h * 0.5)), (0, 255, 0), 5)

            error = lane_center - center_x
            if error > 20:
                direction = "RIGHT"
                movement.move_right(70, 0.1)
            elif error < -20:
                direction = "LEFT"
                movement.move_left(70, 0.1)
            else:
                direction = "FORWARD"
                movement.move_forward(70, 0.1)

        elif len(left_x) > 0:
            direction = "RIGHT (Adjusting)"
            movement.move_right(65, 0.15)
        elif len(right_x) > 0:
            direction = "LEFT (Adjusting)"
            movement.move_left(65, 0.15)
        else:
            direction = "SEARCHING"
            movement.move_forward(60, 0.1)

        print(f"Detected Direction: {direction}")
        movement.wait_for_completion()
        cv2.putText(output_img, f"Dir: {direction}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imwrite('lanes_result.jpg', output_img)

except KeyboardInterrupt:
    print("\nSTOPPING")
