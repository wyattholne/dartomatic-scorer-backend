import cv2
import numpy as np
from dataclasses import dataclass

@dataclass
class ARGuide:
    message: str
    position: tuple
    color: tuple
    thickness: int = 2

class ARGuidanceSystem:
    def __init__(self):
        self.guides = []
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.7

    def add_guide(self, frame, message: str, position: tuple, color=(0, 255, 0)):
        """Add AR guidance overlay to frame"""
        cv2.putText(frame, message, position, self.font, 
                   self.font_scale, color, 2)
        return frame

    def create_calibration_overlay(self, frame, markers_detected: bool, 
                                 quality_score: float):
        """Create helpful overlay for users during calibration"""
        if not markers_detected:
            self.add_guide(frame, "Move ArUco marker board slowly", 
                         (50, 50), (0, 0, 255))
        else:
            quality_color = (0, 255, 0) if quality_score > 0.8 else (0, 255, 255)
            self.add_guide(frame, f"Quality: {quality_score:.2f}", 
                         (50, 50), quality_color)
        return frame