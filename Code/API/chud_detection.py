import cv2
import numpy as np
import camera_email

# Added a counter variable alongside your boolean
global chud_detected
global detection_counter

chud_detected = False
detection_counter = 0


def detect(img):
    global chud_detected
    global detection_counter

    # 1. MASK OUT THE ROBOT CHASSIS
    # Calculate the bottom 25% of the image to ignore.
    # This prevents the white "Makita" text and chassis glares from triggering false positives.
    height, width = img.shape[:2]
    ignore_bottom_y = int(height * 0.75)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Standard blur to smooth out tile texture
    gauss = cv2.GaussianBlur(hsv, (5, 5), 0)

    # FINETUNED BACKGROUND MASKS
    lower_bg_desat = np.array([0, 0, 0])
    upper_bg_desat = np.array([180, 55, 255])

    lower_bg_dark = np.array([0, 0, 0])
    upper_bg_dark = np.array([180, 255, 40])

    lower_blue = np.array([90, 50, 40])
    upper_blue = np.array([125, 255, 255])

    # Create the masks
    mask_desat = cv2.inRange(gauss, lower_bg_desat, upper_bg_desat)
    mask_dark = cv2.inRange(gauss, lower_bg_dark, upper_bg_dark)
    mask_blue = cv2.inRange(gauss, lower_blue, upper_blue)

    # Combine background maps
    background_mask = cv2.bitwise_or(mask_desat, mask_dark)
    background_mask = cv2.bitwise_or(background_mask, mask_blue)

    # Invert - anything left over is our target
    anomaly_mask = cv2.bitwise_not(background_mask)

    # Morphology to clean up the mask
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

                # CRITICAL FIX: Ignore any contours that are located on the robot itself
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

    # --- NEW TICKER LOGIC ---
    if alien_found_this_frame:
        detection_counter += 1
    else:
        # Reset the counter if the frame is empty. This requires 3 CONSECUTIVE frames.
        # (If you just want 3 frames total, even if broken up, delete this else statement)
        detection_counter = 0

    # Check if we've hit our threshold
    if detection_counter >= 3:
        chud_detected = True
        # Optional: Reset the counter back to 0 here so it doesn't spam emails
        # while the alien continues to sit in front of the camera.
        # detection_counter = 0

    # Ensure your script expects these returns wherever detect() is called
    return output_img, cropped_robot, chud_detected