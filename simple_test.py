import cv2
import numpy as np

def main():
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # Create ArUco dictionary
    # Try different dictionary types:
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)  # Try this first
    # aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)  # Or this
    # aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)  # Or this
    
    # Create detector
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect markers
        corners, ids, rejected = detector.detectMarkers(gray)
        
        # Draw results
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            print(f"Detected markers: {ids.flatten()}")
        
        # Show the frame
        cv2.imshow('Test Frame', frame)
        
        # Press 's' to save frame for debugging
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite('debug_frame.png', frame)
            cv2.imwrite('debug_gray.png', gray)
            print("Saved debug frames")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()