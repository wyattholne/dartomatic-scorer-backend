
from flask import Blueprint, jsonify, send_from_directory
import os

root_bp = Blueprint('root', __name__)

@root_bp.route('/')
def root():
    """Serve the index.html file"""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return send_from_directory(root_dir, 'index.html')

@root_bp.route('/favicon.ico')
def favicon():
    """Serve the favicon.ico file from the public directory"""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return send_from_directory(os.path.join(root_dir, 'public'), 'favicon.ico')

@root_bp.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from the public directory"""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        return send_from_directory(os.path.join(root_dir, 'public'), filename)
    except:
        # If file is not found in public, try to serve index.html for client-side routing
        return send_from_directory(root_dir, 'index.html')

