import cv2
import numpy as np
import camera_email


global chud_detected
chud_detected = False




def detect(img):
   global chud_detected
   hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   gauss = cv2.GaussianBlur(hsv, 5)
   # 1. Define Known Background Color Ranges (Lower, Upper)
   # Turquoise/Blue Tape (from your original code)
   lower_turquoise = np.array([80, 50, 50])
   upper_turquoise = np.array([100, 255, 255])


   # Grout Lines
   lower_grout = np.array([20, 10, 10])
   upper_grout = np.array([40, 35, 40])


   # Tiles
   lower_tile = np.array([25, 10, 55])
   upper_tile = np.array([50, 40, 90])


   # 2. Create masks for all allowed background elements
   mask_turquoise = cv2.inRange(gauss, lower_turquoise, upper_turquoise)
   mask_grout = cv2.inRange(gauss, lower_grout, upper_grout)
   mask_tile = cv2.inRange(gauss, lower_tile, upper_tile)


   # 3. Combine all allowed background elements into one mask
   # cv2.bitwise_or means "if it is tile OR grout OR tape, it is background"
   background_mask = cv2.bitwise_or(mask_turquoise, mask_grout)
   background_mask = cv2.bitwise_or(background_mask, mask_tile)


   # 4. INVERT THE MASK
   # Anything that is NOT background is now white (255), indicating an anomaly
   anomaly_mask = cv2.bitwise_not(background_mask)


   # 5. Clean up noise (stray pixels) using morphology
   kernel = np.ones((5, 5), np.uint8)
   clean_mask = cv2.morphologyEx(anomaly_mask, cv2.MORPH_OPEN, kernel)
   clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_CLOSE, kernel)


   # 6. Find contours of the anomalies
   contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


   output_img = img.copy()
   chud_detected = False


   if contours:
       # Find the largest anomalous object
       largest_contour = max(contours, key=cv2.contourArea)


       # Threshold to ignore tiny specs of noise/lighting changes
       if cv2.contourArea(largest_contour) > 500:
           chud_detected = True
           x, y, w, h = cv2.boundingRect(largest_contour)
           # Draw a red bounding box around the intruder/chud
           cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 0, 255), 4)


   if (chud_detected == True):
       print("Chud Detected")
       camera_email.email(img)