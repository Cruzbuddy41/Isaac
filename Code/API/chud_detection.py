import cv2
import numpy as np
import camera_email

# Keep your counter variables alongside your boolean
global chud_detected
global detection_counter

chud_detected = False
detection_counter = 0


def detect(img):
    global chud_detected
    global detection_counter

    # 1. MASK OUT THE ROBOT CHASSIS
    height, width = img.shape[:2]
    ignore_bottom_y = int(height * 0.75)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Standard blur to smooth out tile texture
    gauss = cv2.GaussianBlur(hsv, (5, 5), 0)

    # --- PERFECTED COLOR RANGE FOR YOUR PURPLE ALIEN ---
    # Low bound dropped to 123 to capture the full indigo-purple spectrum in your photos
    lower_purple = np.array([15, 5, 40])
    upper_purple = np.array([35, 30, 70])

    # Directly isolate the purple alien object
    anomaly_mask = cv2.inRange(gauss, lower_purple, upper_purple)
    # ---------------------------------------------------

    # Morphology to clean up the mask (Kept exactly the same)
    kernel_close = np.ones((7, 7), np.uint8)
    kernel_open = np.ones((3, 3), np.uint8)

    clean_mask = cv2.morphologyEx(anomaly_mask, cv2.MORPH_CLOSE, kernel_close)
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_OPEN, kernel_open)

    # Find contours
    contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output_img = img.copy()
    chud_detected = False
    cropped_robot = None

    # Local flag to track if we saw an alien in THIS specific frame
    alien_found_this_frame = False

    if contours:
        for contour in contours:
            area = cv2.contourArea(contour)

            if area > 30:
                x, y, w, h = cv2.boundingRect(contour)

                # Ignore any contours that are located on the robot itself
                if y > ignore_bottom_y:
                    continue

                # Calculate the aspect ratio to filter out wires/lines
                aspect_ratio = float(w) / h

                if 0.4 < aspect_ratio < 2.5 and w < 150 and h < 150:
                    # We found a valid candidate!
                    alien_found_this_frame = True

                    # Expand crop box slightly
                    crop_h = int(h * 1.3)
                    if y + crop_h > img.shape[0]:
                        crop_h = img.shape[0] - y

                    # Draw bounding box
                    cv2.rectangle(output_img, (x, y), (x + w, y + crop_h), (0, 0, 255), 4)

                    # Crop out the detected object
                    cropped_robot = img[y:y + crop_h, x:x + w]

                    # Break loop since we found our target
                    break

    # --- TICKER LOGIC ---
    if alien_found_this_frame:
        detection_counter += 1
    else:
        detection_counter = 0

    # Check if we've hit our threshold (3 consecutive frames)
    if detection_counter >= 3:
        chud_detected = True

    return output_img, cropped_robot, chud_detected