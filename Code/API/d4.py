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
        output_img = img.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 100, 50])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        roi_mask = np.zeros_like(mask)
        roi_pts = np.array([[0, h], [w, h], [center_x, h // 2]], np.int32)
        cv2.fillPoly(roi_mask, [roi_pts], 255)
        mask = cv2.bitwise_and(mask, roi_mask)
        cv2.line(output_img, (0, h), (center_x, h // 2), (0, 255, 0), 2)
        cv2.line(output_img, (w, h), (center_x, h // 2), (0, 255, 0), 2)
        M = cv2.moments(mask)
        if M["m00"] > 500:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            error = cx - center_x
            path_pts = np.array([[0, h], [cx, cy], [cx - 20, h]], np.int32)
            cv2.fillPoly(output_img, [path_pts], (0, 0, 255))
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
        cv2.putText(output_img, f"Dir: {direction}", (50, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imwrite('lanes_result.jpg', output_img)
        print(f"Status: {direction}")

except KeyboardInterrupt:
    movement.stop()
