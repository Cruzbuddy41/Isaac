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
            print("error loading image")
            continue

        h, w = img.shape[:2]
        center_x = w // 2
        roi_top = int(h * 0.5)
        roi_bottom = h

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 100, 50])
        upper_blue = np.array([130, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        roi_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.rectangle(roi_mask, (0, roi_top), (w, roi_bottom), 255, -1)
        masked_blue = cv2.bitwise_and(blue_mask, roi_mask)
        M = cv2.moments(masked_blue)

        output_img = img.copy()
        cv2.line(output_img, (center_x, 0), (center_x, h), (0, 255, 0), 2)

        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cv2.line(output_img, (cx, roi_top), (cx, roi_bottom), (0, 0, 255), 5)
            error = cx - center_x

            if error > 40:
                direction = "RIGHT"
                movement.move_right(70, 0.1)
            elif error < -40:
                direction = "LEFT"
                movement.move_left(70, 0.1)
            else:
                direction = "FORWARD"
                movement.move_forward(70, 0.1)
        else:
            direction = "SEARCHING"
            movement.move_forward(50, 0.1)

        print(f"Detected Direction: {direction}")
        cv2.putText(output_img, f"Dir: {direction}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imwrite('lanes_result.jpg', output_img)

        movement.wait_for_completion()

except KeyboardInterrupt:
    print("\nSTOPPING...")
