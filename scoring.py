import numpy as np
import cv2
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class ScoringZone:
    points: int
    center: np.ndarray
    radius: float
    confidence: float

class ScoringSystem:
    def __init__(self):
        # Standard dartboard measurements (in meters)
        self.double_ring_radius = 0.170
        self.triple_ring_radius = 0.107
        self.bullseye_radius = 0.0127
        self.double_bull_radius = 0.0318
        self.scoring_zones = self._initialize_scoring_zones()

    def _initialize_scoring_zones(self) -> dict:
        # Define all scoring zones with their positions
        zones = {}
        sections = 20  # Standard dartboard has 20 sections
        for i in range(sections):
            angle = (2 * np.pi * i) / sections
            # Standard dartboard scoring arrangement
            number = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5][i]
            
            zones[f"single_{number}"] = {
                'points': number,
                'multiplier': 1,
                'angle_start': angle,
                'angle_end': angle + (2 * np.pi / sections)
            }
            zones[f"double_{number}"] = {
                'points': number * 2,
                'multiplier': 2,
                'radius_inner': self.double_ring_radius - 0.008,
                'radius_outer': self.double_ring_radius
            }
            zones[f"triple_{number}"] = {
                'points': number * 3,
                'multiplier': 3,
                'radius_inner': self.triple_ring_radius - 0.008,
                'radius_outer': self.triple_ring_radius
            }
        
        return zones

    def detect_impact(self, position: np.ndarray, calibration_data: dict) -> Tuple[int, float]:
        """
        Detect which scoring zone was hit and return points and confidence
        """
        try:
            # Transform position to dartboard coordinate system
            board_position = self._transform_to_board_coordinates(position, calibration_data)
            
            # Calculate distance from center and angle
            distance = np.linalg.norm(board_position[:2])
            angle = np.arctan2(board_position[1], board_position[0])
            if angle < 0:
                angle += 2 * np.pi

            # Check special cases (bullseye)
            if distance <= self.double_bull_radius:
                return 50, 0.95
            elif distance <= self.bullseye_radius:
                return 25, 0.90

            # Find the scoring section
            section_angle = (2 * np.pi) / 20
            section_index = int(angle / section_angle)
            
            # Determine multiplier based on distance
            if abs(distance - self.double_ring_radius) < 0.008:
                multiplier = 2
            elif abs(distance - self.triple_ring_radius) < 0.008:
                multiplier = 3
            else:
                multiplier = 1

            # Get base points for section
            base_points = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5][section_index]
            
            # Calculate confidence based on distance from ideal position
            confidence = self._calculate_scoring_confidence(distance, angle, section_index)
            
            return base_points * multiplier, confidence

        except Exception as e:
            print(f"Error in score detection: {e}")
            return 0, 0.0

    def _calculate_scoring_confidence(self, distance: float, angle: float, section_index: int) -> float:
        """
        Calculate confidence score based on position accuracy
        """
        # Implement confidence calculation based on:
        # 1. Distance from ideal position
        # 2. Angle accuracy
        # 3. Camera calibration quality
        # Returns value between 0 and 1
        pass