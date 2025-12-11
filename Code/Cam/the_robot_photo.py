import cv2
import time

def capture_photo_mac(filename="ph.jpg"):
    # 0 represents the first available camera (usually the built-in one)
    # If you have external cameras, you might use 1, 2, etc.
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Camera opened successfully. Capturing image in 2 seconds...")

    for i in range(30):
        cap.read()
        # Capture a single frame
    ret, frame = cap.read()

    # Release the camera resource
    cap.release()

    if ret:
        # Save the captured frame as a JPEG file
        cv2.imwrite(filename, frame)
        print(f"Picture saved successfully as {filename}")
    else:
        print("Error: Failed to capture frame.")

if __name__ == "__main__":
    capture_photo_mac()
