from functools import wraps
from flask import jsonify

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 500
    return wrapper