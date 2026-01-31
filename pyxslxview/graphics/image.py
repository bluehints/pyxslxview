"""
Image management for graphics
"""

from typing import Optional, Tuple
from ..core.color import Color


class ImageManager:
    """Image manager for graphics operations"""
    
    def __init__(self):
        self._image_cache = {}
    
    def load_image(self, image_path: str) -> Optional[object]:
        """Load image from file"""
        try:
            from PIL import Image
            
            if image_path not in self._image_cache:
                img = Image.open(image_path)
                self._image_cache[image_path] = img
            
            return self._image_cache[image_path]
        except Exception:
            return None
    
    def create_image(self, width: int, height: int, 
                     background_color: Color = None) -> object:
        """Create new image"""
        try:
            from PIL import Image
            
            if background_color is None:
                background_color = Color.white()
            
            bg = background_color.rgba
            img = Image.new("RGBA", (width, height), bg)
            
            return img
        except Exception:
            return None
    
    def resize_image(self, image: object, width: int, height: int) -> object:
        """Resize image"""
        try:
            from PIL import Image
            
            if isinstance(image, Image.Image):
                return image.resize((width, height), Image.Resampling.LANCZOS)
        except Exception:
            pass
        
        return image
    
    def crop_image(self, image: object, x: int, y: int, 
                   width: int, height: int) -> object:
        """Crop image"""
        try:
            from PIL import Image
            
            if isinstance(image, Image.Image):
                box = (x, y, x + width, y + height)
                return image.crop(box)
        except Exception:
            pass
        
        return image
    
    def get_image_size(self, image: object) -> Tuple[int, int]:
        """Get image size"""
        try:
            from PIL import Image
            
            if isinstance(image, Image.Image):
                return image.size
        except Exception:
            pass
        
        return (0, 0)
    
    def clear_cache(self):
        """Clear image cache"""
        self._image_cache.clear()