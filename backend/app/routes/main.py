from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the API"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Tax Agent API is running',
        'version': '1.0.0'
    })

@main_bp.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'AI Tax Return Agent API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'upload': '/api/upload',
            'process': '/api/process',
            'calculate': '/api/calculate',
            'generate': '/api/generate-form'
        }
    }) 