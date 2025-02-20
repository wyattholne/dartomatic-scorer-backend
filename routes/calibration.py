from flask import Blueprint, request, jsonify
import cv2
import cv2.aruco as aruco
import numpy as np
import base64
import logging
from datetime import datetime
import json
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create blueprint
calibration_bp = Blueprint('calibration', __name__)

def data_uri_to_cv2_img(data_uri):
    try:
        header, encoded = data_uri.split(",", 1)
        data = base64.b64decode(encoded)
        np_arr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Failed to decode image")
            
        return img
        
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")

class CalibrationState:
    def __init__(self):
        self.objpoints = []
        self.imgpoints = {}
        self.capture_counts = {0: 0, 1: 0, 2: 0}
        self.calibrated_cameras = set()
        self.calibration_status = {
            "status": "idle",
            "message": "Ready to start calibration",
            "progress": 0
        }
        self.camera_matrices = {}
        self.dist_coeffs = {}

class CalibrationQualityMetrics:
    def __init__(self):
        self.pose_history = []
        self.error_history = []
        self.min_poses = 15
        self.error_threshold = 0.5
        self.coverage_threshold = 0.7
        self.stability_threshold = 0.8
        
    def calculate_metrics(self, corners, ids, image_shape):
        """Calculate quality metrics for current frame"""
        metrics = {
            'reprojection_error': self.calculate_reprojection_error(corners, ids),
            'coverage': self.calculate_coverage(corners, image_shape),
            'stability': self.calculate_stability(corners),
            'pose_count': len(self.pose_history)
        }
        return metrics
        
    def calculate_reprojection_error(self, corners, ids):
        """Calculate reprojection error"""
        if corners is None or len(corners) == 0:
            return 0.0
            
        try:
            # Simple estimation based on corner positions
            error = np.std(corners.reshape(-1, 2))
            self.error_history.append(error)
            if len(self.error_history) > 10:  # Keep last 10 errors
                self.error_history.pop(0)
            return np.mean(self.error_history)
        except:
            return 0.0
    
    def calculate_coverage(self, corners, image_shape):
        """Calculate board coverage of image area"""
        if corners is None or len(corners) == 0:
            return 0.0
            
        try:
            h, w = image_shape
            image_area = h * w
            
            # Calculate convex hull of corners
            hull = cv2.convexHull(corners.reshape(-1, 2))
            board_area = cv2.contourArea(hull)
            
            return min(board_area / image_area, 1.0)
        except:
            return 0.0
    
    def calculate_stability(self, corners):
        """Calculate board position stability"""
        if corners is None or len(corners) == 0:
            return 0.0
            
        try:
            # Calculate current pose
            current_pose = np.mean(corners.reshape(-1, 2), axis=0)
            
            # Add to history
            self.pose_history.append(current_pose)
            if len(self.pose_history) > 10:  # Keep last 10 poses
                self.pose_history.pop(0)
            
            if len(self.pose_history) < 2:
                return 1.0
                
            # Calculate stability from pose differences
            diffs = np.diff(self.pose_history, axis=0)
            movement = np.mean(np.linalg.norm(diffs, axis=1))
            
            # Convert to stability score (0-1)
            stability = 1.0 / (1.0 + movement/50)  # 50 is scaling factor
            return stability
        except:
            return 0.0
    
    def generate_feedback(self, metrics):
        """Generate feedback messages based on metrics"""
        feedback = []
        
        if metrics['reprojection_error'] > self.error_threshold:
            feedback.append("Move board more slowly")
        if metrics['coverage'] < self.coverage_threshold:
            feedback.append("Cover more image area")
        if metrics['stability'] < self.stability_threshold:
            feedback.append("Hold board more steady")
        if metrics['pose_count'] < self.min_poses:
            feedback.append(f"Need {self.min_poses - metrics['pose_count']} more poses")
            
        if not feedback:
            feedback.append("Good capture!")
            
        return feedback

class CalibrationVisualizationSystem:
    def __init__(self):
        self.window_name = "Calibration System"
        self.debug_dir = "debug_images"
        self.setup_windows()
        self.initialize_parameters()
        self.setup_trackbars()
        
    def setup_windows(self):
        """Setup all visualization windows"""
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.namedWindow("Quality Metrics", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Coverage Map", cv2.WINDOW_NORMAL)
        cv2.namedWindow("3D View", cv2.WINDOW_NORMAL)
        
    def initialize_parameters(self):
        """Initialize visualization parameters"""
        self.overlay_alpha = 0.3
        self.history_length = 100
        self.position_history = []
        self.quality_history = []
        self.view_mode = 0  # 0: Normal, 1: Debug, 2: Advanced
        self.show_3d = True
        self.show_metrics = True
        self.show_feedback = True
        
    def setup_trackbars(self):
        """Setup interactive controls"""
        cv2.createTrackbar('Overlay Alpha', self.window_name, 30, 100, 
                          lambda x: setattr(self, 'overlay_alpha', x/100))
        cv2.createTrackbar('View Mode', self.window_name, 0, 2,
                          lambda x: setattr(self, 'view_mode', x))
        cv2.createTrackbar('Show 3D', self.window_name, 1, 1,
                          lambda x: setattr(self, 'show_3d', bool(x)))
        
    def create_visualization(self, frame, corners, ids, quality_metrics, calibration_state):
        """Create comprehensive visualization"""
        # Create main visualization
        main_vis = self.create_main_view(frame, corners, ids, quality_metrics)
        
        # Create quality metrics view
        metrics_vis = self.create_metrics_view(quality_metrics)
        
        # Create coverage map
        coverage_vis = self.create_coverage_view()
        
        # Create 3D view
        three_d_vis = self.create_3d_view(corners, ids) if self.show_3d else None
        
        # Show all windows
        cv2.imshow(self.window_name, main_vis)
        cv2.imshow("Quality Metrics", metrics_vis)
        cv2.imshow("Coverage Map", coverage_vis)
        if three_d_vis is not None:
            cv2.imshow("3D View", three_d_vis)
        
        return main_vis
    
    def create_main_view(self, frame, corners, ids, quality_metrics):
        """Create main visualization view"""
        vis_img = frame.copy()
        h, w = frame.shape[:2]
        
        # Create overlay based on view mode
        if self.view_mode == 0:  # Normal mode
            overlay = self.create_normal_overlay(corners, ids, h, w)
        elif self.view_mode == 1:  # Debug mode
            overlay = self.create_debug_overlay(corners, ids, h, w)
        else:  # Advanced mode
            overlay = self.create_advanced_overlay(corners, ids, h, w)
        
        # Add quality indicators
        self.add_quality_indicators(vis_img, quality_metrics)
        
        # Add feedback
        if self.show_feedback:
            self.add_feedback(vis_img, quality_metrics)
        
        # Blend overlay
        return cv2.addWeighted(vis_img, 1 - self.overlay_alpha, overlay, self.overlay_alpha, 0)
    
    def create_metrics_view(self, metrics):
        """Create quality metrics visualization"""
        h, w = 480, 640
        vis = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Update history
        self.quality_history.append(metrics)
        if len(self.quality_history) > self.history_length:
            self.quality_history.pop(0)
        
        # Draw graphs
        self.draw_metric_graphs(vis)
        
        # Draw current values
        self.draw_metric_values(vis, metrics)
        
        return vis
    
    def create_coverage_view(self):
        """Create coverage visualization"""
        h, w = 480, 640
        vis = np.zeros((h, w, 3), dtype=np.uint8)
        
        if self.position_history:
            # Create heatmap
            heatmap = self.calculate_coverage_heatmap(
                self.position_history,
                (h, w)
            )
            
            # Colorize heatmap
            vis = self.colorize_heatmap(heatmap)
            
            # Add coverage statistics
            self.add_coverage_stats(vis)
        
        return vis
    
    def create_3d_view(self, corners, ids):
        """Create 3D visualization"""
        h, w = 480, 640
        vis = np.zeros((h, w, 3), dtype=np.uint8)
        
        if corners is not None and ids is not None:
            # Estimate pose
            rvec, tvec = self.estimate_pose(corners, ids)
            
            if rvec is not None:
                # Draw 3D coordinate system
                self.draw_3d_coords(vis, rvec, tvec)
                
                # Draw 3D board model
                self.draw_3d_board(vis, rvec, tvec)
                
                # Add pose information
                self.add_pose_info(vis, rvec, tvec)
        
        return vis
    
    def add_quality_indicators(self, img, metrics):
        """Add quality indicators to image"""
        h, w = img.shape[:2]
        
        # Draw quality bars
        self.draw_quality_bars(img, metrics)
        
        # Draw stability indicator
        self.draw_stability_indicator(img, metrics['stability'])
        
        # Draw coverage indicator
        self.draw_coverage_indicator(img, metrics['coverage'])
    
    def draw_quality_bars(self, img, metrics):
        """Draw quality metric bars"""
        h, w = img.shape[:2]
        bar_h = 20
        bar_w = 150
        margin = 10
        
        metrics_to_show = [
            ('Reprojection Error', metrics['reprojection_error'], 0, 1, (0,165,255)),
            ('Coverage', metrics['coverage'], 0, 1, (0,255,0)),
            ('Stability', metrics['stability'], 0, 1, (255,0,0))
        ]
        
        for i, (name, value, min_val, max_val, color) in enumerate(metrics_to_show):
            y = margin + i * (bar_h + 5)
            
            # Draw bar background
            cv2.rectangle(img, (margin,y), (margin+bar_w,y+bar_h), (50,50,50), -1)
            
            # Draw bar value
            normalized = (value - min_val) / (max_val - min_val)
            cv2.rectangle(img, (margin,y), 
                        (margin+int(bar_w*normalized),y+bar_h), 
                        color, -1)
            
            # Draw text
            cv2.putText(img, f"{name}: {value:.2f}", (margin+bar_w+5, y+15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    
    def add_feedback(self, img, metrics):
        """Add real-time feedback messages"""
        h, w = img.shape[:2]
        
        feedback = []
        if metrics['reprojection_error'] > 0.5:
            feedback.append(("Move board more slowly", (0,165,255)))
        if metrics['coverage'] < 0.7:
            feedback.append(("Cover more image area", (0,255,0)))
        if metrics['stability'] < 0.8:
            feedback.append(("Hold board more steady", (255,0,0)))
        if not feedback:
            feedback.append(("Good capture!", (0,255,0)))
        
        # Draw feedback box
        y = h - 10
        for msg, color in reversed(feedback):
            cv2.putText(img, msg, (10, y), cv2.FONT_HERSHEY_SIMPLEX,
                       0.7, color, 2)
            y -= 25
    
    def save_debug_info(self, frame, corners, ids, metrics):
        """Save debug information"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save frame with detections
        debug_frame = frame.copy()
        if corners is not None:
            cv2.aruco.drawDetectedCornersCharuco(debug_frame, corners, ids)
        cv2.imwrite(f"{self.debug_dir}/frame_{timestamp}.jpg", debug_frame)
        
        # Save metrics
        with open(f"{self.debug_dir}/metrics_{timestamp}.json", 'w') as f:
            json.dump(metrics, f, indent=2)

# Create an instance of our visualization system
vis_system = CalibrationVisualizationSystem()

@calibration_bp.route('/capture_checkerboard_image', methods=['POST'])
def capture_checkerboard_image():
    try:
        # Get the image data from the POST request
        data = request.get_json()
        # Convert the base64 image to OpenCV format
        img = data_uri_to_cv2_img(data['image_data'])
        # Get which camera sent the image (0, 1, or 2)
        camera_index = int(data.get('camera_index', 0))
        
        # Try to find the ChArUco board in the image
        success, corners, ids = detect_pattern(img)
        
        # Calculate quality metrics (reprojection error, coverage, etc.)
        quality_metrics = calibration_metrics.calculate_metrics(
            corners, 
            ids, 
            img.shape[:2]
        )
        
        # Create the visualization with overlays
        vis_img = vis_system.create_visualization(
            img,
            corners,
            ids,
            quality_metrics,
            calibration_state
        )
        
        # Save images and metrics for debugging
        vis_system.save_debug_info(img, corners, ids, quality_metrics)
        
        # Convert the visualization image to base64 for web display
        _, buffer = cv2.imencode('.jpg', vis_img)
        vis_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Send back the results
        return jsonify({
            'success': success,  # Whether pattern was found
            'visualization': f'data:image/jpeg;base64,{vis_base64}',  # Image with overlays
            'quality_metrics': quality_metrics,  # Quality measurements
            'feedback': vis_system.generate_feedback(quality_metrics)  # User instructions
        }), 200
        
    except Exception as e:
        logger.exception("Error in capture_checkerboard_image")
        return jsonify({'error': str(e)}), 500

def detect_pattern(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        detector_params = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, detector_params)
        corners, ids, rejected = detector.detectMarkers(gray)
        
        if ids is not None and len(ids) > 0:
            return True, corners, ids
        return False, None, None
        
    except Exception as e:
        logger.error(f"Error in pattern detection: {str(e)}")
        return False, None, None

