import cv2
import numpy as np
import camera_email

global chud_detected
chud_detected = False


def detect(img):
    global chud_detected
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 1. Increase blur slightly to smooth out harsh edges where tape meets floor
    gauss = cv2.GaussianBlur(hsv, (7, 7), 0)

    # 2. BROAD BACKGROUND MASKS
    # Instead of highly specific ranges, use broad bins to catch all background elements.

    # Catch ALL low-saturation colors (Tiles, Grout, Robot Sticker, Dust)
    # This covers tans, whites, grays, and pale colors.
    lower_bg_desat = np.array([0, 0, 0])
    upper_bg_desat = np.array([180, 90, 255])

    # Catch ALL low-value colors (Robot Chassis, Treads, Deep Shadows)
    # This covers blacks and dark grays across all hues.
    lower_bg_dark = np.array([0, 0, 0])
    upper_bg_dark = np.array([180, 255, 60])

    # Catch the highly saturated blue tape
    lower_tape = np.array([90, 60, 50])
    upper_tape = np.array([130, 255, 255])

    # 3. Create the masks
    mask_desat = cv2.inRange(gauss, lower_bg_desat, upper_bg_desat)
    mask_dark = cv2.inRange(gauss, lower_bg_dark, upper_bg_dark)
    mask_tape = cv2.inRange(gauss, lower_tape, upper_tape)

    # 4. Combine all background elements into one massive background map
    background_mask = cv2.bitwise_or(mask_desat, mask_dark)
    background_mask = cv2.bitwise_or(background_mask, mask_tape)

    # 5. INVERT THE MASK - Anything left over is the anomaly (The Alien)
    # Because the purple alien has a hue of ~140, high saturation, and high value,
    # it safely falls completely outside our broad background masks.
    anomaly_mask = cv2.bitwise_not(background_mask)

    # 6. Clean up noise
    # Increased kernel to (5,5) to eat the noise generated at the edges of the tape
    kernel = np.ones((5, 5), np.uint8)
    clean_mask = cv2.morphologyEx(anomaly_mask, cv2.MORPH_OPEN, kernel)
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_CLOSE, kernel)

    # 7. Find contours of the anomalies
    contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output_img = img.copy()
    chud_detected = False
    cropped_robot = None

    if contours:
        for contour in contours:
            area = cv2.contourArea(contour)

            # CRITICAL FIX: Increased threshold to 150.
            # 30 is too small and will detect single flecks of dirt or camera noise.
            # The alien object is large enough to easily pass 150 area.
            if area > 150:
                chud_detected = True
                x, y, w, h = cv2.boundingRect(contour)

                # Adjust height factor for the crop box
                height_multiplier = 1.3
                h = int(h * height_multiplier)
                if y + h > img.shape[0]:
                    h = img.shape[0] - y

                # Draw a red bounding box around the detected anomaly
                cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 0, 255), 4)

                # Crop out the detected object
                cropped_robot = img[y:y + h, x:x + w]

                # We found a valid anomaly, break the loop
                break

    return output_img, cropped_robot