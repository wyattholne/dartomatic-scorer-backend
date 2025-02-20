from dataclasses import dataclass
from typing import List, Dict
import os

@dataclass
class AppConfig:
    DEBUG: bool = os.getenv('DEBUG', 'False') == 'True'
    CAMERA_IDS: List[str] = ['cam1', 'cam2']
    CALIBRATION_SETTINGS: Dict = {
        'marker_size': 0.05,
        'min_poses': 15,
        'error_threshold': 0.5
    }