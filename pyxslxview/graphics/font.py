"""
Font management for graphics
"""

from typing import Dict
from dataclasses import dataclass
from ..core.font import Font


@dataclass
class FontMetrics:
    """Font metrics"""
    
    ascent: float
    descent: float
    height: float
    max_width: float


class FontManager:
    """Font manager for graphics operations"""
    
    def __init__(self):
        self._font_cache: Dict[str, any] = {}
        self._metrics_cache: Dict[str, FontMetrics] = {}
    
    def get_font_key(self, font: Font) -> str:
        """Get unique key for font"""
        return f"{font.name}_{font.size}_{font.bold}_{font.italic}"
    
    def get_font(self, font: Font):
        """Get font object for rendering"""
        key = self.get_font_key(font)
        
        if key not in self._font_cache:
            self._font_cache[key] = self._create_font(font)
        
        return self._font_cache[key]
    
    def _create_font(self, font: Font):
        """Create font object"""
        try:
            from PIL import ImageFont
            
            font_path = self._find_font_path(font.name)
            size = int(font.size)
            
            pil_font = ImageFont.truetype(font_path, size)
            
            return {
                "font": pil_font,
                "name": font.name,
                "size": font.size,
                "bold": font.bold,
                "italic": font.italic,
            }
        except Exception:
            return {
                "font": None,
                "name": font.name,
                "size": font.size,
                "bold": font.bold,
                "italic": font.italic,
            }
    
    def _find_font_path(self, font_name: str) -> str:
        """Find font file path"""
        font_map = {
            "Arial": "arial.ttf",
            "Calibri": "calibri.ttf",
            "Times New Roman": "times.ttf",
            "Courier New": "cour.ttf",
            "Verdana": "verdana.ttf",
        }
        
        return font_map.get(font_name, "arial.ttf")
    
    def get_metrics(self, font: Font) -> FontMetrics:
        """Get font metrics"""
        key = self.get_font_key(font)
        
        if key not in self._metrics_cache:
            self._metrics_cache[key] = self._calculate_metrics(font)
        
        return self._metrics_cache[key]
    
    def _calculate_metrics(self, font: Font) -> FontMetrics:
        """Calculate font metrics"""
        try:
            from PIL import Image, ImageDraw
            
            img = Image.new("RGB", (100, 100))
            draw = ImageDraw.Draw(img)
            
            font_obj = self.get_font(font)
            if font_obj["font"]:
                pil_font = font_obj["font"]
                
                bbox = draw.textbbox((0, 0), "Ay", font=pil_font)
                height = bbox[3] - bbox[1]
                ascent = -bbox[1]
                descent = bbox[3]
                
                width = draw.textlength("M", font=pil_font)
                
                return FontMetrics(
                    ascent=ascent,
                    descent=descent,
                    height=height,
                    max_width=width,
                )
        except Exception:
            pass
        
        return FontMetrics(
            ascent=font.size * 0.8,
            descent=font.size * 0.2,
            height=font.size,
            max_width=font.size * 0.6,
        )
    
    def measure_text(self, font: Font, text: str):
        """Measure text dimensions"""
        metrics = self.get_metrics(font)
        
        char_width = metrics.max_width
        width = char_width * len(text)
        height = metrics.height
        
        return (width, height)
    
    def clear_cache(self):
        """Clear font cache"""
        self._font_cache.clear()
        self._metrics_cache.clear()