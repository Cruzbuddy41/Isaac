import cv2
import numpy as np
import camera_email

global chud_detected
chud_detected = False


def detect(img):
    global chud_detected
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Smooth out camera grain noise
    gauss = cv2.GaussianBlur(hsv, (5, 5), 0)

    # -----------------------------------------------------------------
    # NEW LOGIC: Target the intruder directly by its color (Purple)
    # OpenCV Hue for purple is roughly between 115 and 160
    lower_purple = np.array([115, 50, 50])
    upper_purple = np.array([160, 255, 255])
    # -----------------------------------------------------------------

    # Create a mask that ONLY sees purple objects
    alien_mask = cv2.inRange(gauss, lower_purple, upper_purple)
    kernel = np.ones((5, 5), np.uint8)
    clean_mask = cv2.morphologyEx(alien_mask, cv2.MORPH_OPEN, kernel)
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output_img = img.copy()
    chud_detected = False
    cropped_robot = None

    if contours:
        # Find the largest purple object
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 100:
            chud_detected = True
            x, y, w, h = cv2.boundingRect(largest_contour)
            height_multiplier = 1.3
            h = int(h * height_multiplier)

            if y + h > img.shape[0]:
                h = img.shape[0] - y
            cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 0, 255), 4)
            cropped_robot = img[y:y + h, x:x + w]