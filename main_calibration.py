import asyncio
import cv2
import numpy as np
from calibration_controller import AutomaticCalibrationSystem, CalibrationConfig
from ar_guidance import ARGuidanceSystem
from quality_assessment import QualityAssessor

async def main():
    # Initialize systems
    config = CalibrationConfig()
    calibration_system = AutomaticCalibrationSystem(config)
    ar_system = ARGuidanceSystem()
    quality_assessor = QualityAssessor()
    
    # Initialize cameras
    if not await calibration_system.initialize_cameras():
        return
    
    try:
        while True:
            frames = []
            quality_scores = []
            
            # Capture frames from all cameras
            for cap in calibration_system.cameras:
                ret, frame = cap.read()
                if not ret:
                    raise RuntimeError("Failed to capture frame")
                    
                # Detect ArUco markers
                corners, ids, rejected = cv2.aruco.detectMarkers(
                    frame, calibration_system.aruco_dict, 
                    parameters=calibration_system.aruco_params
                )
                
                # Assess quality
                quality = quality_assessor.assess_detection_quality(corners, ids)
                quality_scores.append(quality)
                
                # Add AR guidance
                frame = ar_system.create_calibration_overlay(
                    frame, ids is not None, quality)
                
                frames.append(frame)
            
            # Display all frames
            combined_frame = np.hstack(frames)
            cv2.imshow('Calibration Progress', combined_frame)
            
            # Auto-capture when quality is good
            if all(score > 0.8 for score in quality_scores):
                await calibration_system.capture_calibration_frame()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        for cap in calibration_system.cameras:
            cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())