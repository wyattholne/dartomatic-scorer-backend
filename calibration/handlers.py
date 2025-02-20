
from flask import jsonify, request
from .wizard import CalibrationWizard
from .storage import upload_calibration_results

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

def start_calibration(request):
    """Handler for starting calibration."""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({})
        return add_cors_headers(response), 200

    try:
        wizard = CalibrationWizard()
        success = wizard.identify_cameras()
        response = jsonify({"success": success})
        return add_cors_headers(response)
    except Exception as e:
        response = jsonify({"success": False, "error": str(e)})
        return add_cors_headers(response), 500

def get_calibration_status(request):
    """Handler for getting calibration status."""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({})
        return add_cors_headers(response), 200

    try:
        status = {
            "status": "detecting",
            "progress": 50,
            "message": "Detecting checkerboard pattern..."
        }
        response = jsonify(status)
        return add_cors_headers(response)
    except Exception as e:
        response = jsonify({"status": "error", "message": str(e), "progress": 0})
        return add_cors_headers(response), 500

def stop_calibration(request):
    """Handler for stopping calibration."""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({})
        return add_cors_headers(response), 200

    try:
        response = jsonify({"success": True})
        return add_cors_headers(response)
    except Exception as e:
        response = jsonify({"success": False, "error": str(e)})
        return add_cors_headers(response), 500

