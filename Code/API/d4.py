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
        lower_blue = np.array([90, 80, 50])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        roi_mask = np.zeros_like(mask)
        cv2.rectangle(roi_mask, (0, h // 2), (w, h), 255, -1)
        mask = cv2.bitwise_and(mask, roi_mask)

        cv2.line(output_img, (0, h // 2), (w, h // 2), (0, 255, 0), 2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        valid_contours = [c for c in contours if cv2.contourArea(c) > 300]
        valid_contours = sorted(valid_contours, key=cv2.contourArea, reverse=True)

        direction = "SEARCHING"
        target_cx = None
        target_cy = None

        if len(valid_contours) >= 2:
            M1 = cv2.moments(valid_contours[0])
            M2 = cv2.moments(valid_contours[1])

            if M1["m00"] > 0 and M2["m00"] > 0:
                cx1 = int(M1["m10"] / M1["m00"])
                cy1 = int(M1["m01"] / M1["m00"])
                cx2 = int(M2["m10"] / M2["m00"])
                cy2 = int(M2["m01"] / M2["m00"])

                target_cx = (cx1 + cx2) // 2
                target_cy = (cy1 + cy2) // 2

                cv2.circle(output_img, (cx1, cy1), 5, (255, 0, 0), -1)
                cv2.circle(output_img, (cx2, cy2), 5, (255, 0, 0), -1)

        elif len(valid_contours) == 1:
            M = cv2.moments(valid_contours[0])
            if M["m00"] > 0:
                target_cx = int(M["m10"] / M["m00"])
                target_cy = int(M["m01"] / M["m00"])

        if target_cx is not None:
            cv2.circle(output_img, (target_cx, target_cy), 8, (0, 0, 255), -1)
            cv2.arrowedLine(output_img, (center_x, h), (target_cx, target_cy), (0, 0, 255), 3)

            error = target_cx - center_x

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