import cv2
import numpy as np
import logging
from dataclasses import dataclass
from typing import Tuple, List, Optional

@dataclass
class ArucoConfig:
    """Configuration for ArUco detection"""
    dictionary_type: int = cv2.aruco.DICT_5X5_250
    marker_size: float = 0.05  # marker size in meters
    camera_resolution: Tuple[int, int] = (1920, 1080)
    min_markers: int = 1

class ArucoDetector:
    def __init__(self, config: ArucoConfig):
        self.config = config
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(config.dictionary_type)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)
        self.logger = self._setup_logging()

    def _setup_logging(self):
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def detect_markers(self, frame: np.ndarray) -> Tuple[List, Optional[np.ndarray]]:
        """
        Detect ArUco markers in the given frame
        Returns: (corners, ids)
        """
        if frame is None:
            self.logger.error("No frame provided for marker detection")
            return [], None

        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Optional: Add preprocessing to improve detection
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            gray = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV, 11, 2
            )
            
            # Updated marker detection with modified parameters
            self.parameters.adaptiveThreshWinSizeMin = 3
            self.parameters.adaptiveThreshWinSizeMax = 23
            self.parameters.adaptiveThreshWinSizeStep = 10
            self.parameters.adaptiveThreshConstant = 7
            self.parameters.minMarkerPerimeterRate = 0.03
            self.parameters.maxMarkerPerimeterRate = 4.0
            self.parameters.polygonalApproxAccuracyRate = 0.03
            self.parameters.minCornerDistanceRate = 0.05
            self.parameters.minDistanceToBorder = 3
            
            corners, ids, rejected = self.detector.detectMarkers(gray)

            if ids is not None:
                self.logger.info(f"Detected {len(ids)} markers with IDs: {ids.flatten()}")
                return corners, ids
            else:
                self.logger.debug("No markers detected")
                return [], None

        except Exception as e:
            self.logger.error(f"Error in marker detection: {str(e)}")
            return [], None

    def draw_markers(self, frame: np.ndarray, corners: List, ids: np.ndarray) -> np.ndarray:
        """Draw detected markers on the frame"""
        if ids is not None and len(ids) > 0:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        return frame