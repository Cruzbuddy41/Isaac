import cv2
import numpy as np
import camera_email

global chud_detected
chud_detected = False


def detect(img):
    global chud_detected
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 1. Standard blur to smooth out tile texture
    gauss = cv2.GaussianBlur(hsv, (5, 5), 0)

    # 2. FINETUNED BACKGROUND MASKS

    # White/Grey/Tan floor mask
    lower_bg_desat = np.array([0, 0, 0])
    upper_bg_desat = np.array([180, 55, 255])

    # FIX: Lowered upper value from 45 to 40.
    # Protects dark colored objects (like deep purple) from being treated as pure shadow.
    lower_bg_dark = np.array([0, 0, 0])
    upper_bg_dark = np.array([180, 255, 40])

    # FIX: Lowered upper hue from 135 to 125.
    # Blue painter's tape safely lives between 90-125. Dropping this to 125 prevents
    # the mask from stealing deep indigo/violet shades from your alien.
    lower_blue = np.array([90, 50, 40])
    upper_blue = np.array([125, 255, 255])

    # 3. Create the masks
    mask_desat = cv2.inRange(gauss, lower_bg_desat, upper_bg_desat)
    mask_dark = cv2.inRange(gauss, lower_bg_dark, upper_bg_dark)
    mask_blue = cv2.inRange(gauss, lower_blue, upper_blue)

    # 4. Combine background maps
    background_mask = cv2.bitwise_or(mask_desat, mask_dark)
    background_mask = cv2.bitwise_or(background_mask, mask_blue)

    # 5. Invert - anything left over is our target
    anomaly_mask = cv2.bitwise_not(background_mask)

    # 6. CRITICAL FIX: INVERT MORPHOLOGY ORDER & USE A CLOSING KERNEL FIRST
    # We use a larger 7x7 closing kernel to bridge the gaps caused by the tan dots.
    # This glues the fragmented purple parts back into one solid block.
    kernel_close = np.ones((7, 7), np.uint8)
    kernel_open = np.ones((3, 3), np.uint8)

    # Close the internal holes first, then clear tiny floor speckles
    clean_mask = cv2.morphologyEx(anomaly_mask, cv2.MORPH_CLOSE, kernel_close)
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_OPEN, kernel_open)

    # 7. Find contours
    contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output_img = img.copy()
    chud_detected = False
    cropped_robot = None

    if contours:
        for contour in contours:
            area = cv2.contourArea(contour)

            # Keep this threshold around 30-40 since the figure is physically small in frame
            if area > 30:
                chud_detected = True
                x, y, w, h = cv2.boundingRect(contour)

                # Expand crop box slightly
                h = int(h * 1.3)
                if y + h > img.shape[0]:
                    h = img.shape[0] - y

                # Draw bounding box
                cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 0, 255), 4)
                cropped_robot = img[y:y + h, x:x + w]
                break

    return output_img, cropped_robot