import cv2
import numpy as np
import camera_email

global chud_detected
chud_detected = False


def detect(img):
    global chud_detected
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gauss = cv2.GaussianBlur(hsv, (5, 5), 0)
    # Blue Tape
    lower_turquoise = np.array([85, 40, 40])
    upper_turquoise = np.array([130, 255, 255])

    # Grout Lines
    lower_grout = np.array([10, 5, 20])
    upper_grout = np.array([40, 60, 160])

    # Tiles
    lower_tile = np.array([10, 2, 50])
    upper_tile = np.array([40, 80, 255])

    lower_robot_black = np.array([0, 0, 0])
    upper_robot_black = np.array([180, 255, 75])

    lower_robot_silver = np.array([0, 0, 70])
    upper_robot_silver = np.array([180, 35, 255])
    mask_turquoise = cv2.inRange(gauss, lower_turquoise, upper_turquoise)
    mask_grout = cv2.inRange(gauss, lower_grout, upper_grout)
    mask_tile = cv2.inRange(gauss, lower_tile, upper_tile)
    mask_robot_black = cv2.inRange(gauss, lower_robot_black, upper_robot_black)
    mask_robot_silver = cv2.inRange(gauss, lower_robot_silver, upper_robot_silver)

    background_mask = cv2.bitwise_or(mask_turquoise, mask_grout)
    background_mask = cv2.bitwise_or(background_mask, mask_tile)
    background_mask = cv2.bitwise_or(background_mask, mask_robot_black)
    background_mask = cv2.bitwise_or(background_mask, mask_robot_silver)

    anomaly_mask = cv2.bitwise_not(background_mask)
    kernel = np.ones((5, 5), np.uint8)
    clean_mask = cv2.morphologyEx(anomaly_mask, cv2.MORPH_OPEN, kernel)
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output_img = img.copy()
    chud_detected = False
    cropped_robot = None

    if contours:
        #finds largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 4000:
            chud_detected = True
            x, y, w, h = cv2.boundingRect(largest_contour)
            height_multiplier = 1.3
            h = int(h * height_multiplier)

            if y + h > img.shape[0]:
                h = img.shape[0] - y
            cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 0, 255), 4)
            cropped_robot = img[y:y + h, x:x + w]

    return output_img, cropped_robot