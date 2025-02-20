import cv2
import numpy as np
from typing import List, Tuple, Optional
from aruco_detector import ArucoDetector, ArucoConfig
from camera_handler import CameraHandler
import logging

class MarkerTracker:
    def __init__(self, camera_id: int, aruco_config: ArucoConfig):
        self.camera_handler = CameraHandler(camera_id, aruco_config.camera_resolution)
        self.aruco_detector = ArucoDetector(aruco_config)
        self.logger = logging.getLogger(__name__)
        self.camera_matrix = None
        self.dist_coeffs = None

    def start(self) -> bool:
        """Start the marker tracking system"""
        return self.camera_handler.initialize()

    def stop(self):
        """Stop the marker tracking system"""
        self.camera_handler.release()

    def load_camera_calibration(self, calibration_file: str) -> bool:
        """Load camera calibration parameters"""
        try:
            calibration_data = np.load(calibration_file)
            self.camera_matrix = calibration_data['camera_matrix']
            self.dist_coeffs = calibration_data['dist_coeffs']
            return True
        except Exception as e:
            self.logger.error(f"Error loading calibration: {str(e)}")
            return False

    def track_markers(self) -> Tuple[Optional[np.ndarray], List, Optional[np.ndarray]]:
        """
        Track markers in real-time
        Returns: (frame, corners, ids)
        """
        frame = self.camera_handler.get_frame()
        if frame is None:
            return None, [], None

        corners, ids = self.aruco_detector.detect_markers(frame)
        if ids is not None:
            frame = self.aruco_detector.draw_markers(frame, corners, ids)
            
            if self.camera_matrix is not None and self.dist_coeffs is not None:
                rvecs, tvecs = self.aruco_detector.estimate_pose(
                    corners, ids, self.camera_matrix, self.dist_coeffs
                )
                frame = self.aruco_detector.draw_axes(
                    frame, corners, ids, rvecs, tvecs,
                    self.camera_matrix, self.dist_coeffs
                )

        return frame, corners, ids