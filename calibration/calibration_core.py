
import cv2
import numpy as np
import os

# Constants
CHECKERBOARD_SIZE = (7, 5)  # Inner corners
CAMERA_INDICES = [0, 1, 2] #camera indexes
MIN_CAPTURES_REQUIRED = 15 # Minimum captures

# Termination criteria for the iterative optimization algorithm
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((CHECKERBOARD_SIZE[0] * CHECKERBOARD_SIZE[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD_SIZE[0], 0:CHECKERBOARD_SIZE[1]].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

def run_intrinsic_calibration(camera_index):
    """Runs the intrinsic calibration process for the specified camera."""

    cap = cv2.VideoCapture(camera_index)  # Open camera with given index

    if not cap.isOpened():
        print(f"Error: Cannot open camera {camera_index}")
        return False

    # Create the display window
    cv2.namedWindow(f"Camera {camera_index}", cv2.WINDOW_NORMAL)
        
    # Keep reading frames until we have at least 15 captures
    while len(imgpoints) < MIN_CAPTURES_REQUIRED:
        ret, frame = cap.read()  # Read a frame from the camera
        if not ret:
            print(f"Error: Can't receive frame from camera {camera_index}. Exiting.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD_SIZE, None)
        if ret:
            # Refine the corners
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            # Draw and display the corners
            cv2.drawChessboardCorners(frame, CHECKERBOARD_SIZE, corners2, ret)
            cv2.imshow(f"Camera {camera_index}", frame)
            cv2.waitKey(500)  # Wait 500ms to display the corners

            # Add object points, image points (after refining them)
            objpoints.append(objp)
            imgpoints.append(corners2)

            print(f"Checkerboard found and added to image points! {len(imgpoints)}/{MIN_CAPTURES_REQUIRED}")

        else:
            print("Checkerboard not found.")
            cv2.imshow(f"Camera {camera_index}", frame)
        if cv2.waitKey(1) == ord('q'):  # Press 'q' to quit and start calibration
            break

    cap.release()  # Release camera
    cv2.destroyAllWindows()  # Close display window

    if len(objpoints) == 0 or len(imgpoints) == 0:
        print("Error: No valid images for calibration.")
        return False
    print("Performing calibration...")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    if not ret:
        print("Error: Camera calibration failed.")
        return False

    # Print calibration results
    print("\nCamera matrix:")
    print(mtx)
    print("\nDistortion coefficients:")
    print(dist)

    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        mean_error += error

    print("\nTotal error: {}".format(mean_error / len(objpoints)))

    # Save camera calibration data.
    print (f"Saving calibration data to calib_cam_{camera_index}.npz")
    np.savez(f"calib_cam_{camera_index}.npz", mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
    print("Calibration data saved.")
    return True
