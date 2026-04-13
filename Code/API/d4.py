import cv2
import numpy as np
import time
import the_robot_photo
import movement
import chud_detection
DEBUG_MODE = False


def regionOfInterest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    return cv2.bitwise_and(img, mask)


try:
    while True:
        start_time = time.time()

        img = the_robot_photo.capture_photo_linux()
        if img is None:
            print("Camera failed, using fallback image.")
            img = cv2.imread('lane.jpg')
            time.sleep(0.1)

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
        edges = cv2.Canny(dilated, 50, 150)
        big_pts = np.array([[[0, h], [w, h], [w // 2, int(h * 0.4)]]], np.int32)
        small_pts = np.array([[[int(w * 0.3), int(h * 0.75)],
                               [int(w * 0.7), int(h * 0.75)],
                               [w // 2, int(h * 0.4)]]], np.int32)

        big_edges = regionOfInterest(edges, big_pts)
        small_edges = regionOfInterest(edges, small_pts)
        big_lines = cv2.HoughLinesP(big_edges, 1, np.pi / 180, threshold=30, minLineLength=40, maxLineGap=50)
        small_lines = cv2.HoughLinesP(small_edges, 1, np.pi / 180, threshold=20, minLineLength=20, maxLineGap=50)

        big_right_line_detected = False
        big_left_line_detected = False
        top_line_detected = False

        if big_lines is not None:
            for line in big_lines:
                x1, y1, x2, y2 = line[0]
                slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 999

                if slope > 0.3 and x1 > center_x:
                    big_right_line_detected = True
                    cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                elif slope < -0.3 and x1 < center_x:
                    big_left_line_detected = True
                    cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        if small_lines is not None:
            for line in small_lines:
                x1, y1, x2, y2 = line[0]
                top_line_detected = True
                cv2.line(output_img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.polylines(output_img, big_pts, isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.polylines(output_img, small_pts, isClosed=True, color=(0, 255, 255), thickness=2)
        if top_line_detected and big_right_line_detected:
            direction = "LEFT"
            movement.move_left(55, 0.5)
        elif top_line_detected and big_left_line_detected:
            direction = "RIGHT"
            movement.move_right(55, 0.5)
        elif (big_right_line_detected or big_left_line_detected) and not top_line_detected:
            direction = "FORWARD"
            movement.move_forward(80, 0.2)
        else:
            direction = "SEARCHING"
            movement.move_forward(40, 0.3)
        cv2.putText(output_img, f"Dir: {direction}", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        print(f"Status: {direction}")

        if DEBUG_MODE:
            cv2.imwrite('lanes_result.jpg', output_img)
            cv2.imwrite('test.jpg', mask)

except KeyboardInterrupt:
    movement.stop()
    print("Stopped by user")