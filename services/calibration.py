
import cv2
import numpy as np
import base64
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CalibrationService:
    def __init__(self):
        self.CHECKERBOARD_SIZE = (6, 9)
        self.captured_images = []
        self.calibration_data = None
        logger.info("CalibrationService initialized with checkerboard size: %s", self.CHECKERBOARD_SIZE)

    def data_uri_to_cv2_img(self, uri):
        try:
            logger.debug("Converting data URI to CV2 image")
            if not uri:
                logger.error("No URI provided")
                return None
                
            # Extract the base64 part
            if ',' in uri:
                encoded_data = uri.split(',')[1]
            else:
                logger.error("Invalid data URI format")
                return None

            # Decode base64
            decoded_data = base64.b64decode(encoded_data)
            np_data = np.frombuffer(decoded_data, np.uint8)
            img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            
            if img is None:
                logger.error("Failed to decode image")
                return None
                
            logger.debug("Successfully converted data URI to image with shape: %s", img.shape)
            return img
        except Exception as e:
            logger.exception("Error decoding image: %s", str(e))
            return None

    def find_checkerboard(self, img):
        try:
            logger.debug("Looking for checkerboard pattern")
            if img is None:
                logger.error("Input image is None")
                return False, None
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, self.CHECKERBOARD_SIZE, None)
            
            if ret:
                logger.info("Checkerboard pattern found")
            else:
                logger.info("No checkerboard pattern detected")
                
            return ret, corners
        except Exception as e:
            logger.exception("Error finding checkerboard: %s", str(e))
            return False, None

def run_intrinsic_calibration(self, images):
    logger.info("Starting intrinsic calibration with %d images", len(images))
    objpoints, imgpoints, successful_images = self._process_images(images)

    if successful_images < 10:
        logger.error("Not enough valid images. Found %d checkerboard patterns.", successful_images)
        return None, None, None, successful_images

    return self._perform_calibration(objpoints, imgpoints, successful_images)

def _process_images(self, images):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((self.CHECKERBOARD_SIZE[0] * self.CHECKERBOARD_SIZE[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:self.CHECKERBOARD_SIZE[0], 0:self.CHECKERBOARD_SIZE[1]].T.reshape(-1, 2)

    objpoints = []
    imgpoints = []
    successful_images = 0

    for i, img in enumerate(images):
        logger.debug("Processing image %d/%d", i + 1, len(images))
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, self.CHECKERBOARD_SIZE, None)
            
            if ret:
                successful_images += 1
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
                imgpoints.append(corners2)
                logger.debug("Successfully processed image %d", i + 1)
            else:
                logger.warning("No checkerboard found in image %d", i + 1)
        except Exception as e:
            logger.exception("Error processing image %d: %s", i + 1, str(e))

    return objpoints, imgpoints, successful_images

def _perform_calibration(self, objpoints, imgpoints, successful_images):
    try:
        logger.info("Running calibrateCamera with %d successful images", successful_images)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, self.gray_shape, None, None)
        
        if not ret:
            logger.error("Calibration failed")
            return None, None, None, successful_images
        
        total_error = self._calculate_reprojection_error(objpoints, imgpoints, rvecs, tvecs, mtx, dist)
        
        logger.info("Calibration successful. Reprojection error: %f", total_error)
        return mtx, dist, total_error, successful_images

    except Exception as e:
        logger.exception("Error during calibration: %s", str(e))
        return None, None, None, successful_images

def _calculate_reprojection_error(self, objpoints, imgpoints, rvecs, tvecs, mtx, dist):
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
    return mean_error/len(objpoints)

    def process_image(self, image_data):
        logger.info("Processing new image")
        img = self.data_uri_to_cv2_img(image_data)
        
        if img is None:
            logger.error("Failed to process image")
            return {"success": False, "error": "Failed to process image"}

        ret, corners = self.find_checkerboard(img)
        
        if ret:
            self.captured_images.append(img)
            logger.info("Image captured successfully. Total images: %d", len(self.captured_images))
            return {
                "success": True,
                "message": f"Image {len(self.captured_images)} captured successfully",
                "detected": True
            }
        else:
            logger.warning("No checkerboard pattern detected")
            return {
                "success": True,
                "message": "No checkerboard pattern detected",
                "detected": False
            }

    def get_status(self):
        if len(self.captured_images) < 15:
            logger.info("Not enough images captured yet: %d/15", len(self.captured_images))
            return {
                "status": "collecting",
                "progress": (len(self.captured_images) / 15) * 100,
                "message": f"Captured {len(self.captured_images)}/15 images",
                "imagesRequired": 15 - len(self.captured_images)
            }
        
        if not self.calibration_data:
            logger.info("Running calibration with %d images", len(self.captured_images))
            camera_matrix, dist_coeffs, reprojection_error, successful_images = self.run_intrinsic_calibration(self.captured_images)
            
            if camera_matrix is None:
                logger.error("Calibration failed. Only %d valid images found.", successful_images)
                return {
                    "status": "error",
                    "message": f"Not enough valid images. Only {successful_images} images with clear checkerboard patterns.",
                    "progress": 0
                }
            
            self.calibration_data = {
                "cameraMatrix": camera_matrix.tolist(),
                "distCoeffs": dist_coeffs.tolist(),
                "reprojectionError": float(reprojection_error)
            }
            logger.info("Calibration completed successfully")
        
        return {
            "status": "complete",
            "progress": 100,
            "message": "Calibration complete",
            **self.calibration_data
        }

    def stop(self):
        logger.info("Stopping calibration and clearing data")
        self.captured_images = []
        self.calibration_data = None

