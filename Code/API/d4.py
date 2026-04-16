import cv2
import numpy as np
import the_robot_photo
import movement
import chud_detection

def regionOfInterest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img

try:
    while True:
        img = the_robot_photo.capture_photo_linux()
        if img is None:
            img = cv2.imread('lane.jpg')
        if img is None:
            continue
        if not chud_detection.chud_detected:
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

        # Base edges for the whole image
        edges = cv2.Canny(dilated, 50, 150)
        # Big Triangle
        big_v1 = [0, h]  # Bottom Left
        big_v2 = [w, h]  # Bottom Right
        big_v3 = [w,100]
        big_v4 = [0,100]
        big_pts = np.array([[big_v1, big_v2, big_v3, big_v4]], np.int32)

        # Small Triangle
        small_v1 = [int(w * 0.3), int(h * 0.75)]
        small_v2 = [int(w * 0.7), int(h * 0.75)]
        small_v3 = [w // 2, int(h * 0.4)]
        small_pts = np.array([[small_v1, small_v2, small_v3]], np.int32)

        big_edges = regionOfInterest(edges, big_pts)
        small_edges = regionOfInterest(edges, small_pts)
        big_lines = cv2.HoughLinesP(big_edges, 1, np.pi / 180, threshold=30, minLineLength=40, maxLineGap=50)
        small_lines = cv2.HoughLinesP(small_edges, 1, np.pi / 180, threshold=20, minLineLength=20, maxLineGap=50)
        big_right_line_detected = False
        big_left_line_detected = False
        top_line_detected = False

        #right lines
        if big_lines is not None:
            for line in big_lines:
                x1, y1, x2, y2 = line[0]
                slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 999
                if slope > 0.3 and x1 > center_x:
                    big_right_line_detected = True
                    cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                if slope < -0.3 and x1 < center_x:
                    big_left_line_detected = True
                    cv2.line(output_img, (x1, y1), (x2, y2), (0,0,255), 3)

        #any lines in small triangle
        if small_lines is not None:
            for line in small_lines:
                x1, y1, x2, y2 = line[0]
                top_line_detected = True
                cv2.line(output_img, (x1, y1), (x2, y2), (255, 0, 0), 3)

        cv2.polylines(output_img, big_pts, isClosed=True, color=(0, 255, 0), thickness=2)  # Green = Big
        cv2.polylines(output_img, small_pts, isClosed=True, color=(0, 255, 255), thickness=2)  # Yellow = Small

        if top_line_detected and big_left_line_detected and big_right_line_detected:
            direction = "STOP"
            movement.stop_all()
        elif top_line_detected and big_right_line_detected:
            direction = "LEFT"
            movement.move_left(55, 0.3)
        elif big_right_line_detected and not top_line_detected:
            direction = "FORWARD"
            movement.move_forward(40, 0.3)
        elif(big_left_line_detected and not top_line_detected):
            direction = "FORWARD"
            movement.move_forward(40, 0.3)
        elif top_line_detected and big_left_line_detected:
            direction = "RIGHT"
            movement.move_right(55, 0.3)
        else:
            direction = "SEARCHING"
            movement.move_forward(40, 0.3)

        cv2.putText(output_img, f"Dir: {direction}", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imwrite('lanes_result.jpg', output_img)
        cv2.imwrite('test.jpg', mask)
        print(f"Status: {direction}")

except KeyboardInterrupt:
    movement.stop_all()
    print("Stopped by user")