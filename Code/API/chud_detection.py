import cv2
import numpy as np
import camera_email

global chud_detected
chud_detected = False


def detect(img):
    global chud_detected
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 1. Mild blur to keep small details intact
    gauss = cv2.GaussianBlur(hsv, (5, 5), 0)

    # 2. ADJUSTED BACKGROUND MASKS

    # FIX: Lowered upper saturation from 90 to 55.
    # A threshold of 90 was eating vibrant colors that looked slightly washed out under room lights.
    # 55 is tight enough to only catch true grayscale (white/grey) and pale tans/tiles.
    lower_bg_desat = np.array([0, 0, 0])
    upper_bg_desat = np.array([180, 55, 255])

    # FIX: Lowered upper value from 60 to 45.
    # This ensures deep shadows and dark surfaces are masked out,
    # but dark variations of a colored alien won't be accidentally deleted.
    lower_bg_dark = np.array([0, 0, 0])
    upper_bg_dark = np.array([180, 255, 45])

    # Catch the highly saturated blue tape (Keep this as is)
    lower_tape = np.array([90, 60, 50])
    upper_tape = np.array([130, 255, 255])

    # 3. Create the masks
    mask_desat = cv2.inRange(gauss, lower_bg_desat, upper_bg_desat)
    mask_dark = cv2.inRange(gauss, lower_bg_dark, upper_bg_dark)
    mask_tape = cv2.inRange(gauss, lower_tape, upper_tape)

    # 4. Combine all background elements
    background_mask = cv2.bitwise_or(mask_desat, mask_dark)
    background_mask = cv2.bitwise_or(background_mask, mask_tape)

    # 5. INVERT THE MASK - Anything left over is an anomaly (The Alien)
    anomaly_mask = cv2.bitwise_not(background_mask)

    # 6. FIX: Shrink the cleanup kernel from (5,5) to (3,3)
    # A 5x5 opening completely erases small objects. A 3x3 kernel clears
    # camera grain without destroying a "little figure".
    kernel = np.ones((3, 3), np.uint8)
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

            # FIX: Lowered area threshold from 150 to 35.
            # If the figure is small or far away, its pixel footprint will be tiny.
            if area > 35:
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

                # Found a valid anomaly, break the loop
                break

    return output_img, cropped_robot