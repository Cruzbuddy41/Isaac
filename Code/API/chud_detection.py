import cv2
import numpy as np
import camera_email

chud_detected = False


def detect(img):
    global chud_detected
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gauss = cv2.GaussianBlur(hsv, (5, 5), 0)

    lower_turquoise = np.array([80, 50, 50])
    upper_turquoise = np.array([100, 255, 255])
    lower_grout = np.array([20, 10, 10])
    upper_grout = np.array([40, 35, 40])
    lower_tile = np.array([25, 10, 55])
    upper_tile = np.array([50, 40, 90])

    mask_turquoise = cv2.inRange(gauss, lower_turquoise, upper_turquoise)
    mask_grout = cv2.inRange(gauss, lower_grout, upper_grout)
    mask_tile = cv2.inRange(gauss, lower_tile, upper_tile)

    background_mask = cv2.bitwise_or(mask_turquoise, mask_grout)
    background_mask = cv2.bitwise_or(background_mask, mask_tile)

    anomaly_mask = cv2.bitwise_not(background_mask)

    kernel = np.ones((5, 5), np.uint8)
    clean_mask = cv2.morphologyEx(anomaly_mask, cv2.MORPH_OPEN, kernel)
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output_img = img.copy()
    object_detected = False

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 500:
            object_detected = True
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 0, 255), 4)

    if object_detected:
        print("Chud Detected!")
        camera_email.email(output_img)
        chud_detected = True

    cv2.imwrite('anomaly_debug.jpg', clean_mask)