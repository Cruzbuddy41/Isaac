import cv2
import matplotlib.pyplot as plt
import numpy as np
import camera_email

def detect(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_turquoise = np.array([80, 50, 50])
    upper_turquoise = np.array([100, 255, 255])

    mask = cv2.inRange(hsv, lower_turquoise, upper_turquoise)

    kernel = np.ones((5, 5), np.uint8)

    clean_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output_img = img.copy()
    object_detected = False

    if contours:

        largest_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(largest_contour) > 500:
            object_detected = True

            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 255, 0), 4)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(clean_mask, cmap='gray')
    plt.title('Clean Mask (Grating Removed?)')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
    if object_detected:
        plt.title('Object Found!')
        print("Object Found")
        camera_email.email(output_img)
    else:
        plt.title('No Object Detected')
        print('No Object Detected')

    plt.show()

