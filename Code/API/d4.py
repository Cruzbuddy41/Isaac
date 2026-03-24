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
            print("error ur an idiot")
            continue

        h, w = img.shape[:2]
        center_x = w / 2
        v1 = [int(w * 0.4), int(h * 0.6)]  # Bottom Left
        v2 = [int(w * 0.6), int(h * 0.6)]  # Bottom Right
        v3 = [w // 2, int(h * 0.1)]  # Top Peak
        pts = np.array([v1, v2, v3], np.int32)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 100, 50])
        upper_blue = np.array([130, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        roi_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(roi_mask, [pts], 255)
        masked_blue = cv2.bitwise_and(blue_mask, roi_mask)
        lines = cv2.HoughLinesP(masked_blue, 1, np.pi / 180, threshold=30,
                                minLineLength=40, maxLineGap=100)
        output_img = img.copy()
        cv2.polylines(output_img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

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
            movement.move_forward(70, 0.3)
        elif len(left_slopes) > 0:
            direction = "RIGHT"
            movement.move_right(70, 0.3)
        elif len(right_slopes) > 0:
            direction = "LEFT"
            movement.move_left(70, 0.3)
        else:
            direction = "SEARCHING (FORWARD)"
            movement.move_forward(70, 0.3)
        print(f"Detected Direction: {direction}")
        cv2.putText(output_img, f"Dir: {direction}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imwrite('lanes_result.jpg', output_img)

        movement.wait_for_completion()

except KeyboardInterrupt:
    print("\nIM TRYING TO STOP GNG")