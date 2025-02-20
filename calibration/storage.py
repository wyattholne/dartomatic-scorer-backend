
import os
import json
from google.cloud import storage
from .wizard import CalibrationResult

def upload_calibration_results(camera_index: int, results: CalibrationResult):
    """Upload calibration results to Google Cloud Storage."""
    try:
        storage_client = storage.Client()
        bucket_name = os.environ.get('CALIBRATION_BUCKET')
        bucket = storage_client.bucket(bucket_name)
        
        results_dict = {
            'camera_matrix': results.camera_matrix.tolist(),
            'dist_coeffs': results.dist_coeffs.tolist(),
            'reprojection_error': float(results.reprojection_error)
        }
        
        blob = bucket.blob(f'calibration_results/camera_{camera_index}.json')
        blob.upload_from_string(
            json.dumps(results_dict),
            content_type='application/json'
        )
        
        return True
    except Exception as e:
        print(f"Error uploading results: {str(e)}")
        return False
