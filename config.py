import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    CAMERA_CONFIG = {
        'num_cameras': int(os.getenv('NUM_CAMERAS', '3')),
        'resolution': tuple(map(int, os.getenv('RESOLUTION', '1920,1080').split(',')))
    }