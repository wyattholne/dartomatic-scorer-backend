class CalibrationError(Exception):
    """Base exception for calibration errors"""
    pass

class CameraError(CalibrationError):
    """Exception raised for camera-related errors"""
    pass

class ConfigurationError(CalibrationError):
    """Exception raised for configuration-related errors"""
    pass