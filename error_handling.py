from enum import Enum
from dataclasses import dataclass
from typing import Optional, Callable
import logging
import time

class ErrorType(Enum):
    CAMERA_DISCONNECTED = "camera_disconnected"
    CALIBRATION_LOST = "calibration_lost"
    MARKER_DETECTION_FAILED = "marker_detection_failed"
    TRACKING_LOST = "tracking_lost"
    PROCESSING_ERROR = "processing_error"

@dataclass
class SystemError:
    type: ErrorType
    message: str
    timestamp: float
    recovery_action: Optional[Callable] = None

class SystemMonitor:
    def __init__(self):
        self.errors = []
        self.warning_threshold = 3
        self.error_threshold = 5
        self.recovery_attempts = 0
        self.last_recovery_time = 0
        self.recovery_cooldown = 5.0  # seconds
        
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('DartSystem')

    def handle_error(self, error: SystemError) -> bool:
        """
        Handle system error and attempt recovery
        Returns True if recovery was successful
        """
        self.errors.append(error)
        self.logger.error(f"System error: {error.type.value} - {error.message}")

        # Check if we should attempt recovery
        current_time = time.time()
        if (current_time - self.last_recovery_time) < self.recovery_cooldown:
            return False

        try:
            if error.recovery_action:
                self.recovery_attempts += 1
                self.last_recovery_time = current_time
                
                # Attempt recovery
                success = error.recovery_action()
                
                if success:
                    self.logger.info(f"Recovery successful for {error.type.value}")
                    self.recovery_attempts = 0
                    return True
                else:
                    self.logger.warning(f"Recovery failed for {error.type.value}")
                    return False

        except Exception as e:
            self.logger.error(f"Recovery attempt failed with error: {str(e)}")
            return False

    def check_system_health(self) -> bool:
        """
        Check overall system health
        Returns True if system is healthy
        """
        recent_errors = [
            error for error in self.errors
            if time.time() - error.timestamp < 60.0
        ]

        if len(recent_errors) >= self.error_threshold:
            self.logger.critical("System health check failed: Too many recent errors")
            return False

        if self.recovery_attempts >= self.warning_threshold:
            self.logger.warning("System health warning: Multiple recovery attempts")
            return False

        return True

    def clear_errors(self):
        """
        Clear error history
        """
        self.errors = []
        self.recovery_attempts = 0