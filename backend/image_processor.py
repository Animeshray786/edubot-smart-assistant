"""
Image Recognition & OCR Processor
Handles image uploads, OCR text extraction, and image analysis
"""

import base64
import os
from datetime import datetime
from typing import Dict, Optional
from PIL import Image
import io

class ImageProcessor:
    """Process and analyze uploaded images"""
    
    def __init__(self, upload_folder='uploads/images'):
        """
        Initialize image processor
        
        Args:
            upload_folder: Directory to save uploaded images
        """
        self.upload_folder = upload_folder
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.max_dimension = 4096  # Max width/height
        
        # Create upload folder if not exists
        os.makedirs(self.upload_folder, exist_ok=True)
        
    def is_allowed_file(self, filename: str) -> bool:
        """
        Check if file extension is allowed
        
        Args:
            filename: File name
            
        Returns:
            bool: True if allowed
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def process_upload(self, file_data, filename: str) -> Dict:
        """
        Process uploaded image file
        
        Args:
            file_data: File object or base64 string
            filename: Original filename
            
        Returns:
            dict: Processing result with file_path, size, dimensions, etc.
        """
        try:
            # Check file extension
            if not self.is_allowed_file(filename):
                return {
                    'success': False,
                    'error': f'File type not allowed. Allowed: {", ".join(self.allowed_extensions)}'
                }
            
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_filename = f"{timestamp}_{filename}"
            file_path = os.path.join(self.upload_folder, safe_filename)
            
            # Save file
            if isinstance(file_data, str):
                # Base64 encoded data
                image_data = base64.b64decode(file_data.split(',')[1] if ',' in file_data else file_data)
                with open(file_path, 'wb') as f:
                    f.write(image_data)
            else:
                # File object
                file_data.save(file_path)
            
            # Get image info
            img = Image.open(file_path)
            width, height = img.size
            file_size = os.path.getsize(file_path)
            
            # Check file size
            if file_size > self.max_file_size:
                os.remove(file_path)
                return {
                    'success': False,
                    'error': f'File too large. Max size: {self.max_file_size / (1024*1024)}MB'
                }
            
            # Check dimensions
            if width > self.max_dimension or height > self.max_dimension:
                # Resize image
                img.thumbnail((self.max_dimension, self.max_dimension), Image.Resampling.LANCZOS)
                img.save(file_path)
                width, height = img.size
            
            return {
                'success': True,
                'file_path': file_path,
                'filename': safe_filename,
                'size': file_size,
                'width': width,
                'height': height,
                'format': img.format,
                'mode': img.mode
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error processing image: {str(e)}'
            }
    
    def preprocess_for_ocr(self, image_path: str) -> str:
        """
        Preprocess image for better OCR results
        
        Args:
            image_path: Path to image file
            
        Returns:
            str: Path to preprocessed image
        """
        try:
            img = Image.open(image_path)
            
            # Convert to grayscale
            img = img.convert('L')
            
            # Enhance contrast (simple method)
            # For better results, consider using PIL.ImageEnhance
            
            # Save preprocessed image
            preprocessed_path = image_path.replace('.', '_preprocessed.')
            img.save(preprocessed_path)
            
            return preprocessed_path
            
        except Exception as e:
            print(f"[ImageProcessor] Preprocessing error: {e}")
            return image_path
    
    def get_image_data_url(self, image_path: str) -> Optional[str]:
        """
        Convert image to base64 data URL
        
        Args:
            image_path: Path to image file
            
        Returns:
            str: Base64 data URL or None
        """
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            encoded = base64.b64encode(image_data).decode('utf-8')
            
            # Determine mime type
            ext = image_path.rsplit('.', 1)[1].lower()
            mime_type = f'image/{ext}' if ext != 'jpg' else 'image/jpeg'
            
            return f'data:{mime_type};base64,{encoded}'
            
        except Exception as e:
            print(f"[ImageProcessor] Error creating data URL: {e}")
            return None
    
    def delete_image(self, file_path: str) -> bool:
        """
        Delete uploaded image
        
        Args:
            file_path: Path to image file
            
        Returns:
            bool: Success status
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                
                # Also delete preprocessed version if exists
                preprocessed = file_path.replace('.', '_preprocessed.')
                if os.path.exists(preprocessed):
                    os.remove(preprocessed)
                
                return True
            return False
            
        except Exception as e:
            print(f"[ImageProcessor] Error deleting image: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """
        Get image processor statistics
        
        Returns:
            dict: Statistics
        """
        try:
            images = os.listdir(self.upload_folder)
            total_size = sum(
                os.path.getsize(os.path.join(self.upload_folder, img)) 
                for img in images
            )
            
            return {
                'total_images': len(images),
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'upload_folder': self.upload_folder
            }
            
        except Exception as e:
            print(f"[ImageProcessor] Error getting stats: {e}")
            return {
                'total_images': 0,
                'total_size_bytes': 0,
                'total_size_mb': 0,
                'upload_folder': self.upload_folder
            }


# Global instance
image_processor = None


def init_image_processor(upload_folder='uploads/images'):
    """
    Initialize image processor
    
    Args:
        upload_folder: Directory for uploads
        
    Returns:
        ImageProcessor: Initialized processor
    """
    global image_processor
    image_processor = ImageProcessor(upload_folder)
    print(f"[OK] Image Processor initialized (folder: {upload_folder})")
    return image_processor
