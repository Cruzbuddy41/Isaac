import cv2
import numpy as np
import os


import the_robot_photo
import movement
import chud_detection
import camera_email

not_stop_count = 0
chud_detection.chud_detected = False
waittimer = 6

def regionOfInterest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img


def takeImage():
    global waittimer
    global not_stop_count
    direction = "SEARCHING"

    img = the_robot_photo.capture_photo_linux()
    if img is None:
        img = cv2.imread('lane.jpg')
    if img is None:
        return None, "ERROR"



    h, w = img.shape[:2]
    center_x = w // 2
    output_img = img.copy()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([100, 150, 100]), np.array([130, 255, 255]))
    edges = cv2.Canny(cv2.dilate(cv2.GaussianBlur(mask, (5, 5), 0), np.ones((5, 5), np.uint8), iterations=1), 50, 150)

    big_pts = np.array([[[0, h], [w, h], [w, 100], [0, 100]]], np.int32)
    small_pts = np.array([[[int(w * 0.3), int(h * 0.75)], [int(w * 0.7), int(h * 0.75)], [w // 2, int(h * 0.4)]]],
                         np.int32)

    big_lines = cv2.HoughLinesP(regionOfInterest(edges, big_pts), 1, np.pi / 180, 30, minLineLength=40, maxLineGap=50)
    small_lines = cv2.HoughLinesP(regionOfInterest(edges, small_pts), 1, np.pi / 180, 20, minLineLength=20,
                                  maxLineGap=50)

    r_det, l_det, t_det = False, False, False

    if big_lines is not None:
        for line in big_lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 999
            if slope > 0.3 and x1 > center_x:
                r_det = True
                cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            if slope < -0.3 and x1 < center_x:
                l_det = True
                cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 3)

    if small_lines is not None:
        t_det = True
        for line in small_lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(output_img, (x1, y1), (x2, y2), (255, 0, 0), 3)

    not_stop = True
    cv2.polylines(output_img, big_pts, True, (0, 255, 0), 2)
    cv2.polylines(output_img, small_pts, True, (0, 255, 255), 2)

    # ... (Keep all your existing lane tracking logic exactly the same) ...

    if t_det and l_det and r_det and not_stop:
        if not_stop_count <= 5:
            movement.move_left(55, 0.1)
            direction = "STOP"
            not_stop_count += 1
            print(not_stop_count)
        else:
            direction = "STOP"
            not_stop_count = 10
    elif t_det and r_det:
        direction = "LEFT"
    elif t_det and l_det:
        direction = "RIGHT"
    elif r_det or l_det:
        direction = "FORWARD"
    elif t_det:
        direction = "Searching for side"
    else:
        direction = "SEARCHING"

    # --- MINIMAL NECESSARY CHANGE HERE ---
    # Only count down and run the alien detector when the robot is actively SEARCHING
    if direction == "SEARCHING":
        if waittimer == 0:
            if not chud_detection.chud_detected:
                chud_detection.detect(img)
                if chud_detection.chud_detected == True:
                    print("Chud Detected")
                    camera_email.email(img)
        else:
            waittimer -= 1
    else:
        # Reset the timer if it finds the tape again, ensuring it doesn't
        # false-trigger during normal line navigation
        waittimer = 6

    cv2.putText(output_img, f"Dir: {direction}", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imwrite('lanes_result.jpg', output_img)
    return output_img, direction