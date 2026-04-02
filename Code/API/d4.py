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
        lower_blue = np.array([100, 150, 100])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        blurred = cv2.GaussianBlur(mask, (5, 5), 0)
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(blurred, kernel, iterations=1)

        edge = cv2.Canny(dilated, 50, 150)
        v1 = [0, int(h * 0.95)]  # Bottom Left
        v2 = [int(w), int(h * 0.95)]  # Bottom Right
        v3 = [w // 2, 0]  # Top Peak
        pts = np.array([v1, v2, v3], np.int32)

        lines = cv2.HoughLinesP(edge, 1, np.pi / 180, threshold=30,
                                minLineLength=40, maxLineGap=50)

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
            movement.move_forward(80, 0.2)
        elif len(left_slopes) > 0:
            direction = "RIGHT"
            movement.move_right(55, 0.2)
        elif len(right_slopes) > 0:
            direction = "LEFT"
            movement.move_left(55, 0.2)
        else:
            direction = "SEARCHING"
            movement.move_forward(40, 0.1)
        cv2.polylines(output_img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(output_img, f"Dir: {direction}", (50, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imwrite('lanes_result.jpg', output_img)
        print(f"Status: {direction}")

        cv2.imwrite('test.jpg', mask)

except KeyboardInterrupt:
    movement.stop()
    print("Stopped by user")
