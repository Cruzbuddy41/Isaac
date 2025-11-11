import cv2

# Open the default camera (usually index 0)
# If you have multiple cameras, you might need to try other indices (1, 2, etc.)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video device.")
else:
    # Loop to continuously capture frames
    while True:
        ret, frame = cap.read()  # Read a frame from the camera

        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the captured frame
        cv2.imshow('Logitech Camera Feed', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and destroy all windows when done
    cap.release()
    cv2.destroyAllWindows()

