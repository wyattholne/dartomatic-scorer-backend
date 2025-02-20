import cv2
from aruco_detector import ArucoConfig
from marker_tracker import MarkerTracker

def main():
    # Create configuration with more lenient settings
    config = ArucoConfig(
        dictionary_type=cv2.aruco.DICT_5X5_250,
        marker_size=0.05,
        camera_resolution=(1920, 1080),
        min_markers=1  # Changed from 4 to 1 to detect single markers
    )

    # Create tracker
    tracker = MarkerTracker(camera_id=0, aruco_config=config)

    # Start tracking
    if not tracker.start():
        print("Failed to start tracker")
        return

    try:
        while True:
            # Track markers
            frame, corners, ids = tracker.track_markers()
            
            if frame is not None:
                # Add debug info to frame
                if ids is not None:
                    print(f"Detected markers: {ids.flatten()}")
                else:
                    cv2.putText(frame, "No markers detected", (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Display frame size
                height, width = frame.shape[:2]
                cv2.putText(frame, f"Frame: {width}x{height}", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Display results
                cv2.imshow('ArUco Detection', frame)
                
                # Break loop on 'q' press
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):  # Save frame for debugging
                    cv2.imwrite('debug_frame.png', frame)
                    print("Saved debug frame")
            else:
                print("Failed to get frame")
                break

    finally:
        # Cleanup
        tracker.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

