"""
Image Recognition API Routes
Handles image uploads and OCR text extraction
"""

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from backend.image_processor import image_processor
import os

image_bp = Blueprint('image', __name__)


@image_bp.route('/upload', methods=['POST'])
def upload_image():
    """
    Upload and process an image
    
    Form data:
        file: Image file
        OR
        image_data: Base64 encoded image
        filename: Original filename
    
    Returns:
        {
            "status": "success",
            "data": {
                "file_path": "uploads/images/20231119_123456_image.jpg",
                "filename": "20231119_123456_image.jpg",
                "size": 12345,
                "width": 1920,
                "height": 1080,
                "format": "JPEG",
                "preview_url": "data:image/jpeg;base64,..."
            }
        }
    """
    try:
        # Check if file in request
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({
                    'status': 'error',
                    'message': 'No file selected'
                }), 400
            
            filename = secure_filename(file.filename)
            result = image_processor.process_upload(file, filename)
            
        elif 'image_data' in request.json:
            # Base64 encoded image
            data = request.json
            image_data = data.get('image_data')
            filename = secure_filename(data.get('filename', 'image.png'))
            
            result = image_processor.process_upload(image_data, filename)
            
        else:
            return jsonify({
                'status': 'error',
                'message': 'No image data provided'
            }), 400
        
        if not result['success']:
            return jsonify({
                'status': 'error',
                'message': result['error']
            }), 400
        
        # Generate preview URL (optional, can be large)
        # preview_url = image_processor.get_image_data_url(result['file_path'])
        
        return jsonify({
            'status': 'success',
            'message': 'Image uploaded successfully',
            'data': {
                'file_path': result['file_path'],
                'filename': result['filename'],
                'size': result['size'],
                'width': result['width'],
                'height': result['height'],
                'format': result['format']
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Upload error: {str(e)}'
        }), 500


@image_bp.route('/analyze', methods=['POST'])
def analyze_image():
    """
    Analyze uploaded image with OCR
    NOTE: This is a placeholder. For production, integrate with:
    - Tesseract OCR (pytesseract)
    - Google Cloud Vision API
    - Azure Computer Vision API
    - AWS Rekognition
    
    Body:
        {
            "file_path": "uploads/images/image.jpg",
            "extract_text": true,
            "detect_objects": false
        }
    
    Returns:
        {
            "status": "success",
            "data": {
                "text": "Extracted text from image",
                "confidence": 0.95,
                "objects": [],
                "metadata": {}
            }
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing file_path in request body'
            }), 400
        
        file_path = data['file_path']
        extract_text = data.get('extract_text', True)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({
                'status': 'error',
                'message': 'Image file not found'
            }), 404
        
        # Placeholder response
        # In production, integrate with OCR service
        result = {
            'text': 'OCR text extraction coming soon! This is a placeholder response. To enable real OCR, integrate Tesseract.js on the frontend or a backend OCR service.',
            'confidence': 0.0,
            'detected': False,
            'note': 'Frontend OCR with Tesseract.js is recommended for client-side processing'
        }
        
        return jsonify({
            'status': 'success',
            'data': result,
            'file_path': file_path
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Analysis error: {str(e)}'
        }), 500


@image_bp.route('/delete', methods=['POST'])
def delete_image():
    """
    Delete uploaded image
    
    Body:
        {
            "file_path": "uploads/images/image.jpg"
        }
    
    Returns:
        {
            "status": "success",
            "message": "Image deleted"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing file_path in request body'
            }), 400
        
        file_path = data['file_path']
        success = image_processor.delete_image(file_path)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Image deleted successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to delete image'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Delete error: {str(e)}'
        }), 500


@image_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get image processor statistics
    
    Returns:
        {
            "status": "success",
            "stats": {
                "total_images": 10,
                "total_size_mb": 5.2,
                "upload_folder": "uploads/images"
            }
        }
    """
    try:
        stats = image_processor.get_stats()
        
        return jsonify({
            'status': 'success',
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting stats: {str(e)}'
        }), 500
