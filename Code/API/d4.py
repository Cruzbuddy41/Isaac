import cv2
import numpy as np
import the_robot_photo
import movement

try:
    while True:
        img = the_robot_photo.capture_photo_linux()
        if img is None:
            img = cv2.imread('lane.jpg')
        if img is None:
            continue

        h, w = img.shape[:2]
        center_x = w // 2

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 100, 50])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        roi = np.zeros_like(mask)
        pts = np.array([[0, h], [w, h], [w, h // 2], [0, h // 2]], np.int32)
        cv2.fillPoly(roi, [pts], 255)
        mask = cv2.bitwise_and(mask, roi)

        M = cv2.moments(mask)
        output_img = img.copy()

        if M["m00"] > 500:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            error = cx - center_x
            cv2.circle(output_img, (cx, cy), 10, (0, 255, 0), -1)

            if abs(error) < 30:
                movement.move_forward(70, 0.1)
                direction = "FORWARD"
            elif error > 0:
                movement.move_right(80, 0.1)
                direction = "RIGHT"
            else:
                movement.move_left(80, 0.1)
                direction = "LEFT"
        else:
            movement.move_left(60, 0.1)
            direction = "SEARCHING"

        cv2.putText(output_img, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imwrite('lanes_result.jpg', output_img)
        print(f"Status: {direction}")

except KeyboardInterrupt:
    movement.stop()
