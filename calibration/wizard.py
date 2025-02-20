
import cv2
import numpy as np
import json
from typing import List, Optional
from dataclasses import dataclass

# Constants matching our React implementation
CHECKERBOARD_SIZE = (8, 6)
MIN_CAPTURES_REQUIRED = 15

@dataclass
class CalibrationResult:
    camera_matrix: np.ndarray
    dist_coeffs: np.ndarray
    reprojection_error: float

class CalibrationWizard:
    def __init__(self):
        self.cameras: List[cv2.VideoCapture] = []
        self.current_step = 0
        self.captured_images: List[np.ndarray] = []
        self.calibration_results: Optional[CalibrationResult] = None

    def identify_cameras(self) -> bool:
        """Step 1: Camera Identification"""
        print("\n=== Step 1: Camera Identification ===")
        
        # Try to identify up to 3 cameras
        for i in range(3):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.cameras.append(cap)
                print(f"Camera {i + 1} initialized successfully")
                
                # Display camera properties
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                fps = cap.get(cv2.CAP_PROP_FPS)
                print(f"Resolution: {width}x{height}, FPS: {fps}")
            else:
                print(f"Could not initialize camera {i + 1}")

        return len(self.cameras) > 0

    def capture_calibration_frames(self, camera_index: int = 0) -> bool:
        """Step 2: Intrinsic Calibration"""
        print(f"\n=== Step 2: Intrinsic Calibration - Camera {camera_index + 1} ===")
        # ... keep existing code (the long capture_calibration_frames method)

    def save_calibration_results(self, camera_index: int):
        """Save calibration results to a JSON file"""
        if self.calibration_results is None:
            return

        results = {
            'camera_matrix': self.calibration_results.camera_matrix.tolist(),
            'dist_coeffs': self.calibration_results.dist_coeffs.tolist(),
            'reprojection_error': float(self.calibration_results.reprojection_error)
        }

        filename = f'camera_{camera_index}_calibration.json'
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nCalibration results saved to {filename}")

    def cleanup(self):
        """Release all camera resources"""
        for cap in self.cameras:
            cap.release()
        cv2.destroyAllWindows()
