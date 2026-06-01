import cv2
import numpy as np
import camera_email

# Keep your globals
global chud_detected
global detection_counter

chud_detected = False
detection_counter = 0

def detect(img):
    global chud_detected
    global detection_counter

    # ... (Keep your chassis masking setup) ...
    height, width = img.shape[:2]
    ignore_bottom_y = int(height * 0.75)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gauss = cv2.GaussianBlur(hsv, (5, 5), 0)

    # --- REFINED BACKGROUND MASKS FOR image_0.png ---

    # Floor Mask: Explicitly targets the beige/yellowish tile color
    lower_floor = np.array([15, 10, 180])
    upper_floor = np.array([40, 120, 255])
    mask_floor = cv2.inRange(gauss, lower_floor, upper_floor)

    # Blue Tape Mask: A much more precise range for the saturated tape
    lower_blue = np.array([95, 120, 100])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(gauss, lower_blue, upper_blue)

    # Dark/Robot Mask: Focuses solely on very dark areas like the chassis and tracks
    lower_dark = np.array([0, 0, 0])
    upper_dark = np.array([180, 255, 60])
    mask_dark = cv2.inRange(gauss, lower_dark, upper_dark)

    # Keep a desaturated mask to catch any other light, neutral textures
    lower_bg_desat = np.array([0, 0, 180]) # Targets high value, low saturation
    upper_bg_desat = np.array([180, 60, 255])
    mask_desat = cv2.inRange(gauss, lower_bg_desat, upper_bg_desat)

    # --- Combine ALL background maps ---
    background_mask = cv2.bitwise_or(mask_floor, mask_blue)
    background_mask = cv2.bitwise_or(background_mask, mask_dark)
    background_mask = cv2.bitwise_or(background_mask, mask_desat)

    # --- Invert - anything left over is our target ---
    anomaly_mask = cv2.bitwise_not(background_mask)

    # ... (Keep your morphology and contour logic, it was sound) ...
    kernel_close = np.ones((7, 7), np.uint8)
    kernel_open = np.ones((3, 3), np.uint8)
    clean_mask = cv2.morphologyEx(anomaly_mask, cv2.MORPH_CLOSE, kernel_close)
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_OPEN, kernel_open)
    contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output_img = img.copy()
    chud_detected = False
    cropped_robot = None
    alien_found_this_frame = False

    if contours:
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 30:
                x, y, w, h = cv2.boundingRect(contour)
                if y > ignore_bottom_y:
                    continue
                aspect_ratio = float(w) / h
                if 0.4 < aspect_ratio < 2.5 and w < 150 and h < 150:
                    alien_found_this_frame = True
                    # Draw and break
                    cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 0, 255), 4)
                    cropped_robot = img[y:y + h, x:x + w]
                    break

    # ... (Keep ticker logic) ...
    if alien_found_this_frame:
        detection_counter += 1
    else:
        detection_counter = 0

    if detection_counter >= 3:
        chud_detected = True

    return output_img, cropped_robot, chud_detected