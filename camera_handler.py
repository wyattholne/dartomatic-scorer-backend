import cv2
import numpy as np
from typing import Tuple, Optional
import logging

class CameraHandler:
    def __init__(self, camera_id: int, resolution: Tuple[int, int]):
        self.camera_id = camera_id
        self.resolution = resolution
        self.cap = None
        self.logger = logging.getLogger(__name__)

    def initialize(self) -> bool:
        """Initialize the camera"""
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            if not self.cap.isOpened():
                self.logger.error(f"Failed to open camera {self.camera_id}")
                return False

            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            return True

        except Exception as e:
            self.logger.error(f"Error initializing camera: {str(e)}")
            return False

    def get_frame(self) -> Optional[np.ndarray]:
        """Capture a frame from the camera"""
        if self.cap is None or not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()
        if not ret:
            self.logger.error("Failed to capture frame")
            return None

        return frame

    def release(self):
        """Release the camera"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None